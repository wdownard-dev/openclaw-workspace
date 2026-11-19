const fs = require('fs');
const m = JSON.parse(fs.readFileSync('/tmp/rv3a/motion.json'));
const shots = [[0,5.166,'enter'],[5.166,8.941,'mistake'],[8.941,12.54,'owner'],[12.54,17.743,'boulder'],[17.743,22.399,'wine'],[22.399,26.17,'loves']];
const S = 6; // 320 -> 1920 px
const rms = (a) => a.length ? Math.sqrt(a.reduce((s, v) => s + v * v, 0) / a.length) : 0;
const pct = (a, p) => { const b = [...a].sort((x, y) => x - y); return b.length ? b[Math.min(b.length - 1, Math.floor(p * b.length))] : 0; };
const rows = [];
for (const [s, e, id] of shots) {
  // skip 4 frames at each end (transitions)
  const fr = m.filter((r) => r.t > s + 0.2 && r.t < e - 0.05 && r.diff < 40); // exclude cut frames
  if (fr.length < 5) { rows.push({id, n: fr.length}); continue; }
  const sp = fr.map((r) => Math.hypot(r.dx, r.dy) * S);
  const spTop = fr.map((r) => Math.hypot(r.tdx, r.tdy) * S);
  const spBot = fr.map((r) => Math.hypot(r.bdx, r.bdy) * S);
  // jerk: second difference of dx,dy (full)
  const jx = [], jy = [];
  for (let i = 2; i < fr.length; i++) { jx.push((fr[i].dx - 2 * fr[i-1].dx + fr[i-2].dx) * S); jy.push((fr[i].dy - 2 * fr[i-1].dy + fr[i-2].dy) * S); }
  // sign flips of dy (oscillation)
  let flips = 0; for (let i = 1; i < fr.length; i++) if (Math.sign(fr[i].dy) * Math.sign(fr[i-1].dy) < 0 && Math.abs(fr[i].dy) > 0.15) flips++;
  rows.push({id, n: fr.length, diff: +(fr.reduce((a, r) => a + r.diff, 0) / fr.length).toFixed(2), speed_mean: +(sp.reduce((a,b)=>a+b,0)/sp.length).toFixed(2), speed_p95: +pct(sp, .95).toFixed(1), top_mean: +(spTop.reduce((a,b)=>a+b,0)/spTop.length).toFixed(2), bot_mean: +(spBot.reduce((a,b)=>a+b,0)/spBot.length).toFixed(2), jerk_rms_x: +rms(jx).toFixed(2), jerk_rms_y: +rms(jy).toFixed(2), dy_flips_per_s: +(flips / (fr.length / 30)).toFixed(1)});
}
console.table(rows);
// big-spike frames
const spikes = m.filter((r) => Math.hypot(r.dx, r.dy) * S > 18 && r.diff < 40).map((r) => `${r.t}s(${(r.dx*S).toFixed(0)},${(r.dy*S).toFixed(0)})`);
console.log('frames with |shift|>18px@1080p:', spikes.join(' '));
const cuts = m.filter((r) => r.diff >= 40).map((r) => r.t); console.log('hard cut-like frames (diff>=40):', cuts.join(' '));

const all=m.filter(r=>r.diff<40);const jj=[];for(let i=2;i<all.length;i++){if(all[i].f-all[i-2].f!==2)continue;jj.push((all[i].dx-2*all[i-1].dx+all[i-2].dx)*S,(all[i].dy-2*all[i-1].dy+all[i-2].dy)*S)}
console.log('clip-wide jerk rms (px@1080p):',rms(jj).toFixed(2),' max |shift| px/frame:',Math.max(...all.map(r=>Math.hypot(r.dx,r.dy)*S)).toFixed(1));
const B=[5.166,8.941,12.54,17.743,22.399];
const far=(t)=>B.every(b=>Math.abs(t-b)>0.15);
const ins=m.filter(r=>far(r.t)&&r.diff<40);const jj2=[];for(let i=2;i<ins.length;i++){if(ins[i].f-ins[i-2].f!==2)continue;jj2.push((ins[i].dx-2*ins[i-1].dx+ins[i-2].dx)*S,(ins[i].dy-2*ins[i-1].dy+ins[i-2].dy)*S)}
console.log('excluding +-0.15s around cuts: jerk rms',rms(jj2).toFixed(2),'max |shift|',Math.max(...ins.map(r=>Math.hypot(r.dx,r.dy)*S)).toFixed(1),'px/frame; frames >15px:',ins.filter(r=>Math.hypot(r.dx,r.dy)*S>15).length);
