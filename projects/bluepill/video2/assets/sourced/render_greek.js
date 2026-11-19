// Renders greek_line_9_394.png: Odyssey 9.394 in GFS Didot (OFL), ink on transparent, 1800 px wide.
// Run: FONTCONFIG_FILE=$PWD/fonts/fonts.conf node render_greek.js
const sharp=require('/home/williamdownard/.openclaw/workspace/projects/bluepill/pipeline/node_modules/sharp');
const line='ὣς τοῦ σίζ᾽ ὀφθαλμὸς ἐλαϊνέῳ περὶ μοχλῷ.';
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="260">
<text x="900" y="150" text-anchor="middle" font-family="GFS Didot" font-size="96" fill="#1a1204">${line}</text>
<text x="900" y="230" text-anchor="middle" font-family="GFS Didot" font-size="40" fill="#1f3a5f">Ὀδύσσεια 9.394</text>
</svg>`;
sharp(Buffer.from(svg)).png().toFile('greek_line_9_394.png').then(()=>console.log('ok'));
