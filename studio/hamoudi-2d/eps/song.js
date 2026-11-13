const path = require('path');
const { SR, Bus } = require('./engine/audio/dsp');
const I = require('./engine/audio/instruments');
const MIX = require('./engine/audio/mix');
const Genre = require('./engine/audio/genres');
const sc = require('./score');
const { DURATION, m, clock, chordAt, ev, EP } = sc;
const N = Math.ceil(DURATION * SR);
const bus = () => new Bus(N);
const drums = bus(), bass = bus(), pad = bus(), keys = bus(), fx = bus(), voice = bus();
const bars = Math.ceil(DURATION / 2) + 1;
Genre.play('chiptune', { clock, from: 0, to: bars, chordAt, buses: { drums, bass, pad, keys }, gain: 0.7 });
const g = ev.gag;
if (EP === 3) { for (let k = 0; k < 6; k++) fx.addMono(I.pulse(m('C6') - k * 3, 0.07, { duty: 0.5 }), g + k * 0.07, 0.22); fx.addMono(I.noiseSweep(0.5, 4000, 300, { q: 1 }), g, 0.25); fx.addMono(I.bwomp(), g + 0.45, 0.4); }
if (EP === 4) { fx.addMono(I.scratch(0.3), g, 0.5); fx.addMono(I.subBoom(0.8, 90, 40), g, 0.5); fx.addMono(I.bwomp(), g + 0.4, 0.4); }
if (EP === 5) { ['C5', 'E5', 'G5', 'C6'].forEach((n, k) => fx.addMono(I.pulse(m(n), k === 3 ? 0.6 : 0.12, { duty: 0.25 }), g + k * 0.12, 0.25)); drums.addMono(I.crash(3), g + 0.36, 0.5); fx.addMono(I.subBoom(1, 80, 35), g + 0.36, 0.5); }
if (EP === 6) { fx.addMono(I.noiseSweep(0.9, 3000, 60, { q: 2 }), g, 0.3); fx.addMono(I.subBoom(1.2, 70, 25), g, 0.6); fx.addMono(I.tvClick(), g, 0.6); }
if (EP === 7) { fx.addMono(I.noiseSweep(0.35, 600, 5000, { q: 1 }), g, 0.25); for (let k = 0; k < 6; k++) fx.addMono(I.pop(1 + k * 0.15), g + 0.1 + k * 0.08, 0.3); fx.addMono(I.bwomp(), g + 0.7, 0.35); }
fx.addMono(I.paperFwip(1.2), ev.end, 0.4);
for (const l of sc.vo) { const b = MIX.loadAudio(path.join(__dirname, l.file), { at: l.at, gain: 1, length: DURATION }); for (let i = 0; i < N; i++) { voice.L[i] += b.L[i]; voice.R[i] += b.R[i]; } }
const music = [drums, bass, pad, keys];
if (EP === 6) for (const b of music) MIX.gate(b, g, ev.end, 0.01); // the power is out: the music dies
MIX.duck(music, voice, { depth: 0.65 });
const stems = { drums, bass, pad, keys, fx, voice };
const GAIN = { drums: 0.7, bass: 0.55, pad: 0.55, keys: 0.55, fx: 1, voice: 2.6 };
const mix = MIX.mixdown(stems, GAIN, {});
MIX.highpass(mix, 30); MIX.fadeOut(mix, DURATION - 0.8, DURATION);
const res = MIX.master(mix, 0.8, undefined, { lufs: -14 });
MIX.writeWav(path.join(__dirname, 'out', 'music.wav'), mix);
console.log('ep', EP, DURATION, res.lufs.toFixed(1));
