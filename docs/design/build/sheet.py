import sys, subprocess
from PIL import Image
names = sys.argv[2:]; out = sys.argv[1]
subprocess.run(['python3', 'shot.py'] + [n + '.dc.html' for n in names], capture_output=True)
W, H = 960, 600; rows = (len(names) + 1) // 2
im = Image.new('RGB', (W * 2 + 10, H * rows + 10 * (rows - 1)), 'white')
for j, f in enumerate(names):
    t = Image.open(f'/home/claude/ff-design/shots/{f}.png').convert('RGB').resize((W, H), Image.LANCZOS)
    im.paste(t, ((j % 2) * (W + 10), (j // 2) * (H + 10)))
im.save(out)
