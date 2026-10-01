import io, base64, json
from PIL import Image, ImageDraw, ImageFilter
im=Image.open('../images/4.jpg').convert('L')
# fall, art, which: (box, whiteouts)
C={
 ('nase','mann','A'):((38,405,156,553),[(149,458,158,481)]),
 ('nase','mann','B'):((190,405,291,553),[]),
 ('nase','frau','A'):((35,680,158,838),[(136,806,158,840)]),
 ('nase','frau','B'):((212,680,340,838),[]),
 ('auge','mann','A'):((380,355,500,520),[]),
 ('auge','mann','B'):((548,355,655,520),[]),
 ('auge','frau','A'):((375,668,500,830),[]),
 ('auge','frau','B'):((548,668,665,830),[]),
 ('dk','frau','A'):((40,958,128,1048),[]),
 ('dk','frau','B'):((126,958,226,1048),[]),
 ('dk','mann','A'):((250,960,338,1048),[]),
 ('dk','mann','B'):((338,958,440,1048),[(338,950,362,970)]),
 ('rund','mann','A'):((493,975,560,1082),[]),
 ('rund','mann','B'):((562,972,644,1082),[]),
 ('rund','frau','A'):((40,1270,124,1385),[]),
 ('rund','frau','B'):((122,1270,210,1385),[]),
 ('ohr','frau','A'):((254,1272,336,1385),[]),
 ('ohr','frau','B'):((342,1272,430,1385),[]),
 ('ohr','mann','A'):((488,1278,566,1395),[]),
 ('ohr','mann','B'):((568,1275,656,1395),[]),
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
