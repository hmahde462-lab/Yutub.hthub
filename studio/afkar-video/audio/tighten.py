import numpy as np, wave, json, sys
KN, KB = float(sys.argv[1]), float(sys.argv[2])
w=wave.open('audio/vo.wav'); sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
hop=sr//100; n=len(x)//hop
db=np.array([20*np.log10(np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2))+1e-9) for i in range(n)])
sil=db<-48; gaps=[];i=0
while i<n:
    if sil[i]:
        j=i
        while j<n and sil[j]: j+=1
        if (j-i)>=35: gaps.append((i/100,j/100))
        i=j
    else: i+=1
bounds=[7.79,17.81,28.88,38.56,49.90,60.42]
keep=[];cur=0.0
for a,b in gaps:
    isb=any(a<=t<=b+0.05 for t in bounds)
    k=min(KB if isb else KN, b-a)
    keep.append((cur,a+k*0.4)); cur=b-k*0.6
keep.append((cur,len(x)/sr))
fade=int(0.008*sr);out=[];t=0.0;mapping=[]
for a,b in keep:
    seg=x[int(a*sr):int(b*sr)].copy()
    seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
    mapping.append((a,b,t)); t+=len(seg)/sr; out.append(seg)
y=np.concatenate(out)
def m(tt):
    for a,b,s in mapping:
        if a<=tt<=b: return s+(tt-a)
    for a,b,s in mapping:
        if a>tt: return s
nb=[round(m(tt)-0.25,3) for tt in bounds]
print("new length",round(len(y)/sr,2),"bounds",nb)
wv=wave.open('audio/vo_tight.wav','wb');wv.setnchannels(1);wv.setsampwidth(2);wv.setframerate(sr)
wv.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes());wv.close()
json.dump({"len":len(y)/sr,"bounds":nb},open('audio/tight.json','w'))
