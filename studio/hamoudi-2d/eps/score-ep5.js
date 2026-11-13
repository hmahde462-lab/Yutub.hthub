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
  const EP = 5, TITLE = "ماما الپرو";
  const DURATION = 13.92;
  const shots = [{"kind": "wide", "who": null, "t0": 0.0}, {"kind": "close", "who": "mama", "t0": 4.136}, {"kind": "gag", "who": null, "t0": 6.497}, {"kind": "close", "who": "mama", "t0": 7.897}];
  const vo = [{"at": 0.8, "dur": 2.886, "file": "out/l1.wav", "who": "hamoudi", "text": "يمّه، خليني ألعب دورة وحدة بس!"}, {"at": 4.386, "dur": 1.661, "file": "out/l2.wav", "who": "mama", "text": "اسكت! آني وخالتك بنص الفايت!"}, {"at": 8.147, "dur": 2.327, "file": "out/l3.wav", "who": "mama", "text": "وينر وينر! دجاج للعشا!"}];
  const ev = { gag: 6.497, end: 11.324 };
  const { chords, chordAt } = makeChords(clock, { C: { notes: ['C4','E4','G4'], bass: 'C2' }, Am: { notes: ['A3','C4','E4'], bass: 'A1' }, F: { notes: ['F3','A3','C4'], bass: 'F1' }, G: { notes: ['G3','B3','D4'], bass: 'G1' } },
    Array.from({ length: 12 }, (_, b) => [b, 0, 4, ['C','Am','F','G'][b % 4]]));
  const markers = { gag: { t: ev.gag, sync: 'av' }, end: ev.end };
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, chords, chordAt, EP, TITLE, shots, vo, ev, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
