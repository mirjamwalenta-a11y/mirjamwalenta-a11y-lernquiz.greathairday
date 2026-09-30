import json, math, re
import numpy as np
S=3
d=json.load(open('haar-front.json'))
out={}
for name,C in [('frau',(216,300)),('mann',(185,300))]:
    sil=np.load('th-%s-sil.npy'%name); H,W=sil.shape
    cx,cy=C
    # r_in / r_out je Winkel (Grad, gegen Uhrzeigersinn, 0 = rechts)
    th=np.arange(-90,271,1.0); rin=np.full(th.shape,np.nan); rout=np.full(th.shape,np.nan)
    for i,a in enumerate(th):
        ca,sa=math.cos(math.radians(a)),-math.sin(math.radians(a))
        hit=[]
        for r in np.arange(0,400,0.5):
            x,y=int((cx+ca*r)*S),int((cy+sa*r)*S)
            if 0<=x<W and 0<=y<H and sil[y,x]: hit.append(r)
        if hit: rin[i]=hit[0]; rout[i]=hit[-1]
    ok=~np.isnan(rin)
    # zusammenhängender Bereich über oben: rechts-unten bis links-unten
    idx=np.where(ok)[0]; aR,aL=th[idx[0]],th[idx[-1]]
    dick=rout-rin; med=np.nanmedian(dick)
    while name=='frau' and aR<aL and not (dick[int(aR-th[0])]>=0.7*med): aR+=1
    while name=='frau' and aL>aR and not (dick[int(aL-th[0])]>=0.7*med): aL-=1
    # glätten
    def glatt(v):
        v=v.copy(); m=~np.isnan(v)
        for _ in range(3):
            w=v.copy()
            for i in range(1,len(v)-1):
                if m[i-1] and m[i] and m[i+1]: w[i]=(v[i-1]+2*v[i]+v[i+1])/4
            v=w
        return v
    rin=glatt(rin); rout=glatt(rout)
    # Bogenlänge von Innenkante und Außenkontur über den Winkel (rechts unten -> oben -> links unten)
    sel=[i for i in range(len(th)) if aR<=th[i]<=aL]
    def bogen(rr):
        pts=[(cx+rr[i]*math.cos(math.radians(th[i])), cy-rr[i]*math.sin(math.radians(th[i]))) for i in sel]
        L=[0.0]
        for j in range(1,len(pts)): L.append(L[-1]+math.hypot(pts[j][0]-pts[j-1][0],pts[j][1]-pts[j-1][1]))
        return [v/L[-1] for v in L]
    fin=bogen(rin); fout=bogen(rout)
    def uv(x,y):
        a=math.degrees(math.atan2(-(y-cy),x-cx))
        if a<-90: a+=360
        ax=a; a=min(max(a,aR),aL)
        j=(a-th[0]); i0=int(j); f=j-i0; i1=min(i0+1,len(th)-1)
        ri=rin[i0]*(1-f)+rin[i1]*f; ro=rout[i0]*(1-f)+rout[i1]*f
        if np.isnan(ri) or np.isnan(ro): ri,ro=rin[i0],rout[i0]
        r=math.hypot(x-cx,y-cy)
        t=(r-ri)/max(ro-ri,1)
        k=a-aR; k0=int(k); kf=k-k0; k1=min(k0+1,len(sel)-1); k0=min(k0,len(sel)-1)
        ui=fin[k0]*(1-kf)+fin[k1]*kf; uo=fout[k0]*(1-kf)+fout[k1]*kf
        if ax<aR: ui+=(ax-aR)*(fin[1]-fin[0]); uo+=(ax-aR)*(fout[1]-fout[0])
        if ax>aL: ui+=(ax-aL)*(fin[-1]-fin[-2]); uo+=(ax-aL)*(fout[-1]-fout[-2])
        return ui,uo,t
    def umrechnen(p):
        nums=re.findall(r'[MLCZ]|-?\d+(?:\.\d+)?',p); o=[]; i=0
        while i<len(nums):
            tkn=nums[i]
            if tkn in 'MLCZ': o.append(tkn); i+=1; continue
            x,y=float(nums[i]),float(nums[i+1]); i+=2
            ui,uo,t=uv(x,y); o.append("%d,%d,%d"%(round(uo*2000),round((ui-uo)*2000),round(t*1000)))
        return " ".join(o).replace(" C "," C").replace(" L "," L").replace("M ","M").replace(" Z","Z")
    out[name]={"pfad":umrechnen(d[name]['linien']),"aR":aR,"aL":aL}
    print(name,aR,aL,len(out[name]['pfad']))
json.dump(out,open('haar-uv.json','w'))
