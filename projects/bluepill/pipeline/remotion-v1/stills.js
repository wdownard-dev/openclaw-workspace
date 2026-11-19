// usage: node stills.js <outDir> <t1> <t2> ...   (seconds)  or  --shots n1 n2 ... (mid-shot-time + 1.2s into the shot)
const {bundle} = require('@remotion/bundler'); const {renderStill, selectComposition, openBrowser} = require('@remotion/renderer');
const path = require('path'), fs = require('fs');
(async () => {
  const args = process.argv.slice(2); const out = args[0]; fs.mkdirSync(out, {recursive: true});
  let times = [];
  if (args[1] === '--shots') { const sl = require('./src/data/shots_timed.json').shot_list; for (const n of args.slice(2)) { const s = sl.find((x) => x.shot === +n); times.push([`s${String(n).padStart(3, '0')}${process.env.LATE ? 'L' : ''}`, process.env.LATE ? s.end - 0.3 : Math.min(s.end - 0.05, s.start + Math.min(2.2, s.sec * 0.6))]); } }
  else times = args.slice(1).map((x) => [`t${parseFloat(x).toFixed(1)}`, parseFloat(x)]);
  const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), onProgress: () => {}});
  const check = process.env.CHECK === '1'; const inputProps = {withAudio: false, check};
  const comp = await selectComposition({serveUrl, id: 'Video1Silent', inputProps});
  const browser = await openBrowser('chrome');
  for (const [name, t] of times) { await renderStill({composition: comp, serveUrl, frame: Math.round(t * 30), output: path.join(out, `${name}.png`), imageFormat: 'png', puppeteerInstance: browser, inputProps, onBrowserLog: (l) => { if (process.env.DEBUG) console.log('LOG', l.text.slice(0, 200)); if (l.text.startsWith('OVERFLOW_CHECK')) { const m = l.text.split(' '); const arr = JSON.parse(l.text.slice(l.text.indexOf('[', 15))); if (arr.length) console.log('\nOVERFLOW', name, arr.join(' | ')); } }}); process.stdout.write(name + ' '); }
  await browser.close({silent: true}); console.log('done');
})().catch((e) => { console.error(e); process.exit(1); });
