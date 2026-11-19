const sharp=require('sharp');const B='../brand',C='../tests/cutouts';
(async()=>{
 // avatar: pad slightly so the circular crop never clips the gold ring
 const raw=await sharp(`${B}/avatar_raw.png`).raw().toBuffer({resolveWithObject:true});
 const px=[raw.data[0],raw.data[1],raw.data[2]];const bg={r:px[0],g:px[1],b:px[2]};
 const inner=await sharp(`${B}/avatar_raw.png`).resize(736,736).toBuffer();
 await sharp({create:{width:800,height:800,channels:3,background:bg}}).composite([{input:inner,left:32,top:32}]).png().toFile(`${B}/avatar_800.png`);
 // banner
 const W=2560,H=1440,bandTop=509,bandBottom=932;
 const base=await sharp(`${B}/banner_bg_raw.png`).resize(W,H).toBuffer();
 const heights={hero:340,athena:370,zeus:380,cyclops:420};
 const load=async n=>{const b=await sharp(`${C}/${n}.png`).resize({height:heights[n]}).toBuffer();const m=await sharp(b).metadata();return {b,w:m.width,h:m.height}};
 const [hero,athena,zeus,cy]=await Promise.all(['hero','athena','zeus','cyclops'].map(load));
 const base_y=bandBottom-8;
 const comps=[];
 const shadow=(cx,w)=>Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><ellipse cx="${cx}" cy="${base_y}" rx="${w*0.5}" ry="14" fill="#000" opacity="0.35"/></svg>`);
 const put=(c,x)=>{comps.push({input:shadow(x+c.w/2,c.w*0.8)});comps.push({input:c.b,left:Math.round(x),top:Math.round(base_y-c.h)});};
 put(hero,100);put(athena,100+hero.w+40);
 put(cy,W-100-cy.w);put(zeus,W-100-cy.w-40-zeus.w);
 // title plate and text in the mobile-safe zone (x 662..1898, y 551..889)
 const cx=W/2;
 const text=Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
  <defs><radialGradient id="g" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#050a24" stop-opacity="0.62"/><stop offset="0.7" stop-color="#050a24" stop-opacity="0.45"/><stop offset="1" stop-color="#050a24" stop-opacity="0"/></radialGradient></defs>
  <ellipse cx="${cx}" cy="${(bandTop+bandBottom)/2}" rx="780" ry="215" fill="url(#g)"/>
  <text x="${cx}" y="${(bandTop+bandBottom)/2+8}" text-anchor="middle" font-family="DejaVu Serif, FreeSerif, serif" font-weight="700" font-size="80" letter-spacing="4" fill="#fff1c9" stroke="#1a1204" stroke-width="3">THE MYTH LEDGER</text>
  <line x1="${cx-250}" y1="${(bandTop+bandBottom)/2+34}" x2="${cx+250}" y2="${(bandTop+bandBottom)/2+34}" stroke="#f2b632" stroke-width="3"/>
  <text x="${cx}" y="${(bandTop+bandBottom)/2+84}" text-anchor="middle" font-family="DejaVu Serif, FreeSerif, serif" font-style="italic" font-size="40" fill="#f2b632">Every myth, accounted for.</text>
 </svg>`);
 comps.push({input:text});
 await sharp(base).composite(comps).jpeg({quality:90}).toFile(`${B}/banner_2560x1440.jpg`);
 // previews: desktop band and mobile-safe crop
 await sharp(`${B}/banner_2560x1440.jpg`).extract({left:0,top:bandTop,width:W,height:bandBottom-bandTop}).resize(1280).jpeg({quality:85}).toFile(`${B}/preview_desktop.jpg`);
 await sharp(`${B}/banner_2560x1440.jpg`).extract({left:662,top:551,width:1236,height:338}).jpeg({quality:85}).toFile(`${B}/preview_mobile.jpg`);
 console.log('done');
})();
