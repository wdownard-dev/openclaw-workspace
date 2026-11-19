const sharp=require('sharp'),fs=require('fs');
(async()=>{const T='../../tests/v2/';const nw=fs.readdirSync(T).filter(f=>/^v2_\d+/.test(f)).sort();const od=fs.readdirSync(T+'old').sort();
const W=640,H=360,L=44;const tiles=[];
const lab=(txt,w,h)=>Buffer.from(`<svg width="${w}" height="${h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#222"/><text x="12" y="${h-12}" fill="#fff" font-size="26" font-family="DejaVu Sans" font-weight="bold">${txt}</text></svg>`);
const rows=[['OLD PROOF (54.7 s, 6 shots, ~6.5 cuts/min)',od.map(f=>T+'old/'+f)],['V2 UPGRADE TEST (76.5 s, 20 shots, ~15.7 cuts/min)',nw.map(f=>T+f)]];
let y=0;const comp=[];
for(const [t,fs_] of rows){comp.push({input:lab(t,W*4,L),left:0,top:y});y+=L;
 for(let r=0;r<2;r++){for(let c=0;c<4;c++){comp.push({input:await sharp(fs_[r*4+c]).resize(W,H).toBuffer(),left:c*W,top:y});}y+=H;}}
await sharp({create:{width:W*4,height:y,channels:3,background:'#000'}}).composite(comp).jpeg({quality:85}).toFile(T+'compare.jpg');console.log('ok',y)})()
