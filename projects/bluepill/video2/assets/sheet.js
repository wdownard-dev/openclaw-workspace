// Contact sheet: node sheet.js <out.jpg> <cellW> <cellH> <cols> <label=path> ... ; cells on a mid-grey ground, label strip under each.
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
(async()=>{const [out,cw,ch,cols,...items]=process.argv.slice(2);const CW=+cw,CH=+ch,C=+cols,LB=26;
  const rows=Math.ceil(items.length/C);const comps=[];
  for(let i=0;i<items.length;i++){const eq=items[i].indexOf('=');const label=items[i].slice(0,eq),p=items[i].slice(eq+1);
    const x=(i%C)*CW,y=Math.floor(i/C)*(CH+LB);
    try{const img=await sharp(p).resize(CW-6,CH-6,{fit:'inside'}).png().toBuffer();const m=await sharp(img).metadata();
      comps.push({input:img,left:x+Math.round((CW-m.width)/2),top:y+Math.round((CH-m.height)/2)});}catch(e){}
    const svg=`<svg width="${CW}" height="${LB}"><rect width="100%" height="100%" fill="#222"/><text x="4" y="18" font-family="sans-serif" font-size="15" fill="#fff">${label.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</text></svg>`;
    comps.push({input:Buffer.from(svg),left:x,top:y+CH});}
  await sharp({create:{width:C*CW,height:rows*(CH+LB),channels:3,background:'#8a8a8a'}}).composite(comps).jpeg({quality:82}).toFile(out);
  console.log(out,C*CW,rows*(CH+LB));})();
