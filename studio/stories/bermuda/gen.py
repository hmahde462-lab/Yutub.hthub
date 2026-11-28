import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. ")
PIL = "US Navy pilots in 1945: khaki flight suits, leather flight helmets with goggles, yellow life vests. The leader Lt. Charles Taylor has dark hair and a thin moustache. "
RAD = "A 1945 US Navy radio room in Florida: radio operators with big headphones, old valve radios, a wall map of Florida and the Bahamas. "
POST = " Historically accurate 1945. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... خمس طيارات حربية، طالعة بتدريب عادي، بيوم مشمس. وبعد ساعتين، القائد يصيح بالراديو: ما أعرف وين إحنا!","Five 1945 US Navy TBM Avenger torpedo bombers flying in formation over a bright turquoise sea, seen from above.",0,{}),
(1,"وبعدها... ولا طيارة رجعت. ولا ولا جثة. ولا ولا قطعة حديد.","An empty dark ocean at dusk under heavy clouds, no trace of anything, ominous.",0,{}),
(1,"الرحلة تسعطعش... ولغز مثلث برمودا.","",0,{"hud":"title","sfx":"boom"}),
(1,"منطقة بالبحر، يگولون تبلع الطيارات والسفن... بس شنو اللي صار بالضبط؟ هاي قصة حقيقية.","An old nautical map with a triangle drawn between Florida, Bermuda and Puerto Rico, a compass and a pencil on it.",0,{}),
(2,"خمسة كانون الأول، ألف وتسعمية وخمسة وأربعين... الحرب العالمية الثانية توها خالصة.","A 1945 US Navy air station in Fort Lauderdale, Florida, with palm trees and rows of Avenger planes on the tarmac, sunny afternoon.",0,{"hud":"day","day":"١٩٤٥م"}),
(2,"وبقاعدة بحرية بفلوريدا، أربعطعش طيار وفني صعدوا بخمس طيارات اسمها أفنجر.","Fourteen US Navy airmen walking across the tarmac toward five Avenger torpedo bombers, carrying helmets.",1,{}),
(2,"قائدهم الملازم تشارلز تايلر... طيار خبرة، عنده آلاف الساعات بالجو، وحارب بالمحيط الهادئ.","Lt. Charles Taylor, a confident experienced pilot with a thin moustache, standing in front of his plane, arms crossed.",1,{}),
(2,"بس هذا اليوم جان متضايق... وطلب ياخذ تدريب غيره. وطلبه انرفض.","Lt. Charles Taylor talking to an officer at a desk, looking uneasy, the officer shaking his head.",1,{}),
(3,"الخطة سهلة: يطيرون شرق للبحر، يرمون قنابل تدريب، يلفون شمال، وبعدين يرجعون غرب للقاعدة. ساعتين بالكثير.","A pilot's briefing board with a simple triangular flight route drawn over the sea east of Florida, a pointer stick.",1,{}),
(3,"الساعة ثنين وعشر دقايق الظهر... طارت الخمس طيارات... والجو صافي، والبحر هادي، ومحد متوقع أي شي.","Five Avenger planes taking off one by one from the runway into a clear blue sky.",0,{}),
(3,"وأول جزء مشى تمام... رموا القنابل، وضحكوا بالراديو.","Avenger planes dropping small practice bombs on a tiny shipwreck target in shallow turquoise water, splashes.",0,{}),
(3,"وبعدين... صار شي غريب.","Close-up of a 1945 aircraft cockpit compass needle spinning slowly, sunlight on the glass.",0,{}),
(4,"الساعة ثلاثة وأربعين... الراديو بالقاعدة سمع صوت تايلر: البوصلات مالتي الثنتين عاطلات!","Inside the cockpit, Lt. Charles Taylor tapping a broken compass with a worried face, talking into the radio microphone.",1,{}),
(4,"وگال: آني فوق جزر... بس ما أعرف وين. أعتقد إحنا فوق جزر فلوريدا الجنوبية.","View from a cockpit window of small green islands and reefs below in a vast turquoise sea.",0,{}),
(4,"بس الحقيقة... هو جان فوق جزر البهاما، بالجهة الثانية تماماً.","A cinematic aerial view of the Bahamas islands, white sand and shallow water, beautiful but confusing from the air.",0,{}),
(4,"فتايلر قرر يطير شمال شرق... يعني بالضبط عكس الطريق، باتجاه نص المحيط.","Five Avenger planes turning together in the sky, heading away from land toward open dark ocean.",0,{}),
(5,"وبالراديو، الطيارين الشباب كانوا يتهامسون: لو نطير غرب... چان وصلنا.","A young pilot in his cockpit looking at the sun and pointing west, frustrated, talking into his radio.",1,{}),
(5,"بس محد تجرأ يخالف القائد... بالجيش، القائد هو القائد.","Two young pilots in separate cockpits exchanging worried looks through their windows, flying side by side.",1,{}),
(5,"وبالقاعدة، الكل صار يحاول يحدد مكانهم بالراديو... بس الإشارة ضعيفة، ويضيع بيها الصوت.","Radio operators in headphones leaning over valve radios, writing notes quickly, tense.",2,{}),
(5,"وأكو طيار ثاني بالجو سمعهم، وگال لتايلر: خلّي الشمس على يسارك، وطير... بس الإشارة انقطعت.","Another pilot in a different plane talking urgently on the radio, static lines around the radio speaker.",1,{}),
(6,"الساعات تمشي... والشمس صارت تنزل، والجو صار يخرب، والموج يكبر.","Dark storm clouds gathering over a rough grey ocean at sunset, wind whipping the waves.",0,{}),
(6,"وتايلر غيّر الاتجاه مرة غرب، ومرة شرق... ضايع بين قراره وقرار طياريه. والقاعدة تسمعهم، بس ما تگدر توصلهم.","Five planes flying in a zigzag through grey clouds over a dark sea, tiny against the sky.",0,{}),
(6,"والبانزين... كل دقيقة يخلص أكثر.","Close-up of an aircraft fuel gauge needle near empty, red warning mark, vibrating.",0,{}),
(6,"وبالساعة ستة وعشرين... تايلر گال الجملة اللي ظلت لهسه: كلنا راح ننزل سوية... لما توصل أي طيارة لعشر غالونات.","Lt. Charles Taylor in his dim cockpit at dusk speaking calmly into the radio, determined but sad.",1,{}),
(7,"وبعدها بشوية... آخر كلمات وصلت بالراديو. وبعدين: سكوت.","A radio operator in the 1945 radio room slowly taking off his headphones, shocked, silent room.",2,{}),
(7,"الساعة سبعة بالليل... الطيارات مختفية بنص المحيط المظلم.","A pitch-black stormy ocean at night with high waves and rain, no lights anywhere.",0,{}),
(7,"وفوراً، طلعت طيارات بحث... وحدة منهن جبيرة، طيارة مائية اسمها مارينر، بيها ثلطعش رجال.","A big 1945 PBM Mariner flying boat taking off from the water at night, spray behind it, searchlights.",0,{}),
(7,"وبعد عشرين دقيقة من طيرانها... سفينة شافت نار جبيرة بالسما، وبقعة بانزين تحترگ على الماي.","Sailors on a ship deck at night pointing at a huge fireball in the distant sky reflected on the black sea.",3,{"sfx":"boom"}),
(8,"والمارينر هم اختفت. ثلطعش رجال ثانيين... راحوا.","Burning oil on the dark ocean surface at night, flames on the waves, nothing else left.",0,{}),
(8,"يعني بليلة وحدة... ست طيارات، وسبعة وعشرين رجال. والبحر بلعهم كلهم.","Six empty pilot chairs in a dim 1945 briefing room, helmets left on them, sad atmosphere.",0,{}),
(8,"وبالأيام الجاية، صارت أكبر عملية بحث بتاريخ ذاك الوقت: مئات الطيارات والسفن.","Dozens of navy ships and planes searching a wide calm ocean in daylight, aerial view.",0,{}),
(8,"خمس أيام يدورون... وما لگوا ولا شي. ولا قطعة وحدة، ولا بقعة زيت، ولا سترة نجاة.","Navy sailors on a ship deck scanning the empty sea with binoculars, disappointed.",3,{}),
(9,"الجيش بالأول لام تايلر... گالوا ضاع، وضيّع ويا الباقين.","A stern navy officer reading a report at a long table to other officers in 1945, serious faces.",3,{}),
(9,"بس أمه رفضت... وگالت: ابني ما يضيع بالجو. وحاربت سنين حتى يغيرون التقرير.","Lt. Taylor's mother, an elderly woman in a 1940s dress, holding his photo and arguing firmly with navy officers.",3,{}),
(9,"وبالأخير، غيروه... وكتبوا: السبب مجهول.","Close-up of an old typewritten navy report with a stamp, a hand signing it, dramatic light.",0,{}),
(9,"وهالكلمتين... سووا أكبر أسطورة بالبحر.","A misty ocean with a glowing triangle shape faintly visible in the clouds, mysterious, cinematic.",0,{}),
(10,"بالستينات، كاتب أمريكي سمّى المنطقة: مثلث برمودا. وصار يجمع كل سفينة وطيارة اختفت هناك.","A 1960s writer typing in a smoky office surrounded by newspaper clippings of lost ships and planes pinned to the wall.",3,{}),
(10,"وطلعت كتب، وأفلام، ونظريات: ناس گالوا مغناطيس غريب، وناس گالوا مدينة أتلانتس الغرقانة...","A dramatic cinematic illustration of a ruined ancient city glowing under the deep sea, light beams.",0,{}),
(10,"وناس وصلت تگول: كائنات فضائية خطفتهم! حتى فلم مشهور طلّع الطيارات الخمسة بنص الصحرا.","Five old WWII planes sitting mysteriously in a desert at night under a bright light from the sky, sand blowing.",0,{}),
(10,"بس العلماء عدهم رأي ثاني.","A modern scientist in a lab coat looking at ocean maps and weather charts on a big screen, calm.",3,{}),
(11,"أولاً: هاي المنطقة من أزحم مناطق البحر بالعالم... فطبيعي تصير بيها حوادث أكثر.","A modern satellite view of busy ship and airplane traffic lines over the Atlantic near Florida.",0,{}),
(11,"والجو بيها يتقلب بسرعة... عواصف مفاجئة، وتيار الخليج القوي يسحب أي شي بسرعة لبعيد.","A powerful ocean current shown with foam lines and sudden storm clouds over the Atlantic.",0,{}),
(11,"وطيارات الأفنجر ثقيلة... إذا نزلت بالبحر بالليل وبالموج العالي، تغرق بأقل من دقيقة.","A heavy Avenger plane splashing down into huge dark waves at night, sinking quickly, spray.",0,{}),
(11,"والمارينر؟ جانوا يسمونها: خزان بانزين طاير... لأن أي شرارة تفجرها.","Close-up of an old aircraft fuel line leaking near a spark, cinematic macro, danger.",0,{}),
(12,"وبالتسعينات، لگوا خمس طيارات أفنجر بقاع البحر قرب فلوريدا... والكل گال: لگيناهم!","Underwater divers with lights finding the wreck of an old Avenger plane on the sandy sea floor.",3,{}),
(12,"بس طلعت طيارات ثانية... مو هي. والرحلة تسعطعش، لهسه محد لگاها.","Close-up of an old plane wreck under water covered with corals, a diver's light on it, fish around.",0,{}),
(12,"يمكن مو مثلث ملعون... يمكن قائد ضايع، وبحر ما يرحم، وليل طويل.","Five small planes flying into a dark sunset over the ocean, silhouettes, quiet and sad.",0,{}),
(12,"وانت؟ تصدّق بلعنة مثلث برمودا، لو بالعلم؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img:
        if ch == 1: d["prompt"] = G + PIL + img + POST
        elif ch == 2: d["prompt"] = G + RAD + img + POST
        elif ch == 3: d["prompt"] = G + img + " Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
        else: d["prompt"] = img + NOCH
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
