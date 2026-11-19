const fs=require('fs');
const wav=process.argv[2];
const buf=fs.readFileSync(wav);let off=12;while(off<buf.length){const id=buf.toString('ascii',off,off+4);const sz=buf.readUInt32LE(off+4);if(id==='data'){off+=8;break;}off+=8+sz;}
const n=(buf.length-off)>>2;const SR=44100,H=2205;const nf=Math.floor(n/H);
const mid=new Float32Array(nf),side=new Float32Array(nf);
for(let f=0;f<nf;f++){let m=0,s=0;for(let i=0;i<H;i++){const l=buf.readInt16LE(off+4*(f*H+i))/32768,r=buf.readInt16LE(off+4*(f*H+i)+2)/32768;m+=((l+r)/2)**2;s+=((l-r)/2)**2;}mid[f]=Math.sqrt(m/H);side[f]=Math.sqrt(s/H);}
const db=v=>20*Math.log10(Math.max(v,1e-9));
const idx=[...Array(nf).keys()].sort((a,b)=>mid[a]-mid[b]);
const q=idx.slice(0,Math.floor(nf*0.05)),loud=idx.slice(Math.floor(nf*0.5));
const avg=(ids,a)=>ids.reduce((s,i)=>s+a[i]**2,0)/ids.length;
console.log('quietest 5% frames: mid',db(Math.sqrt(avg(q,mid))).toFixed(1),'side',db(Math.sqrt(avg(q,side))).toFixed(1));
console.log('loud 50% frames: mid',db(Math.sqrt(avg(loud,mid))).toFixed(1),'side',db(Math.sqrt(avg(loud,side))).toFixed(1));
// simple spectrum of quietest frames (mono): DFT of 50ms frames at selected bins using Goertzel for bands
const bands=[[50,150],[150,300],[300,600],[600,1200],[1200,2500],[2500,5000],[5000,10000]];
function bandE(frame0){const res=[];const N=H;const x=new Float32Array(N);for(let i=0;i<N;i++){x[i]=(buf.readInt16LE(off+4*(frame0*H+i))+buf.readInt16LE(off+4*(frame0*H+i)+2))/65536*(0.5-0.5*Math.cos(2*Math.PI*i/N));}
 for(const [a,b] of bands){let e=0;for(let fr=a;fr<b;fr+=20){let re=0,im=0;const w=2*Math.PI*fr/SR;for(let i=0;i<N;i++){re+=x[i]*Math.cos(w*i);im+=x[i]*Math.sin(w*i);}e+=(re*re+im*im);}res.push(e);}return res;}
const acc=bands.map(()=>0);const sample=q.filter((_,k)=>k%3===0).slice(0,60);
for(const f of sample){const e=bandE(f);e.forEach((v,i)=>acc[i]+=v);}
const tot=acc.reduce((a,b)=>a+b,0);
console.log('quiet-frame band share (%) 50-150,150-300,300-600,600-1.2k,1.2-2.5k,2.5-5k,5-10k:',acc.map(v=>(100*v/tot).toFixed(1)).join(', '));
