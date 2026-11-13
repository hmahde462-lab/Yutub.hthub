const path = require('path');
const { SR, Bus } = require('./engine/audio/dsp');
const I = require('./engine/audio/instruments');
const MIX = require('./engine/audio/mix');
const Genre = require('./engine/audio/genres');
const sc = require('./score');
const { T, BEAT, DURATION, m, ev, clock, chordAt } = sc;
const N = Math.ceil(DURATION * SR);
const bus = () => new Bus(N);
const drums = bus(), bass = bus(), pad = bus(), keys = bus(), fx = bus(), voice = bus();
// sneaking in: tiptoe pizzicato
const sneak = ['A3', 'C4', 'E4', 'C4', 'A3', 'C4', 'E4', 'G#3'];
sneak.forEach((n, i) => fx.addMono(I.pizz(m(n)), 0.2 + i * BEAT * 0.5 + (i > 3 ? 0.2 : 0), 0.35, i % 2 ? 0.3 : -0.3));
fx.addMono(I.paperFwip(1.3), ev.snatch, 0.6);
fx.addMono(I.tvClick(), ev.play - 0.05, 0.5);
// the game: chiptune
Genre.play('chiptune', { clock, from: 1.5, to: 4.5, chordAt, buses: { drums, bass, pad, keys }, gain: 0.8 });
// star dings (rising coins)
ev.stars.forEach((t, i) => { fx.addMono(I.pulse(m('E6') + i * 2, 0.08, { duty: 0.25 }), t, 0.25); fx.addMono(I.pulse(m('B6') + i * 2, 0.18, { duty: 0.25 }), t + 0.08, 0.22); });
// SIX: crash + siren
drums.addMono(I.crash(3), ev.six, 0.6);
fx.addMono(I.subBoom(1, 90, 35), ev.six, 0.6);
for (let k = 0; k < 14; k++) fx.addMono(I.pulse(m(k % 2 ? 'E5' : 'B5'), 0.27, { duty: 0.5, slide: k % 2 ? 5 : -5 }), ev.six + 0.05 + k * 0.28, 0.07);
// slipper: record scratch + whoosh
fx.addMono(I.scratch(0.3), ev.slipper, 0.5);
fx.addMono(I.noiseSweep(0.25, 800, 4000, { q: 1 }), ev.slipper + 0.02, 0.2);
fx.addMono(I.bwomp(), T(7, 1.6), 0.3);
// outro groove
Genre.play('chiptune', { clock, from: 7.5, to: 9.5, chordAt, buses: { drums, bass, pad, keys }, gain: 0.85 });
// dialogue
for (const l of sc.vo) { const b = MIX.loadAudio(path.join(__dirname, l.file), { at: l.at, gain: 1, length: DURATION }); for (let i = 0; i < N; i++) { voice.L[i] += b.L[i]; voice.R[i] += b.R[i]; } }
const music = [drums, bass, pad, keys];
for (const b of music) MIX.gate(b, ev.wake + 0.05, ev.outro - 0.02, 0.01);
MIX.duck(music, voice, { depth: 0.6 });
const stems = { drums, bass, pad, keys, fx, voice };
const GAIN = { drums: 0.8, bass: 0.6, pad: 0.6, keys: 0.6, fx: 1, voice: 2.2 };
const mix = MIX.mixdown(stems, GAIN, { stemDir: process.env.STEMS ? path.join(__dirname, 'out') : null });
MIX.highpass(mix, 30);
MIX.fadeOut(mix, DURATION - 0.8, DURATION);
const res = MIX.master(mix, 0.8, undefined, { lufs: -14 });
MIX.writeWav(path.join(__dirname, 'out', 'music.wav'), mix);
console.log(`out/music.wav ${DURATION.toFixed(1)}s ${res.lufs.toFixed(1)} LUFS`);
