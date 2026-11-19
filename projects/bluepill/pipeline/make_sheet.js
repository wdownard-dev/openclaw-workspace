const sharp = require('sharp'); const { character } = require('./character');
const out = '../tests/round2'; require('fs').mkdirSync(out, { recursive: true });
(async () => {
  const combos = [['neutral','idle'],['happy','cheer'],['shocked','idle'],['angry','point']];
  for (const [e,p] of combos) await sharp(Buffer.from(character({expr:e,pose:p}))).png().toFile(`${out}/pip_${e}_${p}.png`);
  const tiles = await Promise.all(combos.map(([e,p]) => sharp(Buffer.from(character({expr:e,pose:p}))).resize(300,450).png().toBuffer()));
  await sharp({create:{width:1200,height:450,channels:4,background:'#efe6d6'}}).composite(tiles.map((t,i)=>({input:t,left:i*300,top:0}))).png().toFile(`${out}/pip_sheet.png`);
  console.log('ok');
})();
