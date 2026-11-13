import numpy as np, json, wave
st=json.load(open('out/stats.json'));fps=st['fps'];total=st['total'];S=st['stats']
sr=44100;N=int(total*sr);rng=np.random.default_rng(3)
w=wave.open('audio/vo_final.wav');v=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
voice=np.zeros(N,np.float32);voice[:min(N,len(v))]=v[:N]
def band(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/sr);X[(f<lo)|(f>hi)]=0;return np.fft.irfft(X,len(x)).astype(np.float32)
def env_from(vals,smooth=0.03):
    fr=np.repeat(np.array(vals,np.float32),sr//fps);fr=np.pad(fr,(0,max(0,N-len(fr))))[:N]
    k=int(smooth*sr);return np.convolve(fr,np.ones(k)/k,'same')
t=np.arange(N)/sr
e=env_from([1.0 if s['drawing'] else 0.0 for s in S],0.08)
sh=band(rng.normal(0,1,N).astype(np.float32),4500,11000); sh=sh/np.sqrt(np.mean(sh**2))*10**(-36/20)
tw=sum(np.sin(2*np.pi*f*t+ph) for f,ph in [(1568,0),(2093,1.1),(2637,2.3)])*0.012*(0.5+0.5*np.sin(2*np.pi*3*t))
magic=(sh*(0.55+0.45*np.sin(2*np.pi*11*t))+tw)*e
ew=env_from([s['whoosh']**2 for s in S],0.05)
whn=band(rng.normal(0,1,N).astype(np.float32),150,1400); whn=whn/np.sqrt(np.mean(whn**2))*10**(-27/20)*ew
mix=voice+magic+whn
wv=wave.open('audio/mix_pres.wav','wb');wv.setnchannels(1);wv.setsampwidth(2);wv.setframerate(sr);wv.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes());wv.close()
print('mix ok',round(total,2))
