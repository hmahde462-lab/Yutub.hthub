import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon sandals, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "Miyamoto Musashi: messy black hair tied loosely, rough stubble, plain dark grey kimono and hakama, two katana swords at his waist. ")
POST = " Historically accurate early 17th century Edo-period Japan. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
K = "Sasaki Kojiro: long black hair in a high ponytail, elegant bright red kimono, an extremely long katana on his back. "
S = [
(1,"تخيّل... مبارزة على جزيرة صغيرة. واحد من أقوى سيافين اليابان واگف يستنى... وخصمه متأخر ساعات.","A lone samurai with a very long sword waiting impatiently on a small beach of an island, sea and morning sun.",3,{}),
(1,"وأخيراً يوصل الخصم بقارب... وبإيده مو سيف حديد، سيف خشب نحته من مجداف!","A small wooden rowing boat arriving at an island beach, Musashi standing in it holding a long wooden sword carved from an oar.",1,{}),
(1,"مياموتو موساشي... قديس السيف.","",0,{"hud":"title"}),
(1,"منو هذا الرجل اللي ما انغلب بولا مبارزة؟ وليش بآخر عمره رمى السيف ومسك الفرشاة؟ هاي قصة حقيقية.","A katana resting beside an ink brush and a sheet of calligraphy paper on a low wooden table, soft light.",0,{}),
(2,"اليابان، أواخر القرن السادس عشر... بلد كله حروب بين الأمراء والساموراي.","Feudal Japanese landscape with a castle on a hill, armies with banners marching through rice fields, smoke on the horizon.",0,{"hud":"day","day":"١٥٨٤م"}),
(2,"وبقرية صغيرة، انولد طفل اسمه موساشي... وأبوه جان مدرب سيف قاسي.","A strict samurai father training a young boy with a wooden sword in a village courtyard, thatched houses.",1,{}),
(2,"الطفل جان عصبي وقوي... ويتعلم السيف لحاله أغلب الوقت.","A young boy alone practicing with a wooden sword under a big tree in a mountain village, determined face.",1,{}),
(2,"وبعمر ثلطعش سنة... سوّى أول مبارزة بحياته.","A 13-year-old boy holding a wooden stick facing a tall adult samurai in a village square, villagers watching.",1,{}),
(3,"خصمه جان ساموراي محترف اسمه أريما كيهي... والكل گال الطفل راح يموت.","A proud adult samurai laughing and pointing at a boy with a wooden stick, village crowd worried.",1,{}),
(3,"بس موساشي رماه على الگاع... وغلبه بعصا خشب!","A boy knocking down an adult samurai with a wooden stick, dust flying, crowd shocked.",1,{"sfx":"hit"}),
(3,"ومن هذاك اليوم، گرر: راح يصير أقوى سياف باليابان.","Teenage Musashi standing on a hill at sunset looking over the land, wooden sword on his shoulder.",1,{}),
(3,"وطلع يمشي بالبلاد... بلا بيت، بلا سيد، بلا فلوس.","Musashi walking alone along a misty mountain road in Japan, straw hat, two swords, autumn leaves.",1,{}),
(4,"بسنة ألف وستمية... دخل بأكبر معركة بتاريخ اليابان: سيكيغاهارا.","A huge samurai battle at Sekigahara with thousands of soldiers, banners, fog and arrows.",0,{"hud":"day","day":"١٦٠٠م","sfx":"boom"}),
(4,"جماعته خسروا... بس هو نجا، وهرب بين الجثث.","Musashi escaping through a foggy battlefield after defeat, broken banners and fallen spears around him.",1,{}),
(4,"وبعدها راح للعاصمة كيوتو... وتحدى أشهر مدرسة سيف بيها: عائلة يوشيوكا.","Musashi standing at the gate of a famous sword school in old Kyoto, students staring at him.",1,{}),
(4,"غلب رئيس المدرسة... وبعدين غلب أخوه.","Musashi defeating a samurai master in a duel in a snowy field in Kyoto, wooden sword raised.",1,{"sfx":"hit"}),
(5,"العائلة عصبت... وجهزت كمين: عشرات الرجال بالسيوف والرماح والقوس.","Dozens of samurai with swords, spears and bows hiding around a large pine tree at night, ambush.",1,{}),
(5,"وحطوا طفل صغير من العائلة گدامهم... كرمز إنهم القائد.","A young boy in fine clothes standing in front of armed samurai under a pine tree at dawn, serious.",1,{}),
(5,"موساشي وصل قبلهم، واختبأ... وهجم فجأة.","Musashi hiding in tall grass at dawn watching the group of samurai under the pine tree.",1,{}),
(5,"يگولون شق طريقه بينهم... وهرب حي. ومن هنا، الكل صار يخاف اسمه.","Musashi fighting through many samurai with two swords at dawn, dramatic motion, mist.",1,{"sfx":"boom"}),
(6,"وموساشي جان عنده أسلوب غريب: يقاتل بسيفين... واحد بكل إيد.","Musashi in a fighting stance holding a long katana in one hand and a short sword in the other, dojo background.",1,{}),
(6,"ذاك الوقت، الساموراي يمسك السيف بالإيدين الثنتين... فهذا جان شي جديد.","Two samurai comparing stances in a dojo, one with a two-handed grip, Musashi with two swords, students watching.",1,{}),
(6,"وما جان يهتم بالشكل: ملابسه وسخة، وشعره منكوش، وما يحب يتحمم!","Musashi with messy hair and dirty clothes sitting relaxed while elegant samurai look at him with disgust.",1,{}),
(6,"بس بالمبارزة... محد جان يگدر يلمسه.","Musashi calmly dodging a fast sword strike from a skilled opponent, dust in the air, dojo.",1,{}),
(7,"وبعدين... إجت أشهر مبارزة بتاريخ اليابان.","A mysterious calm sea at dawn with a small island in the middle, mist.",0,{}),
(7,"خصمه: ساساكي كوجيرو... سياف وسيم، سيفه طويل لدرجة يسمّوه «عمود نشر الهدوم»!","Sasaki Kojiro posing proudly with his extremely long katana in a beautiful garden with cherry blossoms.",3,{}),
(7,"وكوجيرو جان عنده حركة مشهورة: «ضربة السنونو»... ضربة سريعة لدرجة تقص طير بالهوا.","Sasaki Kojiro slicing his long sword through the air as swallows fly around him, motion blur.",3,{}),
(7,"المبارزة انحددت على جزيرة صغيرة اسمها غانريو... بسنة ألف وستمية وثنعش.","Crowds of people watching from boats near a tiny island at sunrise, flags.",0,{"hud":"day","day":"١٦١٢م"}),
(8,"وكوجيرو وصل بالوقت... بس موساشي ما إجه.","Sasaki Kojiro standing alone on the island beach, angry and tense, looking at the sea.",3,{}),
(8,"ساعة... ساعتين... وكوجيرو يعصّب أكثر وأكثر.","Close view of Sasaki Kojiro clenching his teeth, gripping his long sword, sweat, sun rising higher.",3,{}),
(8,"وموساشي بالقارب، ياخذ مجداف، ويقعد ينحته... لسيف خشب أطول من سيف كوجيرو.","Musashi sitting in a small boat carving a long oar into a wooden sword with a knife, boatman rowing.",1,{}),
(8,"ولما وصل، كوجيرو سحب سيفه... ورمى الغمد بالماي.","Sasaki Kojiro drawing his long sword and throwing the scabbard into the sea, Musashi stepping off a boat.",4,{}),
(9,"وموساشي گلّه: «خسرت يا كوجيرو... لو جنت راح تفوز، ما جنت ترمي غمدك».","Musashi smiling calmly on the beach pointing his wooden sword at a furious Kojiro.",4,{}),
(9,"وهجموا... ضربة وحدة.","Musashi and Kojiro clashing on the beach in a single explosive strike, sand and water spraying, slow motion.",4,{"sfx":"boom"}),
(9,"وكوجيرو وگع على الرمل... وموساشي ركب القارب ورجع، بدون ولا كلمة.","Kojiro lying defeated on the sand while Musashi walks back to the boat at sunrise, calm.",4,{}),
(9,"وبعدها... موساشي بطّل المبارزات للموت.","Musashi standing alone on a cliff looking at the sea, wooden sword lowered, thoughtful.",1,{}),
(10,"وصار يدوّر على شي ثاني: طريق السيف... مو بس القتل.","Older Musashi meditating under a waterfall in the mountains, calm.",1,{}),
(10,"وصار رسام، وخطاط، ونحات... ولوحاته موجودة بمتاحف اليابان لهسه.","Older Musashi painting a bird on a branch with ink brush on paper, calm studio.",1,{}),
(10,"يگولون رسم طير الصرد على غصن... بنفس هدوء ضربة السيف.","Close-up of a traditional Japanese ink painting of a shrike bird on a dry branch, brush beside it.",0,{}),
(10,"وعلّم تلاميذ... بس جان يگول: أهم شي إنك تفهم، مو تقلد.","Older Musashi teaching young students in a dojo, pointing at their stance.",1,{}),
(11,"وبآخر عمره، راح وعاش بكهف بالجبل... اسمه كهف ريغندو.","A mountain cave with a small shrine inside, mist and trees around, lantern light.",0,{"hud":"day","day":"١٦٤٣م"}),
(11,"وهناك كتب كتاب اسمه: كتاب الحلقات الخمس... الأرض، والماي، والنار، والريح، والفراغ.","Old Musashi with grey hair writing with a brush on scrolls inside a cave by candlelight.",1,{}),
(11,"وبعد أسابيع من إكماله... مات، بعمر حوالي ستين سنة.","An empty cave with a finished scroll, a brush and two swords placed neatly, candle burned out.",0,{}),
(11,"بس كتابه ما مات.","An old scroll rolled out on a table with sunlight falling on it.",0,{}),
(12,"اليوم يقروه رجال أعمال، ورياضيين، ومدربين... بكل العالم.","Modern business people and athletes reading the same small book in different places, office and gym.",2,{}),
(12,"وقصته صارت أفلام، وروايات، ومانغا مشهورة.","A modern bookstore shelf full of samurai manga and novels, readers browsing.",2,{}),
(12,"ودرس موساشي بسيط: القوة مو بالسيف... بالعقل اللي يمسكه.","Silhouette of a samurai with two swords standing on a hill at sunset, wind in the grass.",0,{}),
(12,"انت لو تختار سلاح واحد بحياتك: السيف لو القلم؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
G2 = G.split("Miyamoto Musashi")[0].replace("chunky cartoon sandals", "chunky cartoon shoes")
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img:
        if ch == 1: d["prompt"] = G + img + POST
        elif ch == 3: d["prompt"] = G.split("Miyamoto Musashi")[0] + K + img + POST
        elif ch == 4: d["prompt"] = G + K + img + POST
        elif ch == 2: d["prompt"] = G2 + img + " Modern day. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
        else: d["prompt"] = img + NOCH
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
