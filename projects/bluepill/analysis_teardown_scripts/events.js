const fs=require('fs');
const [pre]=process.argv.slice(2);
const S=JSON.parse(fs.readFileSync(pre+'.series.json'));
const g=fs.readFileSync(pre+'.gray80');
const N=S.N,d=S.diff,FR=3600;
function frac(i,j,thr){const a=i*FR,b=j*FR;let c=0,s=0;for(let p=0;p<FR;p++){const x=Math.abs(g[a+p]-g[b+p]);if(x>thr)c++;s+=x;}return [c/FR,s/FR];}
const ev=[];
for(let i=2;i<N-2;i++){
  if(d[i]>2.5 && d[i]>=d[i-1] && d[i]>=d[i+1]){
    const [f,m]=frac(i-1,Math.min(N-1,i+2),25);
    ev.push({i,t:+(i/30).toFixed(2),d:d[i],frac:+f.toFixed(2),m:+m.toFixed(1)});
  }
}
fs.writeFileSync(pre+'.events.json',JSON.stringify(ev));
const bins={};for(const e of ev){const k=e.frac>=0.6?'full>=.6':e.frac>=0.3?'big.3-.6':e.frac>=0.1?'part.1-.3':'small<.1';bins[k]=(bins[k]||0)+1;}
console.log(pre,'events',ev.length,JSON.stringify(bins));
