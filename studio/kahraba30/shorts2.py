# Cut vertical (1080x1920) Shorts from episode2.mp4 using timeline.json (scene ranges are 1-based, inclusive).
import json, subprocess, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ep2'); os.chdir(D)
tl = json.load(open('timeline.json'))
SH = {'a': (1, 5), 'b': (7, 13), 'c': (14, 19), 'd': (21, 28), 'e': (37, 47), 'f': (48, 54)}
os.makedirs('shorts', exist_ok=True)
for k, (a, b) in SH.items():
    t0 = tl[a-1]['start']; t1 = tl[b-1]['start'] + tl[b-1]['dur']; d = t1 - t0
    vf = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.15[bg];"
          "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-80[v]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', 'episode2.mp4', '-filter_complex', vf, '-map', '[v]', '-map', '0:a',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', f'shorts/k2-{k}.mp4'], check=True)
    print(k, round(d, 1))
