import base64,json,os,urllib.request
B='/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/'
K=os.environ['GEMINI_API_KEY']; M='gemini-3.1-flash-image'
STYLE=("Style: exactly match the character reference cards: thick dark ink outline, flat warm gouache colour, painted background, round-white-head stick-figure humans with simple dot eyes. "
 "YouTube thumbnail, 16:9, bold simple composition, high contrast, readable at phone size. Characters LARGE. Do not copy the card layouts, titles or turnaround poses; use the characters only. "
 "ABSOLUTELY NO text, letters, captions or watermark anywhere. Keep the top-left and bottom-right areas calmer where text will be overlaid.")
ID_ODIN="Odin identity: round white head with a BLACK EYE PATCH over one eye and ONE dot eye on the other side, long grey beard, wide blue-grey pointed hat, dark blue cloak with gold trim, red tunic. Exactly one visible eye plus the patch. "
ID_ODIN_ARMED="Odin armed: same face, iron-grey breastplate, tall gold spear Gungnir. "
ID_FEN="Fenrir identity: iron-grey shaggy wolf, narrow yellow eyes, huge white teeth. "
J={
'A':(["scenes/full/img/S01_base.png","library/refs/odin_one_eye__card.png"],
 ID_ODIN+"The giant skull-shaped dome of the sky from the first reference (plate) fills the background at dusk over a dark sea. In the lower foreground stands tiny Odin seen from behind-three-quarter, large enough that his hat, beard and black eye patch read clearly (about one third of the frame height), looking up at the skull. Skull top-right, Odin lower-left."),
'B':(["library/refs/fenrir_grown__card.png","library/refs/odin_armed__card.png"],
 ID_FEN+ID_ODIN+ID_ODIN_ARMED+"Fenrir's enormous jaws wide open fill the upper two thirds of the frame, looming over Odin who stands small but clear at the lower left with his spear raised, black eye patch clearly visible facing the viewer. Stormy dark grey and ember-red sky, dramatic low angle."),
}
for k,(refs,p) in J.items():
  for n in (1,2):
    parts=[{"text":p+" "+STYLE}]
    for r in refs:
        parts.append({"inline_data":{"mime_type":"image/png","data":base64.b64encode(open(B+r,'rb').read()).decode()}})
    body={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}}
    req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent?key={K}",json.dumps(body).encode(),{"Content-Type":"application/json"})
    r=json.load(urllib.request.urlopen(req,timeout=240))
    for pt in r['candidates'][0]['content']['parts']:
        d=pt.get('inlineData') or pt.get('inline_data')
        if d: open(f'raw/raw_{k}{n}.png','wb').write(base64.b64decode(d['data']));print(k,n,'ok',r.get('usageMetadata',{}).get('candidatesTokenCount'))
