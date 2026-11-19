// Synthesises every sound effect and the music bed from scratch (no samples, no third-party audio).
// Output: public/sfx/*.wav and public/music/bed.wav (mono, 44.1 kHz, 16-bit). Licence: own work (CC0 / public domain dedication).
const fs=require('fs');const SR=44100;
const rnd=(()=>{let s=1234567;return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296*2-1}})();
const buf=(sec)=>new Float32Array(Math.floor(sec*SR));
function write(name,b,gain=0.9){let pk=1e-9;for(const v of b)pk=Math.max(pk,Math.abs(v));const n=b.length,o=Buffer.alloc(44+n*2);
 o.write('RIFF',0);o.writeUInt32LE(36+n*2,4);o.write('WAVEfmt ',8);o.writeUInt32LE(16,16);o.writeUInt16LE(1,20);o.writeUInt16LE(1,22);o.writeUInt32LE(SR,24);o.writeUInt32LE(SR*2,28);o.writeUInt16LE(2,32);o.writeUInt16LE(16,34);o.write('data',36);o.writeUInt32LE(n*2,40);
 for(let i=0;i<n;i++)o.writeInt16LE(Math.round(Math.max(-1,Math.min(1,b[i]/pk*gain))*32767),44+i*2);fs.writeFileSync(name,o);}
// state-variable filter (bandpass/lowpass) with per-sample cutoff
function svf(){let lo=0,bp=0;return(x,fc,q)=>{const f=2*Math.sin(Math.PI*Math.min(0.45,fc/SR));lo+=f*bp;const hi=x-lo-q*bp;bp+=f*hi;return{lo,bp,hi}}}
const env=(i,n,a,r)=>{const t=i/SR,d=n/SR;return Math.min(1,t/a)*Math.min(1,(d-t)/r)};
fs.mkdirSync('public/sfx',{recursive:true});fs.mkdirSync('public/music',{recursive:true});

// whoosh: noise through a bandpass sweeping up then down
{const b=buf(0.75),f=svf(),n=b.length;for(let i=0;i<n;i++){const u=i/n;const fc=250+3200*Math.sin(Math.PI*u)**1.5;const o=f(rnd(),fc,0.35);b[i]=o.bp*Math.sin(Math.PI*u)**1.2}write('public/sfx/whoosh.wav',b)}
// thud: pitch-dropping sine + low noise burst
{const b=buf(0.8),f=svf(),n=b.length;let ph=0;for(let i=0;i<n;i++){const t=i/SR;const fr=45+110*Math.exp(-t*18);ph+=2*Math.PI*fr/SR;const body=Math.sin(ph)*Math.exp(-t*6);const o=f(rnd(),180,0.5);b[i]=body+o.lo*0.9*Math.exp(-t*30)*2}write('public/sfx/thud.wav',b)}
// pop: short pitch-falling blip with click
{const b=buf(0.22),n=b.length;let ph=0;for(let i=0;i<n;i++){const t=i/SR;ph+=2*Math.PI*(900*Math.exp(-t*22)+180)/SR;b[i]=Math.sin(ph)*Math.exp(-t*20)+rnd()*0.25*Math.exp(-t*90)}write('public/sfx/pop.wav',b)}
// tick: tiny click for route steps
{const b=buf(0.07),n=b.length;for(let i=0;i<n;i++){const t=i/SR;b[i]=Math.sin(2*Math.PI*2400*t)*Math.exp(-t*90)}write('public/sfx/tick.wav',b)}
// ding: glassy two-partial bell (wine cup)
{const b=buf(1.1),n=b.length;for(let i=0;i<n;i++){const t=i/SR;b[i]=(Math.sin(2*Math.PI*1318*t)+0.5*Math.sin(2*Math.PI*1318*2.76*t)+0.3*Math.sin(2*Math.PI*1318*5.4*t))*Math.exp(-t*5.5)}write('public/sfx/ding.wav',b)}
// scrape: stake being sharpened - filtered noise with stroke rhythm
{const b=buf(1.2),f=svf(),n=b.length;for(let i=0;i<n;i++){const t=i/SR;const stroke=Math.abs(Math.sin(t*2*Math.PI*3.2));const o=f(rnd(),2500+1500*stroke,0.5);b[i]=o.hi*0.8*stroke*Math.min(1,t*20)*Math.min(1,(1.2-t)*8)}write('public/sfx/scrape.wav',b,0.7)}
// rumble: boulder rolling, low-passed brown noise with wobble
{const b=buf(2.2),f=svf(),n=b.length;let br=0;for(let i=0;i<n;i++){const t=i/SR;br=(br+rnd()*0.06)*0.995;const o=f(br+rnd()*0.05,140+60*Math.sin(t*9),0.7);b[i]=o.lo*(0.6+0.4*Math.sin(t*14))*Math.min(1,t*6)*Math.min(1,(2.2-t)*3)}write('public/sfx/rumble.wav',b)}
// thunder: long brown-noise roll with cracks
{const b=buf(3),f=svf(),n=b.length;let br=0;for(let i=0;i<n;i++){const t=i/SR;br=(br+rnd()*0.08)*0.994;const o=f(br,260*Math.exp(-t*0.5),0.6);const crack=rnd()*Math.exp(-t*40)*0.8;b[i]=o.lo*3*Math.exp(-t*0.9)*(0.7+0.3*Math.sin(t*5.3))+crack}write('public/sfx/thunder.wav',b)}
// sting: chapter sting - bell chord (A minor add9) + low drum + shimmer swell
{const b=buf(3.2),n=b.length;const notes=[220,329.63,440,659.25];for(let i=0;i<n;i++){const t=i/SR;let v=0;notes.forEach((fr,k)=>{v+=(Math.sin(2*Math.PI*fr*t)+0.4*Math.sin(2*Math.PI*fr*2.76*t)+0.2*Math.sin(2*Math.PI*fr*5.4*t))*Math.exp(-t*(1.4+k*0.35))/ (1+k*0.2)});
 v+=Math.sin(2*Math.PI*(52+60*Math.exp(-t*14))*t)*Math.exp(-t*4)*1.8;v+=rnd()*0.06*Math.min(1,t*2)*Math.exp(-t*1.6);b[i]=v}write('public/sfx/sting.wav',b)}

