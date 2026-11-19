import os, json, base64, urllib.request, concurrent.futures as cf
KEY=os.environ["OPENAI_API_KEY"]; OUT="tests/characters"
BASE=" Full-body character design, front view, standing neutral pose, centred on a plain flat off-white background, clean flat 2D vector-style illustration for an animated explainer video, simple shapes, consistent line weight, no text, no letters, no watermark, no background scenery."
C={
"01_round_hero":"A very simple cartoon hero for a mythology channel: perfectly round plain white head, two small dot eyes, tiny mouth, simple stubby body in a short rust-red Greek tunic with a gold laurel wreath and a blue cloth sash, bare feet. Minimal, charming, instantly readable at small size.",
"02_round_hooded":"A simple cartoon narrator character: round white head with dot eyes, wearing a deep teal hooded travel cloak with a gold clasp, holding a small rolled scroll. Minimal flat shapes, mysterious but friendly.",
"03_storybook_adventurer":"A stylised storybook young adventurer in ancient Greece: slightly oversized head, big expressive eyes, messy dark hair, leather satchel, simple tunic and sandals. Modern animated-short look, warm limited palette.",
"04_storybook_scholar":"A wise bearded scholar-storyteller character in a long ochre robe with round glasses pushed up his forehead, holding a quill and a scroll, slightly caricatured, warm expressive face, modern animated-short look.",
"05_greek_vase":"A character drawn in the style of ancient Greek black-figure vase painting: terracotta-orange body shapes with black silhouette details, profile pose, but cleaned up and slightly cartoon so it works as an animated host. Limited palette of terracotta, black and cream.",
"06_egyptian_flat":"A character in the style of Egyptian tomb wall art: flat profile figure with the front-facing eye, gold collar, white linen kilt, bold outlines, but charming and slightly cartoon, suitable as an animated host. Limited warm palette.",
"07_scribe_narrator":"A sarcastic little scribe narrator: round head, half-lidded unimpressed eyes, a tiny quill behind the ear, ink-stained cream tunic, a long unrolled scroll draped over one arm. Simple flat cartoon shapes, funny personality.",
"08_owl_narrator":"A talking owl mascot narrator inspired by the owl of Athena: round fluffy body, big expressive eyes, tiny laurel wreath on its head, small scroll tucked under one wing. Simple flat cartoon, deep blue and gold palette, charming.",
"09_blob_host":"A small round blob-like creature host with a gold laurel crown, two dot eyes and a wide friendly mouth, tiny arms and legs, soft teal body. Extremely simple shapes, very expressive, mascot style.",
"10_rubberhose":"A chunky old-school rubber-hose cartoon hero with noodle limbs, white gloves, round head with simple eyes, wearing a Greek helmet with a red crest and a small round shield. Bold black outlines, retro 1930s cartoon feel but flat colour.",
}
def run(k):
    body=json.dumps({"model":"gpt-image-2.6-sunburst","size":"1024x1024","quality":"medium","n":1,"prompt":C[k]+BASE}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/images/generations",body,{"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=300)); open(f"{OUT}/{k}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"])); return k,"ok"
    except Exception as e: return k,"ERR "+str(getattr(e,'read',lambda:b'')()[:200] or e)
with cf.ThreadPoolExecutor(5) as ex:
    for r in ex.map(run,C): print(*r)
