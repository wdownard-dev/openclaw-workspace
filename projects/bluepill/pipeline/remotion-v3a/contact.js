// node contact.js out.jpg cols tileW img1 img2 ...
const sharp=require('sharp');
(async()=>{const [out,cols,tw,...f]=process.argv.slice(2);const C=+cols,W=+tw,H=Math.round(W*9/16);
const b=await Promise.all(f.map(x=>sharp(x).resize(W,H).toBuffer()));const rows=Math.ceil(b.length/C);
await sharp({create:{width:C*W,height:rows*H,channels:3,background:'#000'}}).composite(b.map((x,i)=>({input:x,left:(i%C)*W,top:Math.floor(i/C)*H}))).jpeg({quality:85}).toFile(out)})()
