import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon sandals, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "King Gilgamesh: long curly black beard, golden crown band, muscular, fringed royal robe with gold. Enkidu: wild long brown hair and beard, animal-skin loincloth. ")
POST = " Historically accurate ancient Uruk, Sumer, Mesopotamia, around 2700 BC. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
G2 = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "George Smith: Victorian Englishman, brown beard, dark suit, waistcoat. ")
POST2 = " Historically accurate Victorian London, 1872. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... موظف بمتحف بلندن، يقرأ لوح طين عمره آلاف السنين، وفجأة يقوم يركض بالقاعة ويفصخ هدومه من الفرحة!","George Smith jumping up excitedly in a museum study room full of clay tablets, pulling off his jacket, colleagues shocked.",2,{}),
(1,"شنو لگا باللوح؟ لگا قصة طوفان... أقدم من كل القصص اللي يعرفها.","Close-up of a broken clay tablet covered in cuneiform signs on a wooden desk, lamp light.",0,{}),
(1,"ملحمة جلجامش... أقدم قصة بالتاريخ، من العراق.","",0,{"hud":"title"}),
(1,"منو جلجامش؟ وشنو سر الخلود اللي دوّر عليه؟ وشلون رجعت قصته للدنيا بعد آلاف السنين؟ هاي القصة.","Ancient Sumerian ziggurat and city walls of Uruk at dawn with mist over the Euphrates marshes.",0,{}),
(2,"قبل حوالي أربع آلاف وسبعمية سنة، جانت أكو مدينة اسمها أوروك... قرب السماوة اليوم.","Aerial view of the ancient city of Uruk with massive mud-brick walls, a white temple on a ziggurat, palm groves and canals.",0,{"hud":"day","day":"٢٧٠٠ ق.م"}),
(2,"وملكها جلجامش... قوي، وجميل، ويگولون ثلثينه إله وثلثه إنسان.","King Gilgamesh standing proudly on the city wall of Uruk, wind in his robe, citizens looking up at him.",1,{}),
(2,"بس جان ملك متكبر... يتعب الناس بالشغل، ومحد يگدر يوقفه.","King Gilgamesh ordering exhausted workers carrying heavy mud bricks to build the giant wall of Uruk, workers tired.",1,{}),
(2,"فالناس دعت الآلهة: انطونا واحد بقوته... يوقف بوجهه.","Worried citizens of Uruk praying at night in a temple, raising hands toward the starry sky.",1,{}),
(3,"فالآلهة خلقت إنكيدو... رجل وحشي، يعيش بالبرية ويا الحيوانات.","Enkidu, a wild man, drinking water at a desert spring together with gazelles and wild animals, sunrise.",1,{}),
(3,"وإنكيدو إجه لأوروك... وتلاگى ويا جلجامش، وصارت بينهم معركة.","Gilgamesh and Enkidu wrestling fiercely in the street of Uruk at a doorway, crowd watching in shock.",1,{"sfx":"hit"}),
(3,"تصارعوا وتصارعوا... ومحد غلب.","Gilgamesh and Enkidu both exhausted sitting on the ground after wrestling, dust in the air.",1,{}),
(3,"وبالأخير ضحكوا... وصاروا أعز صديقين بالدنيا.","Gilgamesh and Enkidu laughing and embracing as friends, the people of Uruk cheering.",1,{}),
(4,"وگرروا يسوون مغامرة كبيرة: يروحون لغابة الأرز... بعيد بالشمال.","Gilgamesh and Enkidu walking with axes across mountains toward a vast dark cedar forest.",1,{}),
(4,"وبالغابة جان يحرسها وحش مخيف اسمه خمبابا.","A monstrous giant guardian Humbaba with a terrifying face of coils among giant cedar trees, Gilgamesh and Enkidu small in front of him.",1,{}),
(4,"تقاتلوا وياه... وانتصروا عليه.","Gilgamesh and Enkidu fighting the giant monster Humbaba in the cedar forest, axes raised, dramatic light.",1,{"sfx":"boom"}),
(4,"ورجعوا لأوروك أبطال... ويا خشب الأرز.","Gilgamesh and Enkidu floating a raft of huge cedar logs down the Euphrates toward Uruk, triumphant.",1,{}),
(5,"بس الإلهة عشتار شافت جلجامش... وطلبت يتزوجها.","The goddess Ishtar, beautiful with a star crown and wings, appearing before Gilgamesh in his palace, offering her hand.",1,{}),
(5,"وجلجامش رفضها... وگلها كلام يجرح.","Gilgamesh turning away and refusing Ishtar with crossed arms, Ishtar looking insulted and furious.",1,{}),
(5,"فعصّبت... ودزت عليهم ثور السما يخرب المدينة.","A giant bull of heaven made of storm clouds and fire stampeding into the city of Uruk, people fleeing.",1,{"sfx":"boom"}),
(5,"بس جلجامش وإنكيدو قتلوا الثور... والآلهة غضبت أكثر.","Gilgamesh and Enkidu standing over the defeated giant bull of heaven, dark storm clouds gathering above.",1,{}),
(6,"والآلهة گررت: لازم واحد منهم يموت... إنكيدو.","Enkidu lying sick in bed in a dark room, Gilgamesh kneeling beside him holding his hand, oil lamp.",1,{}),
(6,"إنكيدو مرض... ومات بحضن صديقه.","Gilgamesh crying holding Enkidu, candles around, deep sorrow.",1,{}),
(6,"وجلجامش بچى عليه سبع أيام وسبع ليالي... وما خلاهم يدفنوه.","Gilgamesh sitting alone mourning beside a covered body, seven candles burning down, dark night.",1,{}),
(6,"ولأول مرة... جلجامش خاف من الموت.","Gilgamesh alone on the walls of Uruk at night staring at the stars, frightened and thoughtful.",1,{}),
(7,"وگرر يدوّر على سر الخلود... حتى ما يموت مثل صديقه.","Gilgamesh in torn animal skins leaving Uruk alone toward the desert, long shadow, sunset.",1,{}),
(7,"مشى بالبراري، وعبر جبال، ومشى بطريق الشمس بالظلام.","Gilgamesh walking through a pitch dark mountain tunnel with only a faint light at the end.",1,{}),
(7,"لحد ما وصل لصاحبة حانة على البحر اسمها سيدوري... گالتله: ارجع واستانس بحياتك.","Gilgamesh meeting a kind tavern keeper woman by a glowing seaside tavern at the edge of the world.",1,{}),
(7,"بس ما سمع... وعبر بحر الموت بالقارب.","Gilgamesh on a small boat crossing a misty dark sea of death with a ferryman, eerie glow.",1,{}),
(8,"ووصل لرجل اسمه أوتنابشتم... الإنسان الوحيد اللي الآلهة انطته الخلود.","Gilgamesh meeting an ancient white-bearded man Utnapishtim on a peaceful paradise island.",1,{}),
(8,"وأوتنابشتم حچاله قصة غريبة... قصة الطوفان.","Utnapishtim telling a story to Gilgamesh by a fire, gesturing dramatically.",1,{}),
(8,"الآلهة گررت تغرق الأرض كلها... فأمروه يبني سفينة كبيرة.","Utnapishtim and workers building a gigantic wooden ark in ancient Mesopotamia, dark clouds gathering.",1,{}),
(8,"وحط بيها عائلته، والحيوانات... وإجه المطر سبع أيام.","A huge ark floating on endless floodwater in heavy rain, animals on deck, lightning.",0,{"sfx":"boom"}),
(9,"ولما وقف المطر، دز طير يشوف إذا الأرض نشفت.","A dove flying from the ark over calm floodwater at sunrise, mountain peaks appearing.",0,{}),
(9,"قصة تشبه هواية قصة نوح... بس مكتوبة قبلها بأكثر من ألف سنة.","Close-up of a clay tablet with cuneiform beside an old open book, soft light, scholarly mood.",0,{}),
(9,"وأوتنابشتم گال لجلجامش: الخلود مو إلك... بس أكو نبتة بقاع البحر ترجعك شباب.","Utnapishtim pointing toward the sea, telling Gilgamesh about a magical plant on the seabed.",1,{}),
(9,"فجلجامش ربط حجار برجليه... ونزل لقاع البحر وجاب النبتة!","Gilgamesh underwater with stones tied to his feet reaching for a glowing thorny plant on the seabed.",1,{}),
(10,"وبطريق الرجعة... وقف يسبح بعين ماي.","Gilgamesh bathing in a desert spring, the glowing plant left on the shore beside his clothes.",1,{}),
(10,"وإجت حية... وأكلت النبتة!","A snake slithering away with the glowing plant in its mouth, shedding its old skin, Gilgamesh shocked in the water.",1,{"sfx":"hit"}),
(10,"وجلجامش گعد يبچي... كل التعب راح.","Gilgamesh sitting on the ground crying in the desert, empty hands, sunset.",1,{}),
(10,"ورجع لأوروك... وشاف سورها العالي، وفهم: الخلود مو بالجسم... الخلود باللي تتركه وراك.","Gilgamesh standing on the great walls of Uruk at sunrise, looking at the city full of life, peaceful.",1,{}),
(11,"والقصة انكتبت على ألواح طين... وانحفظت بمكتبة الملك آشوربانيبال بنينوى.","The library of Ashurbanipal in Nineveh with scribes and shelves full of clay tablets, Assyrian decor.",1,{}),
(11,"بس نينوى احترگت... والألواح اندفنت تحت التراب ألفين وخمسمية سنة.","Burning palace of ancient Nineveh at night, clay tablets falling, flames.",0,{"sfx":"boom"}),
(11,"وبالقرن التاسع عشر، الإنگليز حفروا بالموصل... وطلعوا آلاف الألواح ودزوها للندن.","Victorian archaeologists and local workers digging up clay tablets at the mound of Nineveh near Mosul, 1850s.",3,{}),
(11,"وهناك جورج سميث، موظف بسيط علّم نفسه المسمارية... قرا اللوح، ودار العالم كله يحچي عن جلجامش.","George Smith reading a clay tablet with a magnifying glass at a desk in the British Museum, piles of tablets around.",2,{"hud":"day","day":"١٨٧٢م"}),
(12,"اليوم ملحمة جلجامش مترجمة لعشرات اللغات... ويدرسوها بكل جامعات العالم.","Students in a modern university library reading a book about ancient Mesopotamia, a cuneiform tablet poster on the wall.",3,{}),
(12,"وبسنة ألفين وواحد وعشرين... رجعت لوحة من الملحمة للعراق بعد ما انسرقت.","Iraqi officials and museum staff unveiling a returned small cuneiform tablet in a glass case at the Iraq Museum in Baghdad, cameras flashing.",3,{}),
(12,"أوروك اليوم أطلال بالصحرا... بس قصتها بعدها عايشة.","Aerial view of the ruins of Uruk at Warka in the Iraqi desert at sunset.",0,{}),
(12,"أقدم قصة بالدنيا عن الصداقة والموت والخلود... من العراق. انت لو تلگى نبتة الخلود، تاكلها؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img: d["prompt"] = (G + img + POST) if ch == 1 else (G2 + img + POST2) if ch == 2 else (G2.split("George Smith")[0] + img + " Cinematic lighting. Wide shot, 16:9, no readable text, no logos.") if ch == 3 else (img + NOCH)
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
