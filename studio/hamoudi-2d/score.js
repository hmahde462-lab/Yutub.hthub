// HAMOUDI & MAMA, PART 2 (9:16, 19s): mama sneaks the controller while Hamoudi sleeps,
// gets six police stars in a made-up car-chase game, Hamoudi wakes up, mama pulls the slipper.
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
  const DURATION = T(9, 2);
  const ev = {
    walkIn: 0.4, snatch: T(1, 1), play: T(1, 2),
    stars: [T(2, 0), T(2, 2), T(3, 0), T(3, 2), T(4, 0)],
    six: T(4, 1), wake: T(4, 2), slipper: T(6, 0), outro: T(7, 2), end: T(8, 1),
  };
  // dialogue: Gemini TTS lines (out/l1..l3.wav), placed here so mouths, captions and audio share times
  const vo = [
    { at: 3.3, dur: 4.05, file: 'out/l1.wav', who: 'mama', text: 'واااو! هاي شنو هاللعبة الحلوة! يلا اركض اركض!' },
    { at: T(4, 2.5), dur: 2.65, file: 'out/l2.wav', who: 'hamoudi', text: 'يمّه! هاي لعبتي! وصلتي ست نجوم!' },
    { at: T(6, 0.6), dur: 2.62, file: 'out/l3.wav', who: 'mama', text: 'اسكت! روح نام، باچر عندك دوام!' },
  ];
  const { chords, chordAt } = makeChords(clock, {
    C: { notes: ['C4', 'E4', 'G4'], bass: 'C2' }, Am: { notes: ['A3', 'C4', 'E4'], bass: 'A1' },
    F: { notes: ['F3', 'A3', 'C4'], bass: 'F1' }, G: { notes: ['G3', 'B3', 'D4'], bass: 'G1' },
  }, [[0, 0, 4, 'Am'], [1, 0, 4, 'Am'], [2, 0, 4, 'C'], [3, 0, 4, 'F'], [4, 0, 4, 'G'], [5, 0, 4, 'Am'], [6, 0, 4, 'F'], [7, 0, 4, 'C'], [8, 0, 4, 'G'], [9, 0, 4, 'C']]);
  const markers = {
    snatch: { t: ev.snatch, sync: 'a' },
    star1: { t: ev.stars[0], sync: 'av' }, star3: { t: ev.stars[2], sync: 'av' }, star5: { t: ev.stars[4], sync: 'av' },
    six: { t: ev.six, sync: 'av' }, wake: ev.wake, slipper: { t: ev.slipper, sync: 'av' }, outro: ev.outro, end: ev.end,
  };
  const SCORE = { FPS, FORMAT, W, H, SAFE, DURATION, clock, T, BEAT, m, chords, chordAt, ev, vo, markers };
  if (node) module.exports = SCORE; else globalThis.SCORE = SCORE;
})();
