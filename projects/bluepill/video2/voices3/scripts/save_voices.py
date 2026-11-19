"""Save the four chosen Voice Design previews as permanent voices. Usage: python -I save_voices.py  (key via ELEVENLABS_API_KEY env)"""
import os, sys, json, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); W=os.path.join(os.path.dirname(HERE),"_work")
sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(HERE)),"voices2","scripts"))
from cfg import DESIGN
PICKS=[("ODY","A","VjxhlwVjjBpI2LsBesOS","BP Odysseus","slate 9, preview 3 of 3"),
       ("POLY","B","uM5YTm59xrfl2vmPc47V","BP Polyphemus","slate 26, preview 2 of 3"),
       ("CYC2","B","5yjDNqcqMzshLpW5Xc91","BP Cyclops chorus","slate 54, preview 2 of 3"),
       ("CREW","B","F8If4viPI1f5VSMBsTfa","BP Crew","slate 68, preview 1 of 3")]
res=json.load(open(f"{W}/saved_voices.json")) if os.path.exists(f"{W}/saved_voices.json") else {}
for role,n,gid,name,sl in PICKS:
    if role in res: print("cached",role,res[role]); continue
    prompt=dict(DESIGN[role])[n]
    desc=f"Project Blue Pill video 1 (The Myth Ledger). Voice Design prompt id {role}-{n} ({sl}). Prompt: {prompt}"[:990]
    body={"voice_name":name,"voice_description":desc,"generated_voice_id":gid}
    bp=f"{W}/_savebody.json"; open(bp,"w").write(json.dumps(body))
    r=subprocess.run(["curl","-s","-m","60","-w","\n%{http_code}","-X","POST","https://api.elevenlabs.io/v1/text-to-voice","-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"-H","Content-Type: application/json","-d","@"+bp],capture_output=True,text=True)
    out,code=r.stdout.rsplit("\n",1)
    print(role,code,out[:300])
    if code!="200": continue
    j=json.loads(out); res[role]={"voice_id":j["voice_id"],"name":name,"preview_gid":gid,"prompt_id":f"{role}-{n}"}
    json.dump(res,open(f"{W}/saved_voices.json","w"),indent=1)
