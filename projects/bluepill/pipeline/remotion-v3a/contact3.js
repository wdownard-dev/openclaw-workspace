const sharp=require('../node_modules/sharp');
const d='../../tests/v3a/';const n=['a_establishing','b_boulder','c_face_to_face','d_cup','e_blinded','f_ship'];
(async()=>{const w=800,h=450;const tiles=[];
for(const k of n)tiles.push(await sharp(d+`stills_${k}.jpg`).resize(w,h).toBuffer());
await sharp({create:{width:w*2+30,height:h*3+40,channels:3,background:'#111'}}).composite(tiles.map((b,i)=>({input:b,left:10+(i%2)*(w+10),top:10+Math.floor(i/2)*(h+10)}))).jpeg({quality:88}).toFile(d+'contact.jpg')})()
