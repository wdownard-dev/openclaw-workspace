import React from 'react';
import {Pic, Cutout, CamSpec, inn, out, pan, hold, crop, Family} from './lib/Pic';
import {LowerThird, QuoteBlock, useT, reveal} from './lib/ui';
import {C, FONT, easeOut, ramp} from './lib/theme';
import {CapPos} from './lib/Captions';
import {SHOTS, shotOf, wordAt} from './lib/timing';
import {ChapterCard, NameCard, Ledger, SolidNot, EndCard} from './lib/Cards';
import {MedMap, DwarfMap, EtnaMap, ArgolidMap, WorldPair, FolkMap, SicilyInset} from './lib/Maps';
import {SkullPlate, SplitSkullEye, WagonCount, TallySix, MixCard, WhichFirst, SplitTwo, ThreeCols, FourPanel, ScaleChart, PaperProp} from './lib/Diagrams';
import dims from './data/dims.json';

export type Ctx = {dur: number; t0: number; t1: number; ts: number[]};   // seg duration, start/end seconds, start seconds of each member shot
export type Entry = {kind: 'pic' | 'card'; cap: CapPos; render: (c: Ctx) => React.ReactNode; group?: number[]};

/* ------------------------------------------------------------------ overlays (screen space, rendered inside the shot's own Sequence) */
const LT: React.FC<{label?: string; text: React.ReactNode; w?: number; size?: number; at?: number}> = ({label, text, w, size, at}) => { const t = useT(); return <LowerThird t={t} label={label} text={text} w={w} size={size} at={at} />; };
const Q: React.FC<{quote: string; credit: string; size?: number; top?: number}> = ({quote, credit, size, top}) => { const t = useT(); return <QuoteBlock t={t} quote={quote} credit={credit} size={size} top={top} />; };
const Inset: React.FC = () => { const t = useT(); return <SicilyInset t={t} />; };
const Rod: React.FC = () => {
  const t = useT(); const u = easeOut(ramp(t, 0.6, 1.8));
  const x0 = 330, x1 = 330 + 1250 * u, y = 700;
  const ticks = []; for (let i = 0; i <= 25; i++) { const x = 330 + i * 50; if (x <= x1) ticks.push(<g key={i}><line x1={x} x2={x} y1={y - (i % 5 === 0 ? 30 : 17)} y2={y + (i % 5 === 0 ? 30 : 17)} stroke="#14100c" strokeWidth={9} /><line x1={x} x2={x} y1={y - (i % 5 === 0 ? 28 : 15)} y2={y + (i % 5 === 0 ? 28 : 15)} stroke={C.rustHi} strokeWidth={4} /></g>); }
  return (<svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', left: 0, top: 0}}>
    <line x1={x0} y1={y} x2={x1} y2={y} stroke="#14100c" strokeWidth={13} />{ticks}
    <line x1={x0} y1={y} x2={x1} y2={y} stroke={C.rustHi} strokeWidth={6} />
    <text x={x0} y={y + 74} fill={C.paper} fontSize={32} fontFamily={FONT} fontWeight={700} opacity={u} style={{paintOrder: 'stroke'}} stroke="rgba(0,0,0,0.85)" strokeWidth={7}>measured</text>
  </svg>);
};
const MayText: React.FC = () => {
  const t = useT();
  return (<div style={{position: 'absolute', left: 84, top: 84, width: 1000, padding: '18px 28px 20px 30px', background: 'rgba(16,12,9,0.78)', borderLeft: `6px solid ${C.rust}`, fontFamily: FONT, fontSize: 40, lineHeight: 1.3, color: C.paper, ...reveal(t, 0.3, 0.5, 10)}}>
    Giants, and one-eyed monsters, <span style={{color: C.rustHi, fontWeight: 700, borderBottom: `4px solid ${C.rustHi}`, fontSize: 54}}>may</span> owe something to those finds.</div>);
};

