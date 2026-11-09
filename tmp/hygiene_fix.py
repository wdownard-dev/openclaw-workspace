import json, subprocess, sys
OLD = "If nothing is new or actionable, reply NO_REPLY. Non-urgent routine numbers belong in the 8:15 AM digest, not a separate message."
NEW = "ALWAYS SEND (William, 2026-11-08): this job must send its one message every run, even on a slow day or when nothing changed; a one-line 'no change' with the key numbers is correct. Never reply NO_REPLY for this job. It is a routine report he wants to see daily."
def get(i):
    return json.loads(subprocess.run(["openclaw","automations","get",i],capture_output=True,text=True).stdout)
for i in sys.argv[1:]:
    d=get(i); m=d["payload"]["message"]
    if OLD not in m: print(i,d["name"],"SKIP pattern missing"); continue
    n=m.replace(OLD,NEW)
    r=subprocess.run(["openclaw","automations","edit",i,"--message",n],capture_output=True,text=True)
    m2=get(i)["payload"]["message"]
    print(i,d["name"],"OK" if r.returncode==0 and m2==n and n.count("ALWAYS SEND")==1 else "FAIL",r.stderr[:200])
