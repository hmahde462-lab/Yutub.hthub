// Base specs for parts 9-18 (each different weapon + container). tune.js picks spin/g for a ~21s run.
const P = -Math.PI / 2;
module.exports = [
 { id: 'ep09', partLabel: 'الجزء 9', title: 'السيف ضد الكرة ⚔️', hook: 'سيف يدور داخل مربع... شكد يقطع؟', milestone: 50, milestoneText: 'تجاوزنا 50! 🔥', endSub: 'السلاح الجاي: منشار 🪚', bg: ['#1d1430', '#0d0918'],
   sim: { r0: 110, rMin: 10, container: { sides: 4, R: 470, rot: Math.PI / 4, spin: .25 }, cutters: [{ kind: 'sword', len: 315, spin: 1.6 }] } },
 { id: 'ep10', partLabel: 'الجزء 10', title: 'المنشار الدوّار 🪚', hook: 'منشار يلف داخل مسدس... توقع الرقم!', milestone: 100, milestoneText: 'تجاوزنا 100! 🔥', endSub: 'السلاح الجاي: ليزر 🔴', bg: ['#2a1a0e', '#120a04'],
   sim: { r0: 110, rMin: 8, container: { sides: 6, R: 440, rot: 0, spin: 0 }, cutters: [{ kind: 'saw', orbit: 295, rad: 68, spin: 1.4, selfSpin: 18 }] } },
 { id: 'ep11', partLabel: 'الجزء 11', title: 'الليزر ضد الكرة 🔴', hook: 'ليزر داخل مثلث يدور... منو يصمد؟', milestone: 50, milestoneText: 'تجاوزنا 50! 🔥', endSub: 'السلاح الجاي: نجمة نينجا ⭐', bg: ['#0e1a2a', '#04080f'], laserClip: true,
   sim: { cy: 990, r0: 105, rMin: 10, container: { sides: 3, R: 500, rot: P, spin: .35 }, cutters: [{ kind: 'laser', len: 500, spin: 1.0 }] } },
 { id: 'ep12', partLabel: 'الجزء 12', title: 'نجمة النينجا ⭐', hook: 'نجمة تطفر بحرية... وين تضرب؟', milestone: 100, milestoneText: 'تجاوزنا 100! 🔥', endSub: 'السلاح الجاي: مروحة 🌀', bg: ['#14261c', '#06100a'],
   sim: { r0: 110, rMin: 8, container: { sides: 0, R: 420 }, cutters: [{ kind: 'shuriken', rad: 58, x: 120, y: -60, vx: 400, vy: 300, speed: 640, selfSpin: 16 }] } },
 { id: 'ep13', partLabel: 'الجزء 13', title: 'المروحة القاتلة 🌀', hook: '4 شفرات داخل مثمن... شكد تصير؟', milestone: 100, milestoneText: 'تجاوزنا 100! 🔥', endSub: 'الجاي: بدون سلاح... الحيطان تقطع 🧱', bg: ['#26101e', '#10050c'],
   sim: { r0: 110, rMin: 8, container: { sides: 8, R: 440, rot: Math.PI / 8, spin: 0 }, cutters: [{ kind: 'fan', len: 250, blades: 4, spin: 1.3 }] } },
 { id: 'ep14', partLabel: 'الجزء 14', title: 'الحيطان تقطع! 🧱', hook: 'ولا سلاح... كل ضربة بالحايط = كرتين', milestone: 100, milestoneText: 'تجاوزنا 100! 🔥', endSub: 'الجاي: سيفين بعكس بعض ⚔️⚔️', bg: ['#1a1a1a', '#080808'], ringColor: '#ff3d5a',
   sim: { r0: 110, rMin: 8, wallSplit: true, container: { sides: 5, R: 440, rot: P, spin: .5 }, cutters: [] } },
 { id: 'ep15', partLabel: 'الجزء 15', title: 'سيفين بعكس بعض ⚔️⚔️', hook: 'سيف يمين وسيف يسار... الكرة وين تروح؟', milestone: 100, milestoneText: 'تجاوزنا 100! 🔥', endSub: 'الجاي: 3 مناشير 🪚🪚🪚', bg: ['#10202a', '#050c10'],
   sim: { r0: 110, rMin: 8, container: { sides: 4, R: 470, rot: Math.PI / 4, spin: 0 }, cutters: [{ kind: 'sword', len: 315, spin: 1.3, phase: 0 }, { kind: 'sword', len: 315, spin: -1.55, phase: Math.PI }] } },
 { id: 'ep16', partLabel: 'الجزء 16', title: '3 مناشير 🪚🪚🪚', hook: '3 مناشير بثلاث مدارات... شكد تصير؟', milestone: 200, milestoneText: 'تجاوزنا 200! 🔥', endSub: 'الجاي: ليزر متقاطع ➕', bg: ['#2a2410', '#100c04'],
   sim: { r0: 115, rMin: 6, container: { sides: 0, R: 430 }, cutters: [{ kind: 'saw', orbit: 120, rad: 42, spin: 2.0 }, { kind: 'saw', orbit: 230, rad: 52, spin: -1.4, phase: 2 }, { kind: 'saw', orbit: 368, rad: 50, spin: 1.0, phase: 4 }] } },
 { id: 'ep17', partLabel: 'الجزء 17', title: 'ليزر متقاطع ➕', hook: 'ليزرين متقاطعين داخل مسدس يدور!', milestone: 100, milestoneText: 'تجاوزنا 100! 🔥', endSub: 'الجزء الجاي: الزعيم الأخير 👑', bg: ['#1a0e2a', '#08040f'], laserClip: true,
   sim: { r0: 110, rMin: 8, container: { sides: 6, R: 440, rot: 0, spin: -.3 }, cutters: [{ kind: 'laser', len: 440, spin: .9, phase: 0 }, { kind: 'laser', len: 440, spin: .9, phase: Math.PI / 2 }] } },
 { id: 'ep18', partLabel: 'الجزء 18', title: 'الزعيم الأخير 👑', hook: 'سيف + منشار + نجمة نينجا... سوية!', milestone: 200, milestoneText: 'تجاوزنا 200! 🔥', endSub: 'انتهت السلسلة! تريدون موسم 2؟', bg: ['#2a0e0e', '#0f0404'], ringColor: '#ffcf3a',
   sim: { r0: 120, rMin: 6, container: { sides: 0, R: 460 }, cutters: [{ kind: 'sword', len: 250, spin: 1.2 }, { kind: 'saw', orbit: 398, rad: 52, spin: -1.0, phase: 1.5 }, { kind: 'shuriken', rad: 40, x: -200, y: 150, vx: 300, vy: -400, speed: 500 }] } },
];
