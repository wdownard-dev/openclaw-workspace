#!/bin/bash
# usage: char_cast.sh <style_ref_png> <out_png> <character description>
curl -s https://api.openai.com/v1/images/edits -H "Authorization: Bearer $OPENAI_API_KEY" \
 -F model=gpt-image-2.6-sunburst -F size=1024x1024 -F quality=medium -F "image[]=@$1" \
 -F "prompt=Image 1 is the STYLE reference: a minimal cartoon character with a perfectly round plain white head, two small dot eyes, a tiny smile, simple stubby body, clean thick dark outline, flat colours. Draw a NEW character in exactly the same art style, same head shape, outline weight and proportions: $3. Full-body, front view, centred on a plain off-white opaque background, no text, no watermark." -o "$2.json"
python3 -c "
import json,base64
d=json.load(open('$2'+'.json'))
open('$2','wb').write(base64.b64decode(d['data'][0]['b64_json'])) if 'data' in d else print('ERR $2',str(d)[:200])"
rm -f "$2.json"
