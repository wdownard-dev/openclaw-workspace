const sharp=require('sharp'),fs=require('fs'),path=require('path');
(async()=>{
const [dir,out]=process.argv.slice(2);
const fl=fs.readdirSync(dir).filter(f=>f.endsWith('.png')).sort();
const S=480,P=30,SM=98,H=S+SM+40,cols=3,rows=Math.ceil(fl.length/cols);
const W=cols*(S+P)+P,HH=rows*(H+P)+P;
const circ=(d)=>Buffer.from(`<svg width="${d}" height="${d}"><circle cx="${d/2}" cy="${d/2}" r="${d/2}"/></svg>`);
const comps=[];
for(let i=0;i<fl.length;i++){
 const x=P+(i%cols)*(S+P),y=P+Math.floor(i/cols)*(H+P);
 const f=path.join(dir,fl[i]);
 for(const [d,dx,dy] of [[S,x,y],[SM,x,y+S+15]]){
  const b=await sharp(f).resize(d,d).composite([{input:circ(d),blend:'dest-in'}]).png().toBuffer();
  comps.push({input:b,left:dx,top:dy});
 }
 const lab=Buffer.from(`<svg width="300" height="40"><text x="0" y="28" font-size="26" fill="white" font-family="sans-serif">${fl[i].replace('.png','')}</text></svg>`);
 comps.push({input:lab,left:x+120,top:y+S+40});
}
await sharp({create:{width:W,height:HH,channels:3,background:'#1e1e1e'}}).composite(comps).jpeg({quality:88}).toFile(out);
})();
