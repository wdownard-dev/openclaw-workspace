// usage: node stills.js <outDir> [--shots s001 s006 ...] [--times 12.3 45.6 ...] [--classes]  (default: --classes = one 1080p still per shot class present, plus a bubble shot)
// Renders full 1920x1080 PNGs from the BluePill composition with @remotion/renderer.
const {bundle} = require('@remotion/bundler');
const {renderStill, selectComposition, openBrowser} = require('@remotion/renderer');
const path = require('path'), fs = require('fs');
const TL = require('./src/timeline.json');

const lateTime = (s) => Math.max(s.t0 + 0.05, s.t1 - 0.3); // after the shot's events have landed
function pickPerClass() {
  const picks = [];
  const classes = [...new Set(TL.shots.map((s) => s.class))].sort();
  for (const c of classes) {
    // the shot of this class with the most events (richest frame)
    const cands = TL.shots.filter((s) => s.class === c).map((s) => ({s, n: TL.events.filter((e) => e.shot === s.id && e.kind !== 'sfx').length}));
    cands.sort((a, b) => b.n - a.n);
    picks.push([`class${c}_${cands[0].s.id}`, lateTime(cands[0].s)]);
  }
  // eighth: a class B shot with a bubble (dialogue), if not already chosen
  const bub = TL.shots.find((s) => s.class === 'B' && TL.events.some((e) => e.shot === s.id && e.kind === 'bubble') && !picks.some((p) => p[0].endsWith(s.id)));
  if (bub) picks.push([`classB_bubble_${bub.id}`, lateTime(bub)]);
  return picks.slice(0, 8);
}
(async () => {
  const args = process.argv.slice(2); const out = args[0] || 'out/stills'; fs.mkdirSync(out, {recursive: true});
  let times = [];
  if (args.includes('--shots')) for (const id of args.slice(args.indexOf('--shots') + 1)) { const s = TL.shots.find((x) => x.id === id); if (s) times.push([id, lateTime(s)]); }
  else if (args.includes('--times')) for (const x of args.slice(args.indexOf('--times') + 1)) times.push([`t${parseFloat(x).toFixed(1)}`, parseFloat(x)]);
  else times = pickPerClass();
  const serveUrl = await bundle({entryPoint: path.resolve(__dirname, 'src/index.ts'), onProgress: () => {}});
  const comp = await selectComposition({serveUrl, id: 'BluePill', inputProps: {}});
  const browser = await openBrowser('chrome');
  for (const [name, t] of times) {
    await renderStill({composition: comp, serveUrl, frame: Math.min(comp.durationInFrames - 1, Math.round(t * TL.fps)), output: path.join(out, `${name}.png`), imageFormat: 'png', puppeteerInstance: browser, inputProps: {}, onBrowserLog: (l) => { if (process.env.DEBUG) console.log('LOG', l.text.slice(0, 300)); }});
    process.stdout.write(`${name}@${t.toFixed(2)}s `);
  }
  await browser.close({silent: true}); console.log('\ndone');
})().catch((e) => { console.error(e); process.exit(1); });
