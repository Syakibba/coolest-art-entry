
import math, random
from PIL import Image, ImageFilter, ImageDraw, ImageChops
W=H=1024
random.seed(11)
img=Image.new("RGB",(W,H),(6,4,18))
d=ImageDraw.Draw(img)
# sky gradient deep purple -> magenta near horizon
HOR=640
for y in range(HOR):
    t=y/HOR
    r=int(8+180*t**2.4); g=int(4+30*t**2.0); b=int(28+120*t**1.6)
    d.line([(0,y),(W,y)], fill=(min(r,255),min(g,255),min(b,255)))
# stars
for i in range(420):
    x=random.uniform(0,W); y=random.uniform(0,HOR*0.85); v=random.randint(90,255)
    d.point((x,y), fill=(v,v,min(255,int(v*1.05))))
# big sun disc with horizontal slits
sun=Image.new("RGB",(W,H),(0,0,0)); ds=ImageDraw.Draw(sun)
cx,cy,R=W/2,HOR-70,250
for y in range(int(cy-R), int(cy+R)+1):
    dy=y-cy
    if abs(dy)>R: continue
    half=int((R*R-dy*dy)**0.5)
    t=(y-(cy-R))/(2*R)
    col=(int(255), int(90+120*t), int(40+80*t))
    # slits grow toward bottom
    if dy>0 and (dy % max(6,int(46*(1-t)))) < 3: continue
    ds.line([(cx-half,y),(cx+half,y)], fill=col)
# sun glow
glow=sun.filter(ImageFilter.GaussianBlur(45))
img=ImageChops.screen(img, ImageChops.add(sun, glow))
d=ImageDraw.Draw(img)
# mountains silhouette
pts=[(0,HOR)]
random.seed(5)
x=0
while x<W:
    x+=random.randint(60,140)
    pts.append((x, HOR-random.randint(10,105)))
pts += [(W,HOR),(W,HOR),(0,HOR)]
d.polygon(pts, fill=(10,6,26))
# perspective grid below horizon
d.rectangle([0,HOR,W,H], fill=(8,3,20))
GRID=(255,60,180)
for i in range(-14,15):
    x2=W/2 + i*130
    d.line([(W/2, HOR), (x2, H)], fill=GRID, width=3)
y=HOR+2; step=4
while y<H:
    d.line([(0,y),(W,y)], fill=GRID, width=3)
    step*=1.42; y+=step
# horizon glow line
d.line([(0,HOR),(W,HOR)], fill=(120,240,255), width=4)
out=img.filter(ImageFilter.GaussianBlur(0.4))
out.save('/home/agentuser/coolest-art/synth.png', optimize=True)
import os; print(os.path.getsize('/home/agentuser/coolest-art/synth.png'))
