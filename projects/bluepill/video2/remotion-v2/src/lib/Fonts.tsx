import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

const FACES = [
  ['Permanent Marker', 'fonts/PermanentMarker-Regular.ttf'],
  ['Special Elite', 'fonts/SpecialElite-Regular.ttf'],
];
let loaded: Promise<void> | null = null;
const load = () => {
  if (!loaded) loaded = Promise.all(FACES.map(async ([fam, file]) => { const f = new FontFace(fam, `url(${staticFile(file)})`); await f.load(); (document as any).fonts.add(f); })).then(() => undefined);
  return loaded;
};
/** blocks the render until both display faces are in document.fonts */
export const Fonts: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [h] = useState(() => delayRender('fonts'));
  const [ok, setOk] = useState(false);
  useEffect(() => { load().then(() => { setOk(true); continueRender(h); }).catch((e) => { console.error(e); setOk(true); continueRender(h); }); }, []);
  return ok ? <>{children}</> : null;
};