/* ------------------------------------------------------------------ helpers to declare shots */
type PicOpts = {fam?: Family; cap?: CapPos; scrim?: 'bottom' | 'top' | 'none'; overlay?: React.ReactNode; kickWord?: string; cut?: (dur: number) => React.ReactNode; vignette?: number};
const P = (img: string, cam: CamSpec, o: PicOpts = {}): Entry => ({
  kind: 'pic', cap: o.cap ?? 'bottom',
  render: (c) => (
    <Pic img={img} dur={c.dur} family={o.fam} scrim={o.scrim ?? (o.cap === 'none' ? 'none' : 'bottom')} overlay={o.overlay} vignette={o.vignette}
      cam={o.kickWord ? {...cam, kick: [wordAt(c.t0, c.t1, o.kickWord, 0, 0.5) + 0.04]} : cam}>{o.cut?.(c.dur)}</Pic>),
});
const K = (cap: CapPos, render: (c: Ctx) => React.ReactNode, group?: number[]): Entry => ({kind: 'card', cap, render, group});

const od = dims.ody, cyd = dims.cy, ship = dims.NP04;
const ODY = (x: number, y: number, h: number, extra: any = {}) => <Cutout src="img/ody.png" x={x} y={y} h={h} aspect={od[0] / od[1]} {...extra} />;
const CY = (x: number, y: number, h: number, extra: any = {}) => <Cutout src="img/cy.png" x={x} y={y} h={h} aspect={cyd[0] / cyd[1]} {...extra} />;
const SHIP = (x: number, y: number, h: number) => <Cutout src="img/NP04.png" x={x} y={y} h={h} aspect={ship[0] / ship[1]} shadow={false} filter="saturate(0.9) brightness(0.9) contrast(1.03)" />;
const sil3 = (dx = 0) => (<>{CY(0.34 + dx, 0.80, 0.30, {dark: true, shadow: false})}{CY(0.42 + dx, 0.84, 0.26, {dark: true, shadow: false, flip: true})}{CY(0.28 + dx, 0.86, 0.24, {dark: true, shadow: false})}</>);

const NC = (cap: CapPos, p: Omit<React.ComponentProps<typeof NameCard>, 't0' | 't1'>): Entry => K(cap, (c) => <NameCard t0={c.t0} t1={c.t1} {...p} />);
const LG = (cap: CapPos, p: Omit<React.ComponentProps<typeof Ledger>, 't0' | 't1'>, group?: number[]): Entry => K(cap, (c) => <Ledger t0={c.t0} t1={c.t1} {...p} />, group);
const off = (c: Ctx, i: number) => c.ts[i] - c.ts[0];

export const CHAPTERS: Record<number, [string, string]> = {10: ['I', 'The poem'], 56: ['II', 'The bones'], 88: ['III', 'Other Cyclopes'], 120: ['IV', 'The ledger'], 137: ['V', 'Verdict']};

