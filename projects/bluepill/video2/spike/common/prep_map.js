// renders the shared map background once: node prep_map.js out.png
const sharp = require('../../../pipeline/node_modules/sharp');
const {mapSvg} = require('./anim.js');
const med = require('./med.json');
sharp(Buffer.from(mapSvg(med))).png().toFile(process.argv[2]).then(() => console.log('map ok'));
