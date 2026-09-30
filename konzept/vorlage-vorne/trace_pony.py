import json
from PIL import Image, ImageDraw
import numpy as np, potrace
im=Image.open('th-frau-ink.png').convert('L')   # 2x der Vorlage, Tinte schwarz
S=2
poly=[(300,70),(440,45),(580,70),(665,125),(705,300),(690,400),(560,400),(470,400),(440,300),(410,400),(300,400),(190,400),(185,300),(215,125)]
m=Image.new('L',im.size,0); ImageDraw.Draw(m).polygon(poly,fill=255)
a=np.array(im)<128; a&=np.array(m)>0
d2=Image.new('L',im.size,0); ImageDraw.Draw(d2).polygon([(180,310),(300,330),(300,352),(180,332)],fill=255); a&=~(np.array(d2)>0)
a[:,:]=a
big=np.array(Image.fromarray((a*255).astype('uint8')).resize((im.size[0]*S,im.size[1]*S),Image.LANCZOS))>128
ys,xs=np.nonzero(a); x0,x1=xs.min(),xs.max()
top=np.full(im.size[0],np.nan); bot=np.full(im.size[0],np.nan)
for x in range(x0,x1+1):
    c=np.nonzero(a[:,x])[0]
    if len(c): top[x]=c.min(); bot[x]=c.max()
# glätten
def gl(v):
    v=v.copy()
    for _ in range(25):
        w=v.copy()
        for i in range(1,len(v)-1):
            if not np.isnan(v[i-1]) and not np.isnan(v[i+1]) and not np.isnan(v[i]): w[i]=(v[i-1]+v[i]+v[i+1])/3
        v=w
    return v
idx=np.arange(len(top)); ok=~np.isnan(top)
top=np.interp(idx,idx[ok],top[ok]); bot=np.interp(idx,idx[ok],bot[ok])
def gg(v, sg=40):
    k=np.exp(-0.5*(np.arange(-3*sg,3*sg+1)/sg)**2); k/=k.sum()
    pad=np.pad(v,3*sg,mode='edge'); return np.convolve(pad,k,mode='same')[3*sg:-3*sg]
top=gg(top,30); bot=np.maximum(gg(bot,45), top+40)
pl=potrace.Bitmap(big).trace(turdsize=30, alphamax=1.1, opticurve=True, opttolerance=0.5)
def f(p):
    x=p.x/S; y=p.y/S; xi=int(min(max(round(x),x0),x1))
    t=min(max((y-top[xi])/max(bot[xi]-top[xi],1),-0.05),1.06)
    return "%d,%d"%(round((x-x0)/(x1-x0)*1000),round(t*1000))
out=[]
for cv in pl:
    xs=[p.x for sg in cv.segments for p in ([sg.end_point]+([sg.c] if sg.is_corner else [sg.c1,sg.c2]))]
    if max(xs)-min(xs)>big.shape[1]*0.9: continue
    s="M"+f(cv.start_point)
    for sg in cv.segments:
        s+=(" L"+f(sg.c)+" "+f(sg.end_point)) if sg.is_corner else (" C"+f(sg.c1)+" "+f(sg.c2)+" "+f(sg.end_point))
    out.append(s+"Z")
d=" ".join(out); json.dump({"pony":d},open('pony-vorlage.json','w')); print(len(d),x0,x1)
Image.fromarray(((~a)*255).astype('uint8')).save('pony-ink.png')
