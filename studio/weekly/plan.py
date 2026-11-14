# Builds comps.json: weekly compilations (battles on Tuesday, facts on Friday, 19:00 Baghdad)
import json, datetime as D, subprocess
SP='/tmp/claude-0/-home-user-yutub-hthub/75479b81-b547-55a6-a2f8-a9ffc6cee05d/scratchpad'
ev=json.load(open(SP+'/allev.json'))
ev+= [['2026-11-24T17:00','battle',21],['2026-11-24T21:00','facts',1]]
ev=sorted(ev)
E={x['n']:x for x in json.load(open('../flag-battles/episodes.json'))+json.load(open('../flag-battles/episodes2.json'))}
F=json.load(open('../facts-series/facts.json'))
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
def path(k,n): return f'../../videos/flags/flag-battle-{n:02d}.mp4' if k=='battle' else f'../../videos/facts/facts-{n:02d}.mp4'
def windows(kind, wd):  # wd: 1=Tue,4=Fri
  d=D.date(2026,11,14)
  while d.weekday()!=wd: d+=D.timedelta(1)
  out=[]
  while True:
    lo=(d-D.timedelta(7)).isoformat(); hi=d.isoformat()
    eps=[n for a,k,n in ev if k==kind and lo<=a[:10]<hi]
    if not eps and out and d.isoformat()>ev[-1][0]: break
    if eps: out.append([d,eps])
    d+=D.timedelta(7)
  # merge tiny windows (<5) into neighbour (forward for first, backward-into-next for last)
  i=0
  while i<len(out):
    if len(out[i][1])<5 and len(out)>1:
      if i+1<len(out): out[i+1][1]=out[i][1]+out[i+1][1]; out.pop(i); continue
      else: out[i][1]=out[i-1][1]+out[i][1]; out.pop(i-1); continue
    i+=1
  return out
def ts(s): s=int(s); return f'{s//60}:{s%60:02d}'
comps=[]
for kind,wd in (('battle',1),('facts',4)):
  for w,(d,eps) in enumerate(windows(kind,wd),1):
    chap=[];t=0
    for n in eps:
      if kind=='battle': lab=f"{E[n]['a']} ضد {E[n]['b']}"
      else: lab=f"معلومات غريبة عن {F[n-1]['c']} {F[n-1]['f']}"
      chap.append(f'{ts(t)} {lab}'); t+=dur(path(kind,n))
    if kind=='battle':
      e=E[eps[0]]
      title=f"تجميعة معارك الأسبوع ⚔️ {len(eps)} معارك نارية: {e['a']} ضد {e['b']} وأكثر! | الأسبوع {w}"
      intro=f"كل معارك الكرات اللي نزلت هالأسبوع بفيديو واحد ⚔️🔥\nكل كرة عندها 100 HP والأسلحة تطلع عشوائياً — كلها محاكاة فيزياء حقيقية، محد يختار الفايز.\nاكتب بالتعليقات: أي معركة أقوى؟ 👇"
      tags=['countryballs','ball battle','معركة الأعلام','معركة الفرق','تجميعة','تجميعة الأسبوع','محاكاة','منو يفوز','country balls','football']
    else:
      names='، '.join(F[n-1]['c'] for n in eps[:3])
      title=f"معلومات غريبة عن {len(eps)} دول 🤯 {names} وأكثر | تجميعة الأسبوع {w}"
      intro=f"كل حلقات المعلومات الغريبة اللي نزلت هالأسبوع بفيديو واحد 🤯🌍\n3 معلومات عن كل دولة بصوت عربي.\nإنت من وين؟ اكتب دولتك بالتعليقات حتى نسويلها حلقة 👇"
      tags=['معلومات غريبة','هل تعلم','حقائق','ثقافة عامة','معلومات عن الدول','تجميعة','تجميعة الأسبوع','facts']+[F[n-1]['c'] for n in eps][:12]
    desc=intro+'\n\n⏱️ الحلقات:\n'+'\n'.join(chap)+('\n\n#CountryBalls #معركة_الأعلام #تجميعة' if kind=='battle' else '\n\n#معلومات_غريبة #هل_تعلم #تجميعة')
    comps.append(dict(kind=kind,w=w,date=d.isoformat(),at=d.isoformat()+'T19:00:00+03:00',eps=eps,title=title[:100],desc=desc,tags=tags,dur=round(t),
      files=[path(kind,n) for n in eps],out=f'out/{kind}-week{w:02d}.mp4'))
json.dump(comps,open('comps.json','w'),ensure_ascii=False,indent=1)
for c in comps: print(c['kind'],c['w'],c['date'],c['eps'][0],'-',c['eps'][-1],len(c['eps']),ts(c['dur']),len(c['title']))
