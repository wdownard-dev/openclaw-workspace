// usage: node montage.js out.jpg cols cellW cellH label(0/1) file1 file2 ...
const sharp = require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const path = require('path');
(async () => {
  const [out, cols, cw, ch, lab, ...files] = process.argv.slice(2);
  const C = +cols, W = +cw, H = +ch;
  const rows = Math.ceil(files.length / C);
  const comps = [];
  for (let i = 0; i < files.length; i++) {
    const buf = await sharp(files[i]).resize(W, H, { fit: 'contain', background: '#ffffff' }).flatten({ background: '#ffffff' }).png().toBuffer();
    comps.push({ input: buf, left: (i % C) * W, top: Math.floor(i / C) * H });
    if (+lab) {
      const name = path.basename(files[i]).replace(/\.\w+$/, '');
      const svg = `<svg width="${W}" height="26"><rect width="${W}" height="26" fill="#000" opacity="0.7"/><text x="6" y="19" font-size="16" fill="#fff" font-family="sans-serif">${name}</text></svg>`;
      comps.push({ input: Buffer.from(svg), left: (i % C) * W, top: Math.floor(i / C) * H });
    }
  }
  await sharp({ create: { width: C * W, height: rows * H, channels: 3, background: '#888' } }).composite(comps).jpeg({ quality: 88 }).toFile(out);
})();
