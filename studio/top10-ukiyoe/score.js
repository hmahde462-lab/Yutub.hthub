// TOP 10 IRAQI FOODS in a Japanese ukiyo-e woodblock look (16:9). Times come from the measured narration.
(function () {
  const node = typeof require !== 'undefined';
  const U = node ? require('./engine/util') : globalThis.U;
  const MU = node ? require('./engine/music') : globalThis.MUSIC;
  const { m, makeClock } = MU;
  const FPS = 30, FORMAT = '16:9';
  const [W, H] = U.formatSize(FORMAT);
  const SAFE = U.safeArea(W, H);
  const clock = makeClock({ bpm: 84, offset: 0 });
  const { T, BEAT } = clock;
  const DURATION = 195.12;
  const vo = [{"k": 0, "at": 3.2, "dur": 14.531, "file": "out/seg00.wav"}, {"k": 1, "at": 19.931, "dur": 15.243, "file": "out/seg01.wav"}, {"k": 2, "at": 37.374, "dur": 12.607, "file": "out/seg02.wav"}, {"k": 3, "at": 52.181, "dur": 13.732, "file": "out/seg03.wav"}, {"k": 4, "at": 68.113, "dur": 12.405, "file": "out/seg04.wav"}, {"k": 5, "at": 82.718, "dur": 15.531, "file": "out/seg05.wav"}, {"k": 6, "at": 100.448, "dur": 13.344, "file": "out/seg06.wav"}, {"k": 7, "at": 115.992, "dur": 12.406, "file": "out/seg07.wav"}, {"k": 8, "at": 130.598, "dur": 11.627, "file": "out/seg08.wav"}, {"k": 9, "at": 144.426, "dur": 16.924, "file": "out/seg09.wav"}, {"k": 10, "at": 163.55, "dur": 16.119, "file": "out/seg10.wav"}, {"k": 11, "at": 180.869, "dur": 10.247, "file": "out/seg11.wav"}];
  const items = [{"n": 10, "ar": "لفة الفلافل بالعمبة", "en": "Falafel & Amba", "tag": "أرخص وأطيب ريوگ", "stamp": 17.731, "at": 19.931, "end": 35.174}, {"n": 9, "ar": "التشريب", "en": "Tashreeb", "tag": "أكلة الشتا والبرد", "stamp": 35.174, "at": 37.374, "end": 49.981}, {"n": 8, "ar": "الكليجة", "en": "Kleicha", "tag": "ريحة العيد بالبيت", "stamp": 49.981, "at": 52.181, "end": 65.913}, {"n": 7, "ar": "كبة حلب", "en": "Kubba Halab", "tag": "مقرمشة من برا وطرية من جوة", "stamp": 65.913, "at": 68.113, "end": 80.518}, {"n": 6, "ar": "الباچة", "en": "Pacha", "tag": "أكلة الأبطال الساعة خمسة الصبح", "stamp": 80.518, "at": 82.718, "end": 98.249}, {"n": 5, "ar": "البرياني العراقي", "en": "Iraqi Biryani", "tag": "صينية تشبّع عشيرة", "stamp": 98.248, "at": 100.448, "end": 113.792}, {"n": 4, "ar": "التبسي", "en": "Tepsi", "tag": "أكلة الجمعة", "stamp": 113.792, "at": 115.992, "end": 128.398}, {"n": 3, "ar": "القوزي", "en": "Quzi", "tag": "للضيوف الغالين", "stamp": 128.398, "at": 130.598, "end": 142.225}, {"n": 2, "ar": "الدولمة", "en": "Dolma", "tag": "ملكة المطبخ العراقي", "stamp": 142.226, "at": 144.426, "end": 161.35}, {"n": 1, "ar": "المسگوف", "en": "Masgouf", "tag": "هذا مو أكل… هذا تراث", "stamp": 161.35, "at": 163.55, "end": 179.669}];
  const ev = { title: 0.6, introAt: vo[0].at, outroAt: vo[11].at, end: vo[11].at + vo[11].dur + 0.3 };
  const markers = { title: ev.title, outro: ev.outroAt, end: ev.end };
  items.forEach((it) => { markers['n' + it.n] = { t: it.stamp + 0.35, sync: 'av' }; });
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, vo, items, ev, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
