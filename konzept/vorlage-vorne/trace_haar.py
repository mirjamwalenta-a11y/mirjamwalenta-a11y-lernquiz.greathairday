import json, sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, potrace
F='/root/.claude/uploads/a6e2b49f-253a-5c56-b648-5d91c3f5cdcb/a09d7bba-image.jpg'
S=3
def run(name, off, box, keep, weg_linien, weg_polys, thr=150, close=5):
    im=Image.open(F).convert('L'); ox,oy=off; X0,Y0,X1,Y1=box
    c=im.crop((X0+ox,Y0+oy,X1+ox,Y1+oy)).resize(((X1-X0)*S,(Y1-Y0)*S),Image.LANCZOS)
    tr=lambda pts:[((x-X0)*S,(y-Y0)*S) for x,y in pts]
    km=Image.new('L',c.size,0); ImageDraw.Draw(km).polygon(tr(keep),fill=255)
    d=ImageDraw.Draw(c)
    for l in weg_linien: d.line(tr(l[:2]),fill=255,width=int(3.2*S))
    for p in weg_polys: d.polygon(tr(p),fill=255)
    a=np.array(c); k=np.array(km)>0
    ink=(a<thr)&k
    # Silhouette zuerst: Haar schließen, Hintergrund fluten, dünne Ausläufer (Beschriftungslinien) wegöffnen
    b=Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(close*S//2*2+1))
    b2=Image.new('L',(b.width+2,b.height+2),0); b2.paste(b,(1,1))
    ImageDraw.floodfill(b2,(0,0),128)
    sil=np.array(b2)[1:-1,1:-1]!=128
    sI=Image.fromarray((sil*255).astype('uint8')).filter(ImageFilter.MinFilter(close*S//2*2+1))
    r=4*S//2*2+1
    sI=sI.filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))
    sil=np.array(sI)>0
    ink=ink&(np.array(sI.filter(ImageFilter.MaxFilter(2*S+1)))>0)
    # Linien
    pl=potrace.Bitmap(ink).trace(turdsize=350, alphamax=1.1, opticurve=True, opttolerance=1.2)
    def pfad(pl):
        out=[]
        for cv in pl:
            xs=[p.x for sg in cv.segments for p in ([sg.end_point]+([sg.c] if sg.is_corner else [sg.c1,sg.c2]))]
            ys=[p.y for sg in cv.segments for p in ([sg.end_point]+([sg.c] if sg.is_corner else [sg.c1,sg.c2]))]
            if max(xs)-min(xs)>0.97*(X1-X0)*S and max(ys)-min(ys)>0.97*(Y1-Y0)*S: continue
            f=lambda p:("%.1f,%.1f"%(p.x/S+X0,p.y/S+Y0)).replace(".0,",",").rstrip("0").rstrip(".") if False else "%g,%g"%(round(p.x/S+X0,1),round(p.y/S+Y0,1))
            s="M"+f(cv.start_point)
            for sg in cv.segments:
                s+=(" L"+f(sg.c)+" "+f(sg.end_point)) if sg.is_corner else (" C"+f(sg.c1)+" "+f(sg.c2)+" "+f(sg.end_point))
            out.append(s+"Z")
        return " ".join(out)
    linien=pfad(pl)
    pf=potrace.Bitmap(sil).trace(turdsize=400, alphamax=1.2, opticurve=True, opttolerance=0.5)
    flaeche=pfad(pf)
    np.save(name+'-sil.npy', sil); np.save(name+'-meta.npy', np.array([X0,Y0,S]))
    Image.fromarray(((~ink)*255).astype('uint8')).resize((c.width//S*2,c.height//S*2)).save(name+'-ink.png')
    Image.fromarray((sil*255).astype('uint8')).resize((c.width//S*2,c.height//S*2)).save(name+'-sil.png')
    return {"linien":linien,"flaeche":flaeche}
out={}
out['frau']=run('th-frau',(990,1080),(0,0,440,540),
  keep=[(10,10),(430,10),(430,500),(0,500)],
  weg_linien=[((30,148),(150,174)),((10,274),(96,270)),((18,354),(96,306)),((352,120),(380,104)),((374,252),(420,244)),((356,388),(404,407)),((80,468),(150,450))],
  weg_polys=[[(400,50),(440,50),(440,115),(400,115)],[(0,120),(14,120),(14,160),(0,160)],[(425,230),(440,230),(440,275),(425,275)],[(0,340),(12,340),(12,370),(0,370)],[(415,380),(440,380),(440,445),(415,445)],[(0,455),(62,455),(62,500),(0,500)],
    [(98,248),(120,228),(140,213),(295,213),(318,228),(338,248),(341,300),(335,345),(318,400),(298,450),(262,488),(215,494),(170,488),(135,450),(116,400),(102,345),(96,300)],[(138,209),(196,209),(196,226),(138,226)],[(240,207),(300,207),(300,224),(240,224)],
    [(88,298),(104,298),(104,338),(88,338)],[(332,298),(348,298),(348,338),(332,338)]])
out['mann']=run('th-mann',(250,1080),(0,0,370,540),
  keep=[(15,0),(370,0),(372,160),(335,215),(318,248),(298,238),(292,203),(90,203),(86,232),(72,240),(45,205),(22,140)],
  weg_linien=[((45,89),(85,102)),((314,157),(342,172))],
  weg_polys=[[(350,20),(372,20),(372,60),(350,60)],[(0,60),(18,60),(18,100),(0,100)]])
json.dump(out,open('haar-front.json','w'))
print({k:(len(v['linien']),len(v['flaeche'])) for k,v in out.items()})
