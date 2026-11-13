// TOP 10 GAMES IRAQIS LOVE in a Japanese ukiyo-e woodblock look (16:9). Times come from the measured narration.
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
  const DURATION = 148.72;
  const vo = [{"k": 0, "at": 3.2, "dur": 14.519, "file": "out/seg00.wav"}, {"k": 1, "at": 19.919, "dur": 10.344, "file": "out/seg01.wav"}, {"k": 2, "at": 32.463, "dur": 9.851, "file": "out/seg02.wav"}, {"k": 3, "at": 44.514, "dur": 8.444, "file": "out/seg03.wav"}, {"k": 4, "at": 55.158, "dur": 10.018, "file": "out/seg04.wav"}, {"k": 5, "at": 67.376, "dur": 9.386, "file": "out/seg05.wav"}, {"k": 6, "at": 78.962, "dur": 7.958, "file": "out/seg06.wav"}, {"k": 7, "at": 89.12, "dur": 8.673, "file": "out/seg07.wav"}, {"k": 8, "at": 99.994, "dur": 9.79, "file": "out/seg08.wav"}, {"k": 9, "at": 111.983, "dur": 10.148, "file": "out/seg09.wav"}, {"k": 10, "at": 124.332, "dur": 10.225, "file": "out/seg10.wav"}, {"k": 11, "at": 135.756, "dur": 8.966, "file": "out/seg11.wav"}];
  const items = [{"n": 10, "ar": "صب واي سيرفرس", "en": "Subway Surfers", "tag": "لعبة الصف من ورا المعلم", "stamp": 17.719, "at": 19.919, "end": 30.263}, {"n": 9, "ar": "كلاش أوف كلانس", "en": "Clash of Clans", "tag": "تبني سنين ويهدها واحد", "stamp": 30.263, "at": 32.463, "end": 42.314}, {"n": 8, "ar": "ماين كرافت", "en": "Minecraft", "tag": "تبني بيها بغداد كلها", "stamp": 42.314, "at": 44.514, "end": 52.958}, {"n": 7, "ar": "كول أوف ديوتي موبايل", "en": "CoD Mobile", "tag": "صياح بالمايك", "stamp": 52.958, "at": 55.158, "end": 65.176}, {"n": 6, "ar": "فري فاير", "en": "Free Fire", "tag": "تشتغل على موبايل أبوك", "stamp": 65.176, "at": 67.376, "end": 76.762}, {"n": 5, "ar": "فورت نايت", "en": "Fortnite", "tag": "ابني، قاتل، ارقص", "stamp": 76.762, "at": 78.962, "end": 86.92}, {"n": 4, "ar": "براول ستارز", "en": "Brawl Stars", "tag": "منو السبب بالخسارة؟", "stamp": 86.92, "at": 89.12, "end": 97.793}, {"n": 3, "ar": "جي تي أي", "en": "GTA", "tag": "حتى الأمهات يلعبنها!", "stamp": 97.794, "at": 99.994, "end": 109.784}, {"n": 2, "ar": "بيس", "en": "PES / eFootball", "tag": "الخسران يدفع الحساب", "stamp": 109.783, "at": 111.983, "end": 122.131}, {"n": 1, "ar": "ببجي موبايل", "en": "PUBG Mobile", "tag": "مو لعبة… أسلوب حياة", "stamp": 122.132, "at": 124.332, "end": 134.557}];
  const ev = { title: 0.6, introAt: vo[0].at, outroAt: vo[11].at, end: vo[11].at + vo[11].dur + 0.3 };
  const markers = { title: ev.title, outro: ev.outroAt, end: ev.end };
  items.forEach((it) => { markers['n' + it.n] = { t: it.stamp + 0.35, sync: 'av' }; });
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, vo, items, ev, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
