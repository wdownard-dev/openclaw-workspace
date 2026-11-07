import sys, time, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import null_v2 as N
from PIL import Image
t=time.time()
sheet=Image.new("RGBA",(2400,1200),(30,30,40,255))
for r,v in enumerate("AB"):
    for i,(nm,mo) in enumerate([("smug","closed"),("laugh","wide"),("squint","small"),("raised","closed")]):
        sheet.alpha_composite(N.compose(v,mo,N.EXPR[nm]),(i*600,r*600))
sheet.convert("RGB").save("/tmp/quick.png"); print(time.time()-t)
