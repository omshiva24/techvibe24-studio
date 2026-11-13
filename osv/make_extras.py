'''Thumbnail (1280x720) and notes PDF for the OS video.   python osv/make_extras.py PAGES_DIR OUT_DIR'''
import glob, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); PD, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
F = lambda n, s: ImageFont.truetype(f'{HERE}/fonts/{n}', s)
pages = sorted(glob.glob(f'{PD}/page_*.png'))
# ---- notes PDF
imgs = [Image.open(p).convert('RGB') for p in pages]
imgs[0].save(f'{OUT}/Operating_System_Handwritten_Notes_TechVibe24.pdf', save_all=True, append_images=imgs[1:], resolution=150, quality=85)
# ---- thumbnail
def find(title):
    import json
    tl = json.load(open(f'{HERE}/build/tl.json'))
    for pg in tl['pages']:
        if pg['title'] == title: return Image.open(f'{PD}/page_{pg["i"]:03d}.png').convert('RGB')
th = Image.open(pages[1]).convert('RGB').crop((0, 300, 1920, 1380 - 300)).resize((1280, 720))   # plain ruled paper
th = Image.open(pages[1]).convert('RGB')
paper = th.crop((0, 0, 1920, 1080)).resize((1280, 720)); d0 = ImageDraw.Draw(paper); d0.rectangle([0, 0, 1280, 720], fill=(251, 248, 239))
for k in range(12): d0.line([(0, 100 + 52 * k), (1280, 100 + 52 * k)], fill=(176, 200, 232), width=2)
d0.line([(96, 0), (96, 720)], fill=(232, 150, 150), width=2)
def card(img, box, w, rot):
    c = img.crop(box); c = c.resize((w, int(w * c.height / c.width)), Image.LANCZOS)
    bd = Image.new('RGB', (c.width + 16, c.height + 16), (255, 255, 255)); bd.paste(c, (8, 8))
    bd = bd.convert('RGBA').rotate(rot, expand=True, resample=Image.BICUBIC); return bd
def place(base, im, x, y):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); a = im.split()[3]
    sh.paste((0, 0, 0, 110), (x + 14, y + 18), a); sh = sh.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(sh); base.alpha_composite(im, (x, y))
base = paper.convert('RGBA')
c1 = card(find('Process States'), (160, 230, 1900, 1000), 600, 6)
c2 = card(find('FCFS - First Come First Serve'), (160, 190, 1580, 720), 560, -5)
place(base, c1, 660, 250); place(base, c2, 690, 20)
d = ImageDraw.Draw(base)
d.text((60, 175), 'OPERATING', font=F('Anton.ttf', 118), fill=(16, 24, 58), anchor='ls')
d.text((60, 330), 'SYSTEM', font=F('Anton.ttf', 160), fill=(22, 60, 190), anchor='ls')
d.rounded_rectangle([60, 360, 410, 450], radius=14, fill=(214, 34, 46))
d.text((235, 406), 'ONE SHOT', font=F('Anton.ttf', 66), fill=(255, 255, 255), anchor='mm')
d.rectangle([60, 488, 640, 530], fill=(255, 232, 64))
d.text((66, 522), 'Handwritten Notes + Exam Numericals', font=F('Kalam-Bold.ttf', 34), fill=(30, 30, 36), anchor='ls')
d.text((62, 590), 'B.Tech CSE  ·  All Universities  ·  GATE', font=F('Kalam-Bold.ttf', 34), fill=(204, 36, 40), anchor='ls')
d.rounded_rectangle([60, 625, 330, 685], radius=30, fill=(10, 14, 24))
d.ellipse([68, 633, 112, 677], fill=(46, 230, 255)); d.polygon([(84, 643), (84, 667), (102, 655)], fill=(255, 255, 255))
f = F('SpaceGrotesk.ttf', 28)
try: f.set_variation_by_axes([700])
except Exception: pass
d.text((124, 656), '@TECHVIBE24', font=f, fill=(255, 255, 255), anchor='lm')
base.convert('RGB').save(f'{OUT}/OS_OneShot_Thumbnail.jpg', quality=92)
print('pdf pages', len(imgs), 'thumbnail ok')
