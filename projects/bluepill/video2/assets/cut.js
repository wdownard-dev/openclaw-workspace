// Sprite cutout for video 2: flood-fill from the border (pipeline/cutout.js method), keep the largest blob, clear large
// enclosed near-white pockets, 1 px defringe, trim + 8 px pad; writes <out>.png, <out>.json (feet anchor, size) and a
// dark/light check tile <checkdir>/<name>_check.png.
// usage: node cut.js <in.png> <out.png> [--tol 34] [--check dir] [--nopad] [--keepall]
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const fs=require('fs'),path=require('path');
async function cut(inp,outp,opt={}){
  const tol=opt.tol||34;
  const {data,info}=await sharp(inp).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const W=info.width,H=info.height;
  const bg=[255,255,255];
  const hasAlpha=(await sharp(inp).metadata()).hasAlpha&&!opt.flood;
  const near=i=>hasAlpha?data[i+3]<20:(Math.abs(data[i]-bg[0])<tol&&Math.abs(data[i+1]-bg[1])<tol&&Math.abs(data[i+2]-bg[2])<tol);
  const seen=new Uint8Array(W*H),q=[];
  const push=(x,y)=>{const p=y*W+x;if(!seen[p]&&near(p*4)){seen[p]=1;q.push(p)}};
  for(let x=0;x<W;x++){push(x,0);push(x,H-1)}for(let y=0;y<H;y++){push(0,y);push(W-1,y)}
  while(q.length){const p=q.pop(),x=p%W,y=(p/W)|0;if(x>0)push(x-1,y);if(x<W-1)push(x+1,y);if(y>0)push(x,y-1);if(y<H-1)push(x,y+1)}
  if(hasAlpha){for(let p=0;p<W*H;p++)if(seen[p])data[p*4+3]=0;}else for(let p=0;p<W*H;p++)data[p*4+3]=seen[p]?0:255;
  // enclosed near-white pockets larger than minPocket px -> transparent (gaps between arm and body); small ones (eye whites) stay
  const minPocket=opt.minPocket||900;
  const lab2=new Int32Array(W*H);let k=0;
  for(let s=0;s<W*H;s++){if(seen[s]||lab2[s]||!near(s*4))continue;k++;const st=[s];lab2[s]=k;const mem=[];
    while(st.length){const p=st.pop();mem.push(p);const x=p%W,y=(p/W)|0;
      const nb=[[x-1,y],[x+1,y],[x,y-1],[x,y+1]];for(const [xx,yy] of nb){if(xx<0||yy<0||xx>=W||yy>=H)continue;const pp=yy*W+xx;if(!lab2[pp]&&!seen[pp]&&near(pp*4)){lab2[pp]=k;st.push(pp)}}}
    if(mem.length>=minPocket)for(const p of mem)data[p*4+3]=0;}
  // keep the largest blob (plus blobs >= 2% of it) unless keepall
  if(!opt.keepall){const lab=new Int32Array(W*H);let n=0;const sz=[0];
    for(let s=0;s<W*H;s++){if(lab[s]||data[s*4+3]<40)continue;n++;let c=0;const st=[s];lab[s]=n;while(st.length){const p=st.pop();c++;const x=p%W,y=(p/W)|0;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=W||yy>=H)continue;const pp=yy*W+xx;if(!lab[pp]&&data[pp*4+3]>=40){lab[pp]=n;st.push(pp)}}}sz.push(c)}
    const mx=Math.max(...sz);for(let p=0;p<W*H;p++)if(!lab[p]||sz[lab[p]]<mx*0.02)data[p*4+3]=0;}
  // defringe: edge pixels that are light get alpha 0
  const kill=[];for(let y=1;y<H-1;y++)for(let x=1;x<W-1;x++){const i=(y*W+x)*4;if(data[i+3]<20)continue;let e=false;for(let dy=-1;dy<=1&&!e;dy++)for(let dx=-1;dx<=1;dx++)if(data[((y+dy)*W+x+dx)*4+3]<20){e=true;break}
    if(e&&(data[i]+data[i+1]+data[i+2])/3>205)kill.push(i)}for(const i of kill)data[i+3]=0;
  // bbox
  let x0=W,y0=H,x1=-1,y1=-1;for(let y=0;y<H;y++)for(let x=0;x<W;x++)if(data[(y*W+x)*4+3]>=20){if(x<x0)x0=x;if(x>x1)x1=x;if(y<y0)y0=y;if(y>y1)y1=y}
  if(x1<0)throw new Error('empty cutout '+inp);
  // feet anchor: centre of opaque pixels in the bottom 3% of the figure height
  const band=Math.max(3,Math.round((y1-y0)*0.03));let sx=0,c=0;for(let y=y1-band;y<=y1;y++)for(let x=x0;x<=x1;x++)if(data[(y*W+x)*4+3]>=20){sx+=x;c++}
  const feetX=c?sx/c:(x0+x1)/2;
  const pad=opt.nopad?0:8;
  const cw=x1-x0+1+2*pad,ch=y1-y0+1+2*pad;
  const buf=await sharp(data,{raw:{width:W,height:H,channels:4}}).extract({left:x0,top:y0,width:x1-x0+1,height:y1-y0+1})
    .extend({top:pad,bottom:pad,left:pad,right:pad,background:{r:0,g:0,b:0,alpha:0}}).png().toBuffer();
  fs.writeFileSync(outp,buf);
  const side={file:path.basename(outp),source:path.relative(path.dirname(outp),inp),width:cw,height:ch,
    feet:{x:Math.round(feetX-x0+pad),y:ch-pad-1},height_px_at_1080:ch,src_bbox:[x0,y0,x1,y1],src_size:[W,H]};
  fs.writeFileSync(outp.replace(/\.png$/,'.json'),JSON.stringify(side,null,1));
  if(opt.check){fs.mkdirSync(opt.check,{recursive:true});const s=Math.min(1,500/ch);const w=Math.round(cw*s),h=Math.round(ch*s);
    const small=await sharp(buf).resize(w,h).png().toBuffer();
    const tile=await sharp({create:{width:w*3+40,height:h+20,channels:4,background:'#ffffff'}})
      .composite([{input:await sharp({create:{width:w+10,height:h+20,channels:4,background:'#101010'}}).png().toBuffer(),left:0,top:0},
                  {input:await sharp({create:{width:w+10,height:h+20,channels:4,background:'#808080'}}).png().toBuffer(),left:w+15,top:0},
                  {input:small,left:5,top:10},{input:small,left:w+20,top:10},{input:small,left:2*w+35,top:10}]).jpeg({quality:85}).toFile(path.join(opt.check,path.basename(outp,'.png')+'_check.jpg'));}
  return side;
}
module.exports={cut};
if(require.main===module){const a=process.argv.slice(2);const opt={};for(let i=2;i<a.length;i++){if(a[i]==='--tol')opt.tol=+a[++i];if(a[i]==='--check')opt.check=a[++i];if(a[i]==='--nopad')opt.nopad=true;if(a[i]==='--keepall')opt.keepall=true;if(a[i]==='--pocket')opt.minPocket=+a[++i]}
  cut(a[0],a[1],opt).then(s=>console.log(JSON.stringify(s))).catch(e=>{console.error(e.message);process.exit(1)})}
