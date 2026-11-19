// Gate G2 look test: renders LOOK-G2.jpg (contact sheet) with the proposed palette and fonts.
// Run from video2/:  FONTCONFIG_FILE=$PWD/spike/fonts/fonts.conf node LOOK-G2.js
// No network, no image API. Uses sharp from pipeline/node_modules and the spike's plates/cutout.
const path = require('path');
const sharp = require('../pipeline/node_modules/sharp');
const C = (f) => path.join(__dirname, 'spike/common', f);
const W = 1920, H = 1080;

// Palettes
const NEW = {accent: '#1f3a5f', chip: '#2e7d73', stamp: '#c9a227', stampDeep: '#a8841c', cream: '#f3e9d2', ink: '#1a1204', white: '#ffffff', name: 'ink blue / verdigris / gold'};
const OLD = {accent: '#b8472a', chip: '#b8472a', stamp: '#b8472a', stampDeep: '#b8472a', cream: '#f3e9d2', ink: '#1a1204', white: '#ffffff', name: 'old rust #b8472a'};
const HAND = 'Permanent Marker', TYPE = 'Special Elite';

// Font sizes (px at 1080p). Phone check = these / 4 at 480 px wide.
const SZ = {impact: 170, impactWhite: 190, counter: 260, counterUnit: 110, stamp: 96, stampSmall: 64, chip: 48, bubble: 64, caption: 30};

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const svg = (w, h, inner) => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${inner}</svg>`);

// Hand-lettered text, optional outline (paint-order stroke so the fill stays clean).
const hand = (text, {x, y, size, fill, stroke, rot = 0, anchor = 'middle', font = HAND, sw = 0.11}) =>
  `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${font}" font-size="${size}" fill="${fill}" ${stroke ? `stroke="${stroke}" stroke-width="${size * sw}" stroke-linejoin="round" paint-order="stroke"` : ''} transform="rotate(${rot} ${x} ${y})">${esc(text)}</text>`;

// Rubber stamp: double rounded border + 1-2 lines of text, rotated, slightly translucent like ink.
// halo: cream sticker backing (for stamps over busy paint); like the reference's white sticker edge on cutouts, but on a label.
const stamp = (lines, {x, y, size, color, rot, halo = false}) => {
  const lh = size * 1.05, n = lines.length, longest = Math.max(...lines.map((l) => l.length));
  const w = longest * size * 0.62 + size * 0.9, h = n * lh + size * 0.55;
  const t = lines.map((l, i) => `<text x="${x}" y="${y - ((n - 1) * lh) / 2 + i * lh + size * 0.36}" text-anchor="middle" font-family="${HAND}" font-size="${size}" fill="${color}">${esc(l)}</text>`).join('');
  const hb = halo ? `<rect x="${x - w / 2 - size * 0.1}" y="${y - h / 2 - size * 0.1}" width="${w + size * 0.2}" height="${h + size * 0.2}" rx="${size * 0.22}" fill="#f3e9d2" opacity="0.85"/>` : '';
  return `<g transform="rotate(${rot} ${x} ${y})">${hb}</g><g opacity="0.93" transform="rotate(${rot} ${x} ${y})"><rect x="${x - w / 2}" y="${y - h / 2}" width="${w}" height="${h}" rx="${size * 0.18}" fill="none" stroke="${color}" stroke-width="${size * 0.09}"/><rect x="${x - w / 2 + size * 0.16}" y="${y - h / 2 + size * 0.16}" width="${w - size * 0.32}" height="${h - size * 0.32}" rx="${size * 0.12}" fill="none" stroke="${color}" stroke-width="${size * 0.035}"/>${t}</g>`;
};

// Source chip: typewriter face in a filled pill at the fixed corner (bottom-left, 60 px margins).
const chip = (text, {color, textColor = '#f3e9d2', size = SZ.chip, x = 60, y = H - 60}) => {
  const w = text.length * size * 0.62 + size * 1.2, h = size * 1.7;
  return `<rect x="${x}" y="${y - h}" width="${w}" height="${h}" rx="${h / 2}" fill="${color}"/><text x="${x + w / 2}" y="${y - h / 2 + size * 0.36}" text-anchor="middle" font-family="${TYPE}" font-size="${size}" fill="${textColor}">${esc(text)}</text>`;
};

// Bubble: hand-lettered line, no box, thin curved tail toward the speaker.
const bubble = (text, {x, y, size, color, tail}) =>
  `<text x="${x}" y="${y}" text-anchor="middle" font-family="${HAND}" font-size="${size}" fill="${color}">${esc(text)}</text><path d="${tail}" fill="none" stroke="${color}" stroke-width="4" stroke-linecap="round"/>`;

const plate = (f) => sharp(C(f)).resize(W, H, {fit: 'cover'}).toBuffer();
const white = () => sharp({create: {width: W, height: H, channels: 3, background: '#ffffff'}}).png().toBuffer();
const ody = (h) => sharp(C('odysseus.png')).resize({height: h}).png().toBuffer({resolveWithObject: true});

async function tile(bg, comps) { return sharp(bg).composite(comps).png().toBuffer(); }

