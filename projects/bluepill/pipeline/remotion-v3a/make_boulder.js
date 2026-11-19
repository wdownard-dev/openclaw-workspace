// painted boulder prop cropped from the cave background (matches the painting), elliptical feathered mask
const sharp=require('../node_modules/sharp');
(async()=>{
 const L=150,T=262,W=450,H=410;
 const svg=Buffer.from(`<svg width="${W}" height="${H}"><defs><filter id="b"><feGaussianBlur stdDeviation="3"/></filter></defs><ellipse cx="${W*0.48}" cy="${H*0.54}" rx="${W*0.465}" ry="${H*0.45}" fill="#fff" filter="url(#b)"/></svg>`);
 const mask=await sharp(svg).png().extract({left:0,top:0,width:W,height:H}).ensureAlpha().extractChannel(3).toBuffer();
 const rgb=await sharp('public/bg/cave.jpg').extract({left:L,top:T,width:W,height:H}).removeAlpha().toBuffer();
 await sharp(rgb).joinChannel(mask).png().toFile('public/img3/boulder3.png');
 const m=await sharp('public/img3/boulder3.png').trim().metadata();console.log(m.width,m.height);
})();
