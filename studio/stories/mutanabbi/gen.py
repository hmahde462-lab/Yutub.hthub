import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "Haj Mohammed (old Baghdadi cafe owner, 70s): short white beard, round glasses, grey Iraqi sidara cap, dark suit jacket over a white dishdasha. "
 "Al-Mutanabbi (10th-century Arab poet, in historical scenes only): black beard, white turban, flowing Abbasid robe and sword. ")
POST = " Real Baghdad, Iraq, historically accurate for the era shown. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, real Baghdad Iraq, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... شارع كله كتب. وبيوم جمعة، الصبح... انفجار يحرگه كله.","A narrow old Baghdad street lined with bookshops and stacks of books, thick black smoke rising and burning pages flying in the air.",0,{"sfx":"boom"}),
(1,"وبنص الشارع، گهوة عمرها تسعين سنة... صاحبها خسر بهذا اليوم أربع أولاد وحفيد.","Haj Mohammed sitting alone at a wooden table in an old Baghdad cafe full of old photographs on the walls, grief, dim light.",1,{"sfx":"heart"}),
(1,"قصة شارع المتنبي... الشارع اللي ما مات.","",0,{"hud":"title"}),
(1,"شلون صار هذا الشارع قلب بغداد؟ وليش سموه على شاعر انقتل بسبب بيت شعر؟ وشلون رجع بعد ما احترق؟ هاي قصة حقيقية.","Old books, a brass tea glass and a faded photo of a Baghdad street on a wooden table, warm light.",0,{}),
(2,"نرجع ألف سنة لورا... لشاعر اسمه أبو الطيب المتنبي. أشهر شاعر بتاريخ العرب.","Al-Mutanabbi standing proudly on a sand dune at sunset, robe flowing, horse behind him.",1,{}),
(2,"جان يمدح الملوك ويهجيهم... وكلامه يمشي بين الناس مثل النار.","Al-Mutanabbi reciting poetry in front of a seated Abbasid-era ruler in a palace hall, courtiers listening.",1,{}),
(2,"وهو اللي گال: الخيلُ والليلُ والبيداءُ تعرفني... والسيفُ والرمحُ والقرطاسُ والقلمُ.","Al-Mutanabbi riding a horse at night across the desert under a full moon, sword at his side.",1,{}),
(2,"وبسنة تسعمية وخمسة وستين، طلعوا عليه جماعة بالطريق قريب من بغداد... وانقتل.","Al-Mutanabbi and a few companions surrounded by armed riders on a desert road at dusk, tension.",1,{"sfx":"hit"}),
(3,"ويگولون: جان راح يهرب... بس خادمه ذكّره ببيته: الخيل والليل تعرفني. فرجع يقاتل... وانقتل بسبب بيت شعر.","Al-Mutanabbi turning his horse back toward the attackers, his servant pointing at him, dramatic dusk light.",1,{}),
(3,"ومن ذاك الوقت، ببغداد العباسية، جان أكو سوق اسمه سوق الوراقين... الناس يبيعون وينسخون بيه الكتب.","Abbasid-era Baghdad market of manuscript copyists sitting with paper scrolls and ink, busy alley, warm lantern light.",1,{}),
(3,"بغداد ذاك الوقت كانت عاصمة العلم بالعالم... والكتاب جان أغلى من الذهب.","Bustling medieval Baghdad by the Tigris river with domes, minarets and boats, golden hour.",0,{}),
(3,"ومرت مية سنة ورا مية سنة... والسوق بقى سوق كتب.","Time-lapse style view of an old Baghdad book alley changing through centuries, ottoman arches and lamps.",0,{}),
(4,"وبسنة ألف وتسعمية واثنين وثلاثين، الملك فيصل الأول سمّى الشارع على اسم المتنبي.","1930s Baghdad street with a royal convoy of old cars, a crowd watching a new street sign being put up, sepia tones.",1,{}),
(4,"وصار الشارع مكان المثقفين: شعراء، وكتّاب، وطلاب، وسياسيين... كلهم يتلاگون هنا.","A crowd of 1950s Baghdadi intellectuals in suits and sidara caps browsing books on a busy street.",1,{}),
(4,"وجان أكو مثل مشهور يگول: القاهرة تكتب، وبيروت تطبع... وبغداد تقرأ.","A young Baghdadi man reading a book while walking, surrounded by piles of books, sunlight.",1,{}),
(4,"وبآخر الشارع... القشلة، بنايتها العثمانية وساعتها العالية، وجنبها نهر دجلة.","The old Ottoman Qishla building with its tall clock tower at the end of a Baghdad street, Tigris river beside it.",0,{}),
(5,"وبنص الشارع گهوة الشابندر... انفتحت سنة ألف وتسعمية وسبعطعش.","The front of an old Baghdad cafe with wooden benches, hookahs and walls covered in old black and white photographs.",0,{}),
(5,"صاحبها الحاج محمد الخشالي... گهوته جانت بيت ثاني للمثقفين.","Haj Mohammed pouring tea for customers in his crowded old cafe, smiling, steam rising.",1,{}),
(5,"استكان چاي، ونرگيلة، وحچي عن الشعر والسياسة... وعلى الحايط صور بغداد القديمة.","Close-up of tea glasses, a backgammon board and old photographs on a cafe wall, men laughing.",1,{}),
(5,"والحاج جان يگول: هاي الگهوة مو إلي... هاي لكل بغداد.","Haj Mohammed standing proudly at the cafe entrance, arms open, welcoming people.",1,{}),
(6,"بالتسعينات جا الحصار... والعراقيين صاروا جوعانين.","A 1990s Baghdad family sitting at a nearly empty dinner table, worried faces, dim light.",1,{}),
(6,"وصار الأستاذ والدكتور يجيب مكتبته للشارع... يبيع كتبه حتى يطعم أطفاله.","An old professor with glasses sadly laying his books on the pavement of the book street to sell them.",1,{}),
(6,"ومن هنا بدا سوق الجمعة... كل جمعة، الكتب على الگاع، والناس بالآلاف.","A huge Friday crowd walking through a Baghdad street with books laid out on the ground on both sides.",1,{"hud":"day","day":"كل جمعة"}),
(6,"وصار الشارع مكان الكتب الممنوعة كمان... تنباع بالسر، تحت الطاولة.","A bookseller secretly handing a wrapped book under a table to a young man, looking around nervously.",1,{}),
(7,"وبعد ألفين وثلاثة... العراق دخل بالحرب، والتفجيرات صارت كل يوم.","A Baghdad street with concrete blast walls and checkpoints, smoke in the distance, mid-2000s.",0,{}),
(7,"بس شارع المتنبي بقى مفتوح... الكتب ما وگفت.","Booksellers still arranging books on a street near blast walls, a few customers browsing bravely.",1,{}),
(7,"لحد يوم خمسة آذار، ألفين وسبعة... الصبح، والشارع مزدحم.","The busy book street in the morning, people browsing, a parked old car among them, ominous calm.",1,{"hud":"day","day":"٥ آذار ٢٠٠٧"}),
(7,"سيارة مفخخة... انفجرت بنص الشارع.","Huge explosion fireball in a narrow street, pages and debris flying, everything blurred by the shockwave.",0,{"sfx":"boom"}),
(8,"عشرات الناس راحوا... بين قتيل وجريح.","The burned street after the explosion, smoke, scattered burned books on the ground, no people visible.",0,{}),
(8,"والنار أكلت المكتبات... والكتب صارت تطير بالهوا وهي محروگة.","Burned pages floating in the air above a destroyed bookshop, flames and smoke.",0,{}),
(8,"والحاج محمد... خسر أربع من أولاده وحفيده. كلهم جانوا بالگهوة ويا.","Haj Mohammed sitting in the ruins of his cafe, holding a framed photo of his sons, devastated.",1,{}),
(8,"وگهوة الشابندر... انهدمت.","The destroyed cafe with broken walls and fallen old photographs, dust in the light.",0,{"sfx":"heart"}),
(9,"الكل گال: خلص... شارع المتنبي مات.","A wide view of the ruined empty book street with burned buildings, grey sky, silence.",0,{}),
(9,"بس بعد أيام... صار شي محد توقعه.","A single bookseller walking back into the ruined street carrying a box of books, morning light.",1,{}),
(9,"أصحاب المكتبات رجعوا... فرشوا الكتب على الرماد، وگعدوا يبيعون.","Booksellers laying books on the ground among ruins, determined faces, customers arriving.",1,{}),
(9,"وكتّاب وشعراء إجوا... يقرون شعر بنص الخراب.","A poet reciting to a small crowd standing among ruined buildings in the book street.",1,{}),
(10,"والحاج محمد... رجّع فتح الگهوة. وعلّگ صور أولاده على الحايط، ويا صور بغداد.","Haj Mohammed hanging framed photographs of his sons on the wall of his rebuilt cafe, tearful but strong.",1,{}),
(10,"وگال: إذا سدّيت الگهوة... يعني هم انتصروا.","Close-up of Haj Mohammed sitting in his cafe with a tea glass, determined look, photos behind him.",1,{}),
(10,"وبعيد عن بغداد، بأمريكا، شاعر سمع بالقصة... وبدا مشروع اسمه: شارع المتنبي يبدأ من هنا.","An American poet in a small bookshop in San Francisco reading news about Baghdad, books around him.",1,{}),
(10,"فنانين وكتّاب من كل العالم سووا كتب وقصايد... تضامن ويا الشارع.","Artists from different countries making handmade books and posters in a workshop, solidarity.",1,{}),
(11,"وبنهاية ألفين وثمانية... رجعوا افتتحوا الشارع بعد ما تعمّر.","The rebuilt book street with restored facades, crowds returning, celebration, evening lights.",1,{}),
(11,"وبآخره، تمثال المتنبي واگف... يباوع على دجلة.","The bronze statue of the poet al-Mutanabbi in robes with raised hand at the end of the street near the Tigris river.",0,{}),
(11,"ورجع سوق الجمعة... أكبر من قبل.","A huge joyful Friday crowd in the restored book street, families, students, books everywhere.",1,{}),
(11,"والشباب صاروا يجون يقرون، ويرسمون، ويعزفون... بنفس المكان اللي احترق.","Young Iraqis reading, painting and playing oud in the courtyard of the Qishla building near the street.",1,{}),
(12,"وبكل جمعة، الحاج محمد گاعد بگهوته... يصب چاي، ويحچي للزباين عن أولاده.","Haj Mohammed pouring tea for young customers in his cafe, pointing at the photos of his sons on the wall.",1,{}),
(12,"والكتب اللي احترقت... انطبعت من جديد.","Freshly printed books stacked on a table in a bookshop, a hand picking one up.",1,{}),
(12,"وشارع المتنبي لليوم... أكبر سوق كتب بالعراق.","Aerial view of the crowded book street at golden hour with the Qishla clock tower and the Tigris.",0,{}),
(12,"گدروا يحرگون الكتب... بس ما گدروا يحرگون القرّاي. انت آخر مرة رحت للمتنبي شوكت؟","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img: d["prompt"] = (G + img + POST) if ch else (img + NOCH)
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
