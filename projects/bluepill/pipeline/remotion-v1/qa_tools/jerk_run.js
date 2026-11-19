// usage: node qa_tools/jerk_run.js video.mp4 outDir   -> extracts 320x180 gray frames with the bundled ffmpeg, runs the Editor's motion.js in parallel chunks, merges to motion.json
const cp = require('child_process'), fs = require('fs'), path = require('path');
const FF = path.resolve(__dirname, '../../remotion-proof/node_modules/@remotion/compositor-linux-x64-gnu/ffmpeg');
const [video, out] = process.argv.slice(2); fs.mkdirSync(out, {recursive: true});
const raw = path.join(out, 'gray.raw'); const sharp = require('../../node_modules/sharp');
const pngDir = path.join(out, 'png'); fs.mkdirSync(pngDir, {recursive: true});
let r = cp.spawnSync(FF, ['-hide_banner', '-y', '-i', video, '-an', '-vf', 'scale=320:180:flags=bilinear,format=gray', '-c:v', 'png', path.join(pngDir, 'f%06d.png')], {encoding: 'utf8', maxBuffer: 1 << 28});
if (r.status) { console.error(r.stderr.slice(-600)); process.exit(1); }
const names = fs.readdirSync(pngDir).sort(); const ofd = fs.openSync(raw, 'w');
(async () => {
  for (let i = 0; i < names.length; i += 64) { const bufs = await Promise.all(names.slice(i, i + 64).map((n) => sharp(path.join(pngDir, n)).greyscale().raw().toBuffer({resolveWithObject: false}))); for (const b of bufs) fs.writeSync(ofd, b); }
  fs.closeSync(ofd); fs.rmSync(pngDir, {recursive: true}); go();
})();
function go() {
const N = 320 * 180, size = fs.statSync(raw).size, frames = Math.floor(size / N); const CH = 1500; const jobs = [];
const fd = fs.openSync(raw, 'r');
for (let s = 0, k = 0; s < frames; s += CH, k++) {
  const a = Math.max(0, s - 1), b = Math.min(frames, s + CH); const buf = Buffer.alloc((b - a) * N); fs.readSync(fd, buf, 0, buf.length, a * N);
  const f = path.join(out, `chunk${k}.raw`); fs.writeFileSync(f, buf); jobs.push({f, a, o: path.join(out, `chunk${k}.json`)});
}
let done = 0; const res = [];
jobs.forEach((j) => { const p = cp.spawn('node', [path.resolve(__dirname, 'motion.js'), j.f, '320', '180', j.o], {stdio: 'ignore'}); p.on('exit', () => { done++; if (done === jobs.length) merge(); }); });
const merge = () => { const all = []; jobs.forEach((j) => { const m = JSON.parse(fs.readFileSync(j.o)); m.forEach((x) => { const f = x.f + j.a; if (j.a > 0 && x.f < 1) return; all.push({...x, f, t: +(f / 30).toFixed(3)}); }); }); all.sort((a, b) => a.f - b.f); const uniq = []; let last = -1; for (const x of all) if (x.f !== last) { uniq.push(x); last = x.f; } fs.writeFileSync(path.join(out, 'motion.json'), JSON.stringify(uniq)); jobs.forEach((j) => { fs.unlinkSync(j.f); fs.unlinkSync(j.o); }); console.log('frames', frames, 'motion rows', uniq.length); };
}
