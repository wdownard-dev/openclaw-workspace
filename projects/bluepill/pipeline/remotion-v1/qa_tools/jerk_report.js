// usage: node qa_tools/jerk_report.js motion.json -> per-picture-shot jerk numbers + clip-wide numbers (excluding cuts and +-0.15 s around every segment boundary)
const fs = require('fs'); const path = require('path');
const m = JSON.parse(fs.readFileSync(process.argv[2])); const S = 6;
const sl = require('../src/data/shots_timed.json').shot_list;
const rms = (a) => (a.length ? Math.sqrt(a.reduce((s, v) => s + v * v, 0) / a.length) : 0);
const kinds = JSON.parse(fs.readFileSync(path.resolve(__dirname, 'kinds.json')));  // shot -> 'pic' | 'card'
const bounds = sl.map((s) => s.start);
const near = (t) => bounds.some((b) => Math.abs(t - b) <= 0.2);
const rows = []; const allJ = [];
for (const s of sl) {
  if (kinds[s.shot] !== 'pic') continue;
  const fr = m.filter((r) => r.t > s.start + 0.2 && r.t < s.end - 0.05 && r.diff < 40);
  if (fr.length < 6) continue;
  const jx = [], jy = [];
  for (let i = 2; i < fr.length; i++) { if (fr[i].f - fr[i - 2].f !== 2) continue; jx.push((fr[i].dx - 2 * fr[i - 1].dx + fr[i - 2].dx) * S); jy.push((fr[i].dy - 2 * fr[i - 1].dy + fr[i - 2].dy) * S); }
  const sp = fr.map((r) => Math.hypot(r.dx, r.dy) * S);
  rows.push({shot: s.shot, n: fr.length, jerk_rms: +Math.hypot(rms(jx), rms(jy)).toFixed(2), max_shift_px: +Math.max(...sp).toFixed(1), mean_speed: +(sp.reduce((a, b) => a + b, 0) / sp.length).toFixed(2)});
  allJ.push(...jx, ...jy);
}
const ins = m.filter((r) => !near(r.t) && r.diff < 40);
const jj = []; for (let i = 2; i < ins.length; i++) { if (ins[i].f - ins[i - 2].f !== 2) continue; jj.push((ins[i].dx - 2 * ins[i - 1].dx + ins[i - 2].dx) * S, (ins[i].dy - 2 * ins[i - 1].dy + ins[i - 2].dy) * S); }
const big = ins.filter((r) => Math.hypot(r.dx, r.dy) * S > 15);
const worst = [...rows].sort((a, b) => b.jerk_rms - a.jerk_rms).slice(0, 8);
const out = {picture_shots_analysed: rows.length, per_shot_jerk_rms_max: Math.max(...rows.map((r) => r.jerk_rms)), per_shot_jerk_rms_mean: +(rows.reduce((a, r) => a + r.jerk_rms, 0) / rows.length).toFixed(3), per_shot_max_shift_px: Math.max(...rows.map((r) => r.max_shift_px)), clipwide_jerk_rms_excluding_boundaries: +rms(jj).toFixed(3), frames_over_15px_outside_boundaries: big.length, big_frames: big.slice(0, 20).map((r) => `${r.t}s ${(Math.hypot(r.dx, r.dy) * S).toFixed(1)}px diff ${r.diff}`), worst_shots: worst, rows};
fs.writeFileSync(process.argv[2].replace('motion.json', 'jerk_report.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify({...out, rows: undefined}, null, 1));
