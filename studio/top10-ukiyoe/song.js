const path = require('path');
const { SR, Bus, reverb } = require('./engine/audio/dsp');
const I = require('./engine/audio/instruments');
const MIX = require('./engine/audio/mix');
const U = require('./engine/util');
const sc = require('./score');
const { DURATION, m, clock, BEAT, items, ev } = sc;
const N = Math.ceil(DURATION * SR);
const bus = () => new Bus(N);
const koto = bus(), pad = bus(), perc = bus(), fx = bus(), verb = bus(), voice = bus();
const rng = U.mulberry32(9);
// Japanese "in" scale on D, borrowed for a calm koto line
const scale = ['D4', 'Eb4', 'G4', 'A4', 'Bb4', 'D5', 'Eb5', 'G5'].map(m);
let idx = 3;
for (let t = 1.5; t < DURATION - 3; t += BEAT / 2) {
  if (rng() < 0.42) {
    idx = Math.max(0, Math.min(scale.length - 1, idx + Math.round((rng() - 0.5) * 3)));
    const g = I.guitar(scale[idx], 1.6, { bright: 0.7, sustain: 0.6, seed: Math.floor(t * 10) });
    koto.addMono(g, t, 0.16, (rng() - 0.5) * 0.6); verb.addMono(g, t, 0.06);
  }
}
// drone pad, chord every 4 bars
for (let t = 0; t < DURATION; t += BEAT * 16) for (const n of ['D3', 'A3', 'Eb4']) { const { L, R } = I.padNote(m(n), BEAT * 16 + 1, { cutoff: 900, attack: 2, release: 2 }); pad.addStereo(L, R, t, 0.05); }
// soft shaker pulse
for (let t = 4; t < DURATION - 4; t += BEAT) perc.addMono(I.shaker(0.3), t, 0.05, 0.3);
const taiko = (t, g = 1) => { perc.addMono(I.tom(70, 0.6), t, 0.7 * g); perc.addMono(I.kick({ punch: 0.8, tail: 0.6 }), t, 0.5 * g); fx.addMono(I.subBoom(0.7, 80, 40), t, 0.3 * g); verb.addMono(I.tom(70, 0.6), t, 0.2 * g); };
// title: gong + taiko
taiko(ev.title, 1.2); fx.addMono(I.bell(110, 4, 2.4, 1.41), ev.title, 0.25);
// each number: woodblock clacks, a koto sweep up, then the taiko on the stamp
for (const it of items) {
  const hit = it.stamp + 0.35;
  for (let k = 0; k < 3; k++) fx.addMono(I.woodTick(1.6 + k * 0.1), it.stamp - 0.6 + k * 0.12, 0.25);
  scale.forEach((n, k) => koto.addMono(I.guitar(n, 0.8, { bright: 0.9, seed: k }), it.stamp - 0.3 + k * 0.035, 0.1));
  taiko(hit, it.n === 1 ? 1.4 : 1);
  if (it.n === 1) fx.addMono(I.bell(98, 5, 2.4, 1.41), hit, 0.3);
}
taiko(ev.outroAt - 0.6, 0.8);
// narration
for (const l of sc.vo) { const b = MIX.loadAudio(path.join(__dirname, l.file), { at: l.at, gain: 1, length: DURATION }); for (let i = 0; i < N; i++) { voice.L[i] += b.L[i]; voice.R[i] += b.R[i]; } }
const room = reverb(verb, { room: 0.8, damp: 0.5 });
MIX.duck([koto, pad, perc], voice, { depth: 0.5 });
const stems = { koto, pad, perc, fx, voice, verb: room };
const GAIN = { koto: 4, pad: 2, perc: 1, fx: 1, voice: 2.4, verb: 0.5 };
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? path.join(__dirname, 'out') : null });
MIX.highpass(mix, 30);
MIX.fadeOut(mix, DURATION - 2.5, DURATION);
const res = MIX.master(mix, 0.8, undefined, { lufs: -14 });
MIX.writeWav(path.join(__dirname, 'out', 'music.wav'), mix);
console.log(`music ${DURATION}s ${res.lufs.toFixed(1)} LUFS`);
