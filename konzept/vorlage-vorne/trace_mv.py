import json
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, potrace
F='/root/.claude/uploads/a6e2b49f-253a-5c56-b648-5d91c3f5cdcb/2cd1e28e-image.jpg'
S=3
D={
 'mittel':dict(box=(20,90,485,625),
   gesicht=[(150,335),(170,288),(210,276),(250,272),(290,276),(335,288),(355,335),(378,420),(382,500),(368,560),(345,600),(345,640),(155,640),(155,600),(132,560),(118,500),(122,420)],
   hals=[(175,640),(330,640),(330,700),(175,700)],
   linien=[((400,110),(350,185)),((495,220),(452,300)),((70,550),(38,590)),((125,605),(105,650))],
   weg=[[(355,85),(485,85),(485,116),(355,116)],[(425,160),(485,160),(485,196),(425,196)],[(462,196),(485,196),(485,230),(462,230)],[(0,580),(90,580),(90,660),(0,660)]],
   lm=dict(cx=250,yE=420,ex=70,chin=662,c=264)),
 'lang':dict(box=(525,125,992,815),
   gesicht=[(655,315),(680,280),(730,272),(780,280),(805,315),(850,420),(860,500),(845,570),(810,620),(650,620),(615,570),(600,500),(608,420)],
   hals=[(645,600),(855,600),(870,830),(630,830)],
   linien=[((870,115),(818,202)),((980,225),(918,318)),((595,780),(568,842)),((860,770),(882,842))],
   weg=[[(905,155),(992,155),(992,222),(905,222)],[(525,150),(605,150),(605,196),(525,196)],[(525,196),(566,196),(566,224),(525,224)]],
   lm=dict(cx=730,yE=420,ex=71,chin=662,c=250)),
}
res={}
im=Image.open(F).convert('L')
for k,v in D.items():
    X0,Y0,X1,Y1=v['box']; W,H=X1-X0,Y1-Y0
    c=im.crop(v['box']).resize((W*S,H*S),Image.LANCZOS)
    tr=lambda P:[((x-X0)*S,(y-Y0)*S) for x,y in P]
    d=ImageDraw.Draw(c)
    for l in v['linien']: d.line(tr(l),fill=255,width=int(2.4*S))
    for w in v['weg']: d.polygon(tr(w),fill=255)
    ex=Image.new('L',c.size,0); de=ImageDraw.Draw(ex); de.polygon(tr(v['gesicht']),fill=255); de.polygon(tr(v['hals']),fill=255)
    d.rectangle((0,0,c.width-1,c.height-1),outline=255,width=6)
    a=np.array(c); exm=np.array(ex)>0
    ink=(a<150)&~exm
    cl=5*S//2*2+1
    b=Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(cl))
    b2=Image.new('L',(b.width+2,b.height+2),0); b2.paste(b,(1,1)); ImageDraw.floodfill(b2,(0,0),128)
    sil=np.array(b2)[1:-1,1:-1]!=128
    sI=Image.fromarray((sil*255).astype('uint8')).filter(ImageFilter.MinFilter(cl))
    r=4*S//2*2+1; sI=sI.filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))
    sil=(np.array(sI)>0)&~exm
    ink=ink&(np.array(sI.filter(ImageFilter.MaxFilter(2*S+1)))>0)
    # auf Vorlagen-Normkoordinaten: Gesichtsmitte x=0, Augenlinie y=0, Einheit = Wangenbreite
    L=v['lm']; f=lambda x,y:((x-L['cx'])/L['c'],(y-L['yE'])/(L['chin']-L['yE']))
    def pfad(pl, rahmen=True):
        out=[]
        for cv in pl:
            xs=[p.x for sg in cv.segments for p in ([sg.end_point]+([sg.c] if sg.is_corner else [sg.c1,sg.c2]))]
            ys=[p.y for sg in cv.segments for p in ([sg.end_point]+([sg.c] if sg.is_corner else [sg.c1,sg.c2]))]
            if rahmen and max(xs)-min(xs)>W*S*0.97 and max(ys)-min(ys)>H*S*0.97 and len(cv.segments)<=6: continue
            g=lambda p:"%d,%d"%tuple(round(1000*q) for q in f(p.x/S+X0,p.y/S+Y0))
            s="M"+g(cv.start_point)
            for sg in cv.segments:
                s+=(" L"+g(sg.c)+" "+g(sg.end_point)) if sg.is_corner else (" C"+g(sg.c1)+" "+g(sg.c2)+" "+g(sg.end_point))
            out.append(s+"Z")
        return " ".join(out)
    pl=potrace.Bitmap(ink).trace(turdsize=60, alphamax=1.1, opticurve=True, opttolerance=0.8)
    sil[:3,:]=sil[-3:,:]=False; sil[:,:3]=sil[:,-3:]=False
    pf=potrace.Bitmap(sil).trace(turdsize=400, alphamax=1.2, opticurve=True, opttolerance=0.6)
    res[k]={"linien":pfad(pl),"flaeche":pfad(pf,True)}
    Image.fromarray(((~ink)*255).astype('uint8')).resize((W*2,H*2)).save('mv-%s-ink.png'%k); Image.fromarray((sil*255).astype('uint8')).resize((W,H)).save('mv-%s-sil.png'%k)
    print(k,len(res[k]['linien']),len(res[k]['flaeche']))
json.dump(res,open('haar-mann-vorne.json','w'))
