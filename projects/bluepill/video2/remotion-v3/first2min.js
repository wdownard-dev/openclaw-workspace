// out/FIRST-2MIN*.jpg: one render-time frame per beat V5-001..043 at start+0.3s, 6 cols, labelled with id + narration
const fs=require('fs'),cp=require('child_process');
const FF='/home/williamdownard/openclaw-sites/bin/ffmpeg';
const TL=JSON.parse(fs.readFileSync('src/timeline.json'));
const beats=TL.beats.filter(b=>{const n=+b.id.slice(3);return n>=1&&n<=43;});
const dir='out/first2min';fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir,{recursive:true});
const bundle=dir+'/bundle';
let r=cp.spawnSync('npx',['remotion','bundle','src/index.ts','--out-dir='+bundle,'--log=error'],{stdio:'inherit'});
if(r.status)process.exit(1);
const CONC=process.env.CONC||'4';
for(const b of beats){
  const fr=Math.round((b.start+0.3)*TL.fps);
  r=cp.spawnSync('npx',['remotion','still',bundle,'BluePill',`${dir}/${b.id}.jpg`,'--frame='+fr,'--scale=0.25','--image-format=jpeg','--jpeg-quality=80','--log=error'],{encoding:'utf8'});
  if(r.status){console.error('still failed '+b.id+'\n'+r.stderr);process.exit(1);}
}
const COLS=6,W=410,H=Math.round(W*9/16)+74,GAP=0;   // 6*410=2460px
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
const root=process.cwd();
const CHROME=cp.execSync('ls /home/williamdownard/openclaw-sites/browsers/chromium-*/chrome-linux64/chrome').toString().split('\n')[0];
const rowsPer=Math.floor(3000/H);let parts=[];
for(let i=0;i<beats.length;i+=COLS*rowsPer)parts.push(beats.slice(i,i+COLS*rowsPer));
const names=parts.length===1?['FIRST-2MIN_v6']:parts.map((_,i)=>'FIRST-2MIN_v6_'+'abcdefgh'[i]);
// split only if a single sheet would exceed 3000px
const allRows=Math.ceil(beats.length/COLS);
if(allRows*H<=3000){parts=[beats];names.length=0;names.push('FIRST-2MIN_v6');}
parts.forEach((pb,pi)=>{
  const cells=pb.map(b=>`<div class=c><img src="file://${root}/${dir}/${b.id}.jpg"><b>${b.id}</b><p>${esc(b.text)}</p></div>`).join('');
  const rows=Math.ceil(pb.length/COLS);
  fs.writeFileSync(dir+'/s.html',`<meta charset=utf-8><style>body{margin:0;background:#111;width:${COLS*W}px;display:flex;flex-wrap:wrap}.c{width:${W}px;height:${H}px;box-sizing:border-box;padding:2px;overflow:hidden;color:#eee;font:12px/14px sans-serif}img{width:${W-4}px;height:${Math.round((W-4)*9/16)}px;display:block}b{display:block;color:#c9a227;font:bold 12px monospace;margin-top:2px}p{margin:0}</style>${cells}`);
  cp.spawnSync(CHROME,['--headless=new','--no-sandbox','--allow-file-access-from-files','--hide-scrollbars',`--window-size=${COLS*W},${rows*H}`,`--screenshot=${dir}/s.png`,'file://'+root+'/'+dir+'/s.html']);
  cp.spawnSync(FF,['-y','-loglevel','error','-i',dir+'/s.png','-q:v','3',`out/${names[pi]}.jpg`]);
  console.log('wrote out/'+names[pi]+'.jpg ('+COLS*W+'x'+rows*H+')');
});
