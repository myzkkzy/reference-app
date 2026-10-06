// Reads one JSON request on stdin and returns one JSON response. No diagram files.
const fs = require('node:fs');
const path = require('node:path');

class Resources {
  constructor(location) {
    this.location = location;
    if (fs.statSync(location).isFile()) {
      this.fd = fs.openSync(location, 'r');
      const prefix = Buffer.alloc(16);
      fs.readSync(this.fd, prefix, 0, 16, 0);
      const size = prefix.readUInt32LE(12);
      if (size > 32 * 1024 * 1024) throw new Error('Invalid ASAR header');
      const header = Buffer.alloc(size);
      fs.readSync(this.fd, header, 0, size, 16);
      this.header = JSON.parse(header.toString('utf8'));
      this.offset = 8 + prefix.readUInt32LE(4);
    }
  }
  read(name) {
    const parts = name.split('/');
    if (parts.some(p => !p || p === '..' || p.includes('\\'))) throw new Error('Invalid resource path');
    if (!this.header) return fs.readFileSync(path.join(this.location, ...parts));
    let entry = this.header;
    for (const part of ['drawio', 'src', 'main', 'webapp', ...parts]) entry = entry?.files?.[part];
    if (!entry || entry.files || entry.link || entry.unpacked) throw new Error(`Missing bundled resource: ${name}`);
    const buffer = Buffer.alloc(entry.size);
    fs.readSync(this.fd, buffer, 0, buffer.length, this.offset + Number(entry.offset));
    return buffer;
  }
  close() { if (this.fd !== undefined) fs.closeSync(this.fd); }
}

function browserOptions() {
  if (process.env.DRAWIO_BROWSER) return {executablePath: process.env.DRAWIO_BROWSER};
  if (process.platform === 'win32') {
    for (const root of [process.env['PROGRAMFILES(X86)'], process.env.PROGRAMFILES, process.env.LOCALAPPDATA].filter(Boolean)) {
      const executablePath = path.join(root, 'Microsoft', 'Edge', 'Application', 'msedge.exe');
      if (fs.existsSync(executablePath)) return {executablePath};
    }
  }
  return {}; // Playwright's configured Chromium installation.
}

