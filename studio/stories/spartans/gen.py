import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon sandals, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "King Leonidas: short black beard, bronze Corinthian helmet with a red crest, red cloak, bronze breastplate, round bronze shield. "
 "Spartan soldiers: red cloaks, bronze helmets, round bronze shields and long spears. ")
X = "King Xerxes of Persia: curly black beard, tall golden crown, rich purple and gold robes. Persian soldiers: colorful long robes, wicker shields, bows and short spears. "
POST = " Historically accurate ancient Greece, 480 BC. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... ممر ضيق بين جبل وبحر. على جهة، جيش ضخم ما ينعد. وعلى الجهة الثانية... ثلاثمية جندي بس، يمشطون شعرهم بهدوء، ويستنون الموت.","A narrow coastal mountain pass at dawn, a small line of Spartan soldiers with red cloaks standing calmly, a vast army dust cloud on the horizon.",1,{}),
(1,"والملك العدو يدز رسول يگلهم: سلّموا سلاحكم... وانتو أحرار. والجواب جان كلمتين بس: تعال... وخذها.","A Persian messenger on horseback facing King Leonidas, who holds his spear firmly, Spartan soldiers behind him.",2,{}),
(1,"معركة الثلاثمية إسبرطي.","",0,{"hud":"title"}),
(1,"منو هذوله الإسبرطيين؟ وشلون ثلاثمية رجال وقفوا گدام أكبر جيش بالعالم؟ وليش خسارتهم صارت أشهر من انتصارات غيرهم؟ هاي قصة حقيقية.","Ancient Greek temple ruins on a hill at sunset, a bronze Spartan helmet resting on a stone.",0,{}),
(2,"اليونان، قبل حوالي ألفين وخمسمية سنة... ما جانت دولة وحدة. جانت مدن صغيرة، كل وحدة إلها جيشها وقوانينها.","Aerial view of ancient Greek city-states with temples, harbors and olive groves among mountains.",0,{"hud":"day","day":"٤٨٠ ق.م"}),
(2,"وأغرب مدينة بيهم: إسبرطة. مدينة بلا سور... لأنهم يگولون: سورنا هو رجالنا.","The ancient town of Sparta with simple buildings and no city walls, Spartan soldiers training in a field outside.",1,{}),
(2,"الطفل الإسبرطي، بعمر سبع سنين، ياخذوه من أهله... ويدخل معسكر تدريب قاسي، اسمه الأغوغي.","A crying 7-year-old Spartan boy being led away by a stern instructor from his mother, other boys training in the background.",1,{}),
(2,"يمشي حافي، وياكل قليل، وينام على القصب... حتى يتعلم الصبر والألم. ومن يكبر، يصير جندي ما يعرف غير القتال.","Spartan boys in simple tunics training barefoot with wooden swords and shields in a dusty field, an instructor watching.",1,{}),
(3,"والأم الإسبرطية جانت تنطي ابنها الدرع قبل الحرب، وتگله: ارجع بيه... لو عليه.","A Spartan mother handing a round bronze shield to her son in red cloak at the door of a stone house, serious faces.",1,{}),
(3,"يعني ارجع منتصر وانت شايل درعك... لو ارجع شهيد محمول فوگه. بس لا ترجع هارب.","Close-up of a round bronze shield with a Greek lambda symbol leaning on a stone wall, red cloak draped over it.",0,{}),
(3,"وبنفس الوقت، بالشرق، جانت أكو أكبر إمبراطورية بالعالم: الإمبراطورية الفارسية.","A grand Persian palace at Persepolis with tall columns, guards and golden decorations.",3,{}),
(3,"وملكها خشايارشا... قرر يحتل اليونان كلها، وينتقم لهزيمة أبوه قبل عشر سنين.","King Xerxes sitting on a golden throne in his palace, pointing at a map table, generals bowing.",3,{}),
(4,"جمع جيش ضخم... المؤرخين القدماء گالوا مليون، والمؤرخين اليوم يگولون يمكن مئة لـ ثلاثمية ألف. بس بكل الأحوال... جيش ما ينعد.","A massive Persian army marching across a plain, countless soldiers, cavalry and banners stretching to the horizon.",3,{}),
(4,"ويگولون جيشه جان كبير لدرجة يشربون الأنهار لحد ما تنشف!","Persian soldiers and horses drinking from a river that is nearly dry, the army stretching behind them.",3,{}),
(4,"وبنى جسر من السفن على البحر... حتى يعبر جيشه من آسيا لأوروبا.","A bridge made of hundreds of ships tied together across a strait, the Persian army crossing it.",0,{}),
(4,"واليونانيين انصدموا... والكثير منهم استسلموا من الخوف.","Worried Greek leaders arguing in a council hall, some throwing up their hands in despair.",1,{}),
(5,"بس ملك إسبرطة، ليونيداس، گرر يوقفهم. وجان عمره ستين سنة تقريباً.","King Leonidas standing in front of his house in Sparta, putting on his helmet, determined.",1,{}),
(5,"وما گدر ياخذ كل جيش إسبرطة، لأن جان عدهم عيد ديني... فاختار ثلاثمية رجال بس. وكلهم عندهم ولد، حتى ما تنقطع عوائلهم.","King Leonidas inspecting a line of 300 Spartan soldiers in red cloaks, choosing them one by one.",1,{}),
(5,"وانضموا إلهم جنود من مدن يونانية ثانية... فصار العدد حوالي سبع آلاف.","Spartans marching with other Greek soldiers in different colored cloaks along a mountain road.",1,{}),
(5,"واختار ليونيداس مكان ذكي: ممر ثيرموبيلي... يعني البوابات الحارة. ممر ضيق بين الجبل والبحر.","A very narrow pass between steep cliffs and the sea at Thermopylae, hot springs steaming.",0,{}),
(6,"بالممر الضيق، كثرة الجيش ما تفيد... لأن ما يگدرون يقاتلون إلا عدد قليل بنفس الوقت.","Spartans in a tight shield wall in the narrow pass, only a few Persian soldiers able to reach them at once.",1,{}),
(6,"وخشايارشا وصل، وشاف الإسبرطيين... يمشطون شعرهم، ويسوون رياضة! وضحك عليهم.","Persian king Xerxes on a hill laughing, looking down at Spartans combing their long hair and exercising.",4,{}),
(6,"وواحد گله: هذوله من يمشطون شعرهم... يعني مستعدين يموتون.","A Greek advisor explaining seriously to King Xerxes, Xerxes frowning.",4,{}),
(6,"وانتظر أربع أيام، يستنى يهربون... وما هربوا.","Spartans sitting calmly by campfires at night in the pass, Persian camp fires covering the plain beyond.",1,{}),
(7,"وبيوم الخامس... بدت المعركة. موجة ورا موجة من الجنود الفرس هجمت على الممر.","Waves of Persian soldiers charging into the narrow pass against the Spartan shield wall, dust and spears.",4,{"sfx":"boom"}),
(7,"والإسبرطيين، بدروعهم ورماحهم الطويلة، صاروا مثل جدار حديد... محد يگدر يعبره.","A solid wall of bronze Spartan shields with long spears pushing back attackers in the pass.",1,{}),
(7,"ويگولون الفرس دزوا سهام هواية لدرجة تغطي الشمس... وجندي إسبرطي اسمه دينيكيس گال: زين... نقاتل بالظل!","The sky darkened by thousands of arrows, a Spartan soldier smiling under his raised shield.",1,{}),
(7,"وبعدين دز خشايارشا أحسن جنوده: الخالدين. عشرة آلاف جندي نخبة.","Elite Persian Immortals in ornate robes and golden-tipped spears marching in perfect ranks.",3,{}),
(8,"بس حتى الخالدين... ما گدروا يعبرون. ويگولون خشايارشا گام من كرسيه ثلاث مرات من الخوف على جيشه.","King Xerxes jumping up from his golden throne on a hill in fear, watching the battle below.",3,{}),
(8,"يومين كاملة... والممر ما انفتح.","The narrow pass at sunset after battle, broken spears and shields, Spartans still standing in line.",1,{}),
(8,"بس بعدين... صارت الخيانة. واحد يوناني اسمه إفيالتيس، طمع بالفلوس.","A sneaky Greek shepherd named Ephialtes whispering to Persian officers in a tent, bags of gold.",3,{}),
(8,"وراح لخشايارشا، وگله: أكو طريق سري بالجبل... يلف من ورا الإسبرطيين.","Ephialtes pointing a secret mountain path on a map to King Xerxes, Xerxes smiling.",4,{}),
(9,"وبالليل، مشى الخالدين بالطريق السري... وصاروا وراهم.","Persian Immortals walking at night along a narrow mountain goat path with torches.",3,{}),
(9,"ليونيداس عرف إن المعركة خسرانة... فدز أغلب اليونانيين يرجعون، حتى يعيشون ويقاتلون بعدين.","King Leonidas ordering Greek allies to retreat at dawn, soldiers leaving sadly.",1,{}),
(9,"وبقى هو، والثلاثمية، وحوالي سبعمية من مدينة ثيسبيا رفضوا يتركوه.","Leonidas with the remaining Spartans and other Greek volunteers standing together, determined, dawn light.",1,{}),
(9,"وگال إلهم: افطروا زين... لأن العشا راح يكون بالعالم الثاني.","Spartans eating a simple breakfast around a fire at dawn, Leonidas speaking to them.",1,{}),
(10,"وطلعوا للقتال... من گدام ومن ورا. ولما انكسرت رماحهم، قاتلوا بالسيوف... ولما انكسرت السيوف، قاتلوا بإيدهم.","The final stand: Spartans surrounded on a small hill fighting with swords, Persians attacking from all sides.",4,{"sfx":"boom"}),
(10,"وليونيداس انقتل... والإسبرطيين قاتلوا حتى ياخذون جسده وما يخلونه للعدو.","Spartans fighting fiercely around the fallen body of King Leonidas, protecting it with their shields.",1,{}),
(10,"وبالأخير، الفرس ما گدروا يقربون... فرموهم بالسهام لحد ما ماتوا كلهم.","A storm of arrows falling on the last Spartans on a small hill, silhouettes against the sun.",0,{}),
(10,"خسروا المعركة... بس أخروا أكبر جيش بالعالم أيام، وكلّفوه آلاف القتلى.","The empty pass after the battle, broken shields and red cloaks on the ground, quiet sunset.",0,{}),
(11,"وهاي الأيام كفت اليونانيين يجهزون أسطولهم... وبعد أسابيع، انتصروا على الفرس بمعركة بحرية كبيرة اسمها سلاميس.","A great ancient naval battle with Greek triremes ramming Persian ships near an island.",0,{"hud":"day","day":"سلاميس"}),
(11,"وبالسنة اللي بعدها، اليونانيين انتصروا مرة ثانية... ورجع خشايارشا لبلاده.","Xerxes riding away in his chariot looking back angrily, his army retreating in the distance.",3,{}),
(11,"وبمكان المعركة، حطوا حجر مكتوب عليه: يا غريب، گول لأهل إسبرطة... إحنا هنا نايمين، وطعنا الأمر.","An ancient stone monument with carved Greek inscription at the Thermopylae pass, flowers around it.",0,{}),
(11,"واليوم أكو تمثال برونز لليونيداس بنفس المكان... ومكتوب تحته: تعال وخذها.","A modern bronze statue of King Leonidas with spear and shield at Thermopylae, blue sky.",0,{}),
(12,"وقصتهم صارت أفلام، وألعاب، ورمز للشجاعة بكل العالم.","Modern young people watching an epic Spartan movie in a cinema, faces lit by the screen.",5,{}),
(12,"بس الحقيقة أعمق: مو بس شجاعة... هذا جيش عرف إن الخسارة أحياناً تنقذ الكل.","A lone Spartan helmet and spear on a rock overlooking the sea at sunset.",0,{}),
(12,"ثلاثمية رجال... وقفوا بممر ضيق، وغيروا التاريخ.","Silhouettes of 300 Spartan soldiers standing in a line on a ridge at sunset, cloaks blowing.",0,{}),
(12,"انت لو جنت بمكانهم، تبقى ويا ليونيداس... لو ترجع؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
G0 = G.split("King Leonidas")[0]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img:
        if ch == 1: d["prompt"] = G + img + POST
        elif ch == 2: d["prompt"] = G + "Persian messenger: colorful robes, tall hat. " + img + POST
        elif ch == 3: d["prompt"] = G0 + X + img + POST
        elif ch == 4: d["prompt"] = G + X + img + POST
        elif ch == 5: d["prompt"] = G0.replace("chunky cartoon sandals","chunky cartoon shoes") + img + " Modern day. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
        else: d["prompt"] = img + NOCH
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
