(function () {
  const node = typeof require !== 'undefined';
  const U = node ? require('./engine/util') : globalThis.U;
  const MU = node ? require('./engine/music') : globalThis.MUSIC;
  const { m, makeClock, makeChords } = MU;
  const FPS = 30, FORMAT = '9:16';
  const [W, H] = U.formatSize(FORMAT);
  const SAFE = U.safeArea(W, H);
  const clock = makeClock({ bpm: 120, offset: 0 });
  const { T, BEAT } = clock;
  const EP = 4, TITLE = "الشهادة";
  const DURATION = 14.74;
  const shots = [{"kind": "wide", "who": null, "t0": 0.0}, {"kind": "gag", "who": null, "t0": 4.097}, {"kind": "close", "who": "hamoudi", "t0": 5.497}, {"kind": "close", "who": "mama", "t0": 8.259}];
  const vo = [{"at": 0.8, "dur": 2.847, "file": "out/l1.wav", "who": "mama", "text": "حمودي! هاي شنو؟ أربعة من عشرة؟!"}, {"at": 5.747, "dur": 2.062, "file": "out/l2.wav", "who": "hamoudi", "text": "يمّه، المعلم ما يحب الكيمرز!"}, {"at": 8.509, "dur": 2.777, "file": "out/l3.wav", "who": "mama", "text": "من اليوم، البلي ستيشن ينام بالكنتور!"}];
  const ev = { gag: 4.097, end: 12.136 };
  const { chords, chordAt } = makeChords(clock, { C: { notes: ['C4','E4','G4'], bass: 'C2' }, Am: { notes: ['A3','C4','E4'], bass: 'A1' }, F: { notes: ['F3','A3','C4'], bass: 'F1' }, G: { notes: ['G3','B3','D4'], bass: 'G1' } },
    Array.from({ length: 12 }, (_, b) => [b, 0, 4, ['C','Am','F','G'][b % 4]]));
  const markers = { gag: { t: ev.gag, sync: 'av' }, end: ev.end };
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, chords, chordAt, EP, TITLE, shots, vo, ev, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
