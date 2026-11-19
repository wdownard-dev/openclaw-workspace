// windowed picture-change detector: c(t)=fraction of px differing >25 between gray80 frames t-K and t+K
const fs=require('fs');
const [pre,Karg,thr]=process.argv.slice(2);
const K=+(Karg||6), TH=+(thr||0.30);
const S=JSON.parse(fs.readFileSync(pre+'.series.json'));
const g=fs.readFileSync(pre+'.gray80');
const N=S.N,FR=3600,d=S.diff;
const c=new Float32Array(N);
for(let t=K;t<N-K;t++){const a=(t-K)*FR,b=(t+K)*FR;let n=0;for(let p=0;p<FR;p++)if(Math.abs(g[a+p]-g[b+p])>25)n++;c[t]=n/FR;}
// peaks with NMS (0.5s)
const peaks=[];
for(let t=K;t<N-K;t++){
  if(c[t]>=TH){let ok=true;for(let u=Math.max(K,t-8);u<=Math.min(N-K-1,t+8);u++)if(c[u]>c[t]||(c[u]===c[t]&&u<t)){ok=false;break;}
    if(ok)peaks.push(t);}
}
// merge peaks <15 frames apart keeping the bigger
const m=[];for(const t of peaks){const l=m[m.length-1];if(l!==undefined&&t-l<(+process.env.GAP||15)){if(c[t]>c[l])m[m.length-1]=t;}else m.push(t);}
// classify transition: look at diff profile in [t-10,t+10]
const out=m.map(t=>{
  let mx=0,mi=t,n3=0,sumd=0;
  for(let u=t-10;u<=t+10;u++){if(u<1||u>=N)continue;if(d[u]>mx){mx=d[u];mi=u;}sumd+=d[u];}
  // width: number of frames in window with diff>1.5
  let w=0;for(let u=t-12;u<=t+12;u++){if(u>=1&&u<N&&d[u]>1.5)w++;}
  // mean luminance dip
  let lmin=1e9,lmax=-1;for(let u=t-8;u<=t+8;u++){if(u<0||u>=N)continue;lmin=Math.min(lmin,S.lum[u]);lmax=Math.max(lmax,S.lum[u]);}
  const lb=S.lum[Math.max(0,t-12)],la=S.lum[Math.min(N-1,t+12)];
  return {t:+(t/30).toFixed(2),i:t,c:+c[t].toFixed(2),maxd:+mx.toFixed(1),width:w,lumdip:+(Math.min(lb,la)-lmin).toFixed(1),lumpeak:+(lmax-Math.max(lb,la)).toFixed(1),kind:mx>=14&&w<=4?'hard':(w>=5?'gradual':'mid')};
});
fs.writeFileSync(pre+(process.env.SUF||".seg2")+".json",JSON.stringify(out));
const kinds={};out.forEach(o=>kinds[o.kind]=(kinds[o.kind]||0)+1);
console.log(pre,'K',K,'TH',TH,'boundaries',out.length,JSON.stringify(kinds));
