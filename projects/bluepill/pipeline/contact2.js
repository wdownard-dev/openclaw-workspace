const sharp=require('sharp');const d='../tests/characters2',T=480;
const names=[['03_in_01style','03 adventurer, 01 style'],['03_in_02style','03 adventurer, 02 style'],['04_in_01style','04 scholar, 01 style'],['04_in_02style','04 scholar, 02 style'],['06_in_01style','06 pharaoh, 01 style'],['06_in_02style','06 pharaoh, 02 style']];
(async()=>{const c=[];for(let i=0;i<6;i++){const x=(i%2)*T,y=Math.floor(i/2)*(T+36);
c.push({input:await sharp(`${d}/${names[i][0]}.png`).resize(T,T).toBuffer(),left:x,top:y});
c.push({input:Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${T}" height="36"><rect width="100%" height="100%" fill="#222"/><text x="12" y="25" font-family="DejaVu Sans, Arial" font-size="20" fill="#fff">${names[i][1]}</text></svg>`),left:x,top:y+T});}
await sharp({create:{width:T*2,height:3*(T+36),channels:3,background:'#222'}}).composite(c).jpeg({quality:88}).toFile(`${d}/contact_sheet2.jpg`);})();
