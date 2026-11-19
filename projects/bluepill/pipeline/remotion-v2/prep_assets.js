// Copies/cuts the art into public/ and writes src/assetDims.json (natural sizes for bottom-anchored layout).
const sharp=require('../node_modules/sharp');
const {cutout}=require('../cutout.js');
const fs=require('fs'),path=require('path');
// keep only the largest connected opaque blob (the prop sheet cells can contain slivers of neighbouring props)
async function keepLargest(file,thr=0.06){
  const {data,info}=await sharp(file).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const W=info.width,H=info.height,lab=new Int32Array(W*H);let bestN=0,n=0;const sizes=[0];
  for(let s0=0;s0<W*H;s0++){ if(lab[s0]||data[s0*4+3]<20)continue; n++;let cnt=0;const q=[s0];lab[s0]=n;
    while(q.length){const p=q.pop();cnt++;const x=p%W,y=(p/W)|0;for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){const xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=W||yy>=H)continue;const pp=yy*W+xx;if(!lab[pp]&&data[pp*4+3]>=20){lab[pp]=n;q.push(pp)}}}
    sizes.push(cnt);if(cnt>bestN)bestN=cnt}
  for(let p=0;p<W*H;p++)if(!lab[p]||sizes[lab[p]]<bestN*thr)data[p*4+3]=0;
  // defringe: drop light, low-saturation edge pixels left over from the backdrop (two passes)
  for(let pass=0;pass<2;pass++){const kill=[];for(let y=1;y<H-1;y++)for(let x=1;x<W-1;x++){const p=y*W+x,i=p*4;if(data[i+3]<20)continue;
    let edge=false;for(let dy=-1;dy<=1&&!edge;dy++)for(let dx=-1;dx<=1;dx++){if(data[((y+dy)*W+x+dx)*4+3]<20){edge=true;break}}
    if(!edge)continue;const r=data[i],g=data[i+1],b=data[i+2];if((r+g+b)/3>205&&Math.max(r,g,b)-Math.min(r,g,b)<34)kill.push(i)}
    for(const i of kill)data[i+3]=0}
  await sharp(data,{raw:{width:W,height:H,channels:4}}).trim().png().toFile(file+'.tmp');fs.renameSync(file+'.tmp',file);
}
const T=path.join(__dirname,'../../tests/'), P=path.join(__dirname,'public/');
(async()=>{
  const dims={};
  // characters (already cutouts)
  for(const n of ['hero','cyclops']){fs.copyFileSync(T+`cutouts/${n}.png`,P+`img/${n}.png`);}
  // props: split the 3x2 sheet into cells, flood-fill cut each
  const names=['sheep','cup','stake','boulder','ship','amphora'];
  const meta=await sharp(T+'v2/gen/props_sheet.png').metadata();
  const cw=meta.width/3,ch=meta.height/2;
  for(let i=0;i<6;i++){
    const tmp=P+`img/_cell${i}.png`;
    await sharp(T+'v2/gen/props_sheet.png').extract({left:Math.round((i%3)*cw),top:Math.round(Math.floor(i/3)*ch),width:Math.round(cw),height:Math.round(ch)}).toFile(tmp);
    await cutout(tmp,P+`img/${names[i]}.png`,38); await keepLargest(P+`img/${names[i]}.png`, names[i]==='ship'?0.004:0.06); fs.unlinkSync(tmp);
  }
  // backgrounds -> jpg
  const BG={island:'v2/gen/island_dusk.png',cave:'round1/cyclops_cave__gpt-image-2.6-sunburst.png',cavedark:'round1/cyclops_cave__gpt-image-2.png',
    cavedawn:'v2/gen/cave_mouth_dawn.png',map:'round2/map_sunburst.png',sea:'v2/gen/sea_sunrise.png',storm:'round1/storm_ship__gpt-image-2.6-sunburst.png'};
  for(const [k,f] of Object.entries(BG)){await sharp(T+f).resize(1536).jpeg({quality:90}).toFile(P+`bg/${k}.jpg`);}
  for(const f of fs.readdirSync(P+'img')){const m=await sharp(P+'img/'+f).metadata();dims[f.replace('.png','')]={w:m.width,h:m.height};}
  fs.copyFileSync(path.join(__dirname,'../../brand/avatar_800.png'),P+'img/avatar.png');
  dims.avatar={w:800,h:800};
  fs.writeFileSync(path.join(__dirname,'src/assetDims.json'),JSON.stringify(dims,null,1));
  console.log(dims);
})();
