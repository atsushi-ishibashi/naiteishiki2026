from pathlib import Path
from io import BytesIO
import hashlib,json,itertools
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pdfplumber
R=Path.cwd();pdfmetrics.registerFont(TTFont('JP','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
for f in R.glob('*/試遊素材.pdf'):
 reader=PdfReader(f);writer=PdfWriter();writer.clone_document_from_reader(reader)
 for i,p in enumerate(writer.pages):
  if i==0:continue
  w,h=float(p.mediabox.width),float(p.mediabox.height);b=BytesIO();c=canvas.Canvas(b,pagesize=(w,h));c.setFillColorRGB(1,1,1);c.rect(w-65,14,45,20,fill=1,stroke=0);c.setFillColorRGB(.38,.46,.5);c.setFont('JP',9);c.drawString(w-45,21,str(i+1));c.save();p.merge_page(PdfReader(b).pages[0])
 writer.write(f)
 with pdfplumber.open(f) as doc:
  bad=[]
  for i,p in enumerate(doc.pages):
   for ch in p.chars:
    if ch['x0'] < 0 or ch['x1'] > p.width+.5 or ch['top'] < 0 or ch['bottom']>p.height+.5:bad.append((i+1,ch['text']))
  assert not bad,(f,bad)
  print(f.parent.name,len(doc.pages),'pages',f.stat().st_size,'bytes', 'bounds OK')
old=json.loads((R/'tmp/pdfs/source_hashes.json').read_text())
for k,digest in old.items():assert hashlib.sha256((R/k/'nazotoki.md').read_bytes()).hexdigest()==digest
print('All 7 source files unchanged.')
# Check graph chain, two readings, and survivor letters from actual source data.
exec((R/'tmp/pdfs/build_materials.py').read_text().split('D=Doc(')[0])
s=sources['teamc_first_mission'];cr=table_rows(s,'| カード | −3 |');cy=table_rows(s,'| カード | Y軸の添字')
v=[[1,4,6,9,3,8],[9,3,8,5,1,6],[5,1,6,8,2,5],[8,2,5,4,9,1],[4,9,1,7,5,3],[7,5,3,6,4,2],[9,3,5,2,7,4],[8,2,7,1,6,3],[7,5,8,2,6,1]]
assert [(i,j) for i in range(9) for j in range(9) if i!=j and v[i][3:]==v[j][:3]]==[(0,1),(1,2),(2,3),(3,4),(4,5)]
assert ''.join(cr[i][i+1] for i in range(6))=='最初をゼロに'
assert ''.join(cr[i][i+4] for i in range(6))=='接続部を消せ'
survive=[]
for i in range(6):
 labels={int(a):b for a,b in re.findall(r'(\d+)：([^、]+)',cy[i][1])};remove=set((v[i][:3] if i>0 else [])+(v[i][3:] if i<5 else []));survive += [b for a,b in labels.items() if a not in remove]
assert sorted(survive)==sorted(['Now','cast','の','設','立','日'])
print('Graph connections, both extractions and final fragments verified.')
