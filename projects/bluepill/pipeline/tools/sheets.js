// Builds per-character contact sheets and per-option cast sheets for tests/chars_v3
const sharp = require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const fs = require('fs');
const ROOT = '/home/williamdownard/.openclaw/workspace/projects/bluepill/tests/chars_v3';
const CHARS = ['odysseus', 'cyclops', 'crew', 'sheep', 'poseidon'];
const NAMES = { odysseus: 'ODYSSEUS', cyclops: 'CYCLOPS (POLYPHEMUS)', crew: 'CREW MEMBER', sheep: 'SHEEP', poseidon: 'POSEIDON' };
const OPT = { A: 'A  mature cartoon', B: 'B  painterly storybook', C: 'C  stylised 2D textured', D: 'D  paper-cut collage' };
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const label = (txt, w, h, size, fill = '#111', bg = '#fff', weight = 'bold') => Buffer.from(
  `<svg width="${w}" height="${h}"><rect width="${w}" height="${h}" fill="${bg}"/><text x="${w / 2}" y="${h / 2 + size * 0.35}" text-anchor="middle" font-size="${size}" font-weight="${weight}" fill="${fill}" font-family="DejaVu Sans, sans-serif">${esc(txt)}</text></svg>`);
async function cell(file, W, H, emptyTxt) {
  if (!fs.existsSync(file)) return await sharp(label(emptyTxt || 'MISSING', W, H, 30, '#999', '#f2f2f2')).png().toBuffer();
  const m = await sharp(file).metadata();
  let img = sharp(file);
  if (m.channels === 4) img = img.flatten({ background: '#ffffff' });
  return await img.resize(W, H, { fit: 'contain', background: '#ffffff' }).png().toBuffer();
}
(async () => {
  const W = 420, H = 560, LH = 56, TH = 70;
  for (const c of CHARS) {
    const files = [['CONTROL (current v2)', `${ROOT}/control/${c}.png`], ...['A', 'B', 'C', 'D'].map(o => [OPT[o], `${ROOT}/gen/${c}_${o}.png`])];
    const comps = [{ input: label(NAMES[c], W * 5, TH, 40, '#fff', '#222'), left: 0, top: 0 }];
    for (let i = 0; i < files.length; i++) {
      const isCtl = i === 0;
      comps.push({ input: await cell(files[i][1], W, H, 'NO ART YET'), left: i * W, top: TH });
      comps.push({ input: label(files[i][0], W, LH, 24, isCtl ? '#fff' : '#111', isCtl ? '#b03030' : '#e8e8e8'), left: i * W, top: TH + H });
    }
    await sharp({ create: { width: W * 5, height: TH + H + LH, channels: 3, background: '#fff' } }).composite(comps).jpeg({ quality: 90 }).toFile(`${ROOT}/sheet_${c}.jpg`);
  }
  const cw = 380, ch = 500;
  for (const o of ['A', 'B', 'C', 'D']) {
    const comps = [{ input: label(`CAST OPTION ${OPT[o]}`, cw * 5, 64, 36, '#fff', '#222'), left: 0, top: 0 }];
    for (let r = 0; r < 2; r++) {
      for (let i = 0; i < CHARS.length; i++) {
        const c = CHARS[i];
        const f = r === 0 ? `${ROOT}/control/${c}.png` : `${ROOT}/gen/${c}_${o}.png`;
        comps.push({ input: await cell(f, cw, ch, 'NO ART YET'), left: i * cw, top: 64 + r * (ch + 44) });
        comps.push({ input: label(r === 0 ? `CONTROL ${NAMES[c]}` : NAMES[c], cw, 44, 20, r === 0 ? '#fff' : '#111', r === 0 ? '#b03030' : '#e8e8e8'), left: i * cw, top: 64 + r * (ch + 44) + ch });
      }
    }
    await sharp({ create: { width: cw * 5, height: 64 + 2 * (ch + 44), channels: 3, background: '#fff' } }).composite(comps).jpeg({ quality: 90 }).toFile(`${ROOT}/cast_${o}.jpg`);
  }
  const rw = 300, rh = 400;
  const comps = [{ input: label('WHOLE-CAST OVERVIEW (row 1 = CONTROL)', rw * 6, 56, 30, '#fff', '#222'), left: 0, top: 0 }];
  const rows = ['CONTROL', 'A', 'B', 'C', 'D'];
  for (let r = 0; r < rows.length; r++) {
    comps.push({ input: label(rows[r] === 'CONTROL' ? 'CONTROL' : OPT[rows[r]], rw, rh, 22, '#111', '#e8e8e8'), left: 0, top: 56 + r * rh });
    for (let i = 0; i < CHARS.length; i++) {
      const c = CHARS[i];
      const f = rows[r] === 'CONTROL' ? `${ROOT}/control/${c}.png` : `${ROOT}/gen/${c}_${rows[r]}.png`;
      comps.push({ input: await cell(f, rw, rh, 'NO ART YET'), left: (i + 1) * rw, top: 56 + r * rh });
    }
  }
  await sharp({ create: { width: rw * 6, height: 56 + rows.length * rh, channels: 3, background: '#fff' } }).composite(comps).jpeg({ quality: 88 }).toFile(`${ROOT}/cast_ALL.jpg`);
  console.log('sheets done');
})();
