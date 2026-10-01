import json
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np, potrace
F='/root/.claude/uploads/a6e2b49f-253a-5c56-b648-5d91c3f5cdcb/1249561a-image.jpg'
FQ='/root/.claude/uploads/a6e2b49f-253a-5c56-b648-5d91c3f5cdcb/1c19bc74-image.jpg'
S=4
D={
 'f1':dict(box=(25,156,285,418),eyes=((116.7,273),(176.7,273)),
   gesicht=[(92,259),(206,259),(203,300),(196,330),(185,350),(186,420),(112,420),(112,350),(101,330),(95,300)],
   linien=[((183,203),(233,180)),((192,227),(260,239))],text=[(236,160,290,270)]),
 'f2':dict(box=(395,157,640,418),eyes=((485,273),(543,273)),
   gesicht=[(462,262),(490,252),(515,230),(540,200),(552,205),(565,240),(573,270),(574,305),(565,335),(553,352),(552,420),(478,420),(478,352),(466,335),(461,305)],
   linien=[((565,227),(625,210)),((580,321),(637,332))],text=[(618,185,660,232),(632,305,660,352)]),
 'f3':dict(box=(775,155,992,418),eyes=((865,273),(922,273)),spiegel=893.5,
   gesicht=[(893,198),(905,205),(917,250),(947,278),(953,305),(945,335),(930,352),(927,420),(860,420),(858,352),(843,335),(835,305),(843,278),(870,250),(882,205)],
   linien=[((773,199),(828,247)),((760,370),(828,330))],text=[(760,155,822,192),(760,355,790,430)]),
 'm4':dict(box=(25,625,265,850),eyes=((105.8,784),(175,784)),
   ohren=[[(50,785),(76,780),(78,860),(50,860)],[(205,780),(234,785),(234,860),(205,860)]],
   gesicht=[(75,768),(105,760),(140,765),(175,758),(207,768),(210,800),(206,840),(190,870),(170,890),(140,900),(110,890),(90,870),(76,840),(72,800)],
   linien=[((229,648),(208,671)),((271,714),(233,751)),((194,804),(269,874))],text=[(175,618,300,648),(238,688,300,742)]),
 'm5':dict(box=(405,640,640,830),eyes=((479.5,784),(549,784)),
   ohren=[[(412,790),(442,785),(442,850),(412,850)],[(598,785),(628,790),(628,850),(598,850)]],
   gesicht=[(440,773),(600,773),(605,800),(605,845),(595,870),(560,893),(516,900),(472,893),(440,870),(435,845),(435,800)],
   linien=[((419,652),(460,712)),((615,648),(569,704)),((646,726),(588,767)),((468,802),(406,866))],text=[(390,615,650,648),(628,675,660,705)]),
 'm6':dict(box=(778,640,992,865),eyes=((855.8,786),(925,786)),
   ohren=[[(968,790),(992,785),(992,860),(968,860)]],
   gesicht=[(830,775),(858,745),(896,712),(931,707),(958,727),(970,765),(976,800),(972,845),(955,870),(925,890),(892,898),(860,890),(835,870),(820,845),(818,800)],
   linien=[((796,654),(850,710)),((965,648),(937,693)),((850,821),(769,885)),((969,819),(986,850))],text=[(760,615,992,650)]),
}
D={'mq':dict(f=FQ,thr=95,box=(410,130,590,265),eyes=((470,276),(531,276)),
   ohren=[[(410,250),(430,250),(430,265),(410,265)],[(570,250),(590,250),(590,265),(570,265)]],
   gesicht=[(440,207),(470,200),(500,203),(530,200),(560,207),(565,240),(567,265),(433,265),(435,240)],
   linien=[((587,135),(548,165)),((415,163),(424,180)),((597,245),(573,257))],text=[(400,120,425,150),(572,120,600,150)])}
res={}
SRC={F:Image.open(F).convert('L'),FQ:Image.open(FQ).convert('L')}
for k,v in D.items():
    src=SRC.get(v.get('f',F)); MED=src.filter(ImageFilter.MedianFilter(9))
    m=Image.new('L',src.size,0); dm=ImageDraw.Draw(m)
    for (A,B) in v['linien']:
        L=((B[0]-A[0])**2+(B[1]-A[1])**2)**.5; ux,uy=(B[0]-A[0])/L,(B[1]-A[1])/L
        dm.line([(A[0]-ux*5,A[1]-uy*5),(B[0]+ux*5,B[1]+uy*5)],fill=255,width=5)
    im=Image.composite(MED,src,m); d=ImageDraw.Draw(im)
    for t in v['text']: d.rectangle(t,fill=255)
    if 'spiegel' in v:
        cx=v['spiegel']; X0=int(v['box'][0]); L=im.crop((X0,0,int(cx),im.size[1])); R=ImageOps.mirror(L)
        im.paste(R,(int(cx),0))
    X0,Y0,X1,Y1=v['box']; W,H=X1-X0,Y1-Y0
    c=im.crop(v['box']).resize((W*S,H*S),Image.LANCZOS)
    tr=lambda P:[((x-X0)*S,(y-Y0)*S) for x,y in P]
    ex=Image.new('L',c.size,0); de=ImageDraw.Draw(ex); de.polygon(tr(v['gesicht']),fill=255)
    for o in v.get('ohren',[]): de.polygon(tr(o),fill=255)
    d=ImageDraw.Draw(c); d.rectangle((0,0,c.width-1,c.height-1),outline=255,width=6)
    a=np.array(c); exm=np.array(ex)>0
    ink=(a<v.get('thr',150))&~exm
    cl=5*S//2*2+1
    b=Image.fromarray((ink*255).astype('uint8')).filter(ImageFilter.MaxFilter(cl))
    b2=Image.new('L',(b.width+2,b.height+2),0); b2.paste(b,(1,1)); ImageDraw.floodfill(b2,(0,0),128)
    sil=np.array(b2)[1:-1,1:-1]!=128
    sI=Image.fromarray((sil*255).astype('uint8')).filter(ImageFilter.MinFilter(cl))
    r=3*S//2*2+1; sI=sI.filter(ImageFilter.MinFilter(r)).filter(ImageFilter.MaxFilter(r))
    sil=(np.array(sI)>0)&~exm
    ink=ink&(np.array(sI.filter(ImageFilter.MaxFilter(2*S+1)))>0)
    sil[:3,:]=sil[-3:,:]=False; sil[:,:3]=sil[:,-3:]=False
    (ax,ay),(bx,by)=v['eyes']; cx=(ax+bx)/2; yE=(ay+by)/2; cc=(bx-ax)/0.49; ch=0.98*cc
    f=lambda x,y:((x-cx)/cc,(y-yE)/ch)
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
    pl=potrace.Bitmap(ink).trace(turdsize=25, alphamax=1.0, opticurve=True, opttolerance=0.5)
    pf=potrace.Bitmap(sil).trace(turdsize=400, alphamax=1.2, opticurve=True, opttolerance=0.6)
    res[k]={"linien":pfad(pl),"flaeche":pfad(pf)}
    Image.fromarray(((~ink)*255).astype('uint8')).resize((W*2,H*2)).save('pv-%s-ink.png'%k)
    print(k,len(res[k]['linien']),len(res[k]['flaeche']),res[k]['flaeche'].count('Z'))
json.dump(res,open('haar-quiff.json','w'))
