"""Validate generated local links, anchors, assessment coverage and result files."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json
from questions import QUIZ, MOCK, WRITTEN

BASE = Path(__file__).resolve().parent
class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        for key in ('href','src'):
            if key in attrs: self.links.append(attrs[key])

files=[BASE.parent/'index.html',*BASE.glob('*.html')]
parsed={}
for p in files:
    parser=Inspect(); parser.feed(p.read_text(encoding='utf-8')); parsed[p.resolve()]=parser
    assert len(parser.ids)==len(set(parser.ids)),f'Duplicate IDs: {p}'
    assert '\x00' not in p.read_text(encoding='utf-8')
for p,parser in parsed.items():
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        assert target.exists(),f'Broken link: {p.name}: {link}'
        if u.fragment and target in parsed and target.name!='index.html':
            assert u.fragment in parsed[target].ids,f'Broken anchor: {p}: {link}'
assert len(QUIZ)==48 and Counter(q['ch'] for q in QUIZ)=={n:8 for n in range(7,13)}
assert len(MOCK)==24 and Counter(q['ch'] for q in MOCK)=={n:4 for n in range(7,13)}
assert len(WRITTEN)==6 and sum(w['points'] for w in WRITTEN)+2.5*len(MOCK)==100
for q in QUIZ+MOCK:
    assert len(q['options'])==4 and len(set(q['options']))==4 and 0<=q['answer']<4
    assert q['why']
assert len({q['stem'] for q in QUIZ+MOCK})==72
assert json.loads((BASE/'results/p03_final.json').read_text())['chosen']=='B'
assert json.loads((BASE/'results/p05_final.json').read_text())['chosen']=='OLS'
print(f'PASS: {len(files)} HTML files; local links/anchors; 48 quiz + 24 mock MCQ + 6 written; 100 points; lab results.')
