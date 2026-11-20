import sys,glob
from PIL import Image
files=sorted(glob.glob(sys.argv[1])); cols=int(sys.argv[3]); w,h=int(sys.argv[4]),int(sys.argv[5])
rows=(len(files)+cols-1)//cols; im=Image.new("RGB",(cols*w,rows*h))
for i,f in enumerate(files): im.paste(Image.open(f).resize((w,h)),((i%cols)*w,(i//cols)*h))
im.save(sys.argv[2],quality=88)
