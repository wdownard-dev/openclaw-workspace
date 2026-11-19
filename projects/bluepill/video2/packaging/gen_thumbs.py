import base64,json,os,sys,urllib.request
L='/home/williamdownard/.openclaw/workspace/projects/bluepill/library/'
K=os.environ['GEMINI_API_KEY']
M='gemini-3.1-flash-image'
STYLE=("Style: exactly match the reference images: thick dark ink outline, flat warm gouache colour, painted background, simple round-white-head stick-figure humans with two dot eyes. "
 "Palette ink blue, verdigris teal, antique gold, sandstone, cream, terracotta. YouTube thumbnail, 16:9, bold simple composition readable at small size, high contrast. "
 "ABSOLUTELY NO text, letters, captions or watermark anywhere. Keep the left or bottom area calmer where text will be overlaid later.")
J={
'A':(["characters/polyphemus/face.png","characters/odysseus/turnaround.png","places/cave_interior/night_firelight.png"],
 "Extreme close composition: Polyphemus's single huge eye fills the right half of the frame, angry and glowing in firelight, his shaggy brown hair and beard framing it (exactly ONE eye). In the lower left, tiny Odysseus (beardless, from the reference) stands small, looking up, holding a sharpened stake. Dark firelit cave background."),
'B':(["characters/odysseus/turnaround.png","characters/ram/turnaround.png","places/cave_exterior/day_wide.png"],
 "Giant ram seen from the front at the cave mouth in dawn light, Odysseus (beardless) clinging flat to the ram's underside with arms and legs wrapped in the wool, face peeking out, tense. Huge blurred giant's hand reaching down to pat the ram's back from above. Dramatic low angle."),
'C':(["props/elephant_skull.png","characters/polyphemus/face.png","places/cave_exterior/day_wide.png"],
 "Split composition: left half, the ancient dwarf-elephant skull from the reference with its single large central nasal hole, huge and bone-coloured; right half, Polyphemus's face in the same pose size, one eye. The two echo each other, same single-hole look. Warm sandstone background with a hint of cave and sea."),
}
for k,(refs,p) in J.items():
    parts=[{"text":p+" "+STYLE}]
    for r in refs:
        parts.append({"inline_data":{"mime_type":"image/png","data":base64.b64encode(open(L+r,'rb').read()).decode()}})
    body={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}}
    req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={K}",json.dumps(body).encode(),{"Content-Type":"application/json"})
    r=json.load(urllib.request.urlopen(req,timeout=240))
    for pt in r['candidates'][0]['content']['parts']:
        d=pt.get('inlineData') or pt.get('inline_data')
        if d: open(f'raw/raw_{k}.png','wb').write(base64.b64decode(d['data']));print(k,'ok',r.get('usageMetadata'))
