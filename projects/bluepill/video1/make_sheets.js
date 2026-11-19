// node make_sheets.js : numbered contact sheets of accepted images and rejects
const sharp = require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const fs = require('fs');
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const m = JSON.parse(fs.readFileSync('manifest.json'));
const acc = [];
const order = [...m.assets.map(a => a.id), ...m.reused.map(r => r.id)];
const shotsOf = {}; m.assets.forEach(a => shotsOf[a.id] = a.shots); m.reused.forEach(r => shotsOf[r.id] = r.shots);
for (const id of order) {
  if (fs.existsSync(`images/${id}.png`)) acc.push({ id, file: `images/${id}.png`, label: `${id}  shots ${shotsOf[id].slice(0, 6).join(',')}${shotsOf[id].length > 6 ? '..' : ''}` });
  else if (id === 'NB14') acc.push({ id: 'NB14?', file: 'images/NB14_candidate_a4.png', label: 'NB14 candidate a4 (NEEDS DECISION)', flag: true });
}
const rejects = fs.readdirSync('rejects').filter(f => f.endsWith('.png')).sort().map(f => ({ id: f.replace('.png', ''), file: 'rejects/' + f, label: f.replace('.png', '') + ': ' + fs.readFileSync('rejects/' + f.replace('.png', '.txt'), 'utf8').trim().slice(0, 70) }));
async function sheet(items, out, title, cols, W, H) {
  const PAD = 10, LH = 44, rows = Math.ceil(items.length / cols), cw = W + PAD * 2, ch = H + LH + PAD * 2;
  const comps = [];
  for (let i = 0; i < items.length; i++) {
    const it = items[i], x = (i % cols) * cw, y = Math.floor(i / cols) * ch + 60;
    const img = await sharp(it.file).flatten({ background: '#e8e8e8' }).resize(W, H, { fit: 'contain', background: '#e8e8e8' }).png().toBuffer();
    comps.push({ input: img, left: x + PAD, top: y + PAD });
    comps.push({ input: Buffer.from(`<svg width="${W}" height="${LH}"><text x="0" y="22" font-size="16" font-family="DejaVu Sans, sans-serif" fill="${it.flag ? '#ffb347' : '#fff'}" font-weight="bold">${i + 1}. ${esc(it.label)}</text></svg>`), left: x + PAD, top: y + PAD + H + 4 });
  }
  comps.unshift({ input: Buffer.from(`<svg width="${cw * cols}" height="60"><rect width="100%" height="60" fill="#111"/><text x="20" y="40" font-size="26" font-family="DejaVu Sans, sans-serif" fill="#fff" font-weight="bold">${esc(title)}</text></svg>`), left: 0, top: 0 });
  await sharp({ create: { width: cw * cols, height: ch * rows + 60, channels: 3, background: '#1b1b1b' } }).composite(comps).jpeg({ quality: 88 }).toFile(out);
  console.log(out, items.length);
}
(async () => {
  fs.mkdirSync('contact_sheets', { recursive: true });
  const per = 22;
  for (let s = 0; s * per < acc.length; s++) await sheet(acc.slice(s * per, (s + 1) * per), `contact_sheets/accepted_${s + 1}.jpg`, `Video 1 accepted images, sheet ${s + 1}`, 4, 420, 236);
  const rp = 24;
  for (let s = 0; s * rp < rejects.length; s++) await sheet(rejects.slice(s * rp, (s + 1) * rp), `contact_sheets/rejects_${s + 1}.jpg`, `Video 1 rejects, sheet ${s + 1} (reason after the id)`, 4, 420, 236);
})();
