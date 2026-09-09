#!/usr/bin/env python3
from pathlib import Path
import re
import urllib.request

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets'
USER='ishanraychaudhuri2025'
STREAK='https://streak-stats.demolab.com/'
SNAKE='https://raw.githubusercontent.com/ishanraychaudhuri2025/ishanraychaudhuri2025/output/'

def get(url):
    r=urllib.request.Request(url,headers={'User-Agent':'ishan-profile-activity'})
    with urllib.request.urlopen(r,timeout=30) as h:return h.read().decode()

def unwrap(s):
    m=re.match(r'<svg\b[^>]*>(.*)</svg>\s*$',s.strip(),re.I|re.S)
    if not m: raise ValueError('invalid SVG')
    return m.group(1)

def grp(s,t): return f'<g transform="{t}">{unwrap(s)}</g>'

def streak_url(theme):
    if theme=='dark':
        p=f'?user={USER}&hide_border=true&background=0B0B0F&stroke=C8102E&ring=C8102E&fire=D4AF37&currStreakLabel=FFFFFF&sideLabels=A8A8B0&currStreakNum=FFFFFF&sideNums=FFFFFF&dates=777B85&titleColor=C8102E&card_width=1180'
    else:
        p=f'?user={USER}&hide_border=true&background=FFFFFF&stroke=C8102E&ring=C8102E&fire=D4AF37&currStreakLabel=111116&sideLabels=5E626B&currStreakNum=111116&sideNums=111116&dates=9CA3AF&titleColor=C8102E&card_width=1180'
    return STREAK+p

def frame(theme):
    bg='#06080B' if theme=='dark' else '#F5F5F5'
    streak=(A/f'streak-{theme}.svg').read_text()
    stats=(A/f'stats-{theme}.svg').read_text()
    langs=(A/f'langs-{theme}.svg').read_text()
    snake=(A/f'activity-snake-{theme}.svg').read_text()
    ssx,ssy=1148/1180,178/195
    sx,sy=1128/880,170/192
    return ''.join([
      '<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="670" viewBox="0 0 1180 670" role="img" aria-label="GitHub streak, stats, languages and contribution snake">',
      f'<rect width="1180" height="670" fill="{bg}"/>',
      grp(streak,f'translate(16 16) scale({ssx:.8f} {ssy:.8f})'),
      grp(stats,'translate(26 202) scale(1.1 1)'),
      grp(langs,'translate(604 202) scale(1.1 1)'),
      grp(snake,f'translate({26+16*sx:.8f} {458+32*sy:.8f}) scale({sx:.8f} {sy:.8f})'),
      '<rect x="1" y="1" width="1178" height="668" rx="16" fill="none" stroke="#C8102E" stroke-width="2"/>',
      '</svg>'
    ])

def main():
    A.mkdir(exist_ok=True)
    for theme in ('dark','light'):
        st=get(streak_url(theme)); sn=get(SNAKE+f'snake-{theme}.svg')
        (A/f'streak-{theme}.svg').write_text(st)
        (A/f'activity-snake-{theme}.svg').write_text(sn)
        (A/f'profile-activity-{theme}.svg').write_text(frame(theme))

if __name__=='__main__': main()