export const SPEC: Record<number, Entry> = {
  1: K('bottom', (c) => <MedMap dur={c.dur} />),
  2: K('bottom', (c) => <ScaleChart mode="a" dur={c.dur} />),
  3: K('bottom', (c) => <SkullPlate dur={c.dur} ringNasalAt={0.9} labelNasalAt={1.6} zoom={[1, 1.03]} />),
  4: NC('none', {kicker: 'The claim', title: '1914', titleSize: 250, titleColor: C.rustHi, top: 250, lines: [{text: 'A palaeontologist ties the hole to the Cyclops', at: 'palaeontologist', size: 48, color: C.paper}, {text: 'Othenio Abel, palaeontologist', at: 3.4, size: 32, italic: true}]}),
  5: P('NB01', inn([0.5, 0.45], 1, 1.04)),
  6: K('none', (c) => <SplitSkullEye dur={c.dur} />),
  7: P('NB01', crop([0.47, 0.36], [0.47, 0.34], 1.22, 1.3), {overlay: <LT text="EVIDENCE?" w={470} size={46} at={0.8} />}),
  8: LG('none', {kicker: 'The plan', rows: [{num: '1', label: 'The poem', at: 'poem'}, {num: '2', label: 'The bones', at: 'bones'}, {num: '3', label: 'The people who disagree', at: 'people'}]}, [8, 9]),
  11: P('NB02', inn([0.55, 0.5], 1, 1.04)),
  12: P('NB02', crop([0.4, 0.5], [0.44, 0.5], 1.12, 1.16)),
  13: P('NB02', crop([0.44, 0.3], [0.44, 0.3], 1.26, 1.28)),
  14: P('RS08', inn([0.55, 0.55], 1, 1.04)),
  15: P('NBG01', pan(1, 1.05)),
  16: P('NBG01', crop([0.36, 0.5], [0.46, 0.5], 1.18)),
  17: P('NBG01', crop([0.78, 0.62], [0.8, 0.62], 1.2, 1.22)),
  18: P('NBG02', hold([0.5, 0.5], 1, 0.02)),
  19: P('NBG02', inn([0.38, 0.55], 1, 1.04), {cut: () => ODY(0.34, 0.9, 0.5)}),
  20: P('RC02', inn([0.55, 0.55], 1, 1.04)),
  21: P('NB03', hold([0.65, 0.35], 1, 0.02)),
  22: P('RC11', inn([0.55, 0.5], 1, 1.04)),
  23: K('bottom', (c) => <WagonCount t0={c.t0} t1={c.t1} />),
  24: P('NB04', inn([0.55, 0.45], 1, 1.04)),
  25: P('RS09', hold([0.5, 0.55], 1, 0.025)),
  26: P('NB05', inn([0.5, 0.55], 1, 1.04)),
  27: P('NB05', crop([0.62, 0.5], [0.6, 0.52], 1.12, 1.16)),
  28: K('bottom', () => <TallySix />),
  29: P('NB06', inn([0.5, 0.6], 1, 1.04)),
  30: P('NB06', crop([0.42, 0.72], [0.44, 0.7], 1.15, 1.2)),
  31: P('NB07', inn([0.5, 0.5], 1, 1.04)),
  32: P('NB08', inn([0.5, 0.5], 1, 1.04)),
  33: K('bottom', (c) => <MixCard t0={c.t0} t1={c.t1} />),
  34: P('NB09', inn([0.55, 0.5], 1, 1.04)),
  35: P('NB08', crop([0.74, 0.45], [0.72, 0.45], 1.2, 1.22), {overlay: <LT label="Greek" text={<>Οὖτις <span style={{color: C.muted}}>=</span> &lsquo;Nobody&rsquo;</>} w={620} size={50} at={0.5} />}),
  36: P('NB10', inn([0.45, 0.55], 1, 1.04)),
  37: P('NB11', hold([0.5, 0.5], 1, 0.03), {kickWord: 'into'}),
  38: LG('none', {kicker: 'Search: Odyssey, Book 9', rows: [{label: "‘one eye’", value: '0 hits', at: 1.6, sub: 'Greek text and two English translations'}, {label: '‘forehead’', value: '0 hits', at: 3.1}]}),
  39: P('NB11', crop([0.42, 0.44], [0.44, 0.44], 1.12, 1.14), {overlay: <LT label="Greek, singular" text={<>ὀφθαλμῷ <span style={{color: C.muted}}>=</span> &lsquo;in the eye&rsquo;</>} w={760} size={50} at={0.6} />}),
  40: NC('none', {kicker: 'A different poet', title: 'Hesiod', titleSize: 160, lines: [{text: 'Theogony, line 145', at: 0.9, size: 52, color: C.paper}, {text: 'c. 700 BC', at: 1.6, italic: true}]}),
  41: K('bottom', (c) => <PaperProp src="img/NP02.png" aspect={dims.NP02[0] / dims.NP02[1]} h={680} dur={c.dur} />),
  42: K('bottom', (c) => <PaperProp src="img/NP03.png" aspect={dims.NP03[0] / dims.NP03[1]} h={680} dur={c.dur} />),
  43: P('NBG03', pan(-1, 1.05), {cut: () => sil3(0)}),
  44: P('NB12', inn([0.55, 0.45], 1, 1.04)),
  45: P('NBG03', out([0.45, 0.5], 1.05, 1.0), {cut: () => sil3(-0.06)}),
  46: P('NB13', inn([0.5, 0.55], 1, 1.04)),
  47: P('NB14', inn([0.5, 0.5], 1, 1.04), {fam: 'grey'}),
  48: P('NB15', inn([0.5, 0.5], 1, 1.04)),
  49: P('NB16', hold([0.55, 0.5], 1, 0.025)),
  50: P('NBG04', pan(1, 1.05), {cut: () => SHIP(0.5, 0.8, 0.26)}),
  51: P('NBG04', inn([0.5, 0.6], 1, 1.04), {cut: () => SHIP(0.5, 0.8, 0.26)}),
  52: P('NB17', inn([0.45, 0.45], 1, 1.04)),
  53: P('NB18', hold([0.55, 0.5], 1, 0.02)),
  54: P('NB17', crop([0.55, 0.3], [0.55, 0.3], 1.15, 1.18)),
  55: P('RS10', inn([0.5, 0.45], 1, 1.04)),
  57: K('bottom', (c) => <PaperProp src="img/cy.png" aspect={cyd[0] / cyd[1]} h={740} dur={c.dur} line />),
  58: NC('none', {kicker: 'The source', title: 'Die Tiere der Vorwelt', italic: true, titleSize: 118, lines: [{text: 'Othenio Abel, 1914', at: 1.0, size: 50, color: C.paper}]}),
  59: K('bottom', (c) => <DwarfMap t0={c.t0} t1={c.t1} />, [59, 60]),
  61: K('bottom', (c) => <ScaleChart mode="zoom" dur={c.dur} />),
  62: K('bottom', (c) => <ScaleChart mode="b" dur={c.dur} />),
  63: P('NB19', inn([0.5, 0.5], 1, 1.03)),
  64: K('bottom', (c) => <SkullPlate dur={c.dur} ghostAt={0.4} ghostOutAt={off(c, 1) - 0.1} ringOrbitsAt={off(c, 1) + 0.2} labelOrbitsAt={off(c, 1) + 0.6} ringNasalAt={off(c, 2) + 0.2} labelNasalAt={off(c, 2) + 0.7} zoom={[1, 1.04]} />, [64, 65, 66]),
  67: P('NB20', inn([0.6, 0.55], 1, 1.04)),
  68: P('NB19', crop([0.55, 0.42], [0.55, 0.42], 1.08, 1.1)),
  69: P('NB20', crop([0.62, 0.55], [0.62, 0.55], 1.1, 1.12), {overlay: <LT label="Paraphrase" text="Abel, 1914: a plausible picture, offered without evidence" w={1000} size={40} at={0.6} />}),
  70: NC('none', {kicker: 'Adrienne Mayor', title: 'The First Fossil Hunters', italic: true, titleSize: 110, lines: [{text: 'Princeton University Press, 2000', at: 1.2, size: 46, color: C.paper}, {text: 'Stanford folklorist and historian of science', at: 'Stanford', italic: true, size: 34}]}),
  71: P('NB21', inn([0.5, 0.55], 1, 1.04)),
  72: P('NB21', crop([0.5, 0.58], [0.5, 0.58], 1.15), {overlay: <Rod />}),
  73: P('NB21', crop([0.35, 0.5], [0.4, 0.5], 1.12, 1.16), {overlay: <MayText />}),
  74: LG('none', {kicker: 'The ledger', rows: [{label: 'Mayor on the Cyclops', value: 'careful', at: 0.5, accent: true}]}),
  75: P('NB19', hold([0.5, 0.5], 1.04, 0.015), {cap: 'none', overlay: <Q quote="I don't like to say that the fossils inspired, or were the source of the story, because we just can't prove that." credit="Adrienne Mayor, quoted in Discover Magazine" size={46} top={600} />}),
  76: K('none', (c) => <WhichFirst t77={off(c, 1)} />, [76, 77]),
  78: LG('none', {kicker: 'The problem', rows: [{label: 'Abel: Empedocles reported the bones', sub: 'the most famous version of the theory', at: 0.4}], labelW: 1400, rowH: 150, stamp: {text: 'UNVERIFIED', at: 'problem', left: 990, top: 650}}),
  79: NC('none', {kicker: 'The claim', title: 'Empedocles', titleSize: 150, lines: [{text: 'Greek philosopher, c. 492–432 BC', at: 0.9, size: 46, color: C.paper}, {text: 'said by Abel to have reported giants’ bones on Sicily', at: 'bones', italic: true, size: 34}]}),
  80: LG('none', {kicker: 'The ledger', rows: [{label: 'Claim', value: 'bones reported on Sicily', at: 0.4}, {label: 'Ancient source', mark: 'blank', at: 1.4}], labelW: 700, hotAt: 2.6}),
  81: NC('none', {kicker: 'The critics', title: 'Mark Witton & Richard Hing', titleSize: 100, lines: [{text: 'Interdisciplinary Science Reviews, 2024', at: 1.0, size: 44, color: C.paper}]}),
  82: P('NB19', crop([0.45, 0.45], [0.5, 0.45], 1.05, 1.08), {overlay: <LT label="Paraphrase" text="Witton and Hing (2024), as reported: without the Empedocles story, the idea becomes baseless" w={1100} size={38} at={0.6} />}),
  83: K('none', (c) => <WorldPair t0={c.t0} t1={c.t1} />),
  84: K('bottom', (c) => <MedMap dur={c.dur} z0={1.0} z1={1.2} />),
  85: NC('none', {kicker: 'Scholars of Greek myth', title: 'Mercedes Aguirre & Richard Buxton', titleSize: 96, lines: [{text: 'Cyclops · Oxford University Press, 2020', at: 1.1, size: 44, color: C.paper}]}),
  86: LG('none', {kicker: 'Their verdict', rows: [{label: 'PLAUSIBLE', mark: 'tick', at: 0.3}, {label: 'CHAIN OF ARGUMENT', mark: 'blank', at: 1.3}], labelW: 880, rowH: 140}),
  87: P('NB19', hold([0.5, 0.5], 1.0, 0.02)),
  89: P('NB22', inn([0.5, 0.55], 1, 1.04)),
  90: LG('none', {kicker: 'Hesiod, c. 700 BC', title: 'names three Cyclopes', rows: [{label: 'BRONTES', value: 'thunder', at: 'Brontes'}, {label: 'STEROPES', value: 'lightning', at: 'Steropes'}, {label: 'ARGES', value: 'bright', at: 'Arges'}], labelW: 700}),
  91: P('NB23', hold([0.5, 0.5], 1, 0.02)),
  92: P('NB22', crop([0.5, 0.38], [0.5, 0.36], 1.2, 1.24)),
  93: P('NB22', pan(1, 1.05), {cap: 'none', overlay: <Q quote="one eye only was set in the midst of their foreheads." credit="Hesiod, Theogony 145 (trans. Evelyn-White, 1914)" top={700} />}),
  94: P('NB23', inn([0.5, 0.55], 1.1, 1.14)),
  95: K('none', () => <SplitTwo />),
  96: NC('none', {kicker: 'Scholarly inference', title: 'Walter Burkert', titleSize: 140, lines: [{text: 'suggested the smith Cyclopes may reflect real guilds of metalworkers', at: 'smith', size: 42, color: C.paper}]}),
  97: K('bottom', (c) => <EtnaMap t0={c.t0} t1={c.t1} />),
  98: P('NBG05', inn([0.5, 0.55], 1, 1.04), {cut: () => CY(0.62, 0.93, 0.44, {filter: 'saturate(0.55) brightness(0.42) contrast(1.1)'})}),
  99: P('NBG05', inn([0.5, 0.5], 1, 1.04)),
  100: P('NBG05', crop([0.7, 0.5], [0.7, 0.5], 1.1), {cap: 'none', overlay: <Q quote="the Cyclopes and Laestrygones" credit="Thucydides 6.2 (trans. Crawley)" top={700} />}),
  101: P('NBG05', inn([0.3, 0.5], 1.08, 1.12), {cap: 'none', overlay: <Q quote="I cannot tell of what race they were, or whence they came or whither they went" credit="Thucydides 6.2 (trans. Crawley)" size={48} top={660} />}),
  102: P('NBG06', inn([0.5, 0.5], 1, 1.04)),
  103: P('NBG06', pan(1, 1.06), {fam: 'dawn'}),
  104: P('NB24', inn([0.45, 0.5], 1, 1.04)),
  105: P('NB24', crop([0.38, 0.34], [0.38, 0.34], 1.22, 1.25)),
  106: K('bottom', (c) => <ArgolidMap t0={c.t0} t1={c.t1} />, [106, 107]),
  108: P('NBG07', inn([0.5, 0.5], 1, 1.04)),
  109: P('NBG07', pan(1, 1.05), {cut: () => ODY(0.3, 0.92, 0.2)}),
  110: P('NBG07', hold([0.5, 0.5], 1.05, 0.012), {overlay: <LT label="Pausanias, 2nd century AD" text="Description of Greece, 2.25" w={820} size={40} at={0.4} />}),
  111: P('NBG07', crop([0.3, 0.5], [0.35, 0.5], 1.12, 1.14), {cap: 'none', overlay: <Q quote="a work of the Cyclopes made of unwrought stones, each stone being so big that a pair of mules could not move the smallest" credit="Pausanias 2.25 (trans. W. H. S. Jones, 1918)" size={42} top={660} />}),
  112: P('NB25', hold([0.55, 0.5], 1, 0.02)),
  113: P('NBG08', inn([0.5, 0.5], 1, 1.03)),
  114: P('NBG08', hold([0.5, 0.55], 1.04, 0.01), {overlay: <LT label="Archaeology" text={<><b>cyclopean masonry</b> (n.): a style of building with huge, unworked stones</>} w={1100} size={40} at={0.5} />}),
  115: P('NBG07', crop([0.7, 0.5], [0.7, 0.5], 1.1)),
  116: LG('none', {kicker: 'The Greeks attached giants to what they could not explain', rows: [{label: 'Tiryns walls', to: 'Cyclopes', sub: 'Pausanias', at: 0.6}, {label: 'Fossil bones', to: 'giants', sub: 'Mayor', at: 1.6}, {label: 'Skull', to: 'Cyclops', sub: 'unproven', dashed: true, at: 2.6}], labelW: 620, top: 340}),
  117: P('NBG09', inn([0.55, 0.5], 1, 1.04)),
  118: P('NBG09', crop([0.65, 0.5], [0.65, 0.5], 1.1, 1.14)),
  119: P('NBG09', crop([0.62, 0.55], [0.62, 0.55], 1.08, 1.12), {overlay: <Inset />}),
  121: K('none', (c) => <SolidNot t0={c.t0} t1={c.t1} />),
  122: K('none', (c) => <ThreeCols t0={c.t0} t1={c.t1} />),
  123: LG('none', {kicker: 'A single eye is stated by', rows: [{label: 'Hesiod', mark: 'tick', at: 'Hesiod'}, {label: 'Euripides', mark: 'tick', at: 'Euripides'}, {label: 'Theocritus', mark: 'tick', at: 'Theocritus'}, {label: 'Homer', mark: 'dash', at: 'Homer'}], rowH: 110, top: 270, labelW: 700}),
  124: K('bottom', (c) => <SkullPlate dur={c.dur} inset ringNasalAt={off(c, 1) + 0.15} labelNasalAt={off(c, 1) + 0.7} zoom={[1, 1.03]} />, [124, 125]),
  126: K('bottom', (c) => <FolkMap t0={c.t0} t1={c.t1} />, [126, 127]),
  128: P('RS07', inn([0.5, 0.5], 1, 1.04)),
  129: P('RS07', crop([0.5, 0.42], [0.5, 0.42], 1.12, 1.16)),
  130: P('NB19', crop([0.5, 0.45], [0.5, 0.45], 1.05), {overlay: <LT label="Ancient source" text="none found" w={560} size={46} at={0.3} />}),
  131: P('NB19', pan(-1, 1.05)),
  132: P('NBG06', crop([0.45, 0.55], [0.45, 0.55], 1.12)),
  133: NC('none', {kicker: 'Another suspect', title: 'cyclopia', titleSize: 170, lines: [{text: 'a birth defect in which the eye sits below the nose, not above it', at: 'below', size: 42, color: C.paper}]}),
  134: K('none', (c) => <Ledger t0={c.t0} t1={c.t1} kicker="Four candidates" cols={['CANDIDATE', 'PROOF']} rows={[{label: 'Volcanic craters', mark: 'blank', at: 0.3}, {label: 'Smith guilds', mark: 'blank', at: 0.8}, {label: 'Cyclopia, a birth defect', mark: 'blank', at: 1.3}, {label: 'Dwarf-elephant skulls', mark: 'blank', at: 1.8}]} rowH={112} top={330} labelW={1000} hotAt={off(c, 1) + 0.2} />, [134, 135]),
  136: K('bottom', (c) => <SkullPlate dur={c.dur} ringNasalAt={0.2} zoom={[1, 1.03]} stamp={{text: 'HYPOTHESIS', at: wordAt(c.t0, c.t1, 'hypothesis', 0, 1.0)}} />),
  138: P('NB01', inn([0.5, 0.45], 1, 1.04)),
  139: P('RS08', hold([0.55, 0.6], 1, 0.02)),
  140: LG('none', {kicker: 'The name covers at least four things', rows: [{num: '1', label: "Hesiod’s thunderbolt smiths", at: 0.5}, {num: '2', label: "Homer’s shepherd", at: 1.0}, {num: '3', label: 'Sicilian tradition', at: 1.5}, {num: '4', label: 'Walls you can touch', at: 2.0}], rowH: 112, top: 310, labelW: 1300, labelSize: 56}),
  141: K('none', (c) => <FourPanel t0={c.t0} t1={c.t1} />),
  142: P('NBG07', inn([0.5, 0.5], 1, 1.05)),
  143: K('bottom', (c) => <SkullPlate dur={c.dur} ringNasalAt={0.2} zoom={[1, 1.03]} stamp={{text: 'SUSPECT', at: wordAt(c.t0, c.t1, 'suspect', 0, 2.6)}} />),
  144: P('NBG04', inn([0.5, 0.6], 1, 1.04), {cut: () => <>{SHIP(0.5, 0.8, 0.26)}{ODY(0.56, 0.805, 0.13, {shadow: false})}</>}),
  145: NC('none', {kicker: 'Next time', title: 'The winds, the witch, and the other monsters of the Odyssey', titleSize: 80, top: 330}),
  146: LG('none', {kicker: 'Suspects to check', rows: [{label: 'Scylla', value: '?', at: 0.8}, {label: 'Charybdis', value: '?', at: 1.5}, {label: 'The Sirens', value: '?', at: 2.2}, {label: 'The Laestrygonians', value: '?', at: 2.9}], rowH: 112, top: 310, labelW: 1000}),
  147: K('none', (c) => <EndCard t0={c.t0} t1={c.t1} />),
};
// chapter cards
Object.entries(CHAPTERS).forEach(([n, [num, title]]) => { SPEC[+n] = {kind: 'card', cap: 'none', render: () => <ChapterCard num={num} title={title} />}; });
export const IS_CHAPTER = (n: number) => !!CHAPTERS[n];

export const PAPER = new Set([2, 41, 42, 57, 61, 62]);
export type Seg = {tone: 'light' | 'dark'; n0: number; n1: number; start: number; end: number; kind: 'pic' | 'card'; chapter: boolean; cap: CapPos; entry: Entry; ts: number[]};
export const buildSegs = (): Seg[] => {
  const segs: Seg[] = [];
  const skip = new Set<number>();
  for (const s of SHOTS) {
    if (skip.has(s.shot)) continue;
    const e = SPEC[s.shot];
    if (!e) throw new Error('no spec for shot ' + s.shot);
    const members = e.group ?? [s.shot];
    members.slice(1).forEach((m) => skip.add(m));
    const last = shotOf(members[members.length - 1]);
    segs.push({tone: PAPER.has(s.shot) ? 'dark' : 'light', n0: s.shot, n1: members[members.length - 1], start: s.start, end: last.end, kind: e.kind, chapter: IS_CHAPTER(s.shot), cap: e.cap, entry: e, ts: members.map((m) => shotOf(m).start)});
  }
  return segs;
};
