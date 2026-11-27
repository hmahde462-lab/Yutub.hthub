import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon shoes, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "Caliph al-Ma'mun: black beard, black Abbasid turban, rich dark robe with gold trim. Al-Khwarizmi: grey beard, white turban, blue scholar robe. ")
POST = " Historically accurate 9th century Abbasid Baghdad. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... خليفة يغفى بليلة، ويشوف بالحلم رجال غريب، يگله: آني أرسطو.","Caliph al-Ma'mun sleeping on cushions in a moonlit palace room, a glowing ghostly figure of an ancient Greek philosopher in a toga appearing beside him in a dream.",1,{"sfx":"heart"}),
(1,"يصحى الخليفة، ويقرر: لازم كل علم بالدنيا... يجي لبغداد.","Al-Ma'mun standing at a palace balcony at dawn overlooking Baghdad, determined, pointing toward the horizon.",1,{}),
(1,"قصة بيت الحكمة... المكان اللي غيّر العالم.","",0,{"hud":"title"}),
(1,"شلون مدينة وحدة صارت عاصمة العلم بالعالم كله؟ وشنو اخترعوا بيها؟ وليش لهسه نستخدم شغلهم كل يوم؟ هاي قصة حقيقية.","Old Arabic manuscripts, an astrolabe, an ink pot and a reed pen on a wooden desk lit by an oil lamp.",0,{}),
(2,"بسنة سبعمية واثنين وستين، الخليفة أبو جعفر المنصور بنى مدينة جديدة على دجلة... ودوّرها مثل الدائرة.","Aerial view of the newly built round city of Baghdad in 762 with circular walls, four gates and the Tigris river, golden hour.",0,{"hud":"day","day":"٧٦٢م"}),
(2,"سمّاها: مدينة السلام. وبسرعة صارت أكبر مدينة بالعالم.","Busy Abbasid Baghdad streets full of merchants, camels, boats on the Tigris, domes and minarets.",1,{}),
(2,"وبهديك الأيام، وصل سر جديد من الصين: صناعة الورق.","Workers in an early paper mill pressing pulp into sheets and hanging them to dry, water wheel turning.",1,{}),
(2,"الورق كان أرخص من الجلد بهواية... فصار الكتاب بإيد كل واحد.","A busy Baghdad book market with stalls full of paper books and scribes copying manuscripts.",1,{}),
(3,"هارون الرشيد جمع الكتب بخزانة كبيرة... سمّوها خزانة الحكمة.","Caliph Harun al-Rashid (white turban, brown beard, golden robe) walking among tall shelves of manuscripts with librarians.",1,{}),
(3,"وبعده إجه ابنه المأمون... وكان مجنون بالعلم.","Al-Ma'mun sitting cross-legged reading a large manuscript surrounded by piles of books, eager expression.",1,{}),
(3,"ويگولون، لما انتصر على البيزنطيين، طلب منهم بدل الذهب... كتب!","Al-Ma'mun receiving Byzantine envoys who present chests full of old Greek scrolls instead of gold, his eyes shining.",1,{}),
(3,"وصارت القوافل تجيب كتب من اليونان، والهند، وفارس... لبغداد.","A camel caravan arriving at the gates of Baghdad loaded with chests of scrolls and books, sunset.",1,{}),
(4,"وبيت الحكمة امتلى بالمترجمين: مسلمين، ومسيحيين، وصابئة، وفرس... كلهم بنفس الغرفة.","A large hall in the House of Wisdom with translators of different religions and clothing working together at long tables.",1,{}),
(4,"أشهرهم طبيب مسيحي اسمه حنين بن إسحاق... ترجم كتب الطب اليونانية كلها تقريباً.","Hunayn ibn Ishaq (Christian physician, short dark beard, dark robe and small cap) translating a Greek medical manuscript with anatomical drawings.",1,{}),
(4,"ويگولون المأمون كان يدفعله... وزن الكتاب ذهب.","A brass scale with a book on one side and gold coins on the other, Hunayn and al-Ma'mun watching.",1,{"sfx":"hit"}),
(4,"وبيت الحكمة ما بقى مكتبة بس... صار جامعة، ومختبر، ومرصد.","Scholars debating in a courtyard of the House of Wisdom, some with astrolabes, some drawing geometry in sand.",1,{}),
(5,"وبنص هذا كله، عالم اسمه محمد بن موسى الخوارزمي.","Al-Khwarizmi writing in a manuscript by candlelight, surrounded by geometric drawings and calculations.",1,{}),
(5,"كتب كتاب اسمه: الجبر والمقابلة... أول كتاب يحل المعادلات بطريقة منظمة.","Close-up of al-Khwarizmi's hands drawing squares and geometric diagrams to solve an equation, ink and paper.",1,{}),
(5,"وجاب من الهند فكرة الأرقام والصفر... وكتب عنها كتاب غيّر الحساب للأبد.","Al-Khwarizmi talking with an Indian scholar in a turban, both pointing at numerals written on a board, warm light.",1,{}),
(5,"اليوم، كل طالب يدرس الجبر... يدرس كتاب الخوارزمي من غير ما يدري.","A modern Iraqi classroom with students solving algebra, a ghostly image of al-Khwarizmi standing behind the teacher.",1,{}),
(6,"وثلاث إخوة، اسمهم بنو موسى... كانوا يخترعون آلات ما شافها أحد.","Three young brothers in Abbasid clothes working on brass gears and mechanisms in a workshop.",1,{}),
(6,"كتبوا كتاب الحيل: نافورة تغير شكلها لحالها، وفانوس ما ينطفي، وآلة موسيقية تعزف وحدها.","A brass automatic fountain changing its water shape and a mechanical flute player automaton in a palace garden, people amazed.",1,{}),
(6,"آلة تعزف وحدها... قبل ألف ومية سنة! يعني نوع من البرمجة، قبل الكومبيوتر بقرون.","Close-up of a rotating brass cylinder with pins controlling a mechanical musical instrument, gears turning.",0,{}),
(6,"والناس بالقصر جانوا يتجمعون يتفرجون، مثل ما نتفرج على التكنولوجيا هسه.","Courtiers and children crowding around a mechanical automaton in a palace hall, laughing and amazed.",1,{}),
(7,"وفيلسوف اسمه الكِندي... گالوا عنه فيلسوف العرب.","Al-Kindi (elderly scholar, white beard, grey turban) writing at a desk full of books, thoughtful.",1,{}),
(7,"الكندي كتب بكل شي: الفلسفة، والطب، والموسيقى، والفلك.","Al-Kindi surrounded by an oud, an astrolabe, medicine jars and books, explaining to students.",1,{}),
(7,"بس أغرب شي سواه... فك الرسائل السرية!","A coded letter with strange symbols on a table, al-Kindi studying it with a magnifying lens, candlelight.",1,{"sfx":"heart"}),
(7,"لاحظ إن بعض الحروف تتكرر أكثر من غيرها... وبهاي الطريقة فك الشفرات. وهي نفس الفكرة اللي اشتغلوا بيها بالحرب العالمية بعد ألف سنة.","Al-Kindi counting letter frequencies on a paper with tally marks, a decoded message beside it.",1,{}),
(8,"والمأمون سأل سؤال كبير: شكد حجم الأرض؟","Al-Ma'mun looking at a large globe-like astronomical model with scholars around him, curious.",1,{}),
(8,"دز فريق علماء لصحراء سنجار... ومعاهم حبال وعصي وآلات قياس.","A team of 9th century scholars with ropes, wooden rods and astrolabes walking across a flat desert plain.",1,{}),
(8,"مشوا بالصحراء لحد ما تغير مكان النجمة درجة وحدة... وقاسوا المسافة.","Scholars at night in the desert measuring a star's angle with an astrolabe, stars filling the sky.",1,{}),
(8,"والنتيجة طلعت قريبة هواية من الحقيقة... قبل ما أحد يطلع للفضاء بألف سنة.","The Earth seen from space at sunrise, a faint golden line of measurement drawn across Iraq.",0,{}),
(9,"وبنوا مرصد ببغداد... يراقبون النجوم كل ليلة.","An Abbasid observatory on a hill in Baghdad at night with large stone instruments, scholars looking at the stars.",1,{}),
(9,"وسمّوا نجوم بالعربي... والأسماء بقت لهسه: الدبران، والطائر، ورجل الجبار.","A starry night sky over Baghdad with bright named stars glowing, a scholar pointing at them.",1,{}),
(9,"بغداد ذاك الوقت كانت مثل وادي السيليكون هسه... كل عقل ذكي بالعالم يحلم يجيها.","Travelers from many lands arriving at Baghdad with books under their arms, the city glowing at sunset.",1,{}),
(9,"واستمر هذا العلم مئات السنين...","Wide golden-hour shot of Baghdad and the Tigris with the House of Wisdom glowing, peaceful.",0,{}),
(10,"لحد سنة ألف ومئتين وثمانية وخمسين.","Dark storm clouds over medieval Baghdad, a huge army appearing on the horizon at dusk.",0,{"hud":"day","day":"١٢٥٨م"}),
(10,"المغول، بقيادة هولاكو... حاصروا بغداد ودخلوها.","13th century Mongol horsemen with fur hats and bows storming the gates of Baghdad, smoke and fire.",1,{"sfx":"boom"}),
(10,"حرگوا المدينة، ودمروا بيت الحكمة.","A great library burning, flames climbing the shelves of manuscripts, pages flying in the hot air.",0,{}),
(10,"ويگولون رموا الكتب بدجلة... لحد ما صار الماي أسود من الحبر.","The Tigris river with dark inky water and floating books and manuscripts, smoke over Baghdad.",0,{"sfx":"heart"}),
(11,"بس مو كل شي راح... العالم نصير الدين الطوسي أنقذ آلاف الكتب، وأخذها لمرصد بمراغة.","A 13th century Persian scholar with a grey beard and white turban loading manuscripts onto camels at night, a burning city behind.",1,{}),
(11,"والكتب اللي انترجمت ببغداد، وصلت للأندلس... وبطليطلة رجعوا ترجموها للاتيني.","Medieval scholars translating Arabic manuscripts into Latin at long tables in a stone library in Toledo, candlelight.",1,{}),
(11,"واسم الخوارزمي صار بأوروبا: ألغوريزموس... ومنه طلعت كلمة الخوارزمية.","A medieval European monk reading an Arabic mathematics manuscript by a window, amazed.",1,{}),
(11,"والأرقام اللي تكتب بيها هسه... أوروبا تعلمتها من العرب.","A medieval European merchant learning to write numbers on parchment from an Arab trader, both smiling.",1,{}),
(12,"يعني كل مرة تفتح موبايلك، وكل مرة تحسب... علم بيت الحكمة وياك.","A modern Iraqi young man holding a glowing smartphone, faint golden Arabic manuscripts and geometric diagrams floating around it.",1,{}),
(12,"وبيت الحكمة علمنا شي أكبر من الحساب: لما يشتغل الكل سوا، مهما اختلفوا... يصير المستحيل.","Scholars of different religions and nations shaking hands and smiling in the courtyard of the House of Wisdom, warm sunset.",1,{}),
(12,"وبغداد... جانت قلب العالم.","Aerial view of Baghdad at sunset with the Tigris river, ancient and modern buildings blending.",0,{}),
(12,"بغداد علّمت العالم يقرأ ويحسب. شنو اختراع عربي تعتقد غيّر العالم أكثر؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img: d["prompt"] = (G + img + POST) if ch else (img + NOCH)
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
