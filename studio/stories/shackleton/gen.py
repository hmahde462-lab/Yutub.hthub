import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon boots, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "Ernest Shackleton (the leader, 40): short dark hair parted in the middle, strong jaw, thick dark wool sweater, heavy Burberry gabardine polar jacket, wool balaclava cap. "
 "The crew: 1910s British polar explorers in thick wool sweaters, fur-trimmed windproof jackets, wool hats, mittens, some with beards. ")
POST = " Historically accurate 1914-1916 Antarctic expedition, no modern objects. Cinematic lighting. Wide shot, 16:9, no text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate 1914-1916, 16:9, no text, no logos, no people."
# (part, vo, img, char, extra)
S = [
(1,"تخيّل... سفينتك عالقة بالجليد، بآخر مكان بالأرض. والجليد يعصرها... لحد ما تنكسر وتغرق.","A wooden three-masted sailing ship trapped and crushed by huge pressure ice in the Antarctic, timbers bending, grey sky.",0,{}),
(1,"وانت وثمنية وعشرين رجال... على قطعة ثلج طايفة بالبحر، ومحد بالعالم يعرف وينكم.","The tiny crew standing on a vast floating ice floe, the sinking ship far behind, endless white and dark sea, despair.",1,{"sfx":"heart"}),
(1,"قصة شاكلتون... الرحلة اللي محد رجع منها ميت.","",0,{"hud":"title"}),
(1,"شلون عاشوا أكثر من سنة بالجليد؟ وشنو أكلوا؟ وشلون وصّلوا خبر للعالم... بقارب صغير؟ هاي قصة حقيقية، صارت سنة ألف وتسعمية وأربعطعش.","Old sepia photographs of a polar ship and explorers pinned on a map of Antarctica with a compass and a candle.",0,{}),
(2,"إرنست شاكلتون، مستكشف بريطاني، حلمه يعبر القارة القطبية الجنوبية مشي... من طرف لطرف. شي محد سواه قبله.","Shackleton standing proudly in front of a big map of Antarctica in a London office, pointing at the continent.",1,{}),
(2,"جمع ثمنية وعشرين رجال: بحارة، وعلماء، وطبيب، ونجار... وحتى مصوّر.","Shackleton shaking hands with crew members lining up on a London dock, one holding an old wooden camera, one a toolbox.",1,{}),
(2,"وسفينتهم اسمها: إندورانس... يعني التحمّل. وما كانوا يدرون شكد هالاسم راح يصير حقيقي.","The wooden polar ship Endurance with black hull and three masts docked in a harbour in 1914, flags, crowds.",0,{}),
(2,"طلعوا من بريطانيا بآب، ألف وتسعمية وأربعطعش... ونفس الشهر بدت الحرب العالمية الأولى.","The ship sailing away from an English port while newspaper sellers shout about war, soldiers marching on the quay.",1,{}),
(3,"بعد أشهر بالبحر، وصلوا لبحر ويدل... أبرد وأخطر بحر حول القارة.","The ship pushing through a sea full of floating ice chunks, crew watching from the deck, freezing mist.",1,{}),
(3,"الجليد صار يتكاثف حولهم يوم بعد يوم... والسفينة تمشي أبطأ وأبطأ.","Close view of the ship's bow slowing among thick pack ice, crew with long poles pushing ice away.",1,{}),
(3,"وبكانون الثاني، ألف وتسعمية وخمسطعش... وگفت السفينة. انحبست بالجليد، مثل لوزة بنص شوكولاتة.","The ship completely frozen in a flat white sea of ice, no water visible anywhere, low sun.",0,{"hud":"day","day":"اليوم الأول بالجليد"}),
(3,"وصاروا ينتظرون الصيف حتى يذوب الجليد... بس الجليد ما ذاب.","Crew playing football on the ice next to the frozen ship, Shackleton watching with arms crossed, worried.",1,{}),
(4,"وجا الشتاء القطبي: ظلام أربع أشهر، بدون شمس، والبرد يوصل أربعين تحت الصفر.","The frozen ship at night under a starry sky with aurora, a single lantern glowing in a cabin window.",0,{}),
(4,"وبعدها، الجليد بدا يتحرك... ويضغط على السفينة من كل الجهات.","Huge ice ridges piling up against the ship's wooden hull, cracks forming in the ice.",0,{}),
(4,"صوت الخشب يتكسر كان يشبه صراخ... والسفينة تميل يوم بعد يوم.","Inside the ship's hold, wooden beams bending and splitting, crew watching in fear with lanterns.",1,{"sfx":"hit"}),
(4,"وشاكلتون گال جملة وحدة: السفينة راح تروح.","Shackleton standing on the tilted deck, serious face, looking at the damaged masts.",1,{}),
(5,"بسبعة وعشرين تشرين الأول، ألف وتسعمية وخمسطعش... أمر الكل يطلعون من السفينة.","The crew unloading boxes, sledges and three wooden lifeboats onto the ice beside the tilted ship.",1,{"hud":"day","day":"اليوم ٢٨١"}),
(5,"نزّلوا الخيام، والأكل، وثلاث قوارب نجاة... وگعدوا على الثلج.","Small canvas tents on the ice with the three lifeboats beside them, crew wrapped in blankets.",1,{}),
(5,"وبعد شهر... الجليد عصر السفينة لآخر مرة، وغرقت قدام عيونهم.","The crushed ship sinking through a gap in the ice, stern rising, the crew watching silently in the distance.",1,{"sfx":"boom"}),
(5,"صاروا ثمنية وعشرين رجال... على قطعة جليد طايفة، وأقرب ناس يمهم أكثر من ألف كيلومتر.","Aerial view of the tiny camp on a white ice floe drifting in a huge dark ocean of ice.",0,{}),
(6,"عاشوا على الجليد أشهر... ينامون بالخيام، والثلج يذوب تحتهم بالنهار ويتجمد بالليل.","Crew sleeping crowded in a wet canvas tent on the ice, frost on their beards, dim light.",1,{}),
(6,"أكلوا البطريق والفقمة... وأي شي يلگونه.","Crew cooking penguin and seal meat on a small blubber stove on the ice, penguins walking nearby.",1,{}),
(6,"وشاكلتون جان يمشي بينهم كل يوم، يضحك ويحچي ويا كل واحد... حتى محد يفقد الأمل.","Shackleton laughing with tired crew members around a stove, patting one on the shoulder, encouraging.",1,{}),
(6,"لأنه جان يعرف: إذا انكسرت معنوياتهم... راح يموتون قبل ما يموتون من البرد.","Close-up of Shackleton alone at night outside the tent, worried face, looking at the dark sky.",1,{}),
(7,"وبنيسان، ألف وتسعمية وستطعش... قطعة الجليد اللي عايشين عليها بدت تنشق.","A long crack splitting the ice floe right through the camp, crew jumping back, water appearing.",1,{"sfx":"hit"}),
(7,"نزلوا بالقوارب الثلاثة للبحر... بين موج وجليد يتصادم حولهم.","Three small wooden lifeboats rowing between crashing ice blocks and grey waves, crew rowing hard.",1,{}),
(7,"سبع أيام بالبحر، بدون نوم، مبللين ومتجمدين... وبعض الرجال بدوا يفقدون عقولهم.","Exhausted soaked crew huddled in a lifeboat at night in a storm, ice on their clothes.",1,{}),
(7,"لحد ما شافوا جزيرة صخرية... اسمها جزيرة الفيل.","The lifeboats approaching a rocky snow-covered island with steep black cliffs, dawn light.",1,{}),
(8,"نزلوا على الأرض... لأول مرة من أربعمية وسبعة وتسعين يوم.","Crew stumbling onto a pebble beach, some kneeling and touching the rocks, one laughing with joy.",1,{"hud":"day","day":"٤٩٧ يوم بدون أرض"}),
(8,"بس الفرحة ما طوّلت... الجزيرة بعيدة عن كل طرق السفن، ومحد راح يجي يدور عليهم هنا.","Shackleton standing on the beach looking at the empty stormy horizon, crew behind him.",1,{}),
(8,"فقرر شاكلتون قرار مجنون: ياخذ قارب صغير، ويروح يجيب المساعدة بنفسه.","Shackleton pointing at one of the small lifeboats while crew members look shocked.",1,{}),
(8,"الهدف جزيرة جورجيا الجنوبية، بيها محطة صيد حيتان... بس بينهم ألف وثلثمية كيلومتر، من أخطر بحر بالعالم.","A sea chart showing a tiny island and a long distance across a stormy ocean, a pencil line drawn, candle light.",0,{}),
(9,"أخذ خمس رجال ويا... وقارب طوله سبع أمتار بس، اسمه جيمس كيرد.","Six men pushing a small 7-metre wooden lifeboat into the surf from the rocky beach, others waving.",1,{}),
(9,"وودّع الباقين، وگلهم: راح أرجعلكم.","Shackleton shaking hands with his deputy (thin man with a beard) on the beach as the others watch, emotional.",1,{}),
(9,"ستعش يوم بالبحر... موج بطول بنايات، ورياح تجمّد الماي على القارب، يكسرونه بالفأس حتى ما يغرق.","The small boat climbing a gigantic wave in a storm, men chipping ice off the boat with axes.",1,{}),
(9,"والملاح الوحيد يحسب الطريق بالشمس... اللي ظهرت بس أربع مرات بكل الرحلة.","A navigator holding a sextant up to a brief break of sun in the clouds, standing in the rocking boat.",1,{}),
(10,"وبعد ستعش يوم... شافوا جورجيا الجنوبية!","The exhausted men in the small boat seeing green-black mountains of an island through the mist, joy.",1,{}),
(10,"بس نزلوا بالطرف الغلط من الجزيرة... والمحطة بالطرف الثاني، وبينهم جبال وثلوج محد عبرها قبل.","Shackleton and two men looking up at huge snowy glaciers and jagged peaks from a rocky shore.",1,{}),
(10,"فمشى شاكلتون واثنين ويا... ستة وثلاثين ساعة بدون نوم، بالجبال والثلج، بس بحبل وفأس.","Three tiny figures roped together crossing a vast glacier under the moon, with an ice axe.",1,{}),
(10,"ومن قمة جبل... انزلقوا على الثلج مثل الأطفال، لأنه ما عندهم وقت.","Three men sliding down a steep snow slope sitting on a coiled rope, snow spraying, comic relief.",1,{}),
(11,"وبعشرين أيار... سمعوا صوت صفارة محطة الحيتان. أول صوت بشري من سنة ونص.","The three ragged men on a hill hearing a steam whistle from a whaling station below in a bay.",1,{}),
(11,"دخلوا للمحطة... وجوههم سودة، وشعرهم طويل، وريحتهم ريحة فقمة. والعمال ما عرفوهم.","Three filthy bearded men walking into a 1916 whaling station as shocked workers stare at them.",1,{}),
(11,"مدير المحطة سألهم: منو انتو؟ فجاوب: آني شاكلتون. والرجل بچى.","The whaling station manager in a wool suit staring in disbelief at ragged Shackleton at his doorstep, both emotional.",1,{}),
(11,"بس بعدهم اثنين وعشرين رجال... ينتظرون على جزيرة الفيل.","The stranded men on Elephant Island living under two upturned boats, smoke from a stove, snow.",1,{}),
(12,"حاول يرجعلهم ثلاث مرات... والجليد كل مرة يرجّعه.","A small steamship turning back in front of a wall of pack ice, Shackleton on deck clenching his fist.",1,{}),
(12,"وبالمرة الرابعة، بثلاثين آب، ألف وتسعمية وستطعش... وصل.","A small Chilean steam tug approaching Elephant Island, the men on the beach waving shirts and cheering.",1,{}),
(12,"صاح من القارب: كلكم بخير؟ وجاوبوه: كلنا بخير! ثمنية وعشرين رجال... ولا واحد مات.","Shackleton in a rowing boat near the shore shouting, the men on the beach raising their arms in joy.",1,{}),
(12,"وبألفين واثنين وعشرين، لگوا سفينة إندورانس بقاع البحر، على عمق ثلاث كيلومترات... واسمها بعده مكتوب عليها.","Underwater view of the wooden shipwreck resting on the dark seabed, its stern intact, lit by a submersible light.",0,{}),
(12,"سفينة غرقت... ورجال ما غرقوا. لو انت مكان شاكلتون، جنت تركب القارب؟","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img: d["prompt"] = (G + img + POST) if ch else (img + NOCH)
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
