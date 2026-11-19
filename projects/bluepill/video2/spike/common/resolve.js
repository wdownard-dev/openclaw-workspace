// storyboard.json + words.json -> timeline.json (absolute seconds). argv: words.json out.json [timeScale]
const fs = require('fs');
const [,, wordsPath = 'words.json', out = 'timeline.json', scale = '1'] = process.argv;
const W = JSON.parse(fs.readFileSync(wordsPath));
const k = parseFloat(scale); // simulate re-timed audio: every word time * k
const sb = JSON.parse(fs.readFileSync(__dirname + '/storyboard.json'));
const T = (a) => W[a.word].start * k + (a.off || 0);
const shots = sb.shots.map((s, i) => ({...s, t0: i === 0 ? 0 : T(s.start)}));
shots.forEach((s, i) => (s.t1 = i + 1 < shots.length ? shots[i + 1].t0 : sb.duration * k));
const events = sb.events.map((e) => ({...e, t: T(e.at)}));
fs.writeFileSync(out, JSON.stringify({fps: sb.fps, duration: sb.duration * k, shots, events}, null, 1));
console.log('resolved', shots.length, 'shots,', events.length, 'events ->', out);
