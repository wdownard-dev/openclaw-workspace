// tile the 20 s timeline k times (benchmark only): node tile.js in.json out.json k
const fs = require('fs'); const [,, inp, out, k] = process.argv; const T = JSON.parse(fs.readFileSync(inp)); const n = +k, d = T.duration;
const shots = [], events = [];
for (let i = 0; i < n; i++) { T.shots.forEach((s) => shots.push({...s, id: s.id + '_' + i, t0: s.t0 + i * d, t1: s.t1 + i * d})); T.events.forEach((e) => events.push({...e, shot: e.shot + '_' + i, t: e.t + i * d})); }
fs.writeFileSync(out, JSON.stringify({fps: T.fps, duration: d * n, shots, events, audio: 'narr' + n * 20 + '.mp3', kb: +(process.argv[5] || 0)}));
