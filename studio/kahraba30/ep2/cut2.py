# Per-scene cuts: whisper word timestamps (wts*.json) + paragraph word-count proportion -> boundaries at the biggest word gap near each expected index.
import json,subprocess,re
chunks=json.load(open('ep2_chunks.json')); allcuts={}
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
for ci,c in enumerate(chunks):
    paras=c['text'].split('\n\n'); n=len(paras); f=f'e2c{ci}.mp3'; D=dur(f)
    W=json.load(open(f'wts{ci}.json'))['words']; m=len(W)
    cnt=[len(re.findall(r'\S+',re.sub(r'[.…؟?!،,:]',' ',p))) for p in paras]; tot=sum(cnt)
    cum=0; cuts=[]; prev=0
    for k in range(n-1):
        cum+=cnt[k]; target=cum/tot*m  # expected whisper word index boundary
        # candidates j in (prev+1 .. m-1): boundary between W[j-1] and W[j]
        best=None
        for j in range(prev+1,m-(n-1-k)+1):
            gap=W[j]['start']-W[j-1]['end']
            score=gap*4 - abs(j-target)*0.6
            if best is None or score>best[0]: best=(score,j)
        j=best[1]; prev=j
        cuts.append((W[j-1]['end']+W[j]['start'])/2)
    allcuts[ci]=cuts
    b=[0]+cuts+[D]
    for k in range(n):
        i=c['from']+k
        subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-ss',f'{max(0,b[k]-0.02):.3f}','-to',f'{b[k+1]:.3f}','-ar','48000','-ac','1',f'lines/line{i:02d}.wav'],check=True)
    print(ci,[round(x,1) for x in cuts],[round(b[k+1]-b[k],1) for k in range(n)])
