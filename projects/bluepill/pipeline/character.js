// Original Blue Pill test character ("Pip"): code-built so it never drifts between shots.
const INK = '#2b2630', SKIN = '#f6ecdc', TUNIC = '#c8603a', TRIM = '#e8b64a', SANDAL = '#6b4a32';
const mouths = {
  neutral: `<path d="M 262 232 Q 300 242 338 232" stroke="${INK}" stroke-width="7" fill="none" stroke-linecap="round"/>`,
  happy:   `<path d="M 250 222 Q 300 275 350 222 Z" fill="${INK}"/>`,
  shocked: `<ellipse cx="300" cy="244" rx="22" ry="30" fill="${INK}"/>`,
  angry:   `<path d="M 262 246 Q 300 226 338 246" stroke="${INK}" stroke-width="7" fill="none" stroke-linecap="round"/>`,
};
const eyes = {
  neutral: `<circle cx="248" cy="170" r="11" fill="${INK}"/><circle cx="352" cy="170" r="11" fill="${INK}"/>`,
  happy:   `<circle cx="248" cy="170" r="11" fill="${INK}"/><circle cx="352" cy="170" r="11" fill="${INK}"/>`,
  shocked: `<circle cx="248" cy="168" r="17" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="248" cy="168" r="7" fill="${INK}"/><circle cx="352" cy="168" r="17" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="352" cy="168" r="7" fill="${INK}"/>`,
  angry:   `<circle cx="248" cy="174" r="11" fill="${INK}"/><circle cx="352" cy="174" r="11" fill="${INK}"/><path d="M 218 146 L 272 162" stroke="${INK}" stroke-width="9" stroke-linecap="round"/><path d="M 382 146 L 328 162" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>`,
};
const arms = {
  idle:  `<path d="M 228 372 Q 160 450 172 540" /><path d="M 372 372 Q 440 450 428 540" />`,
  point: `<path d="M 228 372 Q 160 450 172 540" /><path d="M 368 372 Q 450 360 540 330" />`,
  cheer: `<path d="M 232 372 Q 170 300 160 230" /><path d="M 368 372 Q 430 300 440 230" />`,
};
function character({ expr = 'neutral', pose = 'idle' } = {}) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900" width="600" height="900">
  <g stroke="${INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M 270 640 L 262 820" /><path d="M 330 640 L 338 820" />
    <path d="M 240 826 Q 262 806 288 826 L 292 842 L 232 842 Z" fill="${SANDAL}" />
    <path d="M 312 826 Q 338 806 360 826 L 368 842 L 308 842 Z" fill="${SANDAL}" />
    <path d="M 225 350 Q 300 335 375 350 L 410 660 Q 300 690 190 660 Z" fill="${TUNIC}" />
    <path d="M 215 600 Q 300 625 395 600" stroke="${TRIM}" stroke-width="14" />
    <g stroke-width="14">${arms[pose]}</g>
    <ellipse cx="300" cy="195" rx="125" ry="120" fill="${SKIN}" />
  </g>
  ${eyes[expr]}${mouths[expr]}
  </svg>`;
}
module.exports = { character };
