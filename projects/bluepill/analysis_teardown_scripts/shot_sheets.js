// usage: node shot_sheets.js <framesdir> <seg.json> <total_sec> <outprefix> [perSheet]
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const fs=require('fs');
const [dir,segf,total,out,per]=process.argv.slice(2);
const seg=JSON.parse(fs.readFileSync(segf));
const starts=[0,...seg.map(s=>s.t)],ends=[...seg.map(s=>s.t),+total];
const shots=starts.map((a,i)=>({n:i+1,a,b:ends[i]}));
const PER=+(per||36),cols=6,W=280,H=158;
const nf=fs.readdirSync(dir).length;
(async()=>{
 for(let sh=0;sh*PER<shots.length;sh++){
  const part=shots.slice(sh*PER,(sh+1)*PER);const comps=[];
  for(let k=0;k<part.length;k++){
    const s=part[k];const t=s.a+Math.min(0.8*(s.b-s.a),Math.max(0.35*(s.b-s.a),1.2)); // later in shot so pop-ins have happened
    const fi=Math.min(nf,Math.max(1,Math.round(t*30)+1));
    const buf=await sharp(dir+'/f_'+String(fi).padStart(5,'0')+'.png').resize(W,H).toBuffer();
    const x=(k%cols)*(W+4),y=Math.floor(k/cols)*(H+16);
    comps.push({input:buf,left:x,top:y});
    comps.push({input:Buffer.from(`<svg width="${W}" height="14"><text x="2" y="11" font-size="11" fill="#fff">#${s.n}  ${s.a.toFixed(1)}s  len ${(s.b-s.a).toFixed(1)}</text></svg>`),left:x,top:y+H});
  }
  const rows=Math.ceil(part.length/cols);
  await sharp({create:{width:cols*(W+4),height:rows*(H+16),channels:3,background:'#111'}}).composite(comps).jpeg({quality:80}).toFile(`${out}_${sh}.jpg`);
 }
 console.log('shots',shots.length);
})();