// ---- music bed: slow A-minor pad + bass + sparse plucks + soft frame drum, with echo ----
{const dur=84,b=buf(dur),n=b.length,bpm=64,beat=60/bpm,bar=beat*4;
 const chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]; // Am, F, C, G (MIDI)
 const mf=(m)=>440*Math.pow(2,(m-69)/12);
 const lp=svf();
 const nb=Math.ceil(dur/(bar*2));
 for(let c=0;c<nb;c++){const ch=chords[c%4],t0=c*bar*2,len=bar*2;
  for(const m of ch){for(const det of [-0.004,0,0.004]){const fr=mf(m)*(1+det);const i0=Math.floor(t0*SR),i1=Math.min(n,Math.floor((t0+len+0.8)*SR));
   for(let i=i0;i<i1;i++){const t=(i-i0)/SR;const a=Math.min(1,t/1.2)*Math.min(1,(len+0.8-t)/1.2);const ph=(fr*t)%1;const saw=2*ph-1;const tri=Math.abs(4*((fr*t+0.25)%1)-2)-1;b[i]+=(0.5*saw+0.5*tri)*a*0.05}}}
  // bass
  {const fr=mf(ch[0]-24),i0=Math.floor(t0*SR),i1=Math.min(n,Math.floor((t0+len+0.3)*SR));for(let i=i0;i<i1;i++){const t=(i-i0)/SR;b[i]+=Math.sin(2*Math.PI*fr*t)*Math.min(1,t/0.4)*Math.min(1,(len+0.3-t)/0.6)*0.16}}
  // pluck arpeggio, 8th notes, sparse
  const pat=[0,2,1,2,0,1,2,1,0,2,1,2,0,1,2,1];
  for(let k=0;k<16;k++){if(k%4===3&&c%2===0)continue;const m=ch[pat[k]]+12+(k%8===6?12:0);const ts=t0+k*beat/2;const fr=mf(m);const i0=Math.floor(ts*SR),i1=Math.min(n,i0+Math.floor(1.1*SR));
   for(let i=i0;i<i1;i++){const t=(i-i0)/SR;b[i]+=(Math.sin(2*Math.PI*fr*t)+0.3*Math.sin(2*Math.PI*fr*2*t))*Math.exp(-t*4.5)*0.045}}
  // frame drum on bar starts
  for(const off of [0,bar]){const ts=t0+off;const i0=Math.floor(ts*SR),i1=Math.min(n,i0+Math.floor(0.7*SR));let ph=0;for(let i=i0;i<i1;i++){const t=(i-i0)/SR;ph+=2*Math.PI*(58+70*Math.exp(-t*22))/SR;b[i]+=Math.sin(ph)*Math.exp(-t*7)*0.22}}
 }
 // soften the pad/plucks with a gentle lowpass and add echo
 let lo=0;for(let i=0;i<n;i++){lo+=(b[i]-lo)*0.18;b[i]=lo}
 const d1=Math.floor(beat*0.75*SR);for(let i=d1;i<n;i++)b[i]+=b[i-d1]*0.32;
 const fade=Math.floor(2*SR);for(let i=0;i<fade;i++){b[i]*=i/fade;b[n-1-i]*=i/fade}
 write('public/music/bed.wav',b,0.8)}
console.log('ok');
