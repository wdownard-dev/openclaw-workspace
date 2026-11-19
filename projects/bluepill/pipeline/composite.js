const sharp = require('sharp'); const { character } = require('./character');
const R1='../tests/round1', OUT='../tests/round2';
const caption = (t, w, h) => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><text x="${w/2}" y="${h-60}" text-anchor="middle" font-family="Impact, Arial Black, DejaVu Sans, sans-serif" font-weight="900" font-size="120" fill="#ffd23f" stroke="#1a1a1a" stroke-width="10" paint-order="stroke" letter-spacing="4">${t}</text></svg>`);
(async () => {
  const jobs = [
    ['cyclops_cave__gpt-image-2.6-sunburst','shocked','idle','CYCLOPS!',  0.62, 0.05],
    ['storm_ship__gpt-image-2.6-sunburst','angry','point','STORM!',      0.55, 0.60],
    ['olympus__gpt-image-2.6-sunburst','happy','cheer','OLYMPUS',        0.60, 0.12],
  ];
  for (const [bg,e,p,cap,hf,xf] of jobs) {
    const base = sharp(`${R1}/${bg}.png`); const {width:W,height:H} = await base.metadata();
    const ch = Math.round(H*hf);
    const pip = await sharp(Buffer.from(character({expr:e,pose:p}))).resize({height:ch}).png().toBuffer();
    const shadow = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><ellipse cx="${Math.round(W*xf)+ch*0.33}" cy="${H-Math.round(H*0.04)}" rx="${ch*0.22}" ry="${ch*0.035}" fill="#000" opacity="0.28"/></svg>`);
    await base.composite([{input:shadow},{input:pip,left:Math.round(W*xf),top:H-ch-Math.round(H*0.02)},{input:caption(cap,W,H),top:0,left:0}]).png().toFile(`${OUT}/comp_${bg.split('__')[0]}.png`);
  }
  console.log('done');
})();
