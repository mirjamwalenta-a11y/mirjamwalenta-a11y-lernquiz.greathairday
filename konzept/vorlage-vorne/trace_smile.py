import json, math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, potrace
F='/root/.claude/uploads/a6e2b49f-253a-5c56-b648-5d91c3f5cdcb/6dde9b06-image.jpg'
src=Image.open(F).convert('L')
S=8
# box, Schwelle, Anker A,B (Vorlage) -> Zielanker (normiert), Spiegeln
D={
 'frau':dict(box=(108,318,177,357),thr=165,poly=[(108,327),(122,320),(142,318),(162,320),(177,326),(170,345),(150,357),(128,354),(112,342)]),
 'mann':dict(box=(116,843,206,878),thr=140,poly=[(116,852),(130,846),(160,845),(190,846),(206,850),(196,866),(170,878),(140,876),(122,866)]),
}
res={}
for k,v in D.items():
    X0,Y0,X1,Y1=v['box']; W,H=X1-X0,Y1-Y0
    c=src.crop(v['box']).resize((W*S,H*S),Image.LANCZOS)
    m=Image.new('L',c.size,0); ImageDraw.Draw(m).polygon([((x-X0)*S,(y-Y0)*S) for x,y in v['poly']],fill=255)
    a=(np.array(c)<v['thr'])&(np.array(m)>0)
    a[:2,:]=a[-2:,:]=False; a[:,:2]=a[:,-2:]=False
    # kleine Flecken entfernen (Öffnen)
    a=np.array(Image.fromarray((a*255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)))>0
    pl=potrace.Bitmap(a).trace(turdsize=120, alphamax=1.0, opticurve=True, opttolerance=0.4)
    def pts(cv): return [cv.start_point]+[q for sg in cv.segments for q in ([sg.c,sg.end_point] if sg.is_corner else [sg.c1,sg.c2,sg.end_point])]
    keep=[]
    for cv in pl:
        P=pts(cv); xs=[p.x for p in P]; ys=[p.y for p in P]
        if max(xs)-min(xs)<6*S and max(ys)-min(ys)<6*S: continue   # Flecken
        if max(xs)-min(xs)>0.95*W*S and max(ys)-min(ys)>0.95*H*S: continue   # Rahmen
        keep.append(cv)
    allp=[p for cv in keep for p in pts(cv)]
    x0=min(p.x for p in allp)/S+X0; x1=max(p.x for p in allp)/S+X0; y0=min(p.y for p in allp)/S+Y0; y1=max(p.y for p in allp)/S+Y0
    cx=(x0+x1)/2; cy=(y0+y1)/2; bw=x1-x0
    g=lambda p:"%d,%d"%(round((p.x/S+X0-cx)/bw*1000),round((p.y/S+Y0-cy)/bw*1000))
    out=[]
    for cv in keep:
        s="M"+g(cv.start_point)
        for sg in cv.segments:
            s+=(" L"+g(sg.c)+" "+g(sg.end_point)) if sg.is_corner else (" C"+g(sg.c1)+" "+g(sg.c2)+" "+g(sg.end_point))
        out.append(s+"Z")
    res[k]=" ".join(out)
    Image.fromarray(((~a)*255).astype('uint8')).save('smile-%s.png'%k)
    print(k,len(res[k]),round(bw,1),round(y1-y0,1),len(keep))
json.dump(res,open('smile.json','w'))
