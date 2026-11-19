// usage: node sheet.js out.jpg cols cellW file1 file2 ...   -> labelled montage
const sharp = require('../node_modules/sharp'); const path = require('path');
(async () => {
  const [out, colsS, cwS, ...files] = process.argv.slice(2); const cols = +colsS, cw = +cwS, ch = Math.round(cw * 9 / 16), lab = 26;
  const rows = Math.ceil(files.length / cols); const tiles = [];
  for (let i = 0; i < files.length; i++) {
    const b = await sharp(files[i]).resize(cw, ch, {fit: 'fill'}).jpeg({quality: 85}).toBuffer();
    const svg = Buffer.from(`<svg width="${cw}" height="${lab}"><rect width="${cw}" height="${lab}" fill="#111"/><text x="8" y="19" font-size="16" fill="#eee" font-family="DejaVu Sans">${path.basename(files[i]).replace(/\.\w+$/, '')}</text></svg>`);
    tiles.push({input: b, left: (i % cols) * cw, top: Math.floor(i / cols) * (ch + lab) + lab}, {input: svg, left: (i % cols) * cw, top: Math.floor(i / cols) * (ch + lab)});
  }
  await sharp({create: {width: cols * cw, height: rows * (ch + lab), channels: 3, background: '#000'}}).composite(tiles).jpeg({quality: 88}).toFile(out);
})();
