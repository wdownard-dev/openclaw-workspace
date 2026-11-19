// usage: node audio.js <wav16k> <label> [cuts.json]
const fs=require('fs');
const [wav,label,cutsf]=process.argv.slice(2);
const buf=fs.readFileSync(wav);
// find data chunk
let off=12;while(off<buf.length){const id=buf.toString('ascii',off,off+4);const sz=buf.readUInt32LE(off+4);if(id==='data'){off+=8;break;}off+=8+sz;}
const n=(buf.length-off)>>1;const x=new Float32Array(n);for(let i=0;i<n;i++)x[i]=buf.readInt16LE(off+2*i)/32768;
const SR=16000;
const db=v=>20*Math.log10(Math.max(v,1e-9));
// 50 ms rms frames
const HF=800;const nf=Math.floor(n/HF);const rms=new Float32Array(nf);
for(let f=0;f<nf;f++){let s=0;for(let i=0;i<HF;i++){const v=x[f*HF+i];s+=v*v;}rms[f]=Math.sqrt(s/HF);}
const rdb=Array.from(rms,db);
const pct=(a,p)=>{const b=[...a].sort((u,v)=>u-v);return b[Math.min(b.length-1,Math.floor(p*b.length))];};
const out={label,seconds:+(n/SR).toFixed(1)};
out.rms_dbfs_overall=+db(Math.sqrt(x.reduce((s,v)=>s+v*v,0)/n)).toFixed(1);
out.frame_db_p05=+pct(rdb,.05).toFixed(1);out.frame_db_p10=+pct(rdb,.10).toFixed(1);out.frame_db_p50=+pct(rdb,.5).toFixed(1);out.frame_db_p90=+pct(rdb,.9).toFixed(1);out.frame_db_p99=+pct(rdb,.99).toFixed(1);
// per-30s windows: floor (p05) and speech level (p75)
const W=600;const win=[];for(let w=0;w*W<nf;w++){const seg=rdb.slice(w*W,(w+1)*W);if(seg.length<100)continue;win.push({t:w*30,floor:+pct(seg,.05).toFixed(1),med:+pct(seg,.5).toFixed(1),p90:+pct(seg,.9).toFixed(1)});}
out.windows=win;
out.floor_mean=+(win.reduce((s,w)=>s+w.floor,0)/win.length).toFixed(1);
out.floor_std=+Math.sqrt(win.reduce((s,w)=>s+(w.floor-out.floor_mean)**2,0)/win.length).toFixed(1);
out.p90_std=+Math.sqrt(win.reduce((s,w)=>s+(w.p90-win.reduce((a,b)=>a+b.p90,0)/win.length)**2,0)/win.length).toFixed(1);
// fraction of 50ms frames below -50 dBFS (digital-ish silence) and below -40
out.frac_below_m60=+(rdb.filter(v=>v<-60).length/nf).toFixed(3);out.frac_below_m50=+(rdb.filter(v=>v<-50).length/nf).toFixed(3);out.frac_below_m40=+(rdb.filter(v=>v<-40).length/nf).toFixed(3);
// speech dynamic: std of dB among frames > p50 (voiced)
const vo=rdb.filter(v=>v>pct(rdb,.5));const mv=vo.reduce((a,b)=>a+b,0)/vo.length;out.voiced_db_std=+Math.sqrt(vo.reduce((s,v)=>s+(v-mv)**2,0)/vo.length).toFixed(2);
// longest stretches of frames below (floor+6dB) i.e. pauses: count pauses >0.5s,>1s,>2s relative to speech: frame < p50-18dB
const thr=pct(rdb,.5)-18;let run=0;const pauses=[];for(let f=0;f<nf;f++){if(rdb[f]<thr)run++;else{if(run>0)pauses.push(run*0.05);run=0;}}if(run>0)pauses.push(run*0.05);
out.pause_rule_db=+thr.toFixed(1);out.pauses_ge0_3=pauses.filter(p=>p>=0.3).length;out.pauses_ge0_6=pauses.filter(p=>p>=0.6).length;out.pauses_ge1_0=pauses.filter(p=>p>=1.0).length;out.pauses_ge2_0=pauses.filter(p=>p>=2.0).length;out.pause_total_s=+pauses.filter(p=>p>=0.3).reduce((a,b)=>a+b,0).toFixed(1);
// F0 via autocorrelation (voiced frames), semitone std per 20 s window
const FL=512,HP=320;const f0=[];const MED=pct(rdb,.5);
for(let s=0;s+FL<n;s+=HP){
  const fi=Math.floor(s/HF);if(rdb[fi]<MED-6){f0.push(0);continue;}
  let e=0;for(let i=0;i<FL;i++)e+=x[s+i]*x[s+i];if(e<1e-6){f0.push(0);continue;}
  let best=0,bl=0;
  for(let lag=53;lag<=230;lag++){let c=0;for(let i=0;i+lag<FL;i++)c+=x[s+i]*x[s+i+lag];c/=e;if(c>best){best=c;bl=lag;}}
  f0.push(best>0.5?SR/bl:0);
}
const st=f=>12*Math.log2(f/100);
const win2=[];const per=Math.round(20/(HP/SR));
let allst=[];
for(let w=0;w*per<f0.length;w++){const v=f0.slice(w*per,(w+1)*per).filter(f=>f>0).map(st);if(v.length<50)continue;const m=v.reduce((a,b)=>a+b,0)/v.length;win2.push(Math.sqrt(v.reduce((s,u)=>s+(u-m)**2,0)/v.length));allst=allst.concat(v);}
out.f0_voiced_frames=allst.length;out.f0_semitone_std_mean_over_20s=+(win2.reduce((a,b)=>a+b,0)/win2.length).toFixed(2);
const ma=allst.reduce((a,b)=>a+b,0)/allst.length;out.f0_semitone_std_global=+Math.sqrt(allst.reduce((s,u)=>s+(u-ma)**2,0)/allst.length).toFixed(2);
out.f0_median_hz=+(100*Math.pow(2,pct(allst,.5)/12)).toFixed(0);
// onset enrichment near cuts
if(cutsf){
  // high-pass (>2kHz) energy via first-difference twice approx
  const hp=new Float32Array(n);for(let i=2;i<n;i++)hp[i]=x[i]-2*x[i-1]+x[i-2];
  const H=80;const nh=Math.floor(n/H);const he=new Float32Array(nh);for(let f=0;f<nh;f++){let s=0;for(let i=0;i<H;i++)s+=hp[f*H+i]**2;he[f]=Math.sqrt(s/H);}
  const flux=new Float32Array(nh);for(let f=10;f<nh;f++){let m=0;for(let k=1;k<=10;k++)m+=he[f-k];m/=10;flux[f]=Math.max(0,he[f]-m*1.0)/(m+0.002);} // relative rise
  const ordered=[...flux].sort((a,b)=>a-b);const T=ordered[Math.floor((+process.env.PCT||0.97)*nh)];
  const isOn=(t0,t1)=>{for(let f=Math.max(10,Math.floor(t0/0.005));f<=Math.min(nh-1,Math.floor(t1/0.005));f++)if(flux[f]>T)return true;return false;};
  const cuts=JSON.parse(fs.readFileSync(cutsf)).map(c=>c.t);
  let hit=0;for(const t of cuts)if(isOn(t-0.05,t+0.12))hit++;
  // baseline: random times
  let seed=7;const rnd=()=>{seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296;};
  let bh=0,B=4000;for(let k=0;k<B;k++){const t=rnd()*(n/SR-1)+0.5;if(isOn(t-0.05,t+0.12))bh++;}
  out.onset_enrichment={cuts:cuts.length,frac_cuts_with_onset:+(hit/cuts.length).toFixed(3),frac_random_with_onset:+(bh/B).toFixed(3),ratio:+((hit/cuts.length)/(bh/B)).toFixed(2)};
}
console.log(JSON.stringify(out,null,0));
fs.writeFileSync(process.env.OUTJ||('/tmp/audio_'+label+'.json'),JSON.stringify(out));
