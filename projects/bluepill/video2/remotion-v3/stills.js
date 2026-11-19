// stills: chapter first beats + 8 spread; labelled sheet; QA.md
const fs=require('fs'),cp=require('child_process');
const FF='/home/williamdownard/openclaw-sites/bin/ffmpeg';
const TL=JSON.parse(fs.readFileSync('src/timeline.json'));
fs.rmSync('out/stills_v6',{recursive:true,force:true});fs.mkdirSync('out/stills_v6',{recursive:true});
const picks=[];
const N=14;for(let i=0;i<N;i++){const t=TL.audioDur*(i+0.5)/N;const b=TL.beats.filter(x=>x.start<=t).pop();picks.push({t:b.start+Math.min(1,(b.end-b.start)/2),name:'still_'+(i+1)+'_'+b.id});}
const files=[];
for(const p of picks){const o=`out/stills_v6/${p.name}.jpg`;cp.spawnSync(FF,['-y','-loglevel','error','-ss',p.t.toFixed(3),'-i','out/animatic_v6_540p.mp4','-frames:v','1','-q:v','3',o]);files.push({o,p});}
// sheet: 4 columns x 600 px = 2400 wide, labels via headless Chrome (ffmpeg build has no drawtext)
const root=process.cwd();
const cells=files.map(f=>`<div class=c><img src="file://${root}/${f.o}"><span>${f.p.name}</span></div>`).join('');
const rows=Math.ceil(files.length/4);
fs.writeFileSync('out/sheet.html',`<style>body{margin:0;background:#000;width:2400px;display:flex;flex-wrap:wrap}.c{position:relative;width:600px;height:338px}img{width:600px;height:338px}span{position:absolute;left:0;bottom:0;right:0;background:#000b;color:#fff;font:18px monospace;padding:3px 6px}</style>${cells}`);
const CH=cp.execSync('ls /home/williamdownard/openclaw-sites/browsers/chromium-*/chrome-linux64/chrome').toString().split('\n')[0];
cp.spawnSync(CH,['--headless=new','--no-sandbox','--allow-file-access-from-files','--hide-scrollbars',`--window-size=2400,${rows*338}`,'--screenshot=out/s.png','file://'+root+'/out/sheet.html']);
cp.spawnSync(FF,['-y','-loglevel','error','-i','out/s.png','-q:v','3','out/stills_v6_sheet.jpg']);
fs.rmSync('out/s.png');fs.rmSync('out/sheet.html');
console.log('stills',files.length,'sheet done');
