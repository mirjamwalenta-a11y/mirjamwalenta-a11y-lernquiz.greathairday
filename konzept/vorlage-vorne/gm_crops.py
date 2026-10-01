import io, base64, json
from PIL import Image, ImageDraw, ImageFilter
im=Image.open('../images/4.jpg').convert('L')
# fall, art, which: (box, whiteouts)
C={
 ('nase','mann','A'):((35,400,162,552),[(149,452,162,483)]),
 ('nase','mann','B'):((188,400,300,552),[(291,452,300,483)]),
 ('nase','frau','A'):((32,675,166,835),[(140,806,166,836),(158,722,166,745)]),
 ('nase','frau','B'):((208,675,342,835),[]),
 ('auge','mann','A'):((372,350,505,525),[]),
 ('auge','mann','B'):((538,350,664,525),[]),
 ('auge','frau','A'):((370,671,505,835),[]),
 ('auge','frau','B'):((538,671,668,835),[]),
 ('dk','frau','A'):((36,955,128,1078),[(90,1061,128,1080),(100,950,128,966)]),
 ('dk','frau','B'):((126,955,230,1078),[(126,950,150,968),(205,1050,230,1080)]),
 ('dk','mann','A'):((246,955,340,1078),[(246,950,282,961),(292,1061,340,1080)]),
 ('dk','mann','B'):((336,955,446,1078),[(336,950,362,970)]),
 ('rund','mann','A'):((486,962,563,1084),[]),
 ('rund','mann','B'):((558,958,650,1084),[]),
 ('rund','frau','A'):((34,1265,125,1388),[]),
 ('rund','frau','B'):((121,1265,216,1388),[]),
 ('ohr','frau','A'):((250,1265,340,1388),[]),
 ('ohr','frau','B'):((337,1265,436,1388),[]),
 ('ohr','mann','A'):((484,1268,570,1398),[]),
 ('ohr','mann','B'):((565,1265,662,1398),[]),
}
out={}
for (f,a,w),(box,wo) in C.items():
    c=im.copy(); d=ImageDraw.Draw(c)
    for r in wo:
        if len(r)==2: d.line(r,fill=238,width=4)
        else: d.rectangle(r,fill=238)
    c=c.crop(box)
    # nur den Kopf behalten: größte zusammenhängende Fläche (Beschriftung, Pfeilreste und Nachbarköpfe fallen weg)
    import numpy as np
    from scipy import ndimage
    A=np.array(c).astype(float)
    fg=A<205
    fg=ndimage.binary_closing(fg,iterations=2)
    fg=ndimage.binary_fill_holes(fg)
    lab,n=ndimage.label(fg)
    if n:
        sizes=ndimage.sum(fg,lab,range(1,n+1)); k=1+int(np.argmax(sizes))
        weg=ndimage.binary_dilation(fg&(lab!=k),iterations=2)&~ndimage.binary_dilation(lab==k,iterations=1)
        keep=~weg
        bg=np.median(A[~fg]) if (~fg).any() else 238
        A=np.where(keep,A,bg)
    c=Image.fromarray(A.astype("uint8"))
    c=c.resize((c.size[0]*3,c.size[1]*3),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,60,2))
    # einheitliches Format 4:5, Kopf unten bündig, Hintergrund wie Vorlage
    import numpy as np
    arr=np.array(c); bgv=int(np.median(arr[arr>200])) if (arr>200).any() else 238
    W0,H0=c.size; TW=max(W0,int(H0*0.8)); TH=int(TW/0.8)
    if TH<H0: TH=H0; TW=int(TH*0.8)
    can=Image.new('L',(TW,TH),bgv); can.paste(c,((TW-W0)//2,TH-H0)); c=can.resize((480,600),Image.LANCZOS)
    c.save('gmc-%s-%s-%s.png'%(f,a,w))
    b=io.BytesIO(); c.save(b,'JPEG',quality=82,optimize=True)
    out.setdefault(f,{}).setdefault(a,{})[w]={"src":"data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode(),"w":c.size[0],"h":c.size[1]}
json.dump(out,open('gm-bilder.json','w')); print(len(json.dumps(out)))