async function render(request) {
  const {chromium} = require('./node_modules/playwright');
  const resources = new Resources(request.resources);
  // Fail before launching a browser if the required distribution is unavailable.
  resources.read('export3.html');
  resources.read('js/app.min.js');
  const exportCode = resources.read('js/export.js').toString('utf8');
  const shapeBundle = exportCode.match(/mxscript\('(js\/shapes-[^']+\.js)'/);
  if (!shapeBundle) throw new Error('Unsupported draw.io distribution: shape bundle not found');
  let browser;
  let deadline;
  let cancelled = false;
  const blocked = [];
  const errors = [];
  const started = Date.now();
  try {
    const work = async () => {
      browser = await chromium.launch({...browserOptions(), headless: true, timeout: request.timeoutMs});
      if (cancelled) {
        await browser.close();
        throw new Error('Render timeout during browser startup');
      }
      const context = await browser.newContext({acceptDownloads: false, serviceWorkers: 'block', colorScheme: 'light'});
      // Routing disables HTTP cache. Nothing is served by an actual network server.
      await context.route('**/*', async route => {
        const url = new URL(route.request().url());
        if (url.origin !== 'http://drawio.local') {
          blocked.push(url.origin + url.pathname);
          return route.abort();
        }
        try {
          const name = decodeURIComponent(url.pathname.slice(1));
          const body = resources.read(name);
          const types = {'.js': 'text/javascript', '.css': 'text/css', '.html': 'text/html', '.xml': 'text/xml', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2'};
          await route.fulfill({body, contentType: types[path.extname(name)] || 'application/octet-stream'});
        } catch (error) {
          errors.push(error.message);
          await route.abort();
        }
      });
      const page = await context.newPage();
      page.on('pageerror', error => errors.push(error.message));
      await page.goto('http://drawio.local/export3.html', {waitUntil: 'load', timeout: request.timeoutMs});
      await page.waitForFunction(() => typeof Graph !== 'undefined' && typeof render === 'function', null, {timeout: request.timeoutMs});
      // The Desktop export page only preloads these for Electron. Load them explicitly.
      await page.addScriptTag({url: 'http://drawio.local/js/stencils.min.js'});
      await page.addScriptTag({url: 'http://drawio.local/' + shapeBundle[1]});
      await page.evaluate(() => { mxStencilRegistry.allowEval = false; });
      const svg = await page.evaluate(async xml => {
        const doc = mxUtils.parseXml(xml);
        let model = Editor.extractGraphModel(doc.documentElement, true);
        if (model?.nodeName === 'mxfile') model = Editor.parseDiagramNode(model.getElementsByTagName('diagram')[0]);
        if (!model) throw new Error('No graph model');
        // Validate actual registered shapes instead of allowing mxGraph's rectangle fallback.
        const probe = new Graph(document.createElement('div'));
        new mxCodec(model.ownerDocument).decode(model, probe.getModel());
        if (!Object.values(probe.getModel().cells).some(cell => cell.vertex)) throw new Error('No drawable cells');
        for (const cell of Object.values(probe.getModel().cells)) {
          if (!cell.vertex && !cell.edge) continue;
          const shape = probe.getCellStyle(cell)[mxConstants.STYLE_SHAPE];
          if (shape && !mxCellRenderer.defaultShapes[shape] && !mxStencilRegistry.getStencil(shape)) {
            throw new Error(`Unknown shape: ${shape} (cell ${cell.id})`);
          }
        }
        probe.destroy();
        const graph = render({xml, format: 'svg', scale: 1, border: 8, embedXml: '1', theme: 'light'});
        await document.fonts.ready;
        await Promise.all(Array.from(document.images).map(img => img.decode()));
        const result = graph.getSvg(graph.background || '#ffffff', 1, 8, false, null, true, null, null, '_blank', null, null, 'light');
        await new Promise(resolve => new Editor().convertImages(result, resolve));
        for (const image of result.querySelectorAll('image')) {
          const href = image.getAttribute('href') || image.getAttributeNS('http://www.w3.org/1999/xlink', 'href');
          if (href && !href.startsWith('data:')) throw new Error('SVG contains an unembedded image');
        }
        result.setAttribute('content', xml);
        return new XMLSerializer().serializeToString(result);
      }, request.xml);
      if (errors.length || blocked.length) throw new Error(JSON.stringify({resourceErrors: errors, blockedRequests: blocked}));
      let preview;
      if (request.preview) {
        // An optional verification artifact returned in memory, never a renderer output file.
        await page.setContent('<html><meta charset="utf-8"><body style="margin:0">' + svg + '</body></html>');
        await page.evaluate(() => document.fonts.ready);
        preview = (await page.locator('svg').screenshot()).toString('base64');
      }
      return {svg, preview, diagnostics: {elapsedMs: Date.now() - started, blockedRequests: blocked, resourceErrors: errors, desktopLaunched: false}};
    };
    return await Promise.race([work(), new Promise((_, reject) => {
      deadline = setTimeout(() => { cancelled = true; reject(new Error('Render timeout')); }, request.timeoutMs);
    })]);
  } catch (error) {
    throw new Error(`${error.message}; diagnostics=${JSON.stringify({resourceErrors: errors, blockedRequests: blocked})}`);
  } finally {
    clearTimeout(deadline);
    if (browser) await browser.close();
    resources.close();
  }
}

if (require.main === module) {
  let input = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => { input += chunk; });
  process.stdin.on('end', async () => {
    try { process.stdout.write(JSON.stringify(await render(JSON.parse(input)))); }
    catch (error) { process.stderr.write(error.stack + '\n'); process.exitCode = 1; }
  });
}
module.exports = {Resources, render};