async function build(P) {
  const o = await ody(880);
  const odyAt = (x, y) => ({input: o.data, left: Math.round(x - o.info.width / 2), top: Math.round(y - o.info.height)});
  const tiles = {};
  // 1 impact word on a painted plate (night cave), cream with dark outline; chip in the corner
  tiles.impactPlate = await tile(await plate('NB10.png'), [{input: svg(W, H, hand('NOBODY', {x: 1180, y: 300, size: SZ.impact, fill: P.cream, stroke: P.ink, rot: -2}) + chip('HOMER, ODYSSEY 9', {color: P.chip}))}]);
  // 2 impact word on white beside Odysseus, solid accent
  tiles.impactWhite = await tile(await white(), [odyAt(420, 1040), {input: svg(W, H, hand('SIX MEN', {x: 1220, y: 520, size: SZ.impactWhite, fill: P.accent, rot: -3}) + hand('GOT OUT', {x: 1220, y: 720, size: SZ.impactWhite, fill: P.accent, rot: 2}))}]);
  // 3 counter
  tiles.counter = await tile(await white(), [{input: svg(W, H, hand('22', {x: 960, y: 520, size: SZ.counter, fill: P.accent}) + hand('WAGONS', {x: 960, y: 720, size: SZ.counterUnit, fill: P.chip}))}]);
  // 4 four stamps, gold, 3-6 degrees
  tiles.stamps = await tile(await white(), [{input: svg(W, H,
    stamp(['UNPROVEN'], {x: 500, y: 300, size: SZ.stamp, color: P.stamp, rot: -5}) +
    stamp(['PLAUSIBLE'], {x: 1420, y: 300, size: SZ.stamp, color: P.stampDeep, rot: 4}) +
    stamp(['REAL'], {x: 500, y: 760, size: SZ.stamp, color: P.stamp, rot: 6}) +
    stamp(['PROBABLY OLDER', 'THAN HOMER'], {x: 1420, y: 760, size: SZ.stampSmall, color: P.stampDeep, rot: -3}))}]);
  // 5 source chip at the fixed corner on a plate (firelit), plus a small place label to show verdigris on paint
  tiles.chip = await tile(await plate('NB05.png'), [{input: svg(W, H, chip('HOMER, ODYSSEY 9', {color: P.chip}) + hand('THE CAVE', {x: 1500, y: 160, size: 90, fill: P.cream, stroke: P.ink}))}]);
  // 6 bubble line with thin tail, on white beside Odysseus
  tiles.bubble = await tile(await white(), [odyAt(520, 1040), {input: svg(W, H, bubble('MY NAME IS NOBODY.', {x: 1250, y: 420, size: SZ.bubble, color: P.accent, tail: 'M 880 445 Q 740 490 610 345'}))}]);
  // 7 everything together on a plate: impact, stamp, chip (used for the A/B with rust)
  tiles.composite = await tile(await plate('NB01.png'), [{input: svg(W, H, hand('ONE EYE', {x: 1500, y: 240, size: 150, fill: P.cream, stroke: P.ink, rot: -3}) + stamp(['UNPROVEN'], {x: 330, y: 840, size: SZ.stamp, color: P.stampDeep, rot: -5, halo: true}) + chip('MAYOR, 2000', {color: P.chip}))}]);
  return tiles;
}

(async () => {
  const n = await build(NEW), o = await build(OLD);
  // sheet cells: 960x540 each, 3 x 3, caption strip under each
  const cw = 960, ch = 540, cap = 44, cols = 3;
  const cells = [
    ['1 impact on plate: cream + ink outline, chip verdigris', n.impactPlate],
    ['2 impact on white: ink blue #1f3a5f, Permanent Marker 190px', n.impactWhite],
    ['3 counter: number blue, unit verdigris #2e7d73', n.counter],
    ['4 stamps: left gold #c9a227, right deep gold #a8841c; rot -5/4/6/-3', n.stamps],
    ['5 source chip: Special Elite 48px, verdigris pill, fixed bottom-left', n.chip],
    ['6 bubble: ink blue, thin tail, no box', n.bubble],
    ['7 NEW palette on a plate; stamp deep gold on a cream sticker halo', n.composite],
    ['8 OLD rust #b8472a: same elements, same fonts (A/B with 7)', o.composite],
  ];
  const sheetW = cw * cols, rows = Math.ceil((cells.length + 1) / cols), sheetH = (ch + cap) * rows;
  const comps = [];
  for (let i = 0; i < cells.length; i++) {
    const [label, buf] = cells[i], x = (i % cols) * cw, y = Math.floor(i / cols) * (ch + cap);
    comps.push({input: await sharp(buf).resize(cw, ch).toBuffer(), left: x, top: y});
    comps.push({input: svg(cw, cap, `<rect width="${cw}" height="${cap}" fill="#222"/><text x="12" y="30" font-family="DejaVu Sans" font-size="22" fill="#eee">${esc(label)}</text>`), left: x, top: y + ch});
  }
  // 9 phone check: tile 7 at 480 px wide, native pixels (not upscaled), plus tile 2 and 5 at 480 for the small type
  const i = cells.length, x = (i % cols) * cw, y = Math.floor(i / cols) * (ch + cap);
  const ph = await sharp(n.composite).resize(480).png().toBuffer();
  const ph2 = await sharp(n.chip).resize(480).png().toBuffer();
  comps.push({input: svg(cw, ch, `<rect width="${cw}" height="${ch}" fill="#444"/>`), left: x, top: y});
  comps.push({input: ph, left: x, top: y});
  comps.push({input: ph2, left: x + 480, top: y});
  comps.push({input: svg(cw, cap, `<rect width="${cw}" height="${cap}" fill="#222"/><text x="12" y="30" font-family="DejaVu Sans" font-size="22" fill="#eee">9 phone check: tiles 7 and 5 at 480 px wide, 1:1 pixels</text>`), left: x, top: y + ch});
  await sharp({create: {width: sheetW, height: sheetH, channels: 3, background: '#111'}}).composite(comps).jpeg({quality: 90}).toFile(path.join(__dirname, 'LOOK-G2.jpg'));
  await sharp(ph).jpeg({quality: 90}).toFile(path.join(__dirname, 'LOOK-G2.phone480.jpg'));
  console.log('wrote LOOK-G2.jpg', sheetW, 'x', sheetH, 'and LOOK-G2.phone480.jpg');
})();
