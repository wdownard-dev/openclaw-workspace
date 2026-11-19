// usage: node stills_cheap.js <outDir> [scene...]   renders the Stage compositing pass for each preset in src/stagePresets.ts (default: fire sunrise)
const {bundle}=require('@remotion/bundler');const {renderStill,selectComposition}=require('@remotion/renderer');
const path=require('path'),fs=require('fs');
(async()=>{const a=process.argv.slice(2);const out=a[0];fs.mkdirSync(out,{recursive:true});
 const scenes=a.length>1?a.slice(1):['fire','sunrise'];
 const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),onProgress:()=>{}});
 for(const scene of scenes){const comp=await selectComposition({serveUrl,id:'CheapStage',inputProps:{scene}});
  await renderStill({composition:comp,serveUrl,inputProps:{scene},frame:0,output:path.join(out,`arm1_${scene}.jpg`),imageFormat:'jpeg',jpegQuality:92});process.stdout.write(scene+' ')}
 console.log('done')})().catch(e=>{console.error(e);process.exit(1)});
