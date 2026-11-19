// usage: node seq_sheet.js <framesdir> <out.jpg> <step> <ncols> t1 t2 ...
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const [dir,out,step,ncols,...ts]=process.argv.slice(2);
const W=200,H=112,C=+ncols,S=+step;
(async()=>{const comps=[];
 for(let r=0;r<ts.length;r++){const c=Math.round(+ts[r]*30)+1;
  for(let k=0;k<C;k++){const fi=c+(k-Math.floor(C/2))*S;
   const buf=await sharp(dir+'/f_'+String(Math.max(1,fi)).padStart(5,'0')+'.png').resize(W,H).toBuffer();
   comps.push({input:buf,left:k*(W+2),top:r*(H+14)});}
  comps.push({input:Buffer.from(`<svg width="300" height="12"><text x="2" y="10" font-size="10" fill="#fff">t=${ts[r]}s  (frame step ${S})</text></svg>`),left:0,top:r*(H+14)+H});}
 await sharp({create:{width:C*(W+2),height:ts.length*(H+14),channels:3,background:'#000'}}).composite(comps).jpeg({quality:80}).toFile(out);})();
