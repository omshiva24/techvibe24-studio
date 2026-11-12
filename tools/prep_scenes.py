'''Copy the picked candidate of every scene (picks.json: {"c1": "1/A", ...} = release scenes-1, variant A) into www/scn.'''
import json, os, shutil, subprocess, tarfile
picks = json.load(open('picks.json'))
os.makedirs('www/scn/img', exist_ok=True); os.makedirs('www/scn/depth', exist_ok=True)
for rel in sorted({p.split('/')[0] for p in picks.values()}):
    d = f'/tmp/rel{rel}'
    if not os.path.exists(d):
        subprocess.run(['gh', 'release', 'download', f'scenes-{rel}', '-p', 'scenes.tgz', '-D', d, '-R', os.environ['GITHUB_REPOSITORY']], check=True)
        tarfile.open(f'{d}/scenes.tgz').extractall(d)
for sid, p in picks.items():
    rel, v = p.split('/'); src = picks.get(sid)
    base = f'/tmp/rel{rel}'; name = p.split('/', 1)[1]
    cand = name if '_' in name else f'{sid}_{name}'
    shutil.copy(f'{base}/scenes/{cand}.jpg', f'www/scn/img/{sid}.jpg')
    shutil.copy(f'{base}/depth/{cand}.png', f'www/scn/depth/{sid}.png')
print('scenes ready:', len(os.listdir('www/scn/img')))
