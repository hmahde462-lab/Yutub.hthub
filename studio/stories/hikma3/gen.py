import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. ")
POST = " Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... مكتبة ببغداد قبل ألف ومية سنة، أكبر مكتبة بالعالم كله.","A vast Abbasid-era library hall in 9th century Baghdad with tall arches, endless shelves of manuscripts, oil lamps, scholars in turbans reading at low tables.",1,{"sfx":"boom"}),
(1,"الخليفة المأمون جمع بيها علماء من كل الدنيا: عرب، وفرس، وهنود، ويونان.","Caliph al-Ma'mun (black beard, black Abbasid turban, rich dark robe) seated on cushions in a palace hall, welcoming scholars in Persian, Indian and Greek clothing carrying scrolls.",1,{}),
(1,"وجان يدفع للمترجم... وزن الكتاب ذهب!","A large brass balance scale in a palace: a thick old manuscript on one pan and a pile of shining gold coins on the other, a translator watching amazed.",1,{"sfx":"hit"}),
(1,"اسمها بيت الحكمة... وراح تغيّر العالم.","A grand 9th century Abbasid building by the Tigris river in Baghdad at night, warm lamplight glowing from arched windows, boats on the river.",0,{}),
(2,"ببيت الحكمة، عالم اسمه الخوارزمي... كتب كتاب اسمه الجبر.","The scholar al-Khwarizmi (grey beard, white turban, scholar robe) writing in a manuscript with geometric diagrams by candlelight in a library.",1,{}),
(2,"ومن هذا الكتاب طلع علم الجبر... اللي تدرسه انت هسه بالمدرسة.","A modern Iraqi school classroom, a tired student at a desk staring at a whiteboard full of algebra symbols, classmates around.",1,{}),
(2,"ومن اسمه طلعت كلمة الخوارزمية... اللي يشتغل بيها موبايلك هسه.","A modern smartphone glowing on an old wooden desk next to an ancient Arabic manuscript with geometric diagrams, light rays connecting them.",0,{}),
(2,"بس بعد أربعمية سنة... جا يوم أسود على بغداد.","Dark storm clouds over medieval Baghdad's domes and minarets, a huge cavalry army appearing on the horizon at dusk, ominous.",0,{}),
(3,"سنة ألف ومئتين وثمانية وخمسين... المغول دخلوا بغداد.","13th century Mongol horsemen with fur hats and bows storming through the gates of medieval Baghdad, smoke and fire.",1,{"sfx":"boom"}),
(3,"حرگوا المدينة... ودمروا بيت الحكمة.","A great medieval library burning, flames climbing the shelves of manuscripts, pages flying in the hot air.",0,{}),
(3,"ويگولون: رموا الكتب بدجلة، لحد ما صار لون الماي أسود من الحبر.","The Tigris river with dark black inky water, hundreds of old books and manuscripts floating, smoke over Baghdad in the background.",0,{"sfx":"heart"}),
(3,"بس العلم اللي طلع منها وصل للعالم كله. تعرف قصة ثانية عن بغداد؟ اكتبها بالتعليقات.","Sunrise over Baghdad and the Tigris, an old scholar holding a saved manuscript to his chest, looking at the horizon with hope.",1,{}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p, "prompt": (G + img + POST) if ch else (img + NOCH)}
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
for p in (1,2,3): print(p, sum(len(x['vo']) for x in out if x['part']==p))
