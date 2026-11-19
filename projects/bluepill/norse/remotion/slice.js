// usage: node slice.js prep <cuts.json>   -> stages scenes/slice1/img into public/s/, writes src/slice_timeline.json
//        node slice.js sheet              -> out/slice1_sheet.jpg (one render-time frame per beat + narration)
const fs=require('fs'),path=require('path'),cp=require('child_process');
const V=path.resolve(__dirname,'..');  // norse/
const NAME=process.env.SLICE_NAME||'slice1';
const FPS=30,END=parseFloat(process.env.SLICE_END||'155.0'),TAIL=parseFloat(process.env.SLICE_TAIL||'0');
const FF='/home/williamdownard/openclaw-sites/bin/ffmpeg';
if(process.argv[2]==='prep'){
  const cutsPath=path.resolve(process.argv[3]);
  const cuts=JSON.parse(fs.readFileSync(cutsPath)).cuts;
  const imgdir=path.dirname(cutsPath)+'/img';
  fs.rmSync('public/s',{recursive:true,force:true});fs.mkdirSync('public/s',{recursive:true});
  const tarr=JSON.parse(fs.readFileSync(V+'/audio-n/beats_timing.json'));
  const timing=Array.isArray(tarr)?Object.fromEntries(tarr.map(x=>[x.beat,x])):tarr;
  const narr={};for(const s of JSON.parse(fs.readFileSync(V+'/scenes/scene_plan.json')))for(const b of s.per_beat)narr[b.beat]=b.narration_line||'';
  const out=cuts.map((c,i)=>{
    const start=i===0?0:timing[c.beat].start;
    const end=i+1<cuts.length?timing[cuts[i+1].beat].start:END+TAIL;
    fs.copyFileSync(imgdir+'/'+c.image,'public/s/'+c.image);if(c.image2)fs.copyFileSync(imgdir+'/'+c.image2,'public/s/'+c.image2);
    return {...c,start_s:+start.toFixed(3),end_s:+end.toFixed(3),text:narr[c.beat]||''};
  });
  const total=Math.round((END+TAIL)*FPS);
  fs.writeFileSync('src/slice_timeline.json',JSON.stringify({fps:FPS,total,cuts:out},null,1));
  console.log('cuts',out.length,'frames',total);
}else if(process.argv[2]==='sheet'){
  const TL=JSON.parse(fs.readFileSync('src/slice_timeline.json'));
  const beats=TL.cuts;const dir='out/'+NAME;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir,{recursive:true});
  const bundle=dir+'/bundle';
  let r=cp.spawnSync('npx',['remotion','bundle','src/index.ts','--out-dir='+bundle,'--log=error'],{stdio:'inherit'});if(r.status)process.exit(1);
  for(const b of beats){
    const fr=Math.min(TL.total-1,Math.round((b.start_s+0.3)*TL.fps));
    r=cp.spawnSync('npx',['remotion','still',bundle,'Slice',`${dir}/${b.beat}.jpg`,'--frame='+fr,'--scale=0.25','--image-format=jpeg','--jpeg-quality=80','--log=error'],{encoding:'utf8'});
    if(r.status){console.error('still failed '+b.beat+'\n'+r.stderr);process.exit(1);}
  }
  const COLS=6,W=410,H=Math.round(W*9/16)+74;
  const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
  const root=process.cwd();
  const CHROME=cp.execSync('ls /home/williamdownard/openclaw-sites/browsers/chromium-*/chrome-linux64/chrome').toString().split('\n')[0];
  const cells=beats.map(b=>`<div class=c><img src="file://${root}/${dir}/${b.beat}.jpg"><b>${b.beat} ${b.move}${b.image.includes('_v')?' [variant]':''}</b><p>${esc(b.text)}</p></div>`).join('');
  const rows=Math.ceil(beats.length/COLS);
  fs.writeFileSync(dir+'/s.html',`<meta charset=utf-8><style>body{margin:0;background:#111;width:${COLS*W}px;display:flex;flex-wrap:wrap}.c{width:${W}px;height:${H}px;box-sizing:border-box;padding:2px;overflow:hidden;color:#eee;font:12px/14px sans-serif}img{width:${W-4}px;height:${Math.round((W-4)*9/16)}px;display:block}b{display:block;color:#c9a227;font:bold 12px monospace;margin-top:2px}p{margin:0}</style>${cells}`);
  cp.spawnSync(CHROME,['--headless=new','--no-sandbox','--allow-file-access-from-files','--hide-scrollbars',`--window-size=${COLS*W},${rows*H}`,`--screenshot=${dir}/s.png`,'file://'+root+'/'+dir+'/s.html']);
  cp.spawnSync(FF,['-y','-loglevel','error','-i',dir+'/s.png','-q:v','3','out/'+NAME+'_sheet.jpg']);
  console.log('wrote out/'+NAME+'_sheet.jpg ('+COLS*W+'x'+rows*H+')');
}
