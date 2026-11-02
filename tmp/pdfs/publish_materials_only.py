from pathlib import Path
from io import BytesIO
import json, hashlib
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path.cwd();T=R/'tmp/pdfs';O=R/'output/pdf'
pdfmetrics.registerFont(TTFont('JP','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
readers={'paper':PdfReader(O/'01_紙の試遊キット.pdf'),'web':PdfReader(O/'02_Web画面イメージとルール.pdf')}
meta={k:dict(json.loads((T/(k+'_pages.json')).read_text())) for k in readers}
plans={'start_mission':(range(1,8),[]),'teama_first_mission':([11,8,9,10,12,13],[]),'teamb_first_mission':(range(14,20),[]),'teamc_first_mission':(range(20,26),[]),'teama_second_mission':([],[1,2,3,4]),'teamb_second_mission':(range(26,33),[5]),'teamc_second_mission':([],[6,7,8])}
for folder,(pp,wp) in plans.items():
 w=PdfWriter()
 for i,(kind,n) in enumerate([('paper',n) for n in pp]+[('web',n) for n in wp]):
  page=w.add_page(readers[kind].pages[n-1]);pw,ph=float(page.mediabox.width),float(page.mediabox.height)
  # Re-number each mission independently.
  b=BytesIO();c=canvas.Canvas(b,pagesize=(pw,ph));c.setFillColorRGB(1,1,1);c.rect(pw-65,14,45,20,fill=1,stroke=0);c.setFillColorRGB(.38,.46,.5);c.setFont('JP',9);c.drawString(pw-45,21,str(i+1));c.save();page.merge_page(PdfReader(b).pages[0])
  # Screens with no supporting clue text use a compact page around the image.
  if kind=='web' and n in [2,3,5,6,7]:page.cropbox.lower_left=(0,350)
  if kind=='web' and n==8:page.cropbox.lower_left=(0,225)
  w.add_outline_item(meta[kind][n],i)
 w.add_metadata({'/Title':folder+' / 試遊素材','/Subject':'カード・台紙・画面素材'})
 f=R/folder/'試遊素材.pdf';w.write(f);print(folder,len(w.pages))
for k,d in json.loads((T/'source_hashes.json').read_text()).items():assert hashlib.sha256((R/k/'nazotoki.md').read_bytes()).hexdigest()==d
print('Source files unchanged')
