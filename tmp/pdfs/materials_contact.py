from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
p=Path('tmp/pdfs')
files=sorted((p/'materials-only-render').glob('*.png'))
for start in range(0,len(files),12):
 out=Image.new('RGB',(1200,1400),'#dce3e8');d=ImageDraw.Draw(out)
 for i,f in enumerate(files[start:start+12]):
  im=Image.open(f).convert('RGB');im.thumbnail((280,420));x=(i%4)*300+(300-im.width)//2;y=(i//4)*465+25;out.paste(im,(x,y));d.text(((i%4)*300+10,(i//4)*465+7),f.stem,fill='black')
 out.save(p/f'materials-only-{start//12}.jpg')
