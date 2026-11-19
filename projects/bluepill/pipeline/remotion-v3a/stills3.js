// usage: node stills3.js <outDir> [index...]   renders the six key stills (a-f) from src/shots3.tsx; plus clip frames with: --clip t1 t2 ...
const {bundle}=require('@remotion/bundler');const {renderStill,selectComposition}=require('@remotion/renderer');
const path=require('path'),fs=require('fs');
(async()=>{
  const args=process.argv.slice(2);const out=args[0];fs.mkdirSync(out,{recursive:true});
  const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),onProgress:()=>{}});
  const ts=[4.8,2.0,1.5,3.4,1.5,1.5],names=['a_establishing','b_boulder','c_face_to_face','d_cup','e_blinded','f_ship'];
  if(args[1]==='--clip'){const comp=await selectComposition({serveUrl,id:'BluePillV3aClip'});
    for(const x of args.slice(2)){await renderStill({composition:comp,serveUrl,frame:Math.round(parseFloat(x)*30),output:path.join(out,`clip_${x}.jpg`),imageFormat:'jpeg',jpegQuality:88});process.stdout.write(x+' ')}return console.log('done')}
  const idx=args.length>1?args.slice(1).map(Number):[0,1,2,3,4,5];
  for(const i of idx){const comp=await selectComposition({serveUrl,id:'BluePillV3aStill',inputProps:{which:i}});
    await renderStill({composition:comp,serveUrl,inputProps:{which:i},frame:Math.round(ts[i]*30),output:path.join(out,`stills_${names[i]}.jpg`),imageFormat:'jpeg',jpegQuality:90});process.stdout.write(names[i]+' ')}
  console.log('done');
})().catch(e=>{console.error(e);process.exit(1)});
