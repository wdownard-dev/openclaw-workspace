const sharp=require('sharp'),fs=require('fs');const dir='../tests/characters';
const files=fs.readdirSync(dir).filter(f=>/^\d\d_.*\.png$/.test(f)).sort();const T=480,cols=3,rows=Math.ceil(files.length/cols);
(async()=>{const comps=[];for(let i=0;i<files.length;i++){const x=(i%cols)*T,y=Math.floor(i/cols)*(T+36);
comps.push({input:await sharp(`${dir}/${files[i]}`).resize(T,T).toBuffer(),left:x,top:y});
const label=files[i].replace('.png','').replace(/^(\d+)_/,'$1  ').replace(/_/g,' ');
comps.push({input:Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${T}" height="36"><rect width="100%" height="100%" fill="#222"/><text x="12" y="25" font-family="DejaVu Sans, Arial" font-size="20" fill="#fff">${label}</text></svg>`),left:x,top:y+T});}
await sharp({create:{width:T*cols,height:rows*(T+36),channels:3,background:'#222'}}).composite(comps).jpeg({quality:88}).toFile(`${dir}/contact_sheet.jpg`);console.log(files.length)})();
