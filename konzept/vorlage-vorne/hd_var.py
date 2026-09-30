import io, base64, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
out={}
for art in ['frau','mann']:
    im=Image.open('hdc-%s-rund.png'%art).convert('L'); W,H=im.size
    a=np.array(im).astype(float)
    P={'frau':dict(aussen=[(120,15),(145,13),(175,20),(195,35),(207,65),(213,100),(222,150),(232,190),(233,230),(245,258),(215,258),(200,275),(200,285),(40,285),(40,270),(15,262),(28,250),(38,230),(38,190),(28,160),(30,140),(38,100),(50,60),(70,30),(95,18)],
                   gesicht=[(100,62),(125,58),(150,60),(165,75),(170,100),(176,130),(176,160),(175,190),(160,210),(165,250),(170,285),(90,285),(95,250),(100,210),(85,190),(76,160),(73,130),(84,100),(92,75)]),
       'mann':dict(aussen=[(50,12),(75,5),(100,5),(140,15),(160,35),(175,50),(185,60),(185,80),(172,100),(168,125),(170,140),(160,140),(158,110),(150,85),(120,80),(100,88),(80,82),(52,85),(42,110),(40,140),(28,140),(25,110),(15,80),(18,55),(25,40),(35,25)],gesicht=[])}[art]
    mi=Image.new('L',(W,H),0); dd=ImageDraw.Draw(mi); dd.polygon(P['aussen'],fill=255)
    if P['gesicht']: dd.polygon(P['gesicht'],fill=0)
    m=np.array(mi.filter(ImageFilter.GaussianBlur(1.5)))/255.0
    m*=np.clip((250-np.array(im.filter(ImageFilter.GaussianBlur(4))).astype(float))/20,0,1)
    Image.fromarray((m*255).astype('uint8')).save('hdm-%s.png'%art)
    L=np.array(im.filter(ImageFilter.GaussianBlur(7))).astype(float); D=a-L
    mean=(L*m).sum()/m.sum()
    ys=np.arange(H)[:,None]*np.ones((1,W))
    # Grenze Oberkopf/Seiten: Augenhöhe etwas darüber
    g={'frau':H*0.33,'mann':66}[art]
    sig=1/(1+np.exp(-(ys-g)/6))
    varianten={
      'B':L,
      'A':np.full_like(L,mean),
      'umgekehrt':np.clip(0.5*(2*mean-L)+0.5*(70+(205-70)*sig),20,235),
      'hart':np.where(ys<g,225,40),
    }
    varianten['M']=(varianten['A']+L)/2
    out[art]={}
    for k,T in varianten.items():
        r=np.clip(T+D,0,255)
        res=a*(1-m)+r*m
        img=Image.fromarray(res.astype('uint8'))
        img.save('hdv-%s-%s.png'%(art,k))
        b=io.BytesIO(); img.save(b,'JPEG',quality=78,optimize=True)
        out[art][k]="data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()
    out[art]['w']=W; out[art]['h']=H
json.dump(out,open('hd-var.json','w'))
print(sum(len(v) for a in out.values() for k,v in a.items() if isinstance(v,str)))
