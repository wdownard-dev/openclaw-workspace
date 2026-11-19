// Builds public/audio/mix.wav for video 1: processed narration + 5 stings + synthesised ambient bed (ducked under the voice).
// No third-party audio: the bed is generated here from sine partials and filtered noise (see video1/draft/MUSIC.md).
// usage: node make_audio.js   (needs the bundled ffmpeg from remotion-proof)
const fs = require('fs'), path = require('path'), cp = require('child_process');
const FF = path.resolve(__dirname, '../remotion-proof/node_modules/@remotion/compositor-linux-x64-gnu/ffmpeg');
const AUD = path.resolve(__dirname, '../../video1/audio');
const OUT = path.resolve(__dirname, 'public/audio'); fs.mkdirSync(OUT, {recursive: true});
const TMP = '/tmp/v1audio'; fs.mkdirSync(TMP, {recursive: true});
const SR = 44100;
const Q = JSON.parse(fs.readFileSync(path.join(AUD, 'quality.json')));
const TARGET = +(process.env.TARGET_LUFS || -16);
const run = (args) => cp.spawnSync(FF, ['-hide_banner', '-nostats', '-y', ...args], {encoding: 'utf8', maxBuffer: 1 << 28});

const readWav = (f) => { // 16-bit mono/stereo PCM or f32 -> Float32Array channels
  const b = fs.readFileSync(f); let p = 12, fmt = null, data = null;
  while (p < b.length) { const id = b.toString('ascii', p, p + 4), sz = b.readUInt32LE(p + 4); if (id === 'fmt ') fmt = {tag: b.readUInt16LE(p + 8), ch: b.readUInt16LE(p + 10), sr: b.readUInt32LE(p + 12), bits: b.readUInt16LE(p + 22)}; if (id === 'data') { data = b.subarray(p + 8, p + 8 + Math.min(sz, b.length - p - 8)); break; } p += 8 + sz + (sz & 1); }
  const n = data.length / (fmt.bits / 8) / fmt.ch; const chans = Array.from({length: fmt.ch}, () => new Float32Array(n));
  for (let i = 0; i < n; i++) for (let c = 0; c < fmt.ch; c++) { const o = (i * fmt.ch + c) * (fmt.bits / 8); chans[c][i] = fmt.bits === 16 ? data.readInt16LE(o) / 32768 : data.readFloatLE(o); }
  return {sr: fmt.sr, chans, n};
};
const writeWav = (f, chans, bits = 16) => {
  const n = chans[0].length, ch = chans.length, bps = bits / 8, o = Buffer.alloc(44 + n * ch * bps);
  o.write('RIFF', 0); o.writeUInt32LE(36 + n * ch * bps, 4); o.write('WAVEfmt ', 8); o.writeUInt32LE(16, 16); o.writeUInt16LE(bits === 32 ? 3 : 1, 20); o.writeUInt16LE(ch, 22); o.writeUInt32LE(SR, 24); o.writeUInt32LE(SR * ch * bps, 28); o.writeUInt16LE(ch * bps, 32); o.writeUInt16LE(bits, 34); o.write('data', 36); o.writeUInt32LE(n * ch * bps, 40);
  for (let i = 0; i < n; i++) for (let c = 0; c < ch; c++) { const v = chans[c][i]; const off = 44 + (i * ch + c) * bps; if (bits === 16) o.writeInt16LE(Math.round(Math.max(-1, Math.min(1, v)) * 32767), off); else o.writeFloatLE(v, off); }
  fs.writeFileSync(f, o);
};
const loud = (f) => { // integrated LUFS, true peak, LRA via loudnorm's measurement pass (the bundled ffmpeg has no ebur128 filter)
  const r = run(['-i', f, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-']);
  const m = r.stderr.match(/\{[^{}]*"input_i"[^{}]*\}/); if (!m) throw new Error(r.stderr.slice(-800));
  const j = JSON.parse(m[0]); return {lufs: parseFloat(j.input_i), lra: parseFloat(j.input_lra), tp: parseFloat(j.input_tp)};
};
// ---------------- 1. dynamics in plain DSP (the bundled ffmpeg has no compressor or limiter filters) ----------------
const voiceIn = path.join(AUD, 'narration_voice_only.wav'), stIn = path.join(AUD, 'stings_track.wav');
const highpass = (x, fc) => { const a = Math.exp(-2 * Math.PI * fc / SR), y = new Float32Array(x.length); let yp = 0, xp = 0; for (let i = 0; i < x.length; i++) { yp = a * (yp + x[i] - xp); xp = x[i]; y[i] = yp; } return y; };
const compress = (x, thrDb, ratio, kneeDb, attMs, relMs) => {
  const y = new Float32Array(x.length), at = Math.exp(-1 / (attMs / 1000 * SR)), rl = Math.exp(-1 / (relMs / 1000 * SR)); let env = 0;
  for (let i = 0; i < x.length; i++) {
    const a = Math.abs(x[i]); env = a > env ? a + (env - a) * at : a + (env - a) * rl;
    const lv = 20 * Math.log10(env + 1e-9); let gr = 0; const o = lv - thrDb;
    if (2 * o < -kneeDb) gr = 0; else if (2 * Math.abs(o) <= kneeDb) gr = (1 / ratio - 1) * Math.pow(o + kneeDb / 2, 2) / (2 * kneeDb); else gr = (1 / ratio - 1) * o;
    y[i] = x[i] * Math.pow(10, gr / 20);
  }
  return y;
};
/** lookahead peak limiter: sample peaks never exceed `ceil`; stereo-linked when two channels are given */
const limit = (chs, ceil, lookMs = 4, relMs = 70) => {
  const n = chs[0].length, L = Math.round(lookMs / 1000 * SR), rc = 1 - Math.exp(-1 / (relMs / 1000 * SR));
  const ratio = new Float32Array(n); for (let i = 0; i < n; i++) { let pk = 0; for (const c of chs) pk = Math.max(pk, Math.abs(c[i])); ratio[i] = pk > ceil ? ceil / pk : 1; }
  // sliding minimum over [i, i+L)
  const gmin = new Float32Array(n), dq = new Int32Array(n + 1); let h = 0, t = 0;
  for (let k = 0; k < Math.min(L - 1, n); k++) { while (t > h && ratio[dq[t - 1]] >= ratio[k]) t--; dq[t++] = k; }
  for (let i = 0; i < n; i++) { const k = i + L - 1; if (k < n) { while (t > h && ratio[dq[t - 1]] >= ratio[k]) t--; dq[t++] = k; } while (h < t && dq[h] < i) h++; gmin[i] = ratio[dq[h]]; }
  // release smoothing (forward), then moving average of length L keeps every sample at or below its own ratio
  const gr = new Float32Array(n); let gp = 1; for (let i = 0; i < n; i++) { gp = Math.min(gmin[i], gp + (1 - gp) * rc); gr[i] = gp; }
  const g = new Float32Array(n); let acc = 0; for (let i = 0; i < n; i++) { acc += gr[i]; if (i >= L) acc -= gr[i - L]; g[i] = acc / Math.min(L, i + 1); }
  return chs.map((c) => { const y = new Float32Array(n); for (let i = 0; i < n; i++) y[i] = c[i] * g[i]; return y; });
};

// ---------------- 2. ambient bed ----------------
const synthBed = (n) => {
  // chord roots follow the chapters (and the sting roots): D2, D2, C2, E2, A1(+octave), D2
  const cards = Q.cards; const b = [0, cards['2'][0], cards['3'][0], cards['4'][0], cards['5'][0], cards['6'][0]];
  const roots = [73.42, 73.42, 65.41, 82.41, 110.0, 73.42];
  const mult = [1, 1.5, 2, 2.25 / 1.0];   // root, fifth, octave, ninth (very soft)
  const amp = [1.0, 0.55, 0.42, 0.14];
  const L = new Float32Array(n), R = new Float32Array(n);
  const wRoot = (k, t) => { // smoothstep crossfade over 10 s around each boundary
    const lo = k === 0 ? -1e9 : b[k] - 5, hi = k === b.length - 1 ? 1e9 : b[k + 1] - 5;
    const up = k === 0 ? 1 : Math.min(1, Math.max(0, (t - lo) / 10)), dn = k === b.length - 1 ? 1 : 1 - Math.min(1, Math.max(0, (t - hi) / 10));
    const s = (x) => x * x * (3 - 2 * x); return s(up) * s(dn);
  };
  let seed = 424242; const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296 * 2 - 1; };
  let nl = 0, nr = 0, lpL = 0, lpR = 0;
  const TAU = 2 * Math.PI;
  for (let i = 0; i < n; i++) {
    const t = i / SR; let l = 0, r = 0;
    for (let k = 0; k < roots.length; k++) {
      const w = wRoot(k, t); if (w < 1e-4) continue;
      for (let m = 0; m < 4; m++) {
        const f = roots[k] * mult[m]; const lfo = 0.65 + 0.35 * Math.sin(TAU * (1 / (17 + 6 * m)) * t + m * 1.7 + k);
        const aa = w * amp[m] * lfo;
        l += aa * (Math.sin(TAU * f * 0.9976 * t) + 0.18 * Math.sin(TAU * 2 * f * 0.9976 * t));
        r += aa * (Math.sin(TAU * f * 1.0024 * t + 0.6) + 0.18 * Math.sin(TAU * 2 * f * 1.0024 * t + 0.6));
      }
    }
    // soft air: brown-ish noise through two one-pole lowpasses
    nl += (rnd() - nl) * 0.012; nr += (rnd() - nr) * 0.012; lpL += (nl - lpL) * 0.06; lpR += (nr - lpR) * 0.06;
    const air = 0.5 * (0.6 + 0.4 * Math.sin(TAU * t / 29));
    L[i] = l * 0.18 + lpL * air * 1.6; R[i] = r * 0.18 + lpR * air * 1.6;
  }
  const fi = 4 * SR, fo = 6 * SR;
  for (let i = 0; i < fi; i++) { const g = i / fi; L[i] *= g; R[i] *= g; }
  for (let i = 0; i < fo; i++) { const g = i / fo, j = n - 1 - i; L[j] *= g; R[j] *= g; }
  return [L, R];
};

// ---------------- 3. duck envelope from the processed voice ----------------
const duckEnv = (v, depthDb) => {
  const n = v.length, win = Math.round(0.05 * SR), env = new Float32Array(n); let cur = 0;
  const att = Math.exp(-1 / (0.12 * SR)), rel = Math.exp(-1 / (0.9 * SR));
  const depth = Math.pow(10, -depthDb / 20);
  let acc = 0, cnt = 0, level = 0;
  for (let i = 0; i < n; i++) {
    acc += v[i] * v[i]; cnt++;
    if (cnt === win) { const rms = Math.sqrt(acc / cnt); level = rms > 0.012 ? 1 : 0; acc = 0; cnt = 0; }
    const tgt = level; cur = tgt > cur ? tgt + (cur - tgt) * att : tgt + (cur - tgt) * rel;
    env[i] = 1 - cur * (1 - depth);
  }
  return env;
};

(async () => {
  const st = readWav(stIn), v0 = readWav(voiceIn); const n = Math.max(st.n, v0.n); const N = Math.max(n, Math.ceil((Q.total_sec + 0.5) * SR));
  console.log('synth bed...'); const t0 = Date.now();
  const [bedL0, bedR0] = synthBed(N); console.log('bed done', ((Date.now() - t0) / 1000).toFixed(1), 's');
  // normalise bed to a known reference level before gain: measure its loudness once (integrated, ungated by ducking)
  let gain = +(process.env.VOICE_GAIN || 10.35), stGainRel = +(process.env.ST_REL || -9.3), musicLufs = +(process.env.MUSIC_LUFS || -29.5);
  const bedFile = path.join(TMP, 'bed_raw.wav'); writeWav(bedFile, [bedL0, bedR0], 16);
  const bm = loud(bedFile); const bedGain = Math.pow(10, (musicLufs - bm.lufs) / 20);   // brings the un-ducked bed to musicLufs
  console.log('bed raw LUFS', bm.lufs, '-> gain', (20 * Math.log10(bedGain)).toFixed(2), 'dB (target', musicLufs, ')');
  let res;
  const vHP = highpass(v0.chans[0], 65), vComp = compress(vHP, -27, 2.6, 6, 6, 160);
  let vp = null, duck = null;
  for (let iter = 0; iter < 6; iter++) {
    const gl = Math.pow(10, gain / 20); const vg = new Float32Array(vComp.length); for (let i = 0; i < vg.length; i++) vg[i] = vComp[i] * gl;
    [vp] = limit([vg], 0.80, 4, 70); duck = duckEnv(vp, 6.5);
    const sg = Math.pow(10, (gain + stGainRel) / 20);
    const L = new Float32Array(N), R = new Float32Array(N);
    for (let i = 0; i < N; i++) {
      const vv = i < vp.length ? vp[i] : 0, ss = i < st.n ? st.chans[0][i] * sg : 0, d = i < duck.length ? duck[i] : 1;
      L[i] = vv + ss + bedL0[i] * bedGain * d; R[i] = vv + ss + bedR0[i] * bedGain * d;
    }
    const [Lo, Ro] = limit([L, R], 0.82, 4, 90);
    const fin = path.join(OUT, 'mix.wav'); writeWav(fin, [Lo, Ro], 16);
    res = loud(fin); console.log(`iter ${iter}: voice gain ${gain.toFixed(2)} dB -> mix ${res.lufs} LUFS, TP ${res.tp} dBFS, LRA ${res.lra}`);
    if (Math.abs(res.lufs - TARGET) < 0.25 && res.tp <= -1.0) break;
    gain += TARGET - res.lufs;
  }
  // component loudness reports (each rendered alone with the same gains)
  const comp = (name, arrs) => { const f = path.join(TMP, name + '.wav'); writeWav(f, arrs, 16); return loud(f); };
  const vpF = vp;
  const sg = Math.pow(10, (gain + stGainRel) / 20);
  const stOnly = new Float32Array(N); for (let i = 0; i < st.n; i++) stOnly[i] = st.chans[0][i] * sg;
  const musOnL = new Float32Array(N), musOnR = new Float32Array(N); for (let i = 0; i < N; i++) { const d = i < duck.length ? duck[i] : 1; musOnL[i] = bedL0[i] * bedGain * d; musOnR[i] = bedR0[i] * bedGain * d; }
  const vOnly = new Float32Array(N); vOnly.set(vpF);
  const rep = {mix: res, voice: comp('c_voice', [vOnly, vOnly]), stings: comp('c_stings', [stOnly, stOnly]), music_ducked: comp('c_music', [musOnL, musOnR]), voice_gain_db: +gain.toFixed(2), music_bed_gain_db: +(20 * Math.log10(bedGain)).toFixed(2), sting_gain_db: +(gain + stGainRel).toFixed(2), target: TARGET};
  fs.writeFileSync(path.join(__dirname, 'audio_report.json'), JSON.stringify(rep, null, 1));
  console.log(JSON.stringify(rep));
})().catch((e) => { console.error(e); process.exit(1); });
