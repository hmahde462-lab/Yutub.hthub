import json, sys
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon boots, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "The hero: messy curly dark-brown hair on top of the white round head, a thin mustache and a small chin beard, grey t-shirt, dark blue jeans, brown boots. "
 "His mother: black abaya and black headscarf. His grandfather: old man, short white beard, white dishdasha, grey jacket, white skullcap. "
 "Ali the neighbor: skinny teenage boy, short black hair, white shirt. Abu Ali: chubby middle-aged man with black mustache, brown dishdasha. ")
POST = " Background: photorealistic Baghdad, Iraq, summer. Cinematic lighting, dust in the air. Wide shot, 16:9, no text."
NOCH = " Photorealistic Baghdad, Iraq, summer. Cinematic, 16:9, no text, no people."
EP3 = [
(1,"بالحلقة الماضية... رجعت من الامتحان، ولگيت أمك تبچي بالباب.","His mother stands crying at the house door in a narrow alley, neighbors gathered around worried, the hero arriving with his school bag.",1,{"sfx":"heart"}),
(1,"تركض عليها وتصيح: شصار؟","The hero running toward his crying mother in the alley, frightened face.",1,{}),
(1,"اليوم السادس.","",0,{"hud":"title"}),
(1,"تگلك: جدك... وگع من الحر.","The grandfather lying weak on a mattress in a hot dim room with a wet towel on his forehead, family kneeling around him, a silent fan.",1,{}),
(2,"جدك عمره ثمانين سنة، بالليل ما نام من الحر... والصبح ما گام.","Close-up of the weak grandfather with closed eyes, sweat, the hero holding his hand.",1,{}),
(2,"تشيله ويا علي بالسيارة، والشوارع كلها زحمة.","The hero and Ali carrying the grandfather into an old white car in the alley, mother holding the door.",1,{}),
(2,"توصل المستشفى... والمستشفى نفسه شغال على المولدة.","An old Iraqi public hospital entrance at noon with a big noisy diesel generator smoking outside, crowds at the gate.",0,{}),
(2,"الممرات مليانة ناس... كلهم ضربة شمس.","A crowded dim hospital corridor full of patients on benches and the floor, nurses rushing, the hero pushing his grandfather in a wheelchair.",1,{}),
(3,"الطبيب يگلك: لازم يبقى هنا... جسمه لازم يبرد.","A tired doctor in a white coat talking to the hero beside the grandfather's hospital bed.",1,{}),
(3,"بس المكيف بالردهة، يشتغل ساعة... ويطفى ساعة.","A crowded hospital ward with an old wall air conditioner switched off, patients fanning themselves with papers.",1,{}),
(3,"فتبقى يمه طول الليل... تفوّره بكارتونة.","At night in the dim hospital ward the hero sits beside his sleeping grandfather fanning him with a piece of cardboard.",1,{}),
(3,"وجدك يفتح عيونه ويضحك: لا تخاف... آني شايف أيام أصعب.","The grandfather in the hospital bed smiling weakly and patting the hero's hand.",1,{}),
(4,"اليوم العاشر.","A Baghdad street at noon with strong heat haze, empty, burning sun.",0,{"hud":"day","day":"اليوم ١٠"}),
(4,"بالمحلة، الماي صار يجي ساعة وحدة باليوم.","Neighbors in the alley lining up with buckets and jerrycans around a single water tap, kids carrying water.",1,{}),
(4,"والثلج صار أغلى من اللحم... القالب بعشرة آلاف.","A street ice seller cutting a big ice block with people crowding around him holding money.",1,{}),
(4,"وطابور الگاز بالمحطة... أطول من الشارع.","A very long queue of old cars at a Baghdad fuel station in the heat, drivers standing outside.",1,{}),
(5,"بس بهديك الأيام... صار شي حلو.","Evening in the alley, neighbors slowly gathering outside their doors, warm sunset light.",1,{}),
(5,"أبو علي جمع الجيران، وگال: كل واحد يدفع اللي يگدر... ونشغّل مولدة المحلة سوا.","Abu Ali standing on a box talking to the gathered neighbors next to an old big generator in the alley.",1,{}),
(5,"والعوائل اللي ما عدها... الجيران دفعوا عنها.","A neighbor quietly handing money to an old poor man in the alley, both smiling.",1,{}),
(5,"وبالليل... المولدة اشتغلت، وكل بيت أخذ أمبيرين.","At night a tangle of electric cables from the generator to every house, warm lights in the windows, neighbors cheering.",1,{"sfx":"hit"}),
(6,"أمبيرين بس... يا مروحة، يا ثلاجة.","The hero in his dim kitchen looking back and forth between a standing fan and the fridge, thinking.",1,{}),
(6,"وأمك تختار الثلاجة... لأن دوا جدك لازم يبقى بارد.","The mother carefully putting medicine boxes and insulin pens into the fridge, the hero watching.",1,{}),
(6,"وانت تنام بالسطح... ويا كل المحلة.","The hero lying on a mattress on the rooftop at night under the stars, sweating, neighbors on the next rooftops.",1,{}),
(6,"سطوح بغداد كلها صارت غرف نوم.","Wide aerial shot of Baghdad rooftops at night with families sleeping on mattresses under mosquito nets, moonlight.",0,{}),
(7,"اليوم الخامس عشر... جدك يطلع من المستشفى.","The hero helping his grandfather walk out of the hospital gate, both smiling.",1,{"hud":"day","day":"اليوم ١٥"}),
(7,"والجيران يستقبلونه بالباب، والأطفال يصفگون.","Neighbors and kids in the alley clapping and welcoming the grandfather home, Abu Ali shaking his hand.",1,{}),
(7,"بس بنفس اليوم... السما صارت صفرة.","Baghdad skyline under a strange yellow-orange dusty sky, the sun a pale disc.",0,{}),
(7,"عجاجة... ما تشوف بيها إيدك.","The hero in the alley inside a thick dust storm, covering his face with his arm, almost nothing visible.",1,{"sfx":"hit"}),
(8,"التراب دخل لكل مكان: للأكل، للفراش... ولخشمك.","Inside the house covered with a layer of dust, the hero coughing with a cloth over his face.",1,{}),
(8,"وجدك صار يتنفس بصعوبة.","The grandfather breathing with difficulty on his mattress, the mother holding a wet cloth, worried.",1,{}),
(8,"تبلل الشراشف وتعلگها على الشبابيك، حتى توگف التراب.","The hero hanging wet bed sheets over the windows inside the house, orange dusty light behind.",1,{}),
(8,"وبعد يومين... العجاجة راحت.","Clear blue sky again, neighbors sweeping thick dust from the alley and rooftops.",1,{}),
(9,"اليوم التاسع عشر... تسمع إشاعة بالمحلة.","Neighbors whispering excitedly in front of a small grocery shop in the alley.",1,{"hud":"day","day":"اليوم ١٩"}),
(9,"يگولون: الكهرباء راجعة باچر!","Kids jumping with joy in the alley, adults smiling and raising their hands.",1,{}),
(9,"الكل يجهز الأجهزة: المبردات، والتلفزيونات، والسبالت.","The family cleaning and plugging in an air cooler and an old TV with excitement.",1,{}),
(9,"وانت تنام بهديك الليلة... وتحلم بالمبردة.","The hero sleeping on the rooftop smiling in his sleep, a dreamy glowing air cooler floating above him in the night sky.",1,{}),
(10,"اليوم العشرين... الصبح.","Early morning on the rooftop, the hero waking up and stretching, hopeful.",1,{"hud":"day","day":"اليوم ٢٠"}),
(10,"ما رجعت.","The hero flipping a light switch in a dark room, nothing happens, disappointed face.",1,{"sfx":"hit"}),
(10,"بس اللي رجع... أبو علي، ووجهه أصفر.","Abu Ali standing at the hero's door, pale and shocked face, sweating.",1,{}),
(10,"يگلك: مولدة المحلة... انسرقت بالليل!","An empty concrete spot in the alley where the generator was, cut cables hanging, neighbors staring in shock.",1,{"sfx":"boom"}),
(10,"اليوم العشرين خلص... وباقي عشر أيام. والحلقة الجاية... هي الأخيرة.","",0,{"hud":"black"}),
]
EP4 = [
(1,"بالحلقة الماضية... مولدة المحلة انسرقت، وباقي عشر أيام.","An empty concrete spot in the alley where the generator was, cut cables hanging, neighbors staring in shock.",1,{"sfx":"heart"}),
(1,"والمحلة كلها رجعت للظلام.","A completely dark Baghdad alley at night, every window black, only moonlight.",0,{}),
(1,"الحلقة الأخيرة.","",0,{"hud":"title"}),
(1,"وأبو علي گاعد على الرصيف... ساكت.","Abu Ali sitting alone on the curb at night with his head down, the hero standing beside him.",1,{}),
(2,"اليوم الواحد والعشرين... الجيران يتجمعون بالجامع.","Neighborhood men gathering in a mosque courtyard in the evening, serious faces.",1,{"hud":"day","day":"اليوم ٢١"}),
(2,"واحد يگول: نشتري مولدة جديدة... بس منين الفلوس؟","Men in the mosque courtyard arguing and shrugging, empty pockets.",1,{}),
(2,"وجدك يگوم من مكانه... ويطلّع خاتمه الذهب.","The grandfather slowly standing up in the mosque courtyard, taking a gold ring off his finger, everyone turning to look.",1,{}),
(2,"ويگول: هذا خاتم جدتك الله يرحمها... خلي يصير ضو للمحلة.","Close-up of the grandfather holding out the gold ring in his palm, emotional, the men moved.",1,{"sfx":"heart"}),
(3,"وكل واحد طلّع اللي عنده: ساعة، ذهب، فلوس مدخرة.","Neighbors placing watches, gold bracelets and banknotes on a big copper tray in the mosque courtyard.",1,{}),
(3,"وحتى الأطفال... جابوا حصّالاتهم.","Little kids proudly handing their piggy banks and coins to Abu Ali.",1,{}),
(3,"وبثلاث أيام... جمعوا ثمن مولدة جديدة.","A new big yellow generator being unloaded from a truck in the alley, neighbors cheering.",1,{}),
(3,"وانت وعلي... تحرسوها بالليل بالتناوب.","The hero and Ali sitting next to the new generator at night with a flashlight and glasses of tea, guarding it.",1,{}),
(4,"اليوم الخامس والعشرين... تطلع نتايج الامتحان.","Crowds of students rushing toward an Iraqi school gate in the morning.",1,{"hud":"day","day":"اليوم ٢٥"}),
(4,"الإنترنت ماكو... فتروح للمدرسة تشوف الورقة المعلگة.","Students crowding around long paper result lists taped on a school wall.",1,{}),
(4,"تدور على اسمك... وإيدك ترجف.","Close-up of the hero's trembling mitten finger moving down a long list of names on paper.",1,{"sfx":"heart"}),
(4,"ناجح!","The hero jumping high with joy in front of the school wall, arms raised.",1,{"sfx":"hit"}),
(5,"وعلي ناجح هم... وبمعدل أعلى منك!","Ali laughing and hugging the hero in front of the school, both happy.",1,{}),
(5,"ترجع للبيت راكض، وأمك تزغرد من الباب.","The mother ululating with joy at the house door, the hero running toward her in the alley.",1,{}),
(5,"وجدك يگلك: مو گلتلك؟ إذا نجحت بهالظروف... تگدر تسوي أي شي.","The grandfather proudly putting his hand on the hero's shoulder inside the house.",1,{}),
(5,"وبالليل، المحلة سوت حفلة... على ضو مولدتها الجديدة.","A night party in the alley with string lights from the generator, music, kids dancing, big pots of food.",1,{}),
(6,"اليوم الثامن والعشرين... الحر ما خف.","A Baghdad street with heat haze at noon.",0,{"hud":"day","day":"اليوم ٢٨"}),
(6,"بس انت... تغيرت.","The hero calmly reading a book on the rooftop at sunset, relaxed.",1,{}),
(6,"صرت تعرف شلون تعيش بدون مكيف... وبدون إنترنت.","The hero playing dominoes with neighbors on a carpet in the alley at evening, laughing.",1,{}),
(6,"وتعرفت على جيرانك... أكثر من عشرين سنة گبلها.","The hero drinking tea and chatting with an elderly neighbor sitting on his doorstep.",1,{}),
(7,"اليوم الثلاثين... بالليل.","Night on the rooftop, the family sitting together on a mattress, the grandfather with prayer beads.",1,{"hud":"day","day":"اليوم ٣٠"}),
(7,"كل المحلة گاعدة بالسطوح... تعد الدقايق.","Wide shot of many rooftops at night full of families sitting and looking at the dark city.",1,{}),
(7,"الساعة اثنعش... وفجأة.","The dark Baghdad skyline at midnight, silent, only stars.",0,{"sfx":"heart"}),
(7,"بغداد كلها... تضوي!","The Baghdad skyline suddenly lighting up at night, thousands of windows and street lights turning on, families on rooftops cheering.",1,{"sfx":"boom"}),
(8,"المبردات تشتغل، والناس تصيح وتصفگ من السطوح.","People on rooftops jumping, clapping and cheering under the lit city at night.",1,{}),
(8,"وأمك تبچي... بس هالمرة من الفرحة.","The mother crying with joy and hugging the grandfather on the rooftop.",1,{}),
(8,"تنزل للغرفة، وتوگف گدام المبردة... وتغمض عيونك.","The hero standing in front of a running air cooler with closed eyes, his curly hair blowing in the cold air.",1,{}),
(8,"أحلى هوا بحياتك.","Close-up of the hero's blissful smiling face with hair blowing.",1,{}),
(9,"وبعد خمس دقايق...","The hero still standing in front of the air cooler in the lit room, smiling.",1,{}),
(9,"طفت.","The room suddenly completely dark, only the hero's wide open eyes visible.",1,{"sfx":"hit"}),
(9,"وكل المحلة تصيح بصوت واحد: لاااا!","People on all the rooftops shouting at the sky in the dark, comic despair.",1,{}),
(9,"بس انت... تضحك.","The hero laughing in the dark room holding a candle.",1,{}),
(10,"لأن ثلاثين يوم... علمتك شي ما تعلمه أي مدرسة.","The hero, his mother, grandfather and Ali sitting together on the rooftop under the stars with a candle.",1,{}),
(10,"الضو الحقيقي مو بالكهرباء... الضو بالناس اللي يمك.","Wide shot of the whole neighborhood together on connected rooftops at night, candles and lanterns, warm faces.",1,{}),
(10,"انتهت. وانت... شلون تتحمل انقطاع الكهرباء؟ اكتبها بالتعليقات.","",0,{"hud":"black"}),
]
for name, S in (('ep3', EP3), ('ep4', EP4)):
    out = []
    for p, vo, img, ch, ex in S:
        d = {"vo": vo, "img": img, "part": p}
        if img: d["prompt"] = (G + img + POST) if ch else (img + NOCH)
        d.update(ex); out.append(d)
    json.dump(out, open(f'{name}/script.json', 'w'), ensure_ascii=False, indent=1)
    open(f'{name}/vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
    print(name, len(out), sum(len(x['vo']) for x in out), sum(1 for x in out if x['img']))
