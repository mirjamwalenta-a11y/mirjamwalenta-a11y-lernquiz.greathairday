import json, math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, potrace
from prof_def import D
S=3
# Landmarken (Vorlage, Ausschnittkoordinaten): Nasenspitze, Ohrmitte
LM={'pm0':((80,243.5),(245,212)),'pm1':((48.5,245),(207,215)),'pm2':((50,244),(207.5,220)),
    'pf0':((83,235),(246,218)),'pf1':((57,228),(218,218)),'pf2':((64,232),(222,213))}
LK={'m':((374,272),(167.5,242.5)),'f':((371,270),(167.5,242.5))}
def abb(key):
    (n,e)=LM[key]; (N,E)=LK[key[1]]
    # Spiegeln: x -> -x, dann Ähnlichkeit n->N, e->E
    a=complex(-n[0],n[1]); b=complex(-e[0],e[1]); A=complex(*N); B=complex(*E)
    k=(B-A)/(b-a)
    return lambda x,y: ((k*(complex(-x,y)-a)+A).real,(k*(complex(-x,y)-a)+A).imag)
def pfad(pl,f):
    out=[]
    for cv in pl:
        xs=[p.x for sg in cv.segments for p in ([sg.end_point]+([sg.c] if sg.is_corner else [sg.c1,sg.c2]))]
        ys=[p.y for sg in cv.segments for p in ([sg.end_point]+([sg.c] if sg.is_corner else [sg.c1,sg.c2]))]
        if max(xs)-min(xs)>380*S and max(ys)-min(ys)>360*S: continue
        g=lambda p:"%.1f,%.1f"%f(p.x/S,p.y/S)
        s="M"+g(cv.start_point)
        for sg in cv.segments:
            s+=(" L"+g(sg.c)+" "+g(sg.end_point)) if sg.is_corner else (" C"+g(sg.c1)+" "+g(sg.c2)+" "+g(sg.end_point))
        out.append(s+"Z")
    return " ".join(out)
res={}
for key,v in D.items():
    im=Image.open(v['f']).convert('L'); ox,oy=v['off']; W,H=390,370
    c=im.crop((ox,oy,ox+W,oy+H)).resize((W*S,H*S),Image.LANCZOS)
    tr=lambda P:[(x*S,y*S) for x,y in P]
    d=ImageDraw.Draw(c)
    for l in v['linien']: d.line(tr(l),fill=255,width=int(2.3*S))
    for w in v['weg']: d.polygon(tr(w),fill=255)
    km=Image.new('L',c.size,0); ImageDraw.Draw(km).polygon(tr(v['keep']),fill=255)
    om=Image.new('L',c.size,0); ImageDraw.Draw(om).polygon(tr(v['ohr']),fill=255)
    a=np.array(c); ink=(a<150)&(np.array(km)>0)&~(np.array(om)>0)
    cl=5*S//2*2+1
    b=Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(cl))
    b2=Image.new('L',(b.width+2,b.height+2),0); b2.paste(b,(1,1)); ImageDraw.floodfill(b2,(0,0),128)
    sil=np.array(b2)[1:-1,1:-1]!=128
    sI=Image.fromarray((sil*255).astype('uint8')).filter(ImageFilter.MinFilter(cl))
    r=4*S//2*2+1; sI=sI.filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))
    sil=(np.array(sI)>0)&~(np.array(om.filter(ImageFilter.MinFilter(5)))>0)
    ink=ink&(np.array(sI.filter(ImageFilter.MaxFilter(2*S+1)))>0)
    f=abb(key)
    pl=potrace.Bitmap(ink).trace(turdsize=60, alphamax=1.1, opticurve=True, opttolerance=0.8)
    pf=potrace.Bitmap(sil).trace(turdsize=400, alphamax=1.2, opticurve=True, opttolerance=0.6)
    # Punkte (Fade/Stoppeln) bei kurzen Frisuren: kleine dunkle Flecken innerhalb der Haarfläche
    punkte_=""
    if key in ('pm0','pf0'):
        a2=(a<185)&(np.array(km)>0)&~(np.array(om)>0)
        pd=potrace.Bitmap(a2).trace(turdsize=2, alphamax=0.8, opticurve=False)
        kl=[cv for cv in pd if len(cv.segments)<14]
        punkte_=pfad(kl,f)
    res[key]={"linien":pfad(pl,f),"flaeche":pfad(pf,f),"punkte":punkte_}
    Image.fromarray(((~ink)*255).astype('uint8')).resize((W*2,H*2)).save('tp-%s.png'%key)
    print(key,len(res[key]['linien']),len(res[key]['flaeche']))
json.dump(res,open('haar-profil.json','w'))
