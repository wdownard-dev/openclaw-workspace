// usage: node stills.js <outDir> <mode: shots|even|list> [frames/seconds...]
// shots: start+25%+60%+end per shot; even: 8 evenly spaced; list: given seconds
const {bundle}=require('@remotion/bundler');const {renderStill,selectComposition}=require('@remotion/renderer');
const path=require('path'),fs=require('fs');
(async()=>{
  const [out,mode,...rest]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
  const timing=require('./data/timing.json');const fps=timing.fps;
  const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),onProgress:()=>{}});
  const comp=await selectComposition({serveUrl,id:'MythLedgerCyclopsV2'});
  let jobs=[];
  if(mode==='shots'){timing.shots.forEach((s,i)=>{for(const k of [0.06,0.4,0.85]){const t=s.start+(s.end-s.start)*k;jobs.push([`shot${String(i).padStart(2,'0')}_${k}`,Math.round(t*fps)])}})}
  else if(mode==='even'){for(let i=0;i<8;i++){const t=(i+0.5)*timing.duration/8;jobs.push([`v2_${String(i+1).padStart(2,'0')}_${t.toFixed(1)}s`,Math.round(t*fps)])}}
  else rest.forEach(x=>jobs.push([`t${x}`,Math.round(parseFloat(x)*fps)]));
  if(rest.length&&mode==='shots'){const only=new Set(rest.map(Number));jobs=jobs.filter(j=>only.has(parseInt(j[0].slice(4,6))))}
  for(const [name,frame] of jobs){await renderStill({composition:comp,serveUrl,frame,output:path.join(out,name+'.jpg'),imageFormat:'jpeg',jpegQuality:85});process.stdout.write(name+' ')}
  console.log('done');
})().catch(e=>{console.error(e);process.exit(1)});
