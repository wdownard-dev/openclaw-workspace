// SCRIPT-V5.md + beats_timing.json + plates-v5/img -> src/timeline.json; stages plate symlinks in public/p/ (read at render time)
const fs=require('fs'),path=require('path'),cp=require('child_process');
const V=path.resolve(__dirname,'..');
const PLATES_DIR=process.env.PLATES_DIR||'plates-v6';
const FF='/home/williamdownard/openclaw-sites/bin/ffmpeg';
const timing=JSON.parse(fs.readFileSync(V+'/audio-v5/beats_timing.json'));
const lines=fs.readFileSync(V+'/SCRIPT-V5.md','utf8').split('\n');
const meta={};let chapter=null,cur=null,chapterOpen=false;
for(const l of lines){
  let m;
  if((m=l.match(/^## CHAPTER: (.+?)\s+\(/))){chapter=m[1];chapterOpen=true;continue;}
  if(/^## COLD OPEN/.test(l)){chapter=null;chapterOpen=false;continue;}
  if((m=l.match(/^\*\*(V5-\d+)\*\*/))){cur=m[1];meta[cur]={chapterStart:chapterOpen?chapter:null};chapterOpen=false;continue;}
}
// narration lines
for(const l of lines){const m=l.match(/^\*\*(V5-\d+)\*\*\s*(.*)$/);if(m&&meta[m[1]])meta[m[1]].text=m[2].trim();}
const ids=Object.keys(timing).sort();
const dur=(()=>{const r=cp.spawnSync(FF,['-i',V+'/audio-v5/narration_voice_only.wav'],{encoding:'utf8'}).stderr;const m=r.match(/Duration: (\d+):(\d+):([\d.]+)/);return +m[1]*3600+ +m[2]*60+ +m[3];})();
const imgdir=V+'/'+PLATES_DIR+'/img';
fs.rmSync('public/p',{recursive:true,force:true});fs.mkdirSync('public/p',{recursive:true});
const missing=[];const beats=[];
ids.forEach((id,i)=>{
  const start=i===0?0:timing[id].start;
  const next=i+1<ids.length?timing[ids[i+1]].start:dur+2.0;
  const fa=imgdir+'/'+id+'a.png',fb=imgdir+'/'+id+'b.png',f=imgdir+'/'+id+'.png';
  let parts=[],ok;
  if(fs.existsSync(fa)&&fs.existsSync(fb)){parts=[id+'a',id+'b'];ok=true;}
  else{ok=fs.existsSync(f);parts=[id];}
  if(ok)parts.forEach(p=>fs.copyFileSync(imgdir+'/'+p+'.png','public/p/'+p+'.png'));else missing.push(id);
  const mm=meta[id]||{};
  beats.push({id,start,end:next,plate:ok,parts,push:(i+1)%4===0,text:mm.text||''});
});
const fps=30;
const total=Math.round((dur+2.0)*fps);
fs.writeFileSync('src/timeline.json',JSON.stringify({fps,total,audioDur:dur,beats,missing},null,1));
if(missing.length)console.log('MISSING PLATES ('+missing.length+'): '+missing.join(' '));
console.log('beats',beats.length,'missing',missing.length);
