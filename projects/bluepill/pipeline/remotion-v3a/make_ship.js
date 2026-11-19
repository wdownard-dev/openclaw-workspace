// ship prop clean-up: open the alpha (drops the thin ghost outline), then fill interior holes (sail/oar ports) so the sea does not show through
const sharp=require('../node_modules/sharp');
(async()=>{
 const {data,info}=await sharp('public/img/ship.png').ensureAlpha().raw().toBuffer({resolveWithObject:true});
 const W=info.width,H=info.height,a=Buffer.alloc(W*H);for(let i=0;i<a.length;i++)a[i]=data[i*4+3]>128?255:0;
 // opening: erode 3, keep largest blob, dilate 3 via blur/threshold on the 0/255 mask
 let m=await sharp(a,{raw:{width:W,height:H,channels:1}}).blur(1.6).threshold(200).extractChannel(0).raw().toBuffer();
 // largest blob
 const lab=new Int32Array(W*H);let n=0,best=0,bestN=0;const sz=[0];
 for(let s=0;s<W*H;s++){if(lab[s]||!m[s])continue;n++;let c=0;const st=[s];lab[s]=n;while(st.length){const p=st.pop();c++;const x=p%W,y=(p/W)|0;for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=W||yy>=H)continue;const q=yy*W+xx;if(!lab[q]&&m[q]){lab[q]=n;st.push(q)}}}sz[n]=c;if(c>bestN){bestN=c;best=n}}
 const k=Buffer.alloc(W*H);for(let i=0;i<k.length;i++)k[i]=(lab[i]&&sz[lab[i]]>=bestN*0.04)?255:0;
 // regrow 3px (undo erosion) then fill holes
 let g=await sharp(k,{raw:{width:W,height:H,channels:1}}).blur(2.6).threshold(215).extractChannel(0).raw().toBuffer();
 const out=new Uint8Array(W*H),q=[];const push=(x,y)=>{const p=y*W+x;if(!out[p]&&!g[p]){out[p]=1;q.push(p)}};
 for(let x=0;x<W;x++){push(x,0);push(x,H-1)}for(let y=0;y<H;y++){push(0,y);push(W-1,y)}
 while(q.length){const p=q.pop(),x=p%W,y=(p/W)|0;if(x>0)push(x-1,y);if(x<W-1)push(x+1,y);if(y>0)push(x,y-1);if(y<H-1)push(x,y+1)}
 for(let i=0;i<W*H;i++)data[i*4+3]=out[i]?0:255;
 await sharp(data,{raw:{width:W,height:H,channels:4}}).trim().png().toFile('public/img3/ship3.png');
 const mm=await sharp('public/img3/ship3.png').metadata();console.log(mm.width,mm.height);
})();
