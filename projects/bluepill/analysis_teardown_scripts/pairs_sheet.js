// usage: node pairs_sheet.js <framesdir> <events.json> <minfrac> <maxfrac> <count> <out.jpg> [seed]
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const fs=require('fs');
const [dir,evf,mn,mx,cnt,out,seed]=process.argv.slice(2);
let ev=JSON.parse(fs.readFileSync(evf)).filter(e=>e.frac>=+mn&&e.frac<+mx);
let s=+(seed||1);function rnd(){s=(s*1664525+1013904223)%4294967296;return s/4294967296;}
const pick=[];while(pick.length<+cnt&&ev.length){const k=Math.floor(rnd()*ev.length);pick.push(ev.splice(k,1)[0]);}
pick.sort((a,b)=>a.i-b.i);
const W=240,H=135,cols=3; // each cell = pair side by side (480x135)
const rows=Math.ceil(pick.length/cols);
const comps=[];
(async()=>{
  for(let k=0;k<pick.length;k++){
    const e=pick[k];
    const a=await sharp(dir+'/f_'+String(Math.max(1,e.i-1)).padStart(5,'0')+'.png').resize(W,H).toBuffer();
    const b=await sharp(dir+'/f_'+String(Math.min(e.i+3,fs.readdirSync(dir).length)).padStart(5,'0')+'.png').resize(W,H).toBuffer();
    const x=(k%cols)*(2*W+14),y=Math.floor(k/cols)*(H+16);
    comps.push({input:a,left:x,top:y});comps.push({input:b,left:x+W,top:y});
    const svg=Buffer.from(`<svg width="${2*W}" height="14"><text x="2" y="11" font-size="11" fill="white">t=${e.t}s d=${e.d} frac=${e.frac}</text></svg>`);
    comps.push({input:svg,left:x,top:y+H});
  }
  await sharp({create:{width:cols*(2*W+14),height:rows*(H+16),channels:3,background:'#222'}}).composite(comps).jpeg({quality:82}).toFile(out);
  console.log(pick.map(e=>e.t).join(' '));
})();
