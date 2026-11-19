// Code-built crew group sets from single accepted sprites (ASSET-PLAN 2.3): line12, huddle4, workers_group. No API calls.
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');const fs=require('fs');
const S=__dirname+'/sprites/';
async function fig(name,h,flip,rot){let s=sharp(S+name+'.png').resize({height:h});if(flip)s=s.flop();if(rot)s=s.rotate(rot,{background:{r:0,g:0,b:0,alpha:0}});const b=await s.png().toBuffer();const m=await sharp(b).metadata();return {b,w:m.width,h:m.height}}
async function build(out,items,W,H){
  const comps=[];for(const it of items){const f=await fig(it.n,it.h,it.flip,it.rot);comps.push({input:f.b,left:Math.round(it.x-f.w/2),top:Math.round(H-8-f.h+it.dy)})}
  const buf=await sharp({create:{width:W,height:H,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite(comps).png().toBuffer();
  const t=await sharp(buf).trim().png().toBuffer();const m=await sharp(t).metadata();fs.writeFileSync(S+out+'.png',t);
  fs.writeFileSync(S+out+'.json',JSON.stringify({file:out+'.png',source:'code: groups.js from '+[...new Set(items.map(i=>i.n))].join(', '),width:m.width,height:m.height,feet:{x:Math.round(m.width/2),y:m.height-9},height_px_at_1080:m.height},null,1));
  console.log(out,m.width,m.height)}
(async()=>{
  // line12: 12 sailors at 240 px, alternating neutral/point, small offsets (storyboard places it at h=240)
  const line=[];for(let i=0;i<12;i++)line.push({n:i%3==1?'crew__point__a':'crew__neutral__a',h:240,x:60+i*95,dy:(i%2)*6-3,flip:i%4==3});
  await build('crew__line12__a',line,1300,300);
  // huddle4: four at 300 px, outer two mirrored and leaning in
  await build('crew__huddle4__a',[{n:'crew__plead__a',h:300,x:120,dy:0,rot:8},{n:'crew__neutral__a',h:300,x:260,dy:-6},{n:'crew__plead__a',h:300,x:400,dy:-6,flip:true},{n:'crew__neutral__a',h:300,x:540,dy:0,flip:true,rot:-8}],700,360);
  // workers_group: six at 300 px, alternating lookup and point
  const w=[];for(let i=0;i<6;i++)w.push({n:i%2?'crew__point__a':'crew__lookup__a',h:300,x:120+i*150,dy:(i%2)*8-4,flip:i>=3});
  await build('crew__workers_group__a',w,1100,360);
})();
