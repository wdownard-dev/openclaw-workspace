// usage: node cuts.js <prefix> -> prints/writes cuts and transitions
const fs=require('fs');
const [pre]=process.argv.slice(2);
const S=JSON.parse(fs.readFileSync(pre+'.series.json'));
const g=fs.readFileSync(pre+'.gray80');
const N=S.N, d=S.diff, FR=3600;
function fr(i){return g.subarray(i*FR,(i+1)*FR);}
function dist(a,b){let s=0;for(let p=0;p<FR;p++)s+=Math.abs(a[p]-b[p]);return s/FR;}
// robust local baseline
function localMedian(i,w){const a=[];for(let k=Math.max(1,i-w);k<=Math.min(N-1,i+w);k++)a.push(d[k]);a.sort((x,y)=>x-y);return a[a.length>>1];}
const cuts=[];
const T_ABS=+(process.env.TABS||14);
for(let i=1;i<N;i++){
  const base=localMedian(i,15);
  if(d[i]>T_ABS && d[i]>6*Math.max(base,0.3)){
    // local max
    if(d[i]>=d[i-1] && (i+1>=N||d[i]>=d[i+1])) cuts.push(i);
  }
}
// merge cuts within 2 frames
const hard=[];for(const c of cuts){ if(hard.length&&c-hard[hard.length-1]<3)continue; hard.push(c);}
// dissolve detection: windows of W frames; ends a=i, b=i+W, mid m=i+W/2
const dis=[];
for(const W of [6,10,16,24]){
  for(let i=0;i+W<N;i+=1){
    const a=fr(i),b=fr(i+W),m=fr(i+(W>>1));
    const dab=dist(a,b); if(dab<25) continue;
    // max consecutive diff inside window must be modest (no hard cut)
    let mx=0;for(let k=i+1;k<=i+W;k++)mx=Math.max(mx,d[k]);
    if(mx>T_ABS*0.8) continue;
    // blend test
    let e=0;for(let p=0;p<FR;p++)e+=Math.abs(m[p]-(a[p]+b[p])/2);e/=FR;
    const dam=dist(a,m),dmb=dist(m,b);
    if(e<0.45*Math.min(dam,dmb) && dam>8 && dmb>8) dis.push({i,W,dab:+dab.toFixed(1),e:+e.toFixed(1)});
  }
}
// cluster dissolves
dis.sort((x,y)=>x.i-y.i);
const dcl=[];for(const x of dis){const l=dcl[dcl.length-1]; if(l&&x.i<=l.end){l.end=Math.max(l.end,x.i+x.W);l.W=Math.max(l.W,x.W);}else dcl.push({start:x.i,end:x.i+x.W,W:x.W,dab:x.dab});}
fs.writeFileSync(pre+'.cuts.json',JSON.stringify({hard,dissolve:dcl}));
console.log(pre,'hard',hard.length,'dissolve clusters',dcl.length);
