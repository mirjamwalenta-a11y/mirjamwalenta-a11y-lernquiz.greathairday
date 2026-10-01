import io, base64, json
from PIL import Image, ImageDraw, ImageFilter
im=Image.open('../images/4.jpg').convert('L')
im5=Image.open('../images/5.jpg').convert('L')
# fall, art, which: (box, whiteouts)
C={
 ('nase','frau','A'):((30,398,162,552),[(152,452,162,481),(146,463,152,475)],5),
 ('nase','frau','B'):((186,398,320,552),[(293,528,320,556),(304,513,320,528),(312,398,320,440),(262,396,318,405)],5),
 ('nase','mann','A'):((30,398,172,556),[(153,450,172,480)]),
 ('nase','mann','B'):((185,398,318,556),[(301,450,318,477)]),
 ('auge','mann','A'):((370,348,508,526),[]),
 ('auge','mann','B'):((536,348,666,526),[]),
 ('auge','frau','A'):((368,670,508,836),[]),
 ('auge','frau','B'):((536,670,670,836),[]),
 ('dk','frau','A'):((28,672,170,838),[(160,698,170,736),(138,810,170,840)]),
 ('dk','frau','B'):((204,672,346,838),[(204,698,213,736)]),
 ('dk','mann','A'):((242,952,342,1080),[(242,948,282,961),(300,1062,342,1082)]),
 ('dk','mann','B'):((334,952,452,1080),[(334,948,362,970)]),
 ('rund','mann','A'):((482,956,566,1088),[(550,950,566,965),(482,1084,566,1090)]),
 ('rund','mann','B'):((556,954,672,1088),[(556,950,592,973),(556,1084,672,1090),(556,1000,570,1050)]),
 ('rund','frau','A'):((28,1262,126,1390),[(94,1258,126,1283)]),
 ('rund','frau','B'):((117,1262,230,1390),[(119,1258,152,1283)]),
 ('ohr','frau','A'):((249,1262,342,1398),[]),
 ('ohr','frau','B'):((326,1262,450,1398),[]),
 ('ohr','mann','A'):((478,1264,573,1400),[]),
 ('ohr','mann','B'):((561,1262,670,1400),[]),
}
out={}
for (f,a,w),v in C.items():
    box,wo=v[0],v[1]
    c=(im5 if len(v)>2 else im).copy(); d=ImageDraw.Draw(c)
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
        # Reste am Rand (Pfeilspitzen, Panelrand) entfernen
        rand=np.zeros_like(fg); rand[:4,:]=rand[-3:,:]=rand[:,:4]=rand[:,-4:]=True
        lab2,n2=ndimage.label(fg&~(lab==k)); 
        for q in range(1,n2+1):
            mq=lab2==q
            if (mq&rand).any(): A=np.where(ndimage.binary_dilation(mq,iterations=2)&~(lab==k),bg,A)
    c=Image.fromarray(A.astype("uint8"))
    c=c.resize((c.size[0]*3,c.size[1]*3),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,60,2))
    # einheitliches Format 4:5, Kopf unten bündig, Hintergrund wie Vorlage
    import numpy as np
    arr=np.array(c); bgv=int(np.median(arr[arr>200])) if (arr>200).any() else 238
    # Rand rundherum, damit nichts am Bildrand klebt; einheitlich 4:5
    W0,H0=c.size; m=int(max(W0,H0)*0.08); W1,H1=W0+2*m,H0+m
    TW=max(W1,int(H1*0.8)); TH=int(TW/0.8)
    if TH<H1: TH=H1; TW=int(TH*0.8)
    can=Image.new('L',(TW,TH+m),bgv); can.paste(c,((TW-W0)//2,(TH+m-H0)//2)); TH=TH+m; c=can.resize((480,600),Image.LANCZOS)
    c.save('gmc-%s-%s-%s.png'%(f,a,w))
    b=io.BytesIO(); c.save(b,'JPEG',quality=82,optimize=True)
    out.setdefault(f,{}).setdefault(a,{})[w]={"src":"data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode(),"w":c.size[0],"h":c.size[1]}
json.dump(out,open('gm-bilder.json','w')); print(len(json.dumps(out)))
