// usage: node frames_to_bin.js <frames_dir> <out_prefix>
// Reads every PNG, writes gray 80x45 (3600 B/frame) to <out>.gray80, rgb 32x18 (1728 B) to <out>.rgb32, and full gray 320x180 diff series to <out>.diff.json
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const fs=require('fs');
const [dir,out]=process.argv.slice(2);
const files=fs.readdirSync(dir).filter(f=>f.endsWith('.png')).sort();
const N=files.length;
const g80=Buffer.alloc(N*3600), r32=Buffer.alloc(N*1728);
const diff=new Float32Array(N), lum=new Float32Array(N), white=new Float32Array(N), dark=new Float32Array(N), sat=new Float32Array(N);
const edge=new Float32Array(N);
let prev=null;
(async()=>{
  const B=24;
  for(let s=0;s<N;s+=B){
    const batch=files.slice(s,s+B);
    const res=await Promise.all(batch.map(async(f)=>{
      const raw=await sharp(dir+'/'+f).removeAlpha().raw().toBuffer(); // 320x180x3
      const g=await sharp(raw,{raw:{width:320,height:180,channels:3}}).greyscale().raw().toBuffer();
      const s80=await sharp(raw,{raw:{width:320,height:180,channels:3}}).resize(80,45).greyscale().raw().toBuffer();
      const c32=await sharp(raw,{raw:{width:320,height:180,channels:3}}).resize(32,18).raw().toBuffer();
      return {raw,g,s80,c32};
    }));
    for(let k=0;k<res.length;k++){
      const i=s+k, {raw,g,s80,c32}=res[k];
      s80.copy(g80,i*3600); c32.copy(r32,i*1728);
      let sum=0,w=0,d=0,sa=0,e=0;
      for(let p=0;p<g.length;p++){
        sum+=g[p]; if(g[p]>235)w++; if(g[p]<25)d++;
        if(p%320<319){e+=Math.abs(g[p]-g[p+1]);}
      }
      for(let p=0;p<raw.length;p+=3){const mx=Math.max(raw[p],raw[p+1],raw[p+2]),mn=Math.min(raw[p],raw[p+1],raw[p+2]);sa+=mx-mn;}
      lum[i]=sum/g.length; white[i]=w/g.length; dark[i]=d/g.length; sat[i]=sa/(g.length); edge[i]=e/g.length;
      if(prev){let dd=0;for(let p=0;p<g.length;p++)dd+=Math.abs(g[p]-prev[p]);diff[i]=dd/g.length;}
      prev=g;
    }
    if((s/B)%100==0)console.error(s,'/',N);
  }
  fs.writeFileSync(out+'.gray80',g80); fs.writeFileSync(out+'.rgb32',r32);
  fs.writeFileSync(out+'.series.json',JSON.stringify({N,fps:30,diff:Array.from(diff,x=>+x.toFixed(3)),lum:Array.from(lum,x=>+x.toFixed(2)),white:Array.from(white,x=>+x.toFixed(4)),dark:Array.from(dark,x=>+x.toFixed(4)),sat:Array.from(sat,x=>+x.toFixed(2)),edge:Array.from(edge,x=>+x.toFixed(2))}));
  console.error('done',N);
})();
