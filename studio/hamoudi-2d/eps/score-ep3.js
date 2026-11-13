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
  const EP = 3, TITLE = "الراوتر";
  const DURATION = 15.65;
  const shots = [{"kind": "wide", "who": null, "t0": 0.0}, {"kind": "gag", "who": null, "t0": 3.573}, {"kind": "close", "who": "hamoudi", "t0": 4.973}, {"kind": "close", "who": "mama", "t0": 8.758}];
  const vo = [{"at": 0.8, "dur": 2.323, "file": "out/l1.wav", "who": "hamoudi", "text": "يلا يلا! باقي واحد ونفوز!"}, {"at": 5.223, "dur": 3.085, "file": "out/l2.wav", "who": "hamoudi", "text": "يمّه! ليش طفيتي الراوتر؟! آني بنص الماتش!"}, {"at": 9.008, "dur": 3.191, "file": "out/l3.wav", "who": "mama", "text": "ماتش؟ قوم اشتري خبز، الماتش يخلص بروحه!"}];
  const ev = { gag: 3.573, end: 13.049 };
  const { chords, chordAt } = makeChords(clock, { C: { notes: ['C4','E4','G4'], bass: 'C2' }, Am: { notes: ['A3','C4','E4'], bass: 'A1' }, F: { notes: ['F3','A3','C4'], bass: 'F1' }, G: { notes: ['G3','B3','D4'], bass: 'G1' } },
    Array.from({ length: 12 }, (_, b) => [b, 0, 4, ['C','Am','F','G'][b % 4]]));
  const markers = { gag: { t: ev.gag, sync: 'av' }, end: ev.end };
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, chords, chordAt, EP, TITLE, shots, vo, ev, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
