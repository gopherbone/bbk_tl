// Drive headless Chrome over the DevTools protocol: emulate a device, load a
// page, optionally press keys, and save screenshots. Used to check the site.
//   node tools/site/cdp_shot.mjs <url> <out.png> [--w 390 --h 844 --dpr 3 --mobile]
//        [--wait ms] [--keys "Enter:4000,Enter:1500,..."]   (key:delay-before ms)
//        [--eval "async js expression"]   run after the keys, result printed
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i < 0 ? d : args[i + 1]; };
const [url, out] = args;
const W = +opt('w', 390), H = +opt('h', 844), DPR = +opt('dpr', 2), mobile = args.includes('--mobile');
const wait = +opt('wait', 3000), keys = opt('keys', '');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port = 9300 + Math.floor(Math.random() * 500);
const prof = mkdtempSync(join(process.env.TMPDIR || tmpdir(), 'cdp-'));
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`,
  `--user-data-dir=${prof}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pending = new Map(); const logs = [];
try {
  let target;
  for (let i = 0; i < 50 && !target; i++) {
    await sleep(200);
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page'); } catch {}
  }
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  ws.onmessage = m => { const d = JSON.parse(m.data);
    if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); }
    if (d.method === 'Runtime.consoleAPICalled') logs.push(d.params.type + ': ' + d.params.args.map(a => a.value ?? a.description).join(' '));
    if (d.method === 'Runtime.exceptionThrown') logs.push('EXC: ' + JSON.stringify(d.params.exceptionDetails).slice(0, 300)); };
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: DPR, mobile });
  if (mobile) await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await send('Page.enable');
  await send('Page.navigate', { url });
  await sleep(wait);
  const shot = async (file) => { const r = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: !!opt('full', '') });
    writeFileSync(file, Buffer.from(r.result.data, 'base64')); };
  let n = 0;
  for (const step of keys ? keys.split(',') : []) {
    const [k, ms] = step.split(':'); await sleep(+ms || 500);
    const codes = { Enter: 13, Escape: 27, ArrowUp: 38, ArrowDown: 40, ArrowLeft: 37, ArrowRight: 39 };
    for (const type of ['keyDown', 'keyUp'])
      await send('Input.dispatchKeyEvent', { type, key: k, code: k, windowsVirtualKeyCode: codes[k] || 0 });
    if (opt('every', '')) await (await sleep(+opt('every')), shot(out.replace(/\.png$/, `-${++n}.png`)));
  }
  if (keys) await sleep(+opt('after', 1500));
  if (opt('eval', '')) {
    const r = await send('Runtime.evaluate', { expression: `(async () => JSON.stringify(await (${opt('eval')})))()`, awaitPromise: true, returnByValue: true });
    console.log('eval:', r.result.result.value ?? JSON.stringify(r.result));
  }
  await shot(out);
  const ev = await send('Runtime.evaluate', { expression: 'JSON.stringify({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,canvas:document.getElementById("screen")&&document.getElementById("screen").style.width})', returnByValue: true });
  console.log(ev.result.result.value);
  for (const l of logs) console.log(l);
} finally { try { ws && ws.close(); } catch {} chrome.kill('SIGKILL'); }
