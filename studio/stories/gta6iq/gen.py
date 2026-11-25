import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "The hero: messy curly dark-brown hair, thin mustache, small chin beard, grey t-shirt, dark blue jeans. ")
POST = " Background: photorealistic Baghdad, Iraq. Cinematic lighting. Wide shot, 16:9, no text, no logos, no game interface."
S = [
(1,"لو لعبة جي تي أي ستة... انسوت بالعراق.","The hero sitting on a floor cushion in an Iraqi living room holding a game controller, excited, in front of a TV showing a sunny open-world video game of Baghdad streets with palm trees.",{"sfx":"boom"}),
(1,"أول مهمة: روح جيب قنينة غاز... والطابور ساعتين.","The hero standing at the end of a very long queue of people holding blue gas cylinders in a hot Baghdad street, bored face.",{}),
(1,"تسرق سيارة... تطلع عاطلة، وتدفعها انت.","The hero pushing an old broken white car by hand down a Baghdad street in the heat, sweating, smoke from the hood.",{"sfx":"hit"}),
(1,"المطاردة؟ بزحمة الكرادة... الشرطي والحرامي واگفين سوا.","A huge Baghdad traffic jam, the hero in an old car stuck right next to a police car, the policeman and the hero both bored looking at each other.",{}),
(1,"وبدل النجوم... سيطرة: هويتك وياك؟","An Iraqi checkpoint with concrete barriers, a soldier leaning to the car window asking the hero for his ID card, the hero searching his pockets nervously.",{}),
(1,"وأخيراً توصل آخر مهمة... وما حافظ اللعبة.","The hero leaning toward the TV with wide excited eyes gripping the controller at night in his living room, the game glowing on screen.",{}),
(1,"وطفت الكهرباء.","A completely dark Iraqi living room, the TV off, only the hero's round white face with wide shocked eyes and open mouth visible.",{"sfx":"hit"}),
(1,"منو جرّب يلعب بهالظروف؟ اكتبها بالتعليقات.","The hero lying on the floor in the dark living room holding a candle and the controller, laughing at himself.",{}),
]
out = []
for p, vo, img, ex in S:
    d = {"vo": vo, "img": img, "part": p, "prompt": G + img + POST}
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
