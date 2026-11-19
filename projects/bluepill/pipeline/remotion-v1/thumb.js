// thumbnail concept 1 for video 1 (SCRIPT-V1.md): Cyclops face right two thirds, small Odysseus lower-left, "WAS HE REAL?" upper-left. Existing art only.
const sharp = require('../node_modules/sharp'); const path = require('path');
const IMG = path.resolve(__dirname, '../../video1/images'); const OUT = path.resolve(__dirname, '../../video1/draft/thumb_concept_1.png');
(async () => {
  const W = 1280, H = 720;
  const bw = Math.round(1536 * 1.06), bh = Math.round(864 * 1.06);
  const base = await sharp(path.join(IMG, 'NB01.png')).resize(bw, bh, {kernel: 'lanczos3'}).modulate({brightness: 1.02, saturation: 1.05}).sharpen({sigma: 0.8}).toBuffer();
  const baseC = await sharp(base).extract({left: 14, top: 72, width: W, height: H}).png().toBuffer();
  // Odysseus cutout: lower-left, small, with a dark soft shadow
  const ody = await sharp(path.resolve(__dirname, 'public/img/ody.png')).resize({height: 372, kernel: 'lanczos3'}).toBuffer();
  const om = await sharp(ody).metadata();
  const glow = await sharp(ody).ensureAlpha().extractChannel('alpha').blur(10).linear(0.9).toBuffer();
  const shadowRGBA = await sharp({create: {width: om.width, height: om.height, channels: 3, background: '#000'}}).joinChannel(glow).png().toBuffer();
  const svgOverlay = Buffer.from(`<svg width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b0806" stop-opacity="0.78"/><stop offset="0.55" stop-color="#0b0806" stop-opacity="0.15"/><stop offset="1" stop-color="#0b0806" stop-opacity="0"/></linearGradient>
      <radialGradient id="v" cx="0.55" cy="0.45" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.45"/></radialGradient>
    </defs>
    <rect width="${W}" height="${H}" fill="url(#l)"/><rect width="${W}" height="${H}" fill="url(#v)"/>
    <rect x="48" y="56" width="470" height="236" fill="#120e0a" fill-opacity="0.9"/>
    <rect x="48" y="56" width="10" height="236" fill="#c0492b"/>
    <text x="84" y="154" font-family="Noto Serif" font-weight="700" font-size="92" fill="#f1e6cc" letter-spacing="2">WAS HE</text>
    <text x="84" y="262" font-family="Noto Serif" font-weight="700" font-size="104" fill="#e0603f" letter-spacing="2">REAL?</text>
  </svg>`);
  await sharp(baseC).composite([
    {input: ody, left: 70, top: H - om.height - 26},
    {input: svgOverlay, left: 0, top: 0},
  ]).png().toFile(OUT);
  console.log('ok', OUT);
})();
