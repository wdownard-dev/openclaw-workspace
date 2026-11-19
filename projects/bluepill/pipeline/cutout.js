// Free background removal: flood-fill the plain off-white backdrop from the borders. Dark outlines stop the fill, so white heads stay opaque.
const sharp=require('sharp');
async function cutout(inp,outp,tol=34){
  const {data,info}=await sharp(inp).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  const W=info.width,H=info.height,bg=[data[0],data[1],data[2]];
  const near=i=>Math.abs(data[i]-bg[0])<tol&&Math.abs(data[i+1]-bg[1])<tol&&Math.abs(data[i+2]-bg[2])<tol;
  const seen=new Uint8Array(W*H),q=[];
  const push=(x,y)=>{const p=y*W+x;if(!seen[p]&&near(p*4)){seen[p]=1;q.push(p)}};
  for(let x=0;x<W;x++){push(x,0);push(x,H-1)}for(let y=0;y<H;y++){push(0,y);push(W-1,y)}
  while(q.length){const p=q.pop(),x=p%W,y=(p/W)|0;if(x>0)push(x-1,y);if(x<W-1)push(x+1,y);if(y>0)push(x,y-1);if(y<H-1)push(x,y+1)}
  for(let p=0;p<W*H;p++)if(seen[p])data[p*4+3]=0;
  await sharp(data,{raw:{width:W,height:H,channels:4}}).trim().png().toFile(outp);
}
module.exports={cutout};
if(require.main===module)(async()=>{const d='../tests/characters3';const fs=require('fs');fs.mkdirSync('../tests/cutouts',{recursive:true});
 const L=[['../tests/characters/01_round_hero.png','hero'],[d+'/zeus.png','zeus'],[d+'/athena.png','athena'],[d+'/cyclops.png','cyclops'],[d+'/medusa.png','medusa']];
 for(const [i,n] of L){await cutout(i,`../tests/cutouts/${n}.png`);console.log(n)}})();
