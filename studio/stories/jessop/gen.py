import json
PRE = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "The main character (Violet, a young Irish-Argentine woman in her twenties): dark brown hair in a neat bun on top of the white round head, ")
STEW = "wearing a long black stewardess dress with a white apron and a small white cap. "
NURSE = "wearing a white nurse uniform with a red cross on the apron and a white nurse headscarf. "
POST = " Historically accurate early 1900s, no modern objects. Cinematic lighting. Wide shot, 16:9, no text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate early 1900s, 16:9, no text, no logos, no people."
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. ")
# (part, vo, img, kind[0 none,1 stew,2 nurse,3 child/other generic], extra)
S = [
(1,"تخيّل... تنجو من غرق سفينة. وبعدين من سفينة ثانية. وبعدين من ثالثة.","Three giant early 1900s ocean liners side by side on a dark sea, one tilting and sinking, dramatic stormy sky.",0,{}),
(1,"وكل مرة... ترجع للبحر.","Violet standing alone on a ship deck at dusk looking out at the endless ocean, wind in her apron.",1,{"sfx":"heart"}),
(1,"قصة فيوليت جيسوب... البنت اللي ما تغرق.","",0,{"hud":"title"}),
(1,"هاي مو أسطورة بحرية... هاي قصة حقيقية، وصارت بين سنة ألف وتسعمية وإحدعش، وألف وتسعمية وستعش.","Old black-and-white photographs of ocean liners and a stewardess pinned on a wooden board with newspaper clippings, warm lamp light.",0,{}),
(2,"فيوليت انولدت بالأرجنتين، سنة ألف وثمنمية وسبعة وثمانين، لعائلة إيرلندية مهاجرة.","A little girl (young Violet, about 5, dark hair) playing in front of a small house in 1890s Argentina countryside with her Irish family.",3,{}),
(2,"وبطفولتها مرضت مرض خطير بالصدر... والأطباء گالوا لأهلها: ما راح تعيش طويل.","Little Violet lying sick in bed, a doctor with a bag talking to her worried mother by the bedside, dim 1890s room.",3,{}),
(2,"بس فيوليت عاشت... وكأن هاي أول مرة تتحدى الموت.","Little Violet smiling and stepping outside into sunshine, holding her mother's hand.",3,{}),
(2,"ولما توفى أبوها، انتقلت ويا أمها وأخوتها لبريطانيا... وأمها اشتغلت مضيفة بالسفن حتى تعيّش العائلة.","Violet's mother in a stewardess uniform hugging her children goodbye at a busy British harbour with big steamships.",3,{}),
(3,"وبعمر واحد وعشرين سنة، صارت فيوليت هي هم مضيفة بالسفن.","Violet proudly putting on her stewardess cap in front of a small mirror in a tiny ship cabin.",1,{}),
(3,"شغل صعب: سبعطعش ساعة باليوم، تنظف الغرف، وتخدم الركاب، وراتب قليل.","Violet carrying towels and a tray down a narrow ship corridor, tired, other stewardesses around her.",1,{}),
(3,"وبسنة ألف وتسعمية وإحدعش، اشتغلت على أكبر سفينة ركاب بالعالم وقتها... اسمها الأولمبيك.","Violet looking up in awe at the huge RMS Olympic liner with four funnels docked at Southampton, crowds on the pier.",1,{}),
(3,"سفينة فخمة، بيها مطاعم وقاعات... وكلهم يگولون عنها: هاي ما تغرق.","Violet serving tea in a luxurious Edwardian first-class dining saloon on the Olympic, chandeliers, rich passengers.",1,{}),
(4,"بأيلول، ألف وتسعمية وإحدعش... الأولمبيك طالعة من الميناء، وجنبها سفينة حربية بريطانية.","The Olympic liner leaving harbour with a grey British warship (HMS Hawke) sailing close alongside, calm sea.",0,{}),
(4,"وفجأة... السفينة الحربية انسحبت باتجاهها.","The warship swerving toward the side of the Olympic liner, sailors on deck shouting.",0,{}),
(4,"وصدمتها من الجنب... وفتحت بيها فتحة كبيرة.","Close view of a warship bow smashing into the side of an ocean liner, metal tearing, water spraying.",0,{"sfx":"boom"}),
(4,"الماي دخل... بس السفينة ما غرقت، ورجعت للميناء، ومحد مات. وفيوليت طلعت سالمة.","Violet holding the railing as the damaged Olympic limps back to port, a large hole visible in its side, relieved passengers.",1,{}),
(5,"بعدها بسبع أشهر... طلبوا منها تشتغل على السفينة الأخت للأولمبيك. سفينة جديدة، أكبر وأفخم.","Violet at the Southampton dock looking up at a brand new giant liner with four funnels, April 1912, crowds waving.",1,{}),
(5,"اسمها... تايتانك.","The Titanic at the dock, majestic, low angle, morning light, flags.",0,{"sfx":"hit"}),
(5,"بعشرة نيسان، ألف وتسعمية وإثنعش، طلعت التايتانك برحلتها الأولى... وفيوليت عمرها أربعة وعشرين سنة.","Violet waving from the deck of the Titanic as it departs, passengers waving handkerchiefs, tugboats below.",1,{}),
(5,"وبالليلة الرابعة، بعد ما خلصت شغلها... نامت بغرفتها.","Violet asleep in a small bunk in a narrow crew cabin, a little lamp, night.",1,{}),
(6,"قبل نص الليل بشوية... حسّت بصدمة خفيفة، وصوت غريب.","Violet waking up in her bunk, startled, listening, the cabin lamp swinging slightly.",1,{}),
(6,"التايتانك ضربت جبل جليد.","A huge iceberg scraping along the dark side of the Titanic at night, stars, calm black sea.",0,{"sfx":"boom"}),
(6,"طلعت للسطح، وطلبوا منها تمشي قدام الركاب بهدوء... حتى يشوفون شلون يلبسون سترات النجاة ويطلعون.","Violet on the cold deck at night calmly showing worried passengers how to put on life jackets.",1,{}),
(6,"وبعدين... أمروها تصعد بقارب النجاة رقم ستعش.","An officer helping Violet into a wooden lifeboat hanging on davits at night, passengers in coats.",1,{}),
(7,"وقبل ما ينزل القارب... واحد من الضباط حط بحضنها طفل صغير، وگلها: ديري بالج عليه.","An officer handing a small bundled baby to Violet sitting in the lifeboat, night, lights of the ship above.",1,{}),
(7,"نزل القارب للماي البارد... وهي ضامّة الطفل.","The lifeboat being lowered down the huge side of the Titanic toward the black water, Violet hugging the baby.",1,{}),
(7,"ومن بعيد... شافت التايتانك تنكسر، وتغرق.","Violet in the lifeboat watching in horror as the Titanic breaks and sinks in the distance, lights going out.",1,{}),
(7,"وأصوات الناس بالماي... ظلت بذاكرتها طول عمرها.","The dark freezing ocean at night with floating debris and distant lights, small lifeboats, sorrowful.",0,{}),
(8,"بقوا بالبرد ساعات... لحد ما إجت سفينة اسمها كارباثيا وأنقذتهم.","Dawn on the icy sea, the rescue ship Carpathia approaching lifeboats among ice floes.",0,{}),
(8,"وعلى سطح كارباثيا... وحدة ست ركضت عليها، وأخذت الطفل من إيدها، وراحت... بدون ولا كلمة.","On the deck of the Carpathia, a crying woman snatching the baby from Violet's arms, Violet surprised, blankets around survivors.",1,{}),
(8,"أكثر من ألف وخمسمية شخص ماتوا بالتايتانك.","A large ocean memorial with many candles and flowers at a harbour at dusk, sad atmosphere.",0,{}),
(8,"وفيوليت... نجت للمرة الثانية.","Violet wrapped in a blanket on the Carpathia deck holding a cup of tea, staring at the sea.",1,{}),
(9,"وبسنة ألف وتسعمية وأربعطعش... بدت الحرب العالمية الأولى.","Soldiers marching to a harbour with big ships, Union flags, WWI 1914 Britain.",3,{}),
(9,"وفيوليت ما گعدت بالبيت... تطوعت ممرضة ويا الصليب الأحمر.","Violet in a nurse uniform with a red cross tending wounded soldiers in a field hospital ward.",2,{}),
(9,"وشغلوها على سفينة مستشفى... اسمها البريتانيك.","Violet looking at a giant white hospital ship with green stripe and red crosses, the HMHS Britannic, at port.",2,{}),
(9,"والبريتانيك هي... السفينة الأخت الثالثة للأولمبيك والتايتانك.","Three sister ocean liners shown side by side in an illustration-like realistic composition: Olympic, Titanic and the white Britannic.",0,{}),
(10,"بواحد وعشرين تشرين الثاني، ألف وتسعمية وستعش... البريتانيك ماشية بالبحر قرب اليونان.","The white hospital ship Britannic sailing on a calm blue Aegean sea near Greek islands, morning.",0,{}),
(10,"وفجأة... انفجار قوي هز السفينة. ضربت لغم بحري.","A huge explosion bursting against the hull of the white hospital ship, water and smoke shooting up.",0,{"sfx":"boom"}),
(10,"السفينة صارت تغرق بسرعة... أسرع من التايتانك بكثير.","The Britannic tilting forward, bow sinking, lifeboats being lowered, smoke.",0,{}),
(10,"وفيوليت ركضت لغرفتها... وأخذت فرشاة أسنانها! لأنها گالت: بالتايتانك نسيتها، وبقيت مشتاقة إلها.","Violet in nurse uniform grabbing a toothbrush from a small washstand in her cabin in a hurry, comedic urgency, tilted room.",2,{}),
(11,"وصعدت بقارب نجاة... بس القارب صار ينسحب باتجاه مراوح السفينة العملاقة، وهي بعدها تدور.","A lifeboat being dragged toward the giant spinning propellers of the sinking ship, Violet in it, terrified.",2,{}),
(11,"وفيوليت ما عندها خيار... قفزت بالماي.","Violet jumping from the lifeboat into the sea, splash, the ship looming above.",2,{"sfx":"hit"}),
(11,"وانسحبت تحت الماي... وراسها ضرب بجسم السفينة.","Underwater view, Violet sinking in the blue water near the dark hull of the ship, bubbles.",2,{}),
(11,"بس طلعت للسطح... ولگوها، وأنقذوها. ونجت للمرة الثالثة.","Rescuers pulling Violet out of the water into a boat, she coughs, alive, the ship sinking in the background.",2,{}),
(12,"بعدين بسنين... الأطباء لگوا إن جمجمتها جان بيها كسر من ذاك اليوم، وهي ما تدري.","An older Violet (now about 40) sitting in a 1920s doctor's office as a doctor shows her an X-ray of a skull, both surprised.",1,{}),
(12,"وتعتقد... رجعت للبحر؟ إي، رجعت، واشتغلت بالسفن لحد ما تقاعدت.","Older Violet in a 1930s stewardess uniform smiling on the deck of a passenger ship at sunset.",1,{}),
(12,"وعاشت بقرية صغيرة ببريطانيا، بين الحديقة والدجاج... وتوفت سنة ألف وتسعمية وواحد وسبعين، بعمر ثلاثة وثمانين سنة.","Elderly Violet with grey hair in a bun feeding chickens in the garden of a small English country cottage.",3,{}),
(12,"والناس لهسه يسمونها: الآنسة التي لا تغرق.","A vintage portrait-like scene of Violet in her stewardess uniform standing proudly in front of a stormy sea and a liner.",1,{}),
(12,"ثلاث سفن... ثلاث كوارث... وبنت وحدة نجت منهم كلهم. انت تركب سفينة بعدها؟","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, kind, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img:
        if kind == 0: d["prompt"] = img + NOCH
        elif kind == 1: d["prompt"] = PRE + STEW + img + POST
        elif kind == 2: d["prompt"] = PRE + NURSE + img + POST
        else: d["prompt"] = G + img + POST
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
