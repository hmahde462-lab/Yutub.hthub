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
  const EP = 6, TITLE = "الكهرباء راحت";
  const DURATION = 15.1;
  const shots = [{"kind": "wide", "who": null, "t0": 0.0}, {"kind": "gag", "who": null, "t0": 2.6}, {"kind": "close", "who": "hamoudi", "t0": 5.443}, {"kind": "close", "who": "mama", "t0": 7.681}];
  const vo = [{"at": 2.85, "dur": 2.143, "file": "out/l1.wav", "who": "hamoudi", "text": "لا لا لا! الكهرباء راحت قبل الگول!"}, {"at": 5.693, "dur": 1.538, "file": "out/l2.wav", "who": "hamoudi", "text": "يمّه! شغّلي المولدة!"}, {"at": 7.931, "dur": 3.719, "file": "out/l3.wav", "who": "mama", "text": "المولدة للمبردة، مو للبلي! خذ المهفة ونام."}];
  const ev = { gag: 2.6, end: 12.5 };
  const { chords, chordAt } = makeChords(clock, { C: { notes: ['C4','E4','G4'], bass: 'C2' }, Am: { notes: ['A3','C4','E4'], bass: 'A1' }, F: { notes: ['F3','A3','C4'], bass: 'F1' }, G: { notes: ['G3','B3','D4'], bass: 'G1' } },
    Array.from({ length: 12 }, (_, b) => [b, 0, 4, ['C','Am','F','G'][b % 4]]));
  const markers = { gag: { t: ev.gag, sync: 'av' }, end: ev.end };
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, chords, chordAt, EP, TITLE, shots, vo, ev, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
