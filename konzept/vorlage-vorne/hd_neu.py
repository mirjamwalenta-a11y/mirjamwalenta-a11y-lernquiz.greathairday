import io, base64, json
from PIL import Image, ImageDraw, ImageFilter
U='/root/.claude/uploads/a6e2b49f-253a-5c56-b648-5d91c3f5cdcb/'
D={
 'aufsteigend':('a1d3f8a5-image.png',(95,165,605,770),
   [((157,234),(246,339)),((505,205),(466,238)),((165,612),(98,697)),((521,687),(556,756))],
   [(0,0,683,160),(0,150,240,232),(480,160,683,236),(0,690,170,854),(440,745,683,854),(640,150,683,450)]),
 'rechteck':('28a8117d-image.png',(92,215,540,850),
   [((137,235),(214,345)),((460,234),(432,295)),((98,439),(171,476)),((106,683),(61,732))],
   [(0,0,586,150),(0,150,235,228),(420,150,586,236),(0,300,130,432),(0,725,178,863)]),
}
H=json.load(open('hd-bilder.json'))
for k,(f,box,lin,weg) in D.items():
    im=Image.open(U+f).convert('L'); med=im.filter(ImageFilter.MedianFilter(13))
    m=Image.new('L',im.size,0); dm=ImageDraw.Draw(m)
    import numpy as np
    A=np.array(im).astype(int)
    for (x0,y0),(x1,y1) in lin:
        dx,dy=x1-x0,y1-y0; L=(dx*dx+dy*dy)**.5; nx,ny=-dy/L,dx/L; pts=[]
        for t in np.linspace(-0.03,1.03,90):
            x=x0+dx*t; y=y0+dy*t; best=None
            for s_ in range(-8,9):
                px,py=int(round(x+nx*s_)),int(round(y+ny*s_))
                if 0<=px<A.shape[1] and 0<=py<A.shape[0] and (best is None or A[py,px]<best[0]): best=(A[py,px],px,py)
            pts.append(best[1:])
        # glätten
        sm=[(sum(p[0] for p in pts[max(0,i-3):i+4])/len(pts[max(0,i-3):i+4]),sum(p[1] for p in pts[max(0,i-3):i+4])/len(pts[max(0,i-3):i+4])) for i in range(len(pts))]
        dm.line(sm,fill=255,width=8)
    im=Image.composite(med,im,m); d=ImageDraw.Draw(im)
    for r in weg: d.rectangle(r,fill=255)
    c=im.crop(box); c.thumbnail((340,420),Image.LANCZOS)
    c.save('hdn-%s.png'%k)
    b=io.BytesIO(); c.save(b,'JPEG',quality=82,optimize=True)
    H['frau'][k]={"src":"data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode(),"w":c.size[0],"h":c.size[1]}
json.dump(H,open('hd-bilder.json','w'))
