// greedy clustering of shot mid-frames by 20x11 gray signature; prints unique count at several thresholds
const fs=require('fs');
const [pre,segf,total]=process.argv.slice(2);
const seg=JSON.parse(fs.readFileSync(segf));
const g=fs.readFileSync(pre+'.gray80');const N=g.length/3600;
const starts=[0,...seg.map(s=>s.t)],ends=[...seg.map(s=>s.t),+total];
function sig(i){ // downsample 80x45 -> 20x11 (approx by 4x4 blocks)
  const out=new Float32Array(20*11);const a=i*3600;
  for(let y=0;y<11;y++)for(let x=0;x<20;x++){let s=0,n=0;for(let yy=0;yy<4;yy++)for(let xx=0;xx<4;xx++){const py=y*4+yy,px=x*4+xx;if(py<45){s+=g[a+py*80+px];n++;}}out[y*20+x]=s/n;}
  return out;}
const sigs=starts.map((a,k)=>{const b=ends[k];const t=a+0.7*(b-a);return sig(Math.min(N-1,Math.round(t*30)));});
function dist(x,y){let s=0;for(let i=0;i<x.length;i++)s+=Math.abs(x[i]-y[i]);return s/x.length;}
for(const TH of [8,12,16,20]){
  const cl=[];let reuse=0;
  sigs.forEach((s,i)=>{let hit=false;for(const c of cl){if(dist(c,s)<TH){hit=true;break;}}if(hit)reuse++;else cl.push(s);});
  console.log(pre.split('/').pop(),'TH',TH,'shots',sigs.length,'unique',cl.length,'reused',reuse);
}
