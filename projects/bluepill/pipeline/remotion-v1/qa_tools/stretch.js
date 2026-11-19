// computes the effective upscale factor of every picture shot from the spec's camera numbers (source images 1536x864; base fit to 1920x1080 = 1.25x)
const fs = require('fs'); const s = fs.readFileSync(__dirname + '/../src/spec.tsx', 'utf8'); const sl = require('../src/data/shots_timed.json').shot_list;
const rows = [];
for (const m of s.matchAll(/^\s*(\d+): P\('(\w+)', (inn|out|pan|hold|crop)\(([^)]*)\)/gm)) {
  const n = +m[1], img = m[2], kind = m[3], args = m[4].replace(/\[[^\]]*\]/g, 'A').split(',').map((x) => x.trim());
  let z0 = 1, z1 = 1;
  const num = (x, d) => (x === undefined || x === 'A' || isNaN(+x) ? d : +x);
  if (kind === 'inn') { z0 = num(args[1], 1); z1 = num(args[2], 1.04); }
  if (kind === 'out') { z0 = num(args[1], 1.04); z1 = num(args[2], 1); }
  if (kind === 'pan') { z0 = z1 = num(args[1], 1.05); }
  if (kind === 'hold') { z0 = num(args[1], 1); z1 = z0 + num(args[2], 0.012); }
  if (kind === 'crop') { z0 = num(args[2], 1); z1 = num(args[3], z0); }
  const smax = Math.max(z0, z1);
  const src = img === 'NB14' ? 1.5 * 0 + 1.0 : 1;   // NB14 composite is the crop upscaled by 2.0 (999 px display of a 799 px crop is 1.25x; see note)
  rows.push({shot: n, img, zoom: +smax.toFixed(3), eff: +(1.25 * smax * (img === 'NB14' ? 1.0 : 1)).toFixed(2), sec: sl.find((x) => x.shot === n).sec});
}
rows.sort((a, b) => b.eff - a.eff);
console.log(rows.filter((r) => r.eff > 1.3).map((r) => `${r.shot} ${r.img} ${r.eff}x`).join('\n'));
console.log('over 1.3x:', rows.filter((r) => r.eff > 1.3).length, 'of', rows.length, 'max', rows[0].eff);
fs.writeFileSync(__dirname + '/stretch.json', JSON.stringify(rows, null, 1));
