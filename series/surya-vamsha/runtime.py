"""Recompute the अवधि line of every Hindi script: spoken words + marked pauses.
    python3 runtime.py            # all epNN-*-hindi.md in this folder
"""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for f in sorted(glob.glob('ep*-hindi.md')):
    s = open(f).read()
    body = s.split('\n---\n', 1)[1]
    body = re.split(r'## (जाँच लें|कॉपी ब्लॉक)', body)[0]
    w = len(' '.join(l for l in body.splitlines() if '[स्क्रीन' not in l and not l.startswith('#')).split())
    p = body.count('[विराम]')
    m = round(w / 110 + p * 2 / 60, 1)
    s = re.sub(r'(?m)^\*\*अवधि:\*\*.*$', f'**अवधि:** लगभग {w} बोले जाने वाले शब्द और {p} पूरे ठहराव, यानी 110 शब्द प्रति मिनट की गति पर लगभग {m} मिनट। एक बार पढ़कर समय जाँच लें।', s)
    open(f, 'w').write(s)
    print(f'{f:40s} {w:5d} words {p:3d} pauses {m:5.1f} min{"  SHORT" if m < 8.5 else ""}')
