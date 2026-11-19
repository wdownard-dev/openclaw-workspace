const sharp=require('sharp');
(async()=>{const bg='../tests/round1/olympus__gpt-image-2.6-sunburst.png';const m=await sharp(bg).metadata();const H=m.height;
const place=[['zeus',0.62,0.08],['athena',0.50,0.34],['cyclops',0.78,0.60],['medusa',0.42,0.84]];
const comps=[];for(const [n,hf,xf] of place){const buf=await sharp(`../tests/cutouts/${n}.png`).resize({height:Math.round(H*hf)}).toBuffer();const mm=await sharp(buf).metadata();comps.push({input:buf,left:Math.min(Math.round(m.width*xf),m.width-mm.width-5),top:H-mm.height-Math.round(H*0.04)});}
await sharp(bg).composite(comps).png().toFile('../tests/cutouts/demo_olympus_cast.png');
const d='../tests/storyboard',T=600,names=['s1_arrive','s2_trapped','s3_wine','s4_asleep','s5_escape','s6_sail'];const cs=[];
for(let i=0;i<6;i++)cs.push({input:await sharp(`${d}/${names[i]}.png`).resize(T,400).toBuffer(),left:(i%3)*T,top:Math.floor(i/3)*400});
await sharp({create:{width:T*3,height:800,channels:3,background:'#222'}}).composite(cs).jpeg({quality:88}).toFile(d+'/storyboard_sheet.jpg');console.log('ok')})();
