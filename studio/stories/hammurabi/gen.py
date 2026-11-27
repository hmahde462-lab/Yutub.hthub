import json
G = ("A 2D cartoon character composited into a photorealistic cinematic scene. Character style: perfectly round plain white head with no ears and no nose, "
 "thick clean black outline, simple black oval eyes with thick angled black eyebrows, small expressive mouth, thin black stick arms and stick legs, black mitten-like hands, "
 "detailed flat-shaded cartoon clothes and chunky cartoon sandals, clean vector cel shading. All people in the image are drawn as these cartoon characters. "
 "King Hammurabi: long curly black Mesopotamian beard, tall rounded royal cap, fringed robe draped over one shoulder. ")
POST = " Historically accurate ancient Babylon, Mesopotamia, around 1750 BC. Cinematic lighting. Wide shot, 16:9, no readable text, no logos."
NOCH = " Cinematic, photorealistic, historically accurate, 16:9, no readable text, no logos, no people."
S = [
(1,"تخيّل... بنّاء يبني بيت، والبيت يوگع ويموت صاحبه. شنو العقوبة؟ الإعدام.","A collapsed mud-brick house in ancient Babylon with dust rising, a shocked builder with tools standing beside the ruins, crowd gathering.",1,{"sfx":"boom"}),
(1,"هذا مو فلم... هذا قانون مكتوب على حجر أسود، بالعراق، قبل ثلاث آلاف وسبعمية سنة.","A tall black basalt stele carved with dense cuneiform writing standing in a temple courtyard under dramatic light.",0,{}),
(1,"قصة حمورابي... أول ملك كتب القانون للناس.","",0,{"hud":"title"}),
(1,"منو حمورابي؟ وشنو جانت قوانينه؟ وليش مسلته الأصلية اليوم... مو بالعراق؟ هاي قصة حقيقية.","Close-up of ancient cuneiform signs carved into dark stone, a hand-held oil lamp lighting them.",0,{}),
(2,"قبل حوالي ألف وثمانمية سنة قبل الميلاد، جانت بابل مدينة صغيرة... قرب الحلة اليوم.","Aerial view of ancient Babylon as a modest walled city by the Euphrates river surrounded by palm groves and fields.",0,{"hud":"day","day":"١٧٩٢ ق.م"}),
(2,"وصار ملكها شاب اسمه حمورابي.","Young King Hammurabi being crowned in a Babylonian temple hall, priests and nobles around him.",1,{}),
(2,"بلاد الرافدين ذاك الوقت جانت مقسمة: كل مدينة إلها ملك، وكلهم يتحاربون على الماي والأرض.","Ancient Mesopotamian soldiers with spears and shields fighting near a canal, rival city walls in the distance.",1,{}),
(2,"وحمورابي، بالحرب والسياسة، وحّدها كلها تحت بابل.","Hammurabi standing on a ziggurat terrace looking over a vast united land with rivers and cities, banners.",1,{}),
(3,"بس المشكلة الكبيرة: كل مدينة إلها قوانينها... وكل قاضي يحكم على كيفه.","A chaotic ancient courtyard where a corrupt judge takes a bribe while a poor farmer protests, crowd arguing.",1,{}),
(3,"الغني يربح دائماً، والفقير يخسر.","A rich merchant laughing with bags of silver while a poor man sits sadly on the ground, ancient Babylon market.",1,{}),
(3,"فقرر حمورابي يسوي شي ما سواه أحد قبله بهالشكل.","Hammurabi sitting on his throne thinking deeply, scribes waiting with clay tablets.",1,{}),
(3,"يكتب القوانين... ويحطها قدام كل الناس، حتى محد يگول ما دريت.","Hammurabi pointing at a large blank black stone while scribes and stone carvers listen.",1,{}),
(4,"نحتوا مية واثنين وثمانين قانون، على مسلة سودة طولها أكثر من مترين.","Stone carvers chiseling cuneiform text into a tall black basalt stele in a workshop, dust and lamps.",1,{}),
(4,"وفوگ المسلة نحتوا صورة: حمورابي واگف گدام إله الشمس والعدالة... شمش.","Close-up of a relief carving showing a king standing before a seated sun god holding a rod and ring, carved stone.",0,{}),
(4,"والرسالة واضحة: القانون مو من ذوقي... القانون عدالة.","Hammurabi standing beside the finished stele in a temple courtyard at sunrise, people gathering to look.",1,{}),
(4,"وحطوا المسلة بمكان عام، وأي واحد عنده مشكلة... يروح يقرا.","Common people, farmers and merchants, gathered around the stele while a scribe reads it aloud to them.",1,{}),
(5,"وأشهر قانون: العين بالعين، والسن بالسن.","Two men arguing in front of a judge in an ancient Babylonian court, one with a bandaged eye.",1,{"sfx":"hit"}),
(5,"بس انتبه... العقوبة جانت تختلف حسب طبقة الشخص: النبيل، والإنسان العادي، والعبد.","Three ancient Babylonians of different classes standing side by side: a richly dressed noble, a common farmer, and a servant, before a judge.",1,{}),
(5,"يعني جان بيه ظلم... بس جان أول مرة القانون ينكتب، ويعرف الكل شنو ينتظرهم.","A scribe reading the law to a crowd while children listen, warm light.",1,{}),
(5,"وأول قوانين بالمسلة؟ إذا اتهمت واحد بجريمة وما گدرت تثبتها... انت تتعاقب.","A false accuser being led away by guards while the accused man looks relieved, ancient court.",1,{}),
(6,"وأكو قوانين للبنّائين: إذا وگع البيت على صاحبه... البنّاء ينعدم.","A builder inspecting mud-brick walls nervously as a judge watches, ancient Babylon construction site.",1,{}),
(6,"وللأطباء: إذا الطبيب عالج مريض وشفى، ياخذ أجرة محددة.","An ancient Babylonian doctor treating a patient's arm with bandages and herbs, the patient grateful.",1,{}),
(6,"بس إذا العملية فشلت ومات المريض... يگطعون إيد الطبيب!","A terrified ancient doctor hiding his hands behind his back as guards approach, comic fear.",1,{"sfx":"hit"}),
(6,"تخيّل لو هالقانون بعده موجود... جان كل طبيب يفكر ألف مرة.","A modern Iraqi doctor in a white coat sweating nervously holding a scalpel, comic.",1,{}),
(7,"وجان أكو قوانين للتجارة: الأسعار، والأجور، والقروض.","A busy ancient Babylonian market with merchants weighing silver and grain on scales.",1,{}),
(7,"حتى أجرة الفلاح، وأجرة النجار، وإيجار القارب... كلها مكتوبة.","A Babylonian farmer receiving grain as wages from a landowner, a carpenter and a boatman waiting in line.",1,{}),
(7,"وللعائلة: الزواج، والطلاق، والميراث.","An ancient Babylonian wedding ceremony with families exchanging gifts, a scribe writing a clay contract.",1,{}),
(7,"والمرأة جان إلها حق تملك أموال، وتدير تجارة... قبل آلاف السنين.","A Babylonian woman merchant confidently selling textiles at her own market stall, customers around.",1,{}),
(8,"وأكو قانون غريب: إذا اتهموا واحد بالسحر، يرمونه بالنهر.","A crowd on a river bank watching an accused man being led toward the Euphrates, tense.",1,{}),
(8,"إذا غرق... جان مذنب. وإذا طلع سالم... بريء، والمتهِم ينعدم.","The accused man emerging from the river alive while the crowd gasps and points at the accuser.",1,{"sfx":"heart"}),
(8,"يعني النهر جان هو القاضي!","Wide shot of the Euphrates river at sunset with ancient Babylon on its banks.",0,{}),
(8,"قوانين بعضها قاسية... بس جانت خطوة كبيرة: إن الحاكم نفسه يلتزم بقانون مكتوب.","Hammurabi touching the stele respectfully, standing among his people, solemn.",1,{}),
(9,"حمورابي حكم ثنعش وأربعين سنة، ومات حوالي ألف وسبعمية وخمسين قبل الميلاد.","An elderly Hammurabi with a grey beard sitting on his throne, tired, the sun setting through the palace window.",1,{"hud":"day","day":"١٧٥٠ ق.م"}),
(9,"وبعد موته بمئات السنين... بابل ضعفت.","Ancient Babylon walls partly crumbling, sandstorm, abandoned streets.",0,{}),
(9,"ملك عيلامي اسمه شوتروك ناخونتي هجم على بلاد الرافدين...","An Elamite army with chariots attacking a Mesopotamian city, smoke rising.",1,{"sfx":"boom"}),
(9,"وأخذ المسلة غنيمة حرب... لمدينة سوسة، بإيران اليوم.","Soldiers dragging the tall black stele on wooden rollers across the desert toward a distant city.",1,{}),
(10,"وهناك... اندفنت تحت التراب. ونسيها العالم ثلاث آلاف سنة.","The black stele lying buried in sand and ruins, only its top visible, centuries passing, desert.",0,{}),
(10,"لحد سنة ألف وتسعمية وواحد... بعثة فرنسية تحفر بسوسة.","1901 French archaeologists in pith helmets digging in an ancient mound with local workers.",1,{"hud":"day","day":"١٩٠١م"}),
(10,"لگوا قطع حجر أسود... ولما ركبوها، انصدموا.","Archaeologists brushing dust off broken pieces of the black stele, astonished expressions.",1,{"sfx":"heart"}),
(10,"جانت مسلة حمورابي! أقدم مجموعة قوانين كاملة وصلتنا تقريباً.","The reassembled black stele standing upright in an excavation tent, archaeologists gathered around in awe.",1,{}),
(11,"أخذوها لفرنسا... واليوم هي موجودة بمتحف اللوفر بباريس.","The tall black stele displayed in a museum hall in Paris with tourists looking at it.",1,{}),
(11,"وملايين الناس يزورونها كل سنة... بس الأصل مو بالعراق.","Crowds of tourists photographing the black stele in a museum, an Iraqi visitor among them looking sad.",1,{}),
(11,"وبالمتحف العراقي ببغداد أكو نسخة منها.","A replica of the black stele in the Iraq Museum in Baghdad with Iraqi schoolchildren visiting.",1,{}),
(11,"وصورة حمورابي اليوم محفورة حتى ببرلمانات بالعالم... لأنه من أوائل اللي كتبوا القانون.","A marble relief portrait of an ancient bearded lawgiver on the wall of a grand modern government chamber.",0,{}),
(12,"حمورابي علّم العالم فكرة بسيطة: القانون لازم يكون مكتوب، ويعرفه الكل.","Hammurabi standing beside his stele with people of many eras around him, symbolic warm light.",1,{}),
(12,"ومن بابل... بدت فكرة إن الحاكم مو فوق القانون.","Aerial view of the ruins of ancient Babylon near Hillah today at sunset, the Euphrates nearby.",0,{}),
(12,"وكل محكمة بالعالم اليوم... بيها شوية من حجر حمورابي.","A modern courtroom with a judge's bench, a shadow of the ancient stele projected on the wall.",0,{}),
(12,"قانون عمره ثلاث آلاف وسبعمية سنة... تتوقع لازم المسلة ترجع للعراق؟ اكتبها بالتعليقات.","",0,{"hud":"black","sfx":"boom"}),
]
out = []
for p, vo, img, ch, ex in S:
    d = {"vo": vo, "img": img, "part": p}
    if img: d["prompt"] = (G + img + POST) if ch else (img + NOCH)
    d.update(ex); out.append(d)
json.dump(out, open('script.json', 'w'), ensure_ascii=False, indent=1)
open('vo.txt', 'w').write('\n\n'.join(x['vo'] for x in out) + '\n')
print(len(out), sum(len(x['vo']) for x in out))
