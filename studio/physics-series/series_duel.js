// Series 3 "القتال": named balls with 100 HP and random weapons. d08 & d10 are filled from earlier winners by tune_duel.js.
const P = Math.PI;
const ALL = ['sword', 'knife', 'axe', 'hammer', 'spear', 'saw', 'heal', 'shield', 'bomb', 'speed'];
module.exports = [
 { id: 'd01', title: 'معركة البطوطات', hook: 'منو تتوقع يفوز؟ اختار قبل لا تبدي!', endSub: 'توقعك صح؟ اكتبه بالتعليقات', bg: ['#1d1036', '#07040f'], floor: '#24173f',
   fighters: [['الزلبوط', '#ff5a5a'], ['علبوط', '#4f9dff'], ['بلبوط', '#3fd17a'], ['بوط', '#ffd23b']], sim: { R: 430, pool: ALL } },
 { id: 'd02', title: 'نزال السيوف', hook: 'سيوف وفؤوس ودروع... منو يصمد؟', endSub: 'منو كنت تشجع؟ اكتبه', bg: ['#2a1206', '#0c0502'], floor: '#3a2410', ring: '#ffcf3a',
   fighters: [['فرفوط', '#ff8a3a'], ['قرقوط', '#b36bff']], sim: { sides: 4, rot: P / 4, R: 450, r: 60, pool: ['sword', 'sword', 'axe', 'shield', 'heal', 'knife'] } },
 { id: 'd03', title: 'حرب السكاكين', hook: '3 كرات وسكاكين ورماح!', endSub: 'منو البطل؟ اكتبه بالتعليقات', bg: ['#0a2420', '#020c0a'], floor: '#123a33',
   fighters: [['دعبول', '#2fd3e0'], ['كعبول', '#ff4b6e'], ['زعطوط', '#f2c230']], sim: { sides: 6, rot: 0, R: 440, pool: ['knife', 'knife', 'spear', 'spear', 'heal', 'shield', 'speed'] } },
 { id: 'd04', title: 'حرب القنابل', hook: 'قنابل ومناشير... احذر!', endSub: 'منو نجا من القنابل؟ اكتبه', bg: ['#2a0a0a', '#0c0202'], floor: '#3a1414', ring: '#ff3d5a',
   fighters: [['طرطور', '#ff8a3a'], ['بقبوق', '#4f9dff'], ['فلفول', '#3fd17a'], ['كشكوش', '#e070ff']], sim: { sides: 8, rot: P / 8, R: 440, pool: ['bomb', 'bomb', 'saw', 'saw', 'heal', 'shield'] } },
 { id: 'd05', title: 'الأوزان الثقيلة', hook: 'فؤوس ومطارق بس! ضربة وحدة تفرق', endSub: 'منو أقوى؟ اكتبه', bg: ['#14161c', '#050608'], floor: '#22262e', ring: '#c0c8d0',
   fighters: [['الدبدوب', '#a0703f'], ['الفرفور', '#ff5a8a']], sim: { R: 430, r: 64, pool: ['axe', 'hammer', 'hammer', 'axe', 'shield', 'heal'] } },
 { id: 'd06', title: 'المثلث القاتل', hook: '3 كرات بمربع... وحدة بس تطلع حية', endSub: 'توقعك صح؟ اكتبه', bg: ['#10202e', '#04080c'], floor: '#1a3040',
   fighters: [['قمقم', '#ffd23b'], ['دمدم', '#ff4b4b'], ['همهم', '#3b8bff']], sim: { sides: 4, rot: 0, R: 470, pool: ['sword', 'spear', 'saw', 'axe', 'heal', 'shield', 'bomb', 'speed'] } },
 { id: 'd07', title: 'الحلبة تصغر!', hook: 'كل ثانية الحلبة تضيق... منو يصمد؟', endSub: 'شفت شلون ضاقت؟ اكتب الفايز', bg: ['#26101e', '#0a0408'], floor: '#3a1a2e', ring: '#ff3d5a',
   fighters: [['شنكول', '#ff5a5a'], ['منكول', '#4f9dff'], ['زنكول', '#3fd17a'], ['فنكول', '#ffd23b']], sim: { R: 450, shrinkFrom: 6, shrinkTo: 260, shrinkDur: 16, pool: ALL } },
 { id: 'd08', title: 'الثأر!', hook: 'الخسران رجع ينتقم... ينجح؟', endSub: 'نجح الثأر؟ اكتب رأيك', bg: ['#2a0e1a', '#0c0408'], floor: '#3a1426', rematch: 'd01',
   sim: { sides: 6, rot: P / 6, R: 440, r: 60, pool: ALL } },
 { id: 'd09', title: 'معركة المناشير', hook: 'كل الأسلحة مناشير! ⚙️', endSub: 'منو عاش؟ اكتبه بالتعليقات', bg: ['#1e2410', '#080a04'], floor: '#2e3818',
   fighters: [['عنطوز', '#ff8a3a'], ['شنطوز', '#2fd3e0'], ['فنطوز', '#b36bff'], ['زنطوز', '#f2c230']], sim: { sides: 5, rot: -P / 2, R: 450, pool: ['saw', 'saw', 'saw', 'heal', 'shield', 'speed'] } },
 { id: 'd10', title: 'بطولة الأبطال 👑', hook: 'أبطال السلسلة كلهم... بطل واحد بس!', endSub: 'هذا بطل الموسم! تريدون موسم 2؟', bg: ['#2a2008', '#0c0902'], floor: '#3a2e10', ring: '#ffcf3a', champions: ['d01', 'd03', 'd04', 'd07'],
   sim: { R: 460, pool: ALL } },
];
