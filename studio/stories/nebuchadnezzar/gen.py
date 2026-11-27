import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon sandals, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "King Nebuchadnezzar: long curly black Babylonian beard, tall rounded royal cap with gold band, long blue and gold embroidered robe. ")
A = "Queen Amytis: long black hair, gold jewelry, embroidered green Median dress. "
POST = " Historically accurate Neo-Babylonian Babylon, around 580 BC. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... ملكة جاية من بلاد الجبال الخضرة، تعيش وسط صحراء مستوية. تشتاق لأهلها، وتحزن. فزوجها الملك يگرر... يبنيلها جبل!","A sad queen standing on a palace balcony looking over a flat desert city, dreaming of green mountains in the distance.",2,{}),
(1,"جبل من الحدائق والأشجار، معلّق بالسما، بنص الصحرا. وصارت وحدة من عجائب الدنيا السبع.","Legendary Hanging Gardens of Babylon, terraced green gardens with waterfalls rising above a desert city, golden light.",0,{}),
(1,"نبوخذ نصر... والجنائن المعلقة.","",0,{"hud":"title"}),
(1,"منو نبوخذ نصر؟ وشلون صارت بابل أعظم مدينة بالعالم؟ وليش لهسه محد متأكد إذا الجنائن جانت موجودة أصلاً؟ هاي قصة حقيقية.","Ruins of ancient Babylon with partially reconstructed brick walls near Hillah at sunset.",0,{}),
(2,"قبل حوالي ألفين وستمية سنة، جانت بابل تحت حكم الآشوريين... لحد ما ثار عليهم واحد اسمه نبوبولاصر.","Babylonian rebels fighting Assyrian soldiers at the gates of a mud-brick city, dust and banners.",1,{"hud":"day","day":"٦٢٦ ق.م"}),
(2,"وابنه الشاب، نبوخذ نصر، تعلم الحرب من صغره ويا أبوه.","A young Babylonian prince with a short black beard training with a bow on a chariot, his father the king watching.",1,{}),
(2,"وبسنة ستمية وخمسة قبل الميلاد، قاد جيش بابل ضد مصر بمعركة كركميش... وانتصر انتصار كبير.","A great ancient battle at Carchemish by the Euphrates, Babylonian chariots charging against Egyptian soldiers.",1,{"sfx":"boom"}),
(2,"وبنفس السنة، وصله خبر: أبوه مات. فرجع لبابل... وصار ملك.","King Nebuchadnezzar being crowned in a great temple hall in Babylon, priests and nobles bowing.",1,{}),
(3,"وحكم ثلاث وأربعين سنة... وگرر يسوي بابل أعظم مدينة بالدنيا.","King Nebuchadnezzar on a palace terrace pointing over Babylon while architects show him plans on clay tablets.",1,{}),
(3,"بنى أسوار ضخمة... ويگول المؤرخ اليوناني هيرودوت إن عرضها جان يكفي عربة تجرها أربع خيول تدور فوگها!","Massive double city walls of Babylon with towers, a four-horse chariot riding on top of the wall.",0,{}),
(3,"وبنى بوابة عشتار... بوابة زرقاء من الطابوق المزجج، عليها صور تنانين وثيران.","The magnificent blue glazed-brick Ishtar Gate of Babylon decorated with golden dragons and bulls, people walking through.",1,{}),
(3,"ومنها يبدي شارع الموكب، طوله أكثر من كيلومتر، وعلى حيطانه أسود ذهبية.","The Processional Way of Babylon with blue glazed walls decorated with golden lions, a festive procession walking.",1,{}),
(4,"وبنص المدينة، زقورة عالية اسمها إيتيمينانكي... يعني بيت أساس السما والأرض.","The giant stepped ziggurat Etemenanki in the center of Babylon with a temple on top, clouds around it.",0,{}),
(4,"وكثير من المؤرخين يعتقدون... إن هاي الزقورة هي أصل قصة برج بابل.","A dramatic view looking up at a towering ancient ziggurat piercing the clouds, tiny people at its base.",0,{}),
(4,"وكل طابوقة بالمدينة، جان مختوم عليها اسمه: نبوخذ نصر، ملك بابل.","Close-up of an ancient fired mud brick stamped with cuneiform writing, workers' hands stacking bricks.",0,{}),
(4,"ملايين الطابوق، وكلها تحمل اسمه... ولهسه تلگاها بالمتاحف.","A museum display of ancient Babylonian stamped bricks in glass cases, soft light.",0,{}),
(5,"بس نبوخذ نصر جان عنده زوجة اسمها أميتس... بنت ملك ميديا، بلاد الجبال اللي بإيران اليوم.","King Nebuchadnezzar and Queen Amytis at their wedding in a Babylonian palace, guests celebrating.",3,{}),
(5,"والملكة جانت تشتاق لجبالها الخضرة، وأشجارها، ومايها... وبابل أرض مستوية وحارة.","Queen Amytis sitting sadly in a palace courtyard, looking at a small potted plant, hot desert sun.",2,{}),
(5,"فيگولون الملك گرر يبنيلها جبل صناعي... من طوابق، فوگ بعض، مليانة أشجار وورد.","King Nebuchadnezzar showing Queen Amytis a model of terraced gardens, she smiles happily.",3,{}),
(5,"وهيج انولدت أسطورة الجنائن المعلقة.","Workers building huge stone terraces with soil and planting trees, a half-built green structure rising.",1,{}),
(6,"يوصفوها: طوابق حجر عالية، فوگها تراب، وأشجار كبيرة، وكأنها معلّقة بالهوا.","The Hanging Gardens with terraces full of palm trees, flowers and vines hanging over stone arches.",0,{}),
(6,"بس المشكلة الكبيرة: شلون يوصلون الماي لفوگ؟ بدون مكائن، وبدون كهرباء؟","Close-up of terraces of the gardens with water trickling down channels, plants, sunlight.",0,{}),
(6,"يعتقدون استخدموا آلات تدور بالحيوانات أو بالعبيد... ترفع الماي من الفرات.","Workers turning a large wooden wheel with buckets lifting water from the Euphrates up to the gardens.",1,{}),
(6,"وبعضهم يگولون استخدموا لولب أرخميدس... قبل أرخميدس نفسه بمئات السنين!","An ancient screw pump made of wood turned by workers, lifting water up a slope, detailed mechanism.",1,{}),
(7,"وبنفس الوقت... نبوخذ نصر جان قائد حروب قاسي.","King Nebuchadnezzar in armor on a war chariot leading a vast Babylonian army.",1,{}),
(7,"حاصر مدينة صور بلبنان ثلطعش سنة كاملة!","An ancient island city of Tyre with walls surrounded by the sea, Babylonian army camped on the shore for years.",1,{}),
(7,"وهجم على أورشليم، القدس، وأخذ ملكها أسير.","The Babylonian army besieging the walled city of Jerusalem on hills, siege ramps.",1,{"sfx":"boom"}),
(7,"وبالمرة الثانية، سنة خمسمية وسبعة وثمانين قبل الميلاد... دمّر المدينة والمعبد، وأخذ آلاف الناس أسرى لبابل.","Long lines of captives walking from a burning distant city toward Babylon, soldiers guarding them.",1,{}),
(8,"وهذا اللي يسموه السبي البابلي... وانذكر بالتوراة وبكتب كثيرة.","Captives sitting sadly by the rivers of Babylon under willow trees, harps hanging on branches.",1,{}),
(8,"وبسفر دانيال، أكو قصة غريبة: إن نبوخذ نصر انجن سبع سنين... وصار ياكل حشيش مثل الحيوانات!","King Nebuchadnezzar with wild long hair crawling in a field eating grass, dramatic biblical scene, comic sadness.",1,{}),
(8,"المؤرخين ما عدهم دليل على هاي القصة... بس هي من أشهر الحكايات عنه.","An ancient scroll and a clay tablet side by side on a table, candle light, scholarly mood.",0,{}),
(8,"ومات نبوخذ نصر بسنة خمسمية واثنين وستين قبل الميلاد... وبابل بعدها بأقل من خمس وعشرين سنة، سقطت بإيد الفرس.","Persian army of Cyrus entering Babylon through the gates at night, Babylonians watching quietly.",0,{"hud":"day","day":"٥٣٩ ق.م"}),
(9,"وهنا اللغز الكبير... الجنائن المعلقة، وين راحت؟","An empty ancient courtyard in Babylon ruins with wind and dust, mysterious mood.",0,{}),
(9,"الغريب إن بابل عدها آلاف الألواح المكتوبة... وولا لوح واحد يذكر الجنائن!","Archaeologist's table full of cuneiform clay tablets, a magnifying glass, no mention found, puzzled mood.",0,{}),
(9,"حتى المؤرخ هيرودوت، اللي وصف بابل بالتفصيل... ما ذكرها.","An ancient Greek historian in a white robe writing on a scroll while looking at Babylon's walls in the distance.",4,{}),
(9,"وأول من كتب عنها جانوا مؤرخين جاو بعد مئات السنين.","Old parchment scrolls and ancient Greek books stacked in a library, dust and light rays.",0,{}),
(10,"وباحثة بريطانية اسمها ستيفاني دالي، طلعت بنظرية جريئة: الجنائن ما جانت ببابل أصلاً... جانت بنينوى، بالموصل!","A modern British woman researcher with grey hair studying Assyrian reliefs in a museum, excited.",5,{}),
(10,"وبناها ملك آشوري اسمه سنحاريب، قبل نبوخذ نصر بمية سنة.","An Assyrian king with a long square beard and tall crown overseeing gardens and aqueducts in Nineveh.",4,{}),
(10,"وعلى جدران قصره، لگوا نقوش تبين حدائق على طوابق، وقنوات ماي... تشبه وصف الجنائن بالضبط!","Ancient Assyrian stone relief showing terraced gardens with trees and water channels, carved stone.",0,{}),
(10,"يعني يمكن أعظم عجيبة بالعالم... بالعراق، بس مو بالمكان اللي نتوقعه.","Aerial view of Mosul and the ruins of ancient Nineveh by the Tigris river at golden hour.",0,{}),
(11,"وبابل اندفنت تحت التراب... لحد ما إجه عالم ألماني اسمه روبرت كولديفاي سنة ألف وثمنمية وتسعة وتسعين.","German archaeologists in early 1900s clothes with local Iraqi workers excavating glazed bricks at Babylon.",5,{"hud":"day","day":"١٨٩٩م"}),
(11,"حفر سنين، ولگا بوابة عشتار... وأخذوا قطعها لألمانيا.","Workers packing broken blue glazed bricks into wooden crates for shipping, early 1900s.",5,{}),
(11,"واليوم بوابة عشتار مبنية من جديد... بمتحف بيرغامون ببرلين.","The reconstructed blue Ishtar Gate inside the Pergamon Museum in Berlin, tourists walking in front of it.",5,{}),
(11,"وبالثمانينات، صدام حسين رجع بنى قسم من بابل... وختم الطابوق الجديد باسمه، مثل نبوخذ نصر بالضبط!","Reconstructed walls of Babylon built in the 1980s with modern yellow bricks, a palace on a hill in the background.",0,{}),
(12,"اليوم بابل موجودة بقائمة التراث العالمي... وتگدر تزورها قرب الحلة.","Modern visitors walking among the ruins of Babylon near the Ishtar Gate replica, sunny day.",5,{}),
(12,"والجنائن المعلقة... بقت لغز. يمكن ببابل، يمكن بنينوى، ويمكن مجرد حلم.","Dreamy misty image of green terraced gardens fading into the sky above an ancient city.",0,{}),
(12,"بس أكيد شي واحد: هالأرض، بيوم من الأيام، جانت قلب العالم.","Golden sunset over the Euphrates river with palm trees and ancient ruins on the bank.",0,{}),
(12,"انت تعتقد الجنائن المعلقة جانت ببابل لو بنينوى؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
G0 = G.split("King Nebuchadnezzar")[0]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img:
        if ch == 1: d["prompt"] = G + img + POST
        elif ch == 2: d["prompt"] = G0 + A + img + POST
        elif ch == 3: d["prompt"] = G + A + img + POST
        elif ch == 4: d["prompt"] = G0 + img + " Historically accurate ancient Mesopotamia. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
        elif ch == 5: d["prompt"] = G0.replace("chunky cartoon sandals","chunky cartoon shoes") + img + " Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
        else: d["prompt"] = img + NOCH
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
