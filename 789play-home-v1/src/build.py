import base64,glob,os,re
import pathlib; ROOT=pathlib.Path(__file__).resolve().parent.parent; A=str(ROOT/'assets')
html=open(ROOT/'src'/'template.html').read()
def uri(n): return 'data:image/png;base64,'+base64.b64encode(open(f'{A}/{n}.png','rb').read()).decode()
names={'hot':['Genie\'s 3 Wishes','In Between','Higher Lower','Candy Burst','Irich Bingo','Fortune Mouse','Bingo Bite','Fortune Gods','Hip Hop Panda','Bingo Bite','Fortune Gods','Hip Hop Panda'],
'casino':['Candy Burst','Irich Bingo','Fortune Mouse','Bingo Bite','Fortune Gods','Hip Hop Panda','Candy Burst','Irich Bingo','Fortune Mouse','Bingo Bite','Fortune Gods','Hip Hop Panda']}
for g in ['hot','casino']:
    s=''
    for i in range(12):
        r,c=divmod(i,3)
        s+=f'<div class="tile" style="position:relative" data-t="打开游戏：{names[g][i]}"><img src="{uri(f"{g}_{r}{c}")}" alt="{names[g][i]}" width="114" height="140"><span class="fav"></span></div>'
    html=html.replace('{{'+g+'grid}}',s)
def rep(m): return uri(m.group(1))
html=re.sub(r'\{\{(\w+)\}\}',rep,html)

open(ROOT/'789play-home-v1-prototype.html','w').write(html)
print(len(html))
