import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. ")
POST = " Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
S = [
(1,"بس مو كل الكتب غرقت... عالم اسمه نصير الدين الطوسي، أنقذ آلاف الكتب وأخذها لمرصد بمراغة.","A 13th century Persian scholar with a grey beard and white turban loading stacks of old manuscripts onto camels at night, escaping a burning city in the distance.",1,{}),
(1,"وكتب بيت الحكمة وصلت للأندلس، وبطليطلة ترجموها للغة اللاتينية.","Medieval scholars of different origins translating Arabic manuscripts into Latin at long wooden tables in a stone library in Toledo, candlelight.",1,{}),
(1,"واسم الخوارزمي صار بأوروبا: ألغوريزموس... ومنها طلعت كلمة الخوارزمية.","A medieval European monk reading an old Arabic mathematics manuscript with geometric diagrams by a window, amazed expression.",1,{}),
(1,"والأرقام اللي تكتب بيها هسه، أوروبا تعلمتها من العرب. يعني كل مرة تحسب... بيت الحكمة وياك.","A modern Iraqi student writing numbers in a notebook, a translucent glowing image of an Abbasid library appearing behind him.",1,{}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p, "prompt": G + img + POST}
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(sum(len(x['vo']) for x in out))
