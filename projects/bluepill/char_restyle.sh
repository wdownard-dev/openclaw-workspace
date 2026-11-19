#!/bin/bash
# usage: char_restyle.sh <style_ref_png> <char_ref_png> <out_png> <costume description>
curl -s https://api.openai.com/v1/images/edits -H "Authorization: Bearer $OPENAI_API_KEY" \
 -F model=gpt-image-2.6-sunburst -F size=1024x1024 -F quality=medium \
 -F "image[]=@$1" -F "image[]=@$2" \
 -F "prompt=Image 1 is the STYLE reference: a minimal cartoon character with a perfectly round plain white head, two small dot eyes, a tiny smile, simple stubby body, clean thick dark outline, flat colours. Image 2 is the CHARACTER whose identity and costume must be kept. Redraw the character from image 2 in exactly the art style of image 1: round plain white head with dot eyes and tiny mouth (no realistic face, no hair on the head unless it is part of a hat or headdress), simple stubby body, flat colours, same line weight. Keep the costume, accessories and colours of image 2: $4. Full-body, front view, centred on a plain off-white background, no text, no watermark." \
 -o "$3.json"
python3 -c "
import json,base64,sys
d=json.load(open('$3.json'))
open('$3','wb').write(base64.b64decode(d['data'][0]['b64_json'])) if 'data' in d else print('ERR $3',str(d)[:200])"
rm -f "$3.json"
