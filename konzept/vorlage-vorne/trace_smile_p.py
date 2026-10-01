import json
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, potrace
F='/root/.claude/uploads/a6e2b49f-253a-5c56-b648-5d91c3f5cdcb/6dde9b06-image.jpg'
src=Image.open(F).convert('L'); S=8
D={
 'frau':dict(box=(318,314,372,356),thr=150,T=((325,319),(333,351)),A=((335,295.5),(328.75,342.5))),
 'mann':dict(box=(344,830,400,866),thr=115,T=((351,835),(356,866)),A=((335,296),(330,345))),
}
res={}
for k,v in D.items():
    X0,Y0,X1,Y1=v['box']; W,H=X1-X0,Y1-Y0
    c=src.crop(v['box']).resize((W*S,H*S),Image.LANCZOS)
    a=np.array(c)<v['thr']
    a=np.array(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)))>0
    a[:2,:]=a[-2:,:]=False; a[:,:2]=a[:,-2:]=False
    pl=potrace.Bitmap(a).trace(turdsize=60, alphamax=1.0, opticurve=True, opttolerance=0.4)
    (t1,t2),(a1,a2)=v['T'],v['A']
    # Spiegeln (Vorlage blickt nach links) + Ähnlichkeit t1->a1, t2->a2
    T1=complex(-t1[0],t1[1]); T2=complex(-t2[0],t2[1]); A1=complex(*a1); A2=complex(*a2); kk=(A2-A1)/(T2-T1)
    def f(x,y):
        z=kk*(complex(-x,y)-T1)+A1; return "%.1f,%.1f"%(z.real,z.imag)
    out=[]
    for cv in pl:
        P=[cv.start_point]+[q for sg in cv.segments for q in ([sg.c,sg.end_point] if sg.is_corner else [sg.c1,sg.c2,sg.end_point])]
        xs=[p.x for p in P]; ys=[p.y for p in P]
        if max(xs)-min(xs)<5*S and max(ys)-min(ys)<5*S: continue
        if max(xs)-min(xs)>0.95*W*S and max(ys)-min(ys)>0.95*H*S: continue
        g=lambda p:f(p.x/S+X0,p.y/S+Y0)
        s="M"+g(cv.start_point)
        for sg in cv.segments:
            s+=(" L"+g(sg.c)+" "+g(sg.end_point)) if sg.is_corner else (" C"+g(sg.c1)+" "+g(sg.c2)+" "+g(sg.end_point))
        out.append(s+"Z")
    # Abdeckfläche: Ausschnitt der Vorlage, auf den Kopf abgebildet
    box=[(X0,Y0),(X1,Y0),(X1,Y1),(X0,Y1)]
    res[k]={"linien":" ".join(out),"abdecken":"M"+" L".join(f(x,y) for x,y in box)+" Z"}
    Image.fromarray(((~a)*255).astype('uint8')).save('smp-%s.png'%k)
    print(k,len(out),abs(kk))
json.dump(res,open('smile-profil.json','w'))
