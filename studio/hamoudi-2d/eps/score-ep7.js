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
  const EP = 7, TITLE = "العيدية";
  const DURATION = 14.38;
  const shots = [{"kind": "wide", "who": null, "t0": 0.0}, {"kind": "close", "who": "mama", "t0": 3.822}, {"kind": "gag", "who": null, "t0": 6.972}, {"kind": "close", "who": "hamoudi", "t0": 8.372}];
  const vo = [{"at": 0.8, "dur": 2.572, "file": "out/l1.wav", "who": "hamoudi", "text": "أخيراً جمعت العيدية! راح أشتري شدّات!"}, {"at": 4.072, "dur": 2.45, "file": "out/l2.wav", "who": "mama", "text": "هاتها حبيبي، أخليها عندي أمانة."}, {"at": 8.622, "dur": 2.31, "file": "out/l3.wav", "who": "hamoudi", "text": "يمّه… هاي نفس أمانة السنة الماضية؟!"}];
  const ev = { gag: 6.972, end: 11.782 };
  const { chords, chordAt } = makeChords(clock, { C: { notes: ['C4','E4','G4'], bass: 'C2' }, Am: { notes: ['A3','C4','E4'], bass: 'A1' }, F: { notes: ['F3','A3','C4'], bass: 'F1' }, G: { notes: ['G3','B3','D4'], bass: 'G1' } },
    Array.from({ length: 12 }, (_, b) => [b, 0, 4, ['C','Am','F','G'][b % 4]]));
  const markers = { gag: { t: ev.gag, sync: 'av' }, end: ev.end };
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, chords, chordAt, EP, TITLE, shots, vo, ev, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
