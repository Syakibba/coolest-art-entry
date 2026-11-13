
import math, random
from PIL import Image, ImageFilter, ImageDraw, ImageChops
random.seed(3)
W=H=1024
img=Image.new("RGB",(W,H),(4,3,14))
# deep-space bg: layered nebula
for i in range(16):
    cx=random.uniform(-100,W+100); cy=random.uniform(-100,H+100); rad=random.uniform(150,380)
    col=random.choice([(45,15,80),(15,40,90),(80,20,55),(15,55,75),(30,20,70)])
    c=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(c)
    d.ellipse([cx-rad,cy-rad,cx+rad,cy+rad],fill=col)
    img=ImageChops.screen(img,c.filter(ImageFilter.GaussianBlur(130)))
# stars
st=Image.new("RGB",(W,H),(0,0,0)); ds=ImageDraw.Draw(st)
for i in range(700):
    x=random.uniform(0,W); y=random.uniform(0,H); b=random.uniform(40,255)
    ds.point((x,y), fill=(int(b),int(b),int(min(255,b*1.1))))
    if random.random()<0.05:
        ds.ellipse([x-1,y-1,x+1,y+1], fill=(255,255,255))
img=ImageChops.screen(img,st)
# central glowing galaxy swirl of neon streams
def hsv(h,s,v):
    c=v*s; hp=h/60; xx=c*(1-abs(hp%2-1)); m=v-c
    r,g,b=[(c,xx,0),(xx,c,0),(0,c,xx),(0,xx,c),(xx,0,c),(c,0,xx)][int(hp)%6]
    return (int((r+m)*255),int((g+m)*255),int((b+m)*255))
acc=Image.new("RGB",(W,H),(0,0,0))
for i in range(170):
    t0=i/170
    a=t0*math.pi*2*5
    x=W*0.5+math.cos(a)*W*0.05*t0
    y=H*0.5+math.sin(a)*H*0.05*t0
    pts=[]
    for step in range(220):
        # spiral flow towards center w/ turbulence
        dx=W*0.5-x; dy=H*0.5-y
        dist=math.hypot(dx,dy)+1e-6
        ang=math.atan2(dy,dx)+1.25+math.sin(x*0.01+y*0.01+t0*20)*0.35
        sp=2.2+3.2*math.sin(t0*math.pi)
        x+=math.cos(ang)*sp+dx/dist*0.6
        y+=math.sin(ang)*sp+dy/dist*0.6
        pts.append((x,y))
    hue=(i*137.5+200)%360
    col=hsv(hue,0.9,1.0)
    layer=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(layer)
    d.line(pts, fill=col, width=2)
    acc=ImageChops.add(acc, layer.filter(ImageFilter.GaussianBlur(0.7)))
img=ImageChops.screen(img, acc)
# core burst
core=Image.new("RGB",(W,H),(0,0,0)); d=ImageDraw.Draw(core)
d.ellipse([W/2-10,H/2-10,W/2+10,H/2+10], fill=(255,250,230))
img=ImageChops.screen(img, core.filter(ImageFilter.GaussianBlur(30)))
# vignette
vig=Image.new("L",(W,H),0); dv=ImageDraw.Draw(vig)
dv.ellipse([-280,-280,W+280,H+280], fill=255)
vig=vig.filter(ImageFilter.GaussianBlur(190))
img=Image.composite(img, Image.new("RGB",(W,H),(2,1,9)), vig)
im8=Image.new("RGB",(W,H))
im8=img
im8.convert('P', palette=Image.ADAPTIVE, colors=255).convert('RGB').save('/home/agentuser/coolest-art/entry.png', optimize=True)
print('ok')
