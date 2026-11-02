from pathlib import Path
s=Path('tmp/pdfs/materials_only.py').read_text()
prefix=s[:s.index("D=Doc(")]
block=s[s.index('# C first'):s.index('# B second rules')]
old="""  D.text('記録位置',46,top-275,9)
  for i in range(9):
   xx=130+i*44;D.center(str(i-3) if i<4 else '+'+str(i-3),xx,top-275,8,MUTED);D.center(cr[idx][i+1],xx,top-302,14)
"""
new="""  D.text('文字盤',46,top-281,11,TEAL)
  D.text('記録位置',46,top-298,8,MUTED)
  for i in range(9):
   xx=112+i*49
   D.c.setFillColor(PALE);D.c.setStrokeColor(LINE);D.c.setLineWidth(.7)
   D.c.rect(xx,top-287,49,20,fill=1,stroke=1)
   D.c.setFillColor(white);D.c.rect(xx,top-313,49,26,fill=1,stroke=1)
   D.center(str(i-3) if i<4 else '+'+str(i-3),xx+24.5,top-281,10)
   D.center(cr[idx][i+1],xx+24.5,top-306,15)
"""
assert old in block
block=block.replace(old,new)
exec(prefix+"D=Doc('teamc_first_materials.pdf')\n"+block+"\nD.save()\n")
from pypdf import PdfReader,PdfWriter
src=OUT/'teamc_first_materials.pdf';r=PdfReader(src);w=PdfWriter()
for i,p in enumerate(r.pages):
 w.add_page(p)
 w.add_outline_item(D.entries[i][1],i)
w.add_metadata({'/Title':'teamc_first_mission / 試遊素材','/Subject':'カード・台紙・文字盤'})
w.write(R/'teamc_first_mission/試遊素材.pdf')
# Verify both readings from the nine-column table used to draw the cells.
assert ''.join(cr[i][i+1] for i in range(6))=='最初をゼロに'
assert ''.join(cr[i][i+4] for i in range(6))=='接続部を消せ'
print('Updated Team C only: 9 framed letter boards; both readings verified.')
