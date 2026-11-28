import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. ")
AST = "Three astronauts in white 1970 NASA flight suits: Jim Lovell (commander, short brown hair), Jack Swigert (blond hair), Fred Haise (dark hair). "
MC = "NASA Mission Control engineers in 1970: white short-sleeve shirts, thin black ties, headsets, rows of consoles with green screens. Flight director Gene Kranz wears a white vest and a flat-top haircut. "
POST = " Historically accurate 1970. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... انت وصاحبينك داخل علبة حديد صغيرة، بنص الفضا، على بعد ثلاثمية ألف كيلومتر من الأرض. وفجأة... انفجار.","Inside a cramped 1970 spacecraft cabin, three astronauts shaken by a sudden bang, warning lights flashing.",1,{"sfx":"boom"}),
(1,"الأوكسجين يتسرب، والكهرباء تطفي... وأول جملة طلعت من المركبة: هيوستن، عدنا مشكلة.","An astronaut speaking into a microphone headset with worried eyes, red warning lights inside the capsule.",1,{}),
(1,"أبولو ثلطعش... أنجح فشل بالتاريخ.","",0,{"hud":"title"}),
(1,"شلون ثلاث رواد فضاء رجعوا للأرض بمركبة مكسورة؟ وشلون مهندسين على الأرض صلّحوها بشريط لاصق وكارتون؟ هاي قصة حقيقية.","The Earth seen as a small blue marble from deep space, the Moon large in the foreground.",0,{}),
(2,"سنة ألف وتسعمية وسبعين... أمريكا جانت نزلت على الگمر مرتين قبلها، والناس صارت تعتبرها شي عادي.","1970 family living room with a TV showing a Moon landing broadcast, family members bored and yawning.",3,{"hud":"day","day":"١٩٧٠م"}),
(2,"والرحلة الثالثة: أبولو ثلطعش، بقيادة جيم لوفيل... ويمّه فريد هيز، وكين ماتينغلي.","Three astronauts in white flight suits posing smiling in front of a giant Saturn V rocket on the launch pad.",2,{}),
(2,"بس قبل الإطلاق بثلاث أيام... قرروا ينزّلون ماتينغلي، لأنه احتمال يجيه مرض الحصبة!","A sad astronaut in a flight suit sitting on a bench as a NASA doctor in a white coat shakes his head, clipboard.",1,{}),
(2,"وحطوا بداله جاك سويغرت... وماتينغلي بالأخير ما جاته الحصبة أصلاً.","Astronaut Jack Swigert with blond hair excitedly putting on his flight suit in a 1970 preparation room.",2,{}),
(3,"وبيوم حداعش نيسان، انطلق الصاروخ العملاق ساتورن خمسة... ويا هتافات الناس.","A giant Saturn V rocket launching from Florida with massive flames and smoke, crowd watching from far away.",0,{"sfx":"boom"}),
(3,"وأول يومين، كلشي جان تمام. حتى سووا بث تلفزيوني من المركبة... بس القنوات ما عرضته، لأن محد مهتم!","Three astronauts floating and waving at a TV camera inside a spacecraft cabin, smiling.",2,{}),
(3,"وبعد خمسة وخمسين ساعة من الإطلاق... طلبوا من سويغرت يحرك خزانات الأوكسجين.","Astronaut Jack Swigert pressing a switch on a crowded 1970 spacecraft control panel, calm.",2,{}),
(3,"وبثانية وحدة... انفجر الخزان رقم اثنين.","Exterior view of the Apollo service module in space with a panel blown off, gas venting, debris floating.",0,{"sfx":"boom"}),
(4,"المركبة اهتزت... والإنذارات اشتغلت كلها. وسويغرت گال الجملة الشهيرة: هيوستن، عدنا مشكلة هنا.","Inside the capsule, three astronauts grabbing handholds, alarm lights flashing, one speaking into the radio.",2,{}),
(4,"وبمركز التحكم بهيوستن، المهندسين شافوا الأرقام تنهار گدامهم... وما صدقوا.","NASA Mission Control room in 1970 with engineers staring shocked at green console screens.",4,{}),
(4,"لوفيل باوع من الشباك... وشاف غاز يطلع من المركبة للفضا. وعرف: انتهت رحلة الگمر.","An astronaut looking through a small triangular spacecraft window at a white cloud of gas venting into black space.",2,{}),
(4,"وهسه السؤال صار: نگدر نرجعهم أحياء؟","Close-up of Gene Kranz in a white vest at his console in Mission Control, serious and determined.",4,{}),
(5,"المركبة الرئيسية، أوديسي، جانت تموت... أوكسجينها وكهرباءها دا يخلصن.","The Apollo command module interior going dark, panels turning off one by one, astronauts' breath visible.",2,{}),
(5,"فالحل الوحيد: يطلعون لمركبة الهبوط على الگمر، أكواريوس... ويستخدموها قارب نجاة.","Astronauts floating through a narrow tunnel from the command module into the lunar module, carrying equipment.",2,{}),
(5,"بس مشكلة: أكواريوس مصممة لشخصين... ليومين بس. وهم ثلاثة، ويحتاجون أربع أيام!","The cramped lunar module interior with three astronauts squeezed together, very little space.",2,{}),
(5,"ومدير الرحلة جين كرانتز گال لفريقه: إحنا ما راح نخسر طاقم... مو بفترتي.","Gene Kranz standing and speaking firmly to a team of engineers gathered around him in Mission Control.",4,{}),
(6,"وبدل ما يرجعون مباشرة، قرروا يلفون حول الگمر... ويستخدمون جاذبيته حتى ترميهم للأرض.","Diagram-like cinematic view of a small spacecraft looping around the far side of the Moon back toward Earth.",0,{}),
(6,"ولما مرّوا ورا الگمر... صاروا أبعد بشر عن الأرض بالتاريخ كله. رقم لهسه محد كسره.","A spacecraft passing behind the cratered far side of the Moon with the tiny Earth in the distance.",0,{}),
(6,"وبعدين... إجت مشكلة أخطر: ثاني أكسيد الكربون.","Close-up of a carbon dioxide gauge needle rising into the red zone inside a spacecraft.",0,{}),
(6,"أنفاسهم دا تسمم الهوا... والفلاتر بأكواريوس ما تكفي. وإذا ما تصلحت، راح يختنقون.","Astronauts looking tired and dizzy in the cramped lunar module, a warning light glowing.",2,{}),
(7,"والمصيبة: فلاتر أوديسي مربعة... وفتحات أكواريوس مدورة. حرفياً: يريدون يدخلون مربع بدايرة!","Close-up of a square air filter cartridge next to a round filter slot, an astronaut's hand holding it, comic frustration.",2,{}),
(7,"فالمهندسين بالأرض، جمعوا على ميز كل الأغراض الموجودة بالمركبة: أكياس، وكارتون، وشريط لاصق، وجواريب!","NASA engineers in 1970 around a table covered with plastic bags, cardboard, duct tape and socks, brainstorming.",4,{}),
(7,"واشتغلوا ساعات... لحد ما سووا قطعة تربط المربع بالدايرة.","Engineers holding up a strange makeshift contraption made of duct tape, cardboard and plastic bags, excited.",4,{}),
(7,"وقروا الطريقة للرواد خطوة بخطوة بالراديو... والرواد سووها بالفضا. ونجحت!","Astronauts in the lunar module assembling a duct-tape air filter adapter while listening to the radio, then relieved.",2,{}),
(8,"بس المشاكل ما خلصت. حتى يوفرون كهرباء، طفوا كل شي تقريباً... والبرد نزل لحد ثلاث درجات.","Astronauts shivering in the dark cold spacecraft, frost on the windows, breath fog.",2,{}),
(8,"والماي جان قليل... فصاروا يشربون شوية كلش. وفريد هيز صاب بالتهاب، وصار عنده حمى.","Astronaut Fred Haise with a fever lying in the corner of the cold capsule, another astronaut checking on him.",2,{}),
(8,"وما ينامون... لأن البرد يگصهم، والخوف يگصهم أكثر.","Three exhausted astronauts staring out the window at the distant Earth, sleepless.",2,{}),
(8,"وبالأرض، الملايين صاروا يتابعون الأخبار... والكنائس والجوامع تدعي إلهم.","1970 people around the world gathering around TVs and radios watching news anxiously, in homes and shop windows.",3,{}),
(9,"وبعدين لازم يعدلون اتجاه المركبة... بس الكومبيوتر مطفي حتى يوفرون الكهرباء.","Commander Jim Lovell holding a manual control stick in the dark lunar module, focused.",2,{}),
(9,"فلوفيل استخدم طريقة قديمة: خلّى خط الأرض بالشباك... وعدّل المركبة بإيده، مثل البحارة القدماء.","View through a spacecraft window of the Earth's edge line between day and night, used as a guide.",0,{}),
(9,"وشغّلوا المحرك بالضبط أربعطعش ثانية... ونجحت. صاروا على طريق الأرض.","A small spacecraft engine firing briefly in space with Earth growing larger ahead.",0,{}),
(9,"وقرب الأرض، رجعوا لأوديسي الباردة... وشغلوها من جديد، رغم الخوف إن الرطوبة تحرق أسلاكها.","Astronauts switching on panels one by one in the cold command module, water droplets on the panels, tense faces.",2,{}),
(10,"وتركوا قارب النجاة أكواريوس بالفضا... وودّعوه.","The lunar module separating and floating away from the command module above the blue Earth.",0,{}),
(10,"والمشكلة الأخيرة: لما المركبة تدخل الغلاف الجوي، الاتصال ينقطع حوالي أربع دقايق... من الحرارة.","The Apollo capsule glowing with fiery plasma while entering Earth's atmosphere.",0,{"sfx":"boom"}),
(10,"بس هالمرة... الأربع دقايق عبرت، والاتصال ما رجع.","Mission Control engineers silently staring at the clock, holding their breath.",4,{}),
(10,"خمس دقايق... ست دقايق... وكل العالم ساكت.","Close-up of a 1970 mission clock and a silent radio speaker in Mission Control, tension.",0,{}),
(11,"وفجأة، صوت سويغرت بالراديو: أوكي، جو.","Mission Control engineers jumping and cheering, throwing papers, hugging.",4,{}),
(11,"والمظلات انفتحت... والمركبة نزلت بالمحيط الهادئ، بيوم سبعطعش نيسان.","Three red and white parachutes lowering the Apollo capsule into the blue Pacific Ocean.",0,{}),
(11,"وطلعوا الثلاثة أحياء... ضعفانين، تعبانين، بس أحياء.","Three tired astronauts on a navy ship deck waving, sailors cheering around them.",2,{}),
(11,"وماتينغلي، اللي نزّلوه من الرحلة... كان من أهم اللي ساعدوا برجعتهم من الأرض.","Astronaut Ken Mattingly in a 1970 simulator room working through procedures, sweating, determined.",1,{}),
(12,"الرحلة فشلت بهدفها... ما نزلوا على الگمر.","A view of the Moon's surface with no footprints, quiet and empty.",0,{}),
(12,"بس صارت أشهر رحلة فضاء... لأنها بينت شنو يگدر يسوي الإنسان لما ما يستسلم.","A modern museum display of the Apollo 13 command module with visitors looking at it.",3,{}),
(12,"شريط لاصق، وكارتون، وعقول ما تيأس... رجعت ثلاث أرواح من الفضا.","Close-up of a roll of grey duct tape and cardboard on a table with the Earth reflected, symbolic.",0,{}),
(12,"انت لو جنت مكان المهندسين، چان تلگى حل؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img:
        if ch == 1: d["prompt"] = G + img + POST
        elif ch == 2: d["prompt"] = G + AST + img + POST
        elif ch == 3: d["prompt"] = G + img + " Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
        elif ch == 4: d["prompt"] = G + MC + img + POST
        else: d["prompt"] = img + NOCH
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
