// Style-A cutouts: native alpha where present (normalised), else flood fill from the border on near-white, then trim + defringe.
const sharp=require('../node_modules/sharp');const fs=require('fs');
const G='../../tests/chars_v3/gen/',OUT='public/img3/',TST='../../tests/v3a/cut/';
const L={ody:'odysseus_A',cy:'cyclops_A',crew:'crew_A',sheep:'sheep_A',pos:'poseidon_A',ody_shout:'pose_ody_A',cy_blind:'pose_cy_A'};
async function proc(key,file){
  const {data,info}=await sharp(G+file+'.png').ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const W=info.width,H=info.height;const meta=await sharp(G+file+'.png').metadata();
  if(!meta.hasAlpha){ // flood fill white backdrop
    const bg=[data[0],data[1],data[2]],tol=26;
    const near=i=>Math.abs(data[i]-bg[0])<tol&&Math.abs(data[i+1]-bg[1])<tol&&Math.abs(data[i+2]-bg[2])<tol;
    const seen=new Uint8Array(W*H),q=[];const push=(x,y)=>{const p=y*W+x;if(!seen[p]&&near(p*4)){seen[p]=1;q.push(p)}};
    for(let x=0;x<W;x++){push(x,0);push(x,H-1)}for(let y=0;y<H;y++){push(0,y);push(W-1,y)}
    while(q.length){const p=q.pop(),x=p%W,y=(p/W)|0;if(x>0)push(x-1,y);if(x<W-1)push(x+1,y);if(y>0)push(x,y-1);if(y<H-1)push(x,y+1)}
    for(let p=0;p<W*H;p++)data[p*4+3]=seen[p]?0:255;
    // enclosed pure-white pockets (between arm and body etc.) that are large: remove
  } else {
    for(let p=0;p<W*H;p++){const a=data[p*4+3];data[p*4+3]=a>=235?255:a<=20?0:Math.round((a-20)/215*255)}
  }
  // keep largest blob
  const lab=new Int32Array(W*H);let n=0;const sz=[0];
  for(let s=0;s<W*H;s++){if(lab[s]||data[s*4+3]<40)continue;n++;let c=0;const st=[s];lab[s]=n;while(st.length){const p=st.pop();c++;const x=p%W,y=(p/W)|0;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=W||yy>=H)continue;const pp=yy*W+xx;if(!lab[pp]&&data[pp*4+3]>=40){lab[pp]=n;st.push(pp)}}}sz.push(c)}
  const mx=Math.max(...sz);for(let p=0;p<W*H;p++)if(!lab[p]||sz[lab[p]]<mx*0.02)data[p*4+3]=0;
  // defringe 1px: edge pixels that are near-white and light get alpha 0 (flood-filled sources only)
  if(!meta.hasAlpha){for(let pass=0;pass<1;pass++){const kill=[];for(let y=1;y<H-1;y++)for(let x=1;x<W-1;x++){const i=(y*W+x)*4;if(data[i+3]<20)continue;let e=false;for(let dy=-1;dy<=1&&!e;dy++)for(let dx=-1;dx<=1;dx++)if(data[((y+dy)*W+x+dx)*4+3]<20){e=true;break}
    if(e&&(data[i]+data[i+1]+data[i+2])/3>215)kill.push(i)}for(const i of kill)data[i+3]=0}}
  // soften alpha edge slightly (1px blur of alpha only) for AA on flood-filled
  let img=sharp(data,{raw:{width:W,height:H,channels:4}});
  const buf=await img.trim({threshold:1}).png().toBuffer();
  fs.writeFileSync(OUT+key+'.png',buf);
  const m=await sharp(buf).metadata();return {key,w:m.width,h:m.height};
}
(async()=>{const dims={};for(const [k,f] of Object.entries(L)){const r=await proc(k,f);dims[k]={w:r.w,h:r.h};console.log(r)}
 fs.writeFileSync('src/assetDims3.json',JSON.stringify(dims,null,1));
 // edge checks on dark and light
 const keys=Object.keys(L);const tiles=[];
 for(const bgc of [{r:30,g:30,b:50},{r:240,g:230,b:210}]){
  const row=[];for(const k of keys){row.push(await sharp(OUT+k+'.png').resize({height:420,width:300,fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).flatten({background:bgc}).png().toBuffer())}
  tiles.push(await sharp({create:{width:300*keys.length,height:420,channels:3,background:bgc}}).composite(row.map((b,i)=>({input:b,left:i*300,top:0}))).png().toBuffer());}
 await sharp({create:{width:300*keys.length,height:840,channels:3,background:{r:0,g:0,b:0}}}).composite(tiles.map((b,i)=>({input:b,left:0,top:i*420}))).jpeg({quality:90}).toFile(TST+'cut_check.jpg');
})();
