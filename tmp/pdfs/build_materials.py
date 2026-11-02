from pathlib import Path
import re, math, hashlib, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.pagesizes import A4,A3
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
R=Path.cwd(); OUT=R/'output/pdf'; TMP=R/'tmp/pdfs'
sources={p.parent.name:p.read_text() for p in R.glob('*/nazotoki.md') if p.parent.name!='final_mission'}
(TMP/'source_hashes.json').write_text(json.dumps({k:hashlib.sha256(v.encode()).hexdigest() for k,v in sources.items()}))
pdfmetrics.registerFont(TTFont('JP','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('SYM','/System/Library/Fonts/Apple Symbols.ttf'))
INK=HexColor('#172F3D'); TEAL=HexColor('#167C80'); MUTED=HexColor('#617581'); PALE=HexColor('#EFF5F5'); LINE=HexColor('#BCCDD2'); GOLD=HexColor('#D39B3C')
class Doc:
 def __init__(self,name): self.c=canvas.Canvas(str(OUT/name),pagesize=A4); self.c.setTitle(name); self.n=0; self.entries=[]
 def page(self,title,tag='参加者用',size=A4):
  if self.n:self.c.showPage()
  self.n+=1; self.c.bookmarkPage('p'+str(self.n)); self.c.addOutlineEntry(str(self.n)+' / '+title,'p'+str(self.n),level=0); self.W,self.H=size; self.c.setPageSize(size); self.entries.append((self.n,title)); self.c.setFillColor(TEAL); self.c.rect(0,self.H-13,self.W,13,fill=1,stroke=0)
  self.text(tag,32,self.H-39,9,TEAL); self.text(title,32,self.H-70,22)
  self.c.setStrokeColor(LINE); self.c.line(32,35,self.W-32,35); self.text('FINATEXT / 謎解き試遊素材',32,21,8,MUTED); self.text(str(self.n),self.W-45,21,9,MUTED)
 def text(self,s,x,y,size=11,color=INK,font='JP'):
  self.c.setFillColor(color); self.c.setFont(font,size); self.c.drawString(x,y,str(s))
 def center(self,s,x,y,size=11,color=INK,font='JP'):
  self.c.setFillColor(color); self.c.setFont(font,size); self.c.drawCentredString(x,y,str(s))
 def para(self,s,x,y,w,size=11,color=INK):
  st=ParagraphStyle('p',fontName='JP',fontSize=size,leading=size*1.65,textColor=color,wordWrap='CJK'); p=Paragraph(s.replace('\n','<br/>'),st); a,h=p.wrap(w,900); p.drawOn(self.c,x,y-h); return y-h
 def box(self,x,y,w,h,fill=white,stroke=LINE):
  self.c.setFillColor(fill);self.c.setStrokeColor(stroke);self.c.setLineWidth(.7);self.c.roundRect(x,y,w,h,7,fill=1,stroke=1)
 def block(self,title,body,y,w=None,x=36):
  w=w or self.W-72; self.text(title,x,y,14,TEAL); return self.para(body,x,y-15,w,11)-26
 def symbol(self,s,x,y,size=18):self.center(s,x,y,size,INK,'SYM')
 def save(self):self.c.save()
 def grid(self,vals,x,y,cell,cols=3,fontsize=16,numbers=False):
  for i,v in enumerate(vals):
   xx=x+(i%cols)*cell; yy=y-(i//cols+1)*cell
   self.c.setStrokeColor(LINE);self.c.rect(xx,yy,cell,cell,fill=0,stroke=1)
   if numbers:self.text(str(i+1),xx+4,yy+cell-12,7,MUTED)
   self.center(v,xx+cell/2,yy+cell/2-fontsize*.35,fontsize)
 def blanks(self,n,x,y,symbols=None,cell=28):
  for i in range(n):
   self.c.setStrokeColor(INK);self.c.rect(x+i*cell,y,cell,cell)
   if symbols and i in symbols:self.symbol(symbols[i],x+i*cell+cell/2,y+cell+5,15)

def table_rows(text,begin):
 s=text[text.index(begin):]; lines=s.splitlines(); out=[]; started=False
 for l in lines:
  if l.startswith('|'):
   if not started:started=True;continue
   row=[re.sub(r'\*\*','',x.strip()) for x in l.strip('|').split('|')]
   if all(re.fullmatch(r'[-: ]*',x) for x in row):continue
   out.append(row)
  elif started:break
 return out

D=Doc('01_紙の試遊キット.pdf')
D.page('紙の試遊キット','配布準備 / 解答・解説は収録していません')
y=D.block('対象','START、A・B・CのFIRST MISSION、BのSECOND MISSION。\nA・CのSECOND MISSIONとWebの画面イメージは別冊です。',730)
y=D.block('印刷と配布','片面・実際のサイズ（100%）で印刷してください。A3ページはプリンターの用紙設定をA3にします。カードは枠に沿って切り分けます。各ミッションの資料だけを渡して試してください。',y)
y=D.block('A FIRSTの組み立て','カードは表と裏が横につながっています。外枠を切り、中央で折って背中合わせに貼ります。▲の向きをそろえてください。封筒型ケースはA3に片面印刷し、外形を切って破線で折り、印刷面を内側にします。テープで封をせず、開いて戻せる状態で全資料を包みます。',y)
y=D.block('必要な道具','筆記具、消しゴム、はさみ、のり、検索できるスマートフォン。\nB FIRSTは○・△・□・☆の4種類の印を使います。\nB SECONDはカードを置き、矢印を鉛筆で描いて構成を考えます。',y)
y=D.block('試遊用素材について','グラフ・記号・業務カードはゲーム用の設定です。最終ミッションは今回の素材に含めていません。\nWeb版は静止画の試作イメージで、ボタンや自動判定は動作しません。',y)
D.block('収録ページ','START：2〜8　／　A FIRST：9〜14　／　B FIRST：15〜20\nC FIRST：21〜26　／　B SECOND：27〜34\nA3で印刷するページ：8・14・34。ほかはA4です。',y)
# start rules
D.page('最初のオフィスはどこ？','START / 全員で共有')
y=D.block('創業の記録を復元しよう','このソファは、Finatextの始まりを知っている。探しているのは、自宅でも間借りの会議室でもない。初めて自分たちで借りたオフィスだ。\n記録の答えは抜け落ち、宛先の一部は記号に変わってしまった。3本のnoteを手がかりに、みんなで宛先を復元しよう。',730)
y=D.block('記入ルール','答えはカタカナで、左から1マスに1文字ずつ書きます。小さい「ャ・ュ・ョ・ッ」、長音「ー」も1マス。「ガ」「パ」なども1マスです。年数は「○年」、人数は「○人」まで含めます。数字欄は1マス1桁です。\n記号が付いたマスの文字・数字を、宛先の同じ記号に当てはめます。普通の空欄には、それぞれ違う文字が入って構いません。記録も分かったことも自由に見せ合えます。',y)
links=[('Finatextの10年を振り返ってみる','https://note.com/ryotafinatext/n/n3b869fccd918'),('Finatextを創業してから上場するまでの10の学び','https://note.com/ryotafinatext/n/n65ab81d5f084'),('Finatextがビジョン/ミッションからカルチャーをアップデートするまでの全容','https://note.com/110_110_110/n/n76729c01a16f')]
D.text('調べる資料（タイトルをクリック）',36,y,14,TEAL);y-=24
for title,url in links:
 y2=D.para(title,36,y,520,11,TEAL);D.c.linkURL(url,(36,y2,560,y),relative=0);y=y2-18
D.para('カードの答えは、この3本のnoteの中にあります。記事内検索も使えます。宛先が読めたら、Google Mapsなどで調べ、建物名を報告してください。',36,y,520,11)
rows=table_rows(sources['start_mission'],'| 記録 | カードに印刷する問い')
for j in range(0,10,2):
 D.page('創業の記録','START / 切り分けて1人1枚')
 for k,row in enumerate(rows[j:j+2]):
  title,q,boxes=row; ytop=735-k*334; D.box(36,ytop-306,523,306);D.text(title,54,ytop-32,17,TEAL);D.para(q,54,ytop-54,480,12)
  syms=boxes.split(); marks={i:s for i,s in enumerate(syms) if s!='□'};D.blanks(len(syms),60,ytop-159,marks,32)
  sym=list(marks.values())[0];D.symbol(sym,268,ytop-149,18);D.text('が表す文字：',285,ytop-149,11);D.blanks(1,373,ytop-159,cell=32)
  num=j+k+1
  if num in [2,3]:
   question='この引っ越しのとき、気温は何度だった？' if num==2 else '最初に借りたオフィスに、トイレはいくつあった？'
   D.text(question,54,ytop-202,11);D.blanks(2 if num==2 else 1,60,ytop-271,{1:'☁'} if num==2 else {0:'♠'},30);D.text('℃' if num==2 else '個',130,ytop-260,12)
   D.symbol('☁' if num==2 else '♠',268,ytop-260,18);D.text('が表す数字：',285,ytop-260,11);D.blanks(1,373,ytop-271,cell=30)
D.page('最初の独立オフィスへの宛先','START / 共有台紙 / A3',A3)
D.para('カードで分かった文字や数字を、宛先の同じ記号に当てはめてください。',40,1070,750,15)
for i,s in enumerate(['★◆▲●◆★','■♥♣☀','☀♣☂▲♪','♠-9-☁']):
 y=960-i*145
 for j,ch in enumerate(s):
  if ch in '-9':D.center(ch,110+j*54,y,30)
  else:D.symbol(ch,110+j*54,y,32)
 D.c.setStrokeColor(LINE);D.c.line(80,y-60,740,y-60)
for i,ch in enumerate('▲☂♠♥★♪☀●■☁◆♣'):
 x=70+(i%6)*125;y=330-(i//6)*80;D.symbol(ch,x,y,24);D.text('＝',x+22,y,16);D.blanks(1,x+46,y-8,cell=35)
D.para('宛先が読めたら、Google Mapsでその住所を調べよ。\n報告するのは、そこにある建物の名前。',50,155,720,17)
# A first
names=['星','鍵','雲','月','花','傘','本','船','鳥']; ns=[5,2,8,9,1,4,3,7,6]; ks=[3,7,1,5,9,2,8,6,4]; one=list('ふくろのうちがわへ'); two=['母子','保険','はぐ','の','提供','開始','日','は','？']
backs=[]
for i in range(9):
 a=['台帳','ね','保管','区分','め','き','記録','そ','ぬ']; a=a[i:]+a[:i];a[ns[i]-1]=one[i];a[ks[i]-1]=two[i];backs.append(a)
assert ''.join(backs[i][ns[i]-1] for i in range(9))=='ふくろのうちがわへ'
assert ''.join(backs[i][ks[i]-1] for i in range(9))=='母子保険はぐの提供開始日は？'
for page in range(3):
 D.page('記録カード','A FIRST / 外枠を切り、中央で折って貼る / 上端の▲をそろえる')
 for k in range(3):
  i=[5,2,6,0,8,4,1,7,3][page*3+k]; x=118;top=735-k*218; sz=170.079
  D.c.setStrokeColor(INK);D.c.rect(x,top-sz,sz*2,sz);D.c.setDash(3,3);D.c.line(x+sz,top,x+sz,top-sz);D.c.setDash()
  D.center('▲',x+sz/2,top-14,9);D.center(names[i],x+sz/2,top-96,40);D.center('▲',x+sz*1.5,top-14,9)
  D.grid(backs[i],x+sz+12,top-24,(sz-24)/3,fontsize=14,numbers=True)
D.page('最初の顧客はどこにいる？','A FIRST / 案内と部署メモ')
D.para('Inspireの最初の利用者に関する記録が失われた。\n3部署の記録を照合し、保管庫を復元せよ。\n記録はすべて、このふくろに封じて渡してある。',36,735,520,14)
for i,(name,body) in enumerate([('営業','星と雲は同じ行で、間に1枚ある。\n月は鍵より下の行、船より上の行。\n鳥は花のすぐ右下。'),('開発','本と鳥は同じ行で、間に1枚ある。\n雲は傘より上の行。\n鍵と本は同じ列ではない。'),('運用','花は中央。\n星は船より左の列。\n傘と雲は同じ列。')]):
 top=602-i*172;D.box(36,top-151,523,151);D.text('部署メモ / '+name,54,top-28,16,TEAL);D.para(body,54,top-46,485,12)
D.page('保管庫の配置台紙','A FIRST / ▲の向きをそろえて置く')
D.para('カードを裏返し、矢印の順に、マスの数字が示す位置の文字を拾え。',36,735,520,12)
cell=170.079;x=42;top=680
D.grid([str(x) for x in ns],x,top,cell,fontsize=30)
for r in range(3):
 for col in range(3):D.center('▲',x+col*cell+cell/2,top-r*cell-18,10)
 D.text('→',x+cell-10,top-r*cell-cell/2,19,TEAL);D.text('→',x+cell*2-10,top-r*cell-cell/2,19,TEAL)
D.text('読む順：左上から右へ。行の終わりから、次の行の左へ。',40,136,10,MUTED)
D.text('復元した問い：',40,108,12);D.c.line(135,104,550,104);D.text('解答（西暦8桁）：',40,68,12);D.blanks(8,177,58,cell=25)
D.page('封筒型ケース・内面','A FIRST / A3・100% / 枠外の説明は切り落とす',A3)
D.para('印刷面を内側に、左右→下→上の順に折る。破線＝折り線。実線の外形を切り、開ける状態で包む。',36,1096,770,10)
x=117;y=155;s=607;h=850;f=70;t=76
p=D.c.beginPath();p.moveTo(x,y-t);p.lineTo(x+s,y-t);p.lineTo(x+s,y);p.lineTo(x+s+f,y);p.lineTo(x+s+f,y+h);p.lineTo(x+s,y+h);p.lineTo(x+s,y+h+t);p.lineTo(x,y+h+t);p.lineTo(x,y+h);p.lineTo(x-f,y+h);p.lineTo(x-f,y);p.lineTo(x,y);p.close();D.c.setStrokeColor(INK);D.c.drawPath(p)
D.c.setDash(4,4);D.c.rect(x,y,s,h);D.c.setDash();D.center('記録の内側',x+s/2,y+h-145,24,TEAL)
D.grid(['雲','傘','星','鳥','月','船','鍵','本','花'],x+(s-300)/2,y+h-200,100,fontsize=27)
D.para('保険サービスを動かす基盤Inspireは、グループ内の「母子保険はぐ」で活用された。最初の利用者への手がかりは、記録の内側にも残っている。',x+50,y+220,s-100,14)
# B first
D.page('4つのサービス、1つの正体','B FIRST / 全員で共有')
y=D.block('経路を復旧せよ','4つのサービスへの経路が断絶した。それぞれの経路を復旧せよ。未来への問いは、すべてのサービスを支えている場所に残した。',735)
y=D.block('進め方','沿革の断片から4件を歴史順に並べてください。1人1枚のサービスカードを担当します。\nこの記録が歴史の何番目か。その番号のゲートから入り、次の番号のゲートへ抜けよ。（Ⅴ＝現在）\n通ったマスすべてを共通の文字盤に記録します。入口・出口のマスも含め、○・△・□・☆のうち自分の記号で印を付けてください。\n文字盤は上の行から、左から右へ読みます。最後の問いはWebで調べ、西暦8桁で回答してください。',y)
frags=['STREAMの現物取引サービスは、セゾンポケットより前に始まった。','Wealth Wingは、セゾンポケットより後に始まった。','セゾン投信の移管案件は、Wealth Wingより後の出来事だ。']
for i,body in enumerate(frags):
 top=350-i*91;D.box(36,top-75,523,75);D.text('沿革の断片',50,top-22,11,TEAL);D.para(body,50,top-34,490,11)
D.text('沿革の確認資料：スマートプラス公式開示資料 ／ セゾン投信公式発表',36,65,8,MUTED)
D.c.linkURL('https://smartplus-sec.com/assets/static/company/disclosure/report_3_202103.pdf',(36,62,320,76))
D.c.linkURL('https://www.saison-am.co.jp/news/pdf/newsrelease20240104.pdf',(322,62,560,76))
# maze parse and validate
maze_blocks=re.findall(r'```text\n([^`]+)```',sources['teamb_first_mission']);mazes=[b.strip().splitlines() for b in maze_blocks if b.startswith('■Ⅰ')];assert len(mazes)==4
paths=[];gates=[(0,0),(3,0),(6,2),(4,6),(1,6)]
services=['STREAMの現物取引サービス','セゾンポケット','Wealth Wing','セゾン投信の移管案件']
for m in [2,0,3,1]:
 maze,title=mazes[m],services[m]
 assert len(maze)==15 and all(len(l)==15 for l in maze)
 adj={}
 for r in range(7):
  for co in range(7):
   adj[r,co]=[(rr,cc) for rr,cc in [(r-1,co),(r+1,co),(r,co-1),(r,co+1)] if 0<=rr<7 and 0<=cc<7 and maze[r+rr+1][co+cc+1]!='■']
 assert sum(map(len,adj.values()))==96
 def route(v,target,prev=None):
  if v==target:return [v]
  for nxt in adj[v]:
   if nxt!=prev:
    p=route(nxt,target,v)
    if p:return [v]+p
  return None
 paths.append(route(gates[m],gates[m+1]))
 D.page(title,'B FIRST / サービスカード / 1人1枚')
 D.para('この記録が歴史の何番目か。その番号のゲートから入り、\n次の番号のゲートへ抜けよ。（Ⅴ＝現在）',36,735,520,12)
 x=72;top=628;c=64
 D.c.setStrokeColor(LINE);D.c.setLineWidth(.3);D.c.setDash(1,3)
 for j in range(8):
  D.c.line(x+j*c,top,x+j*c,top-7*c);D.c.line(x,top-j*c,x+7*c,top-j*c)
 D.c.setDash()
 for r in range(8):
  for co in range(7):
   if maze[r*2][co*2+1]=='■':D.c.setStrokeColor(INK);D.c.setLineWidth(2);D.c.line(x+co*c,top-r*c,x+(co+1)*c,top-r*c)
 for r in range(7):
  for co in range(8):
   if maze[r*2+1][co*2]=='■':D.c.setStrokeColor(INK);D.c.setLineWidth(2);D.c.line(x+co*c,top-r*c,x+co*c,top-(r+1)*c)
 for r in range(7):
  D.text(str(r+1),48,top-r*c-c/2,10,MUTED);D.center(str(r+1),x+r*c+c/2,top+13,10,MUTED)
 for s,xx,yy in [('Ⅰ',x+c/2,top+33),('Ⅱ',x-19,top-3.5*c),('Ⅲ',x+2.5*c,top-7*c-24),('Ⅳ',x+7*c+18,top-4.5*c),('Ⅴ',x+7*c+18,top-1.5*c)]:D.center(s,xx,yy,20,TEAL)
 D.text('自分の記号：',40,105,12);D.text('入口：　　　　出口：',270,105,12)
common=set.intersection(*(set(p) for p in paths));assert common=={(0,2),(1,5),(3,1),(4,4),(5,2)}
D.page('共通の文字盤','B FIRST / 4人で共有')
D.para('通ったマスに自分の記号を書き込もう。\n読む順：上の行から、左から右へ。',36,735,520,12)
words=table_rows(sources['teamb_first_mission'],'| | 1 | 2 | 3 | 4 | 5 | 6 | 7 |');values=[v for row in words for v in row[1:]];assert len(values)==49
D.grid(values,52,650,70,cols=7,fontsize=16)
for i in range(7):D.center(str(i+1),87+i*70,662,9,MUTED);D.text(str(i+1),36,615-i*70,9,MUTED)
D.text('復元した問い：',40,120,12);D.c.line(140,115,550,115);D.text('解答（西暦8桁）：',40,75,12);D.blanks(8,180,60,cell=28)
# C first
D.page('会社が存在しない会社の記録','C FIRST / 共有台紙')
y=D.block('記録をつなぎ、問いを復元せよ','9枚の記録から、つながる6枚を古い記録から順に並べてください。\n前のカードの最後の3つの値と、次のカードの最初の3つの値が、順番まで同じなら接続できます。グラフは左から右へ読み、カードは逆向きにしません。',735)
y=D.block('最初の基準は「法人化＝0」','座標は年数ではなく、記録の順番です。前後のカードへ1ずつ位置を割り当て、下の欄に書いてください。各カードの位置と同じ数字の文字を「記録位置」の文字盤から1つずつ拾い、カードの並び順に読みます。',y)
for i in range(6):
 top=470-i*43;D.text(str(i+1),40,top,12);D.text('記録名：',64,top,10);D.c.line(110,top-3,350,top-3);D.text('記録位置：',380,top,10);D.c.line(445,top-3,545,top-3)
D.text('復元した言葉：［　　　　　　　　　　　　　　　　］は？',40,175,12);D.text('解答（西暦8桁）：',40,125,12);D.blanks(8,180,110,cell=28)
D.box(40,53,75,33);D.center('0',77,63,22);D.text('← 切り取って動かせる0マーカー',130,64,10,MUTED)
cr=table_rows(sources['teamc_first_mission'],'| カード | −3 |'); cy=table_rows(sources['teamc_first_mission'],'| カード | Y軸の添字');cv=[[1,4,6,9,3,8],[9,3,8,5,1,6],[5,1,6,8,2,5],[8,2,5,4,9,1],[4,9,1,7,5,3],[7,5,3,6,4,2],[9,3,5,2,7,4],[8,2,7,1,6,3],[7,5,8,2,6,1]]
ct=['研究開始','東大日次物価指数の公開','東大と日経デジタルメディアの提携','ナウキャスト設立','日経CPIナウ配信','Finatextとの経営統合','研究記録の整理','新しい集計の検討','配信記録の点検']
cb=['日々の物価を捉える研究が始まった。','研究から生まれた日次物価指数が公開された。','東大と日経デジタルメディアが提携した。','研究プロジェクトを前身としてナウキャストが法人化した。','ナウキャストによる日経CPIナウの配信が始まった。','ナウキャストがFinatextと経営統合した。','研究の途中で、別の集計記録をまとめた。','集計方法を見直すため、観測記録を作成した。','配信の点検に使う観測記録をまとめた。']
# neutral IDs and mixed ordering
ids=['K','R','F','M','T','B','S','D','N'];order=[4,6,1,8,3,0,7,5,2]
for pg in range(5):
 D.page('観測記録カード','C FIRST / 枠で切り分ける / グラフはゲーム用の架空データ')
 for slot,idx in enumerate(order[pg*2:pg*2+2]):
  top=742-slot*343;D.box(33,top-325,529,325);D.text(ids[idx]+' / '+ct[idx],46,top-25,13,TEAL);D.text(cb[idx],46,top-45,9)
  x=134;yb=top-244;w=360;h=170;step=w/6
  labels={int(a):b for a,b in re.findall(r'(\d+)：([^、]+)',cy[idx][1])};v=cv[idx]
  for z in range(11):
   yy=yb+z*h/10;D.c.setStrokeColor(LINE);D.c.setLineWidth(.35);D.c.line(x,yy,x+w,yy);D.text(str(z),116,yy-3,8);D.text(labels.get(z,''),64,yy-3,10)
  D.text('値',113,yb+h+13,9);D.text('時点',x+w+7,yb-12,8)
  pts=[(x+(i+.5)*step,yb+a*h/10) for i,a in enumerate(v)]
  typ=idx if idx<6 else idx-6
  D.c.setStrokeColor(TEAL);D.c.setFillColor(TEAL);D.c.setLineWidth(1.8)
  if typ==0:
   for xx,yy in pts:D.c.rect(xx-12,yb,24,yy-yb,fill=1,stroke=0)
  elif typ==4:
   for i,a in enumerate(v):
    for z in range(a):D.symbol('★',pts[i][0],yb+z*h/10+1,12)
  elif typ==5:
   for i,(xx,yy) in enumerate(pts):
    D.c.line(xx-step/2,yy,xx+step/2,yy)
    if i<5:D.c.line(xx+step/2,yy,xx+step/2,pts[i+1][1])
    D.c.circle(xx,yy,2.5,fill=1)
  elif typ==3:
   p=D.c.beginPath();p.moveTo(pts[0][0],yb)
   for xx,yy in pts:p.lineTo(xx,yy)
   p.lineTo(pts[-1][0],yb);p.close();D.c.setFillColor(HexColor('#D5E8E7'));D.c.drawPath(p,fill=1,stroke=1)
   for xx,yy in pts:D.c.setFillColor(TEAL);D.c.circle(xx,yy,2.5,fill=1)
  else:
   for i,(xx,yy) in enumerate(pts):
    D.c.circle(xx,yy,3,fill=1)
    if typ==1 and i:D.c.line(*pts[i-1],xx,yy)
  for i,(xx,yy) in enumerate(pts):D.center(str(i+1),xx,yb-13,8)
  if typ==4:D.text('★1個＝1',440,top-65,9)
  if typ==5:D.text('各時点の●の高さを読む',365,top-65,9)
  D.text('記録位置',46,top-275,9)
  for i in range(9):
   xx=130+i*44;D.center(str(i-3) if i<4 else '+'+str(i-3),xx,top-275,8,MUTED);D.center(cr[idx][i+1],xx,top-302,14)
# B second rules + cards
D.page('12ポイントで回答を届ける','B SECOND / 目的と接続ルール')
y=D.block('目的','利用者の問い合わせに、根拠を添えた回答を届けよ。構成の工数予算は12pt以下。\n同じ構成で、公開された全テストに対応します。通常2件には回答を届け、根拠不足・資料の食い違い・個別判断は、論点と確認済み出典を残して人に戻します。外部への送信は、人間が回答案を確認して許可した後だけ行います。',735)
y=D.block('カードのつなぎ方','主線の矢印は、左から右へ1回ずつ実行する順番です。入力不足の工程は実行できず、自動で飛ばしたり戻ったりはしません。取得した資料は後のカードでも参照できます。\n「AIから呼出可能」のカードは、主線のほか、AI担当の「使える道具」に接続できます。道具は必要なときに呼び出され、結果をAIへ返します。\n1枚を主線と道具の両方には置けません。同じ機能の人間版・自動版は片方だけで、複製もできません。使わないカードは外せます。',y)
y=D.block('工数と権限','道具を含め、使うカードのptをすべて足します。使わない道具や送信がある案件でも、構成のptは変わりません。案件ごとに構成を変えることもできません。\nカードには印刷された能力だけがあります。H0への正解IDの手入力や、H6による追加調査・回答案の作り直しはできません。H0をつなぐと、この目的カードの条件が方針として渡ります。',y)
D.block('検索の使い方','履歴検索には顧客ID＋検索対象が必要です。「前回の申込」なら最新申込を、それ以外は資料で判明した具体的な手続きIDを検索します。全履歴の一括取得はできません。\n説明書検索にはサービスIDが必要です。全説明書の一括取得はできません。各検索は1案件1回まで、合計最大2回。入力不足は構成エラー、検索後の「該当なし」は保留案件です。',y)
D.page('公開テスト / 通常の問い合わせ','B SECOND / 最初から両方を参照できます')
y=735
for title,body in [('通常A / 顧客U-A','「前回申し込んだサービスの利用条件を教えてください。」\n初期情報：顧客IDと「最新申込」。サービスIDは不明。\nU-Aの最新申込を検索 → サービスS-17。出典L-101。\nS-17の説明書を検索 → 利用条件は基本登録の完了。出典D-17。\n回答にはサービス・利用条件と、出典L-101・D-17を含めます。本人の条件充足まで判定する問い合わせではありません。'),('通常B / 顧客U-B','「サービスS-42は、自分も利用できますか？」\n初期情報：顧客IDとサービスID。調べる手続きは不明。\nS-42の説明書を検索 → 利用条件は手続きZ-6の完了。出典D-42。\nU-BのZ-6を検索 → 完了済み。出典L-202。\n回答には利用条件を満たすことと、出典D-42・L-202を含めます。この架空案件に、ほかの判断条件はありません。')]:y=D.block(title,body,y)-20
D.para('ここに書かれたIDを、事前にカードへ直接埋め込むことはできません。実行中の問い合わせと、その実行で得た資料から検索条件を作ってください。',36,y,520,11)
D.page('公開テスト / 保留する問い合わせ','B SECOND / 例外3件も同じ構成で処理します')
y=735
for title,body in [('根拠不足 / 顧客U-C','前回のサービスの条件を質問。最新申込はS-90（L-303）。S-90の説明書は該当なし。\n説明書が見つからないこととL-303を論点メモに残し、保留・引き継ぎ。外部には送信しません。'),('資料の矛盾 / 顧客U-D','S-50を利用できるか質問。説明書D-50aはZ-6の完了、D-50bはZ-9の完了を条件としており、優先順位は不明。\nどちらかを勝手に採用せず、両方の出典と食い違いを残して保留します。履歴の追加検索は不要です。'),('個別判断 / 顧客U-E','S-60を利用できるか質問。説明書D-60には「担当者による個別判断が必要」と記載。\n個別判断が必要なこととD-60を残して保留します。履歴の追加検索は不要です。')]:y=D.block(title,body,y)-14
D.block('成功条件','通常2件の根拠付き回答の送信と、例外3件の保留・引き継ぎをすべて満たすこと。全件保留や、資料のない一般論では達成になりません。',y)
brows=table_rows(sources['teamb_second_mission'],'| ID | 種別・働き | pt | 入力 | 出力・使える能力 |');assert len(brows)==14
lookup={r[0]:r for r in brows}
for pg in range(4):
 D.page('工程カード','B SECOND / 枠で切り分ける / ptは道具接続時も加算')
 for slot,row in enumerate(brows[pg*4:pg*4+4]):
  id,title,pt,inp,out=row
  if 'と同じ' in inp:inp=lookup[re.search(r'H\d',inp)[0]][3]
  if 'と同じ' in out:
   ref=re.search(r'H\d',out)[0]; out=out.replace(ref+'と同じ検索結果',lookup[ref][4]).replace(ref+'と同じ',lookup[ref][4])
  if id=='A5':out += ' 接続した道具だけを使い、途中の結果から次の検索を選ぶ。資料にない情報を補ったり、外部へ送信したりはできない。'
  x=34+(slot%2)*268;top=741-(slot//2)*344;D.box(x,top-326,255,326);D.text(id,x+14,top-27,20,TEAL);D.text(pt+' pt',x+191,top-27,18)
  yy=D.para(title,x+14,top-42,225,13)-14;D.text('入力',x+14,yy,9,TEAL);yy=D.para(inp,x+14,yy-10,225,10)-13;D.text('出力・能力',x+14,yy,9,TEAL);yy=D.para(out,x+14,yy-10,225,10)
  if id in ['T1','T3']:D.text('AIから呼出可能 ↔ 結果を返す',x+14,top-307,10,TEAL)
  if id=='A5':D.text('使える道具  ○────○',x+14,top-307,11,TEAL)
D.page('構成を組み直そう','B SECOND / 共有作業台紙 / A3',A3)
y=D.block('CURRENT FLOW / これまで使っていた構成','H0 → H1 → H2 → H3 → H4 → H5 → H6 → H7\n1 ＋ 5 ＋ 4 ＋ 5 ＋ 4 ＋ 6 ＋ 3 ＋ 2 ＝ 30pt',1070,w=760)
D.text('主線は → 、道具は ↔ で接続。不要なカードは台紙の外へ。',38,y,13,TEAL)
D.box(35,230,772,630,fill=PALE);D.text('カードを自由に置き、接続を描いてください。',53,825,12,MUTED)
D.text('構成の合計：　　　　　　pt ／ 上限12pt',40,175,18)
D.text('通常A □　通常B □　根拠不足 □　矛盾 □　個別判断 □',40,115,15)
D.text('全件で、同じカードと接続を使って確認してください。',40,75,12)
D.save();(TMP/'paper_pages.json').write_text(json.dumps(D.entries,ensure_ascii=False,indent=2))
# Web mockups are vector illustrations: readable text, static controls.
W=Doc('02_Web画面イメージとルール.pdf')
def screen(title):
 W.box(32,365,531,370,fill=PALE);W.c.setFillColor(INK);W.c.roundRect(32,695,531,40,7,fill=1,stroke=0);W.text('● ● ●',45,708,10,white);W.text(title,112,708,12,white)
def button(label,x,y,w=140):
 W.box(x,y,w,35,fill=TEAL,stroke=TEAL);W.center(label,x+w/2,y+11,12,white)
def person(x,y,name,number=None):
 W.c.setFillColor(HexColor('#B7CCCE'));W.c.circle(x,y+42,24,fill=1,stroke=0);W.c.roundRect(x-38,y-25,76,45,14,fill=1,stroke=0);W.center(name,x,y-46,12)
 if number is not None:W.box(x-18,y-17,36,34);W.center(str(number),x,y-7,22,TEAL)
W.page('認証室 / 呼び出し','A SECOND / 最初に見せる画面 / 静止画イメージ')
screen('認証室');W.text('認証対象：3名 ／ 応答済み：2名',61,663,15)
person(180,565,'左の人');person(413,565,'右の人');button('話を聞く',110,468);button('話を聞く',343,468)
W.text('呼出番号：',62,410,12);W.blanks(3,144,397,cell=34);button('呼び出す',324,397,185)
y=W.block('最後の参加者を呼び出してください','呼出番号は、2・4・8をそれぞれ1回ずつ使う3桁です。認証の開始には、最後の参加者の応答が必要です。',330)
y=W.block('左の人の話','「最後の参加者の呼出番号は、最初の数字が、最後の数字の2倍です。」',y)
W.block('右の人の話','「真ん中の数字が、3つの中でいちばん大きいです。」',y)
W.page('認証室からの呼び出し','A SECOND / 呼出番号が合った後に提示 / 静止画イメージ')
screen('認証室');W.center('認証室からの呼び出し',298,620,25);W.center('呼出先：482',298,555,27,TEAL);button('応答する',198,445,200)
W.block('着信','今操作している同じ画面に、呼び出しが届いています。\n準備ができたら「応答する」を選んでください。',320)
W.page('認証室 / 応答後','A SECOND / 応答した後に提示 / 静止画イメージ')
screen('認証室');W.center('これで3人そろいました。',298,660,18,TEAL);person(180,555,'左の人',2);person(413,555,'右の人',3);W.center('あなた：？',298,450,23);button('認証を開始',198,386,200)
y=W.block('認証のルール','3人はそれぞれ1〜20の整数を1つ付けています。いちばん大きな数は、残り2人の数の合計です。同じ数の人がいても構いません。\n他の2人の数は見えますが、自分の数は見えません。全員がルールを理解し、他の人も理解していると知っています。見える数字と、それまでの発言から論理的に判断します。',337)
y=W.block('発言の順番','左の人 → 右の人 → あなた。自分の数が1つに決まれば「分かった」、複数残れば「分からない」。嘘や当てずっぽうはありません。',y)
W.para('例：2・2・4は成立。2・3・4は不成立。\nチーム全員で「あなた」1人の視点を共有して考えます。',36,y,520,10)
W.page('認証室 / あなたの番','A SECOND / 認証開始後に提示 / 静止画イメージ')
screen('認証室 / 認証中');W.box(58,580,479,88);W.para('左の人（2）\n「自分の数は、まだ分からない。」',76,649,444,13);W.box(58,469,479,94);W.para('右の人（3）\n「左の人の返事を聞いても、自分の数は、まだ分からない。」',76,543,444,13);W.center('あなたの数を申告してください。',298,412,19,TEAL)
y=W.block('申告欄','自分の数：［　　　　　］',331)
y=W.block('理由の確認','自分が1だと仮定したとき、右の人は最終的に：\n□ 分かる　　□ 分からない\n「分かる」なら、右の人が確定する自分の数：［　　　　　］',y)
W.para('見える数字と2人の発言は、何度でも確認できます。',36,y,520,11)
W.page('回答を届ける窓口','B SECOND / 紙カードと組み合わせて使用 / 静止画イメージ')
screen('WORKFLOW / 構成エディター');W.text('構成 30pt ／ 上限 12pt',54,661,17,TEAL)
for i,id in enumerate(['H0','H1','H2','H3','H4','H5','H6','H7']):
 x=55+(i%4)*124;y=580-(i//4)*66;W.box(x,y,103,43);W.center(id,x+51,y+16,17);W.text('→',x+105,y+15,13)
button('次へつなぐ',53,445,148);button('道具として接続',221,445,148);button('構成から外す',389,445,148);button('全テストを実行',176,385,240)
y=W.block('窓口を完成させよう','未来の窓口には、「必要な情報がありません」というAIの下書きが積み上がっている。問い合わせの種類は増えたが、仕事の組み立て方は昔のままだ。条件を満たす構成を完成させてほしい。',332)
y=W.block('操作イメージ','カードを選び、主線の順番をつなぎ直します。「AIから呼出可能」のカードは、AI担当の「使える道具」にも接続できます。主線は一方向、道具は呼出・結果返却の往復線で表示します。',y)
W.para('詳細な目的・14枚の工程カード・5件の公開テスト・接続ルールは、このPDFの前のページにあります。試遊では紙で配置と接続を作ってください。',36,y,520,11)
# C shared and role-specific diagrams
W.page('配信室の復旧','C SECOND / 3人共通の案内')
y=W.block('離れた3つの端末を、言葉でつなごう','未来の配信室では、担当ごとの作業は終わっているのに、データが届かない。観測端末にはランプ、仕様端末には配線の条件、操作端末にはボタンと返送票が残っている。3つの端末で配線を特定し、配信を復旧してほしい。',735)
y=W.block('目標と基本ルール','配線型を特定し、3つのランプをすべて点灯させよ。\nボタンを押すと、つながっているランプの点灯・消灯が入れ替わります。つながっていないランプはそのまま。同じランプを2回反転すると元に戻ります。\n診断に使える操作は2回。診断でもランプの状態は変わります。配線型と各ボタンの作用先は、途中で変わりません。',y)
y=W.block('3つの役割','FIELD：現在のランプ状態を見る。\nRULE：配線の関係を読む。\nCONTROL：操作し、返送票を受け取る。',y)
y=W.block('参加方法','1人1役を担当し、互いの画面が見えない離れた席からMeetの音声通話で相談します。画面共有は使わず、見えているものを言葉で伝えてください。端末に過去のランプ状態は残りません。手元の紙にメモできます。\n各自の役割ページだけを受け取ってください。静止画の試遊ではログイン操作はありません。',y)
W.para('本番では、役割ごとのID・パスワードを紙で個別に受け取り、共通のWebサービスにログインする想定です。',36,y,520,10,MUTED)
W.page('観測端末','C SECOND / FIELD担当だけに配布 / 静止画イメージ')
screen('FIELD / 現在の状態')
for i,name in enumerate(['左','中','右']):
 x=135+i*163;W.center(name,x,622,19);W.c.setFillColor(HexColor('#667783'));W.c.circle(x,548,40,fill=1,stroke=0);W.center('消灯',x,471,18)
W.center('現在のランプ状態',298,403,12,MUTED)
W.block('あなたの端末','左・中・右の現在の状態を読み、音声で仲間へ伝えてください。\n操作が行われると、表示はその時点の状態に切り替わります。直前の状態や履歴は画面に残りません。必要なことは自分のメモに残せます。',327)
W.page('仕様端末','C SECOND / RULE担当だけに配布 / 静止画イメージ')
screen('RULE / 配線の関係');W.text('型',53,656,11,TEAL);W.text('Pと中の関係',103,656,11,TEAL);W.text('Rが反転させるランプ',273,656,11,TEAL)
rr=table_rows(sources['teamc_second_mission'],'| 配線型 | Pと中のランプの関係')
for i,row in enumerate(rr):
 top=630-i*58;W.c.setStrokeColor(LINE);W.c.line(50,top+8,540,top+8);W.text(row[0],54,top-17,15);W.para(row[1],100,top,158,10);W.para(row[2],272,top,264,10)
y=W.block('この表の読み方','実際の配線型はI〜IVのどれか1つです。この表は、ボタン同士の作用の関係を示します。現在点灯しているランプの一覧ではありません。',330)
W.block('Rの欄について','PとQで反転するランプを比べます。「PでもQでも反転する」は、どちらを押したときも反転するランプのことです。\n観測を条件に当てはめ、音声で仲間と確かめてください。',y)
W.page('操作端末','C SECOND / CONTROL担当だけに配布 / 静止画イメージ')
screen('CONTROL / 診断と復旧');W.text('残り診断回数：2',55,656,17);button('接続確認：P',56,595,150)
W.box(228,595,140,35);W.center('Q',298,607,14,MUTED);W.box(390,595,140,35);W.center('R',460,607,14,MUTED);W.text('最初はPのみ操作可能。2回目はP・Q・Rから選択。',56,571,10)
W.text('返送票の対応',56,536,13,TEAL)
for i,line in enumerate(['配線型        P           Q           R','I             白丸○      黒丸●      白丸○','II            黒丸●      白丸○      黒丸●','III           黒丸●      白丸○      黒丸●','IV            黒丸●      白丸○      黒丸●']):W.text(line,70,510-i*25,12)
y=W.block('操作の特性','P・Qは、それぞれ2つのランプを反転させます。PとQの反転対象の組み合わせは異なります。Rは1つだけを反転させ、左のランプには接続されていません。',335)
y=W.block('返送票について','操作後に届く白丸○・黒丸●は、信号が通った経由口の記録です。成功・失敗ではありません。同じ記号でも、ボタンによって候補が変わります。',y)
W.block('診断後の復旧','配線型を申告し、復旧に使うP・Q・Rを選んでまとめて実行します。各ボタンは0回または1回。順序は問いません。診断後の状態から復旧し、全点灯を目指します。',y)
W.save();(TMP/'web_pages.json').write_text(json.dumps(W.entries,ensure_ascii=False,indent=2))
print(json.dumps({'paper_pages':D.n,'web_pages':W.n,'maze_lengths':[len(p) for p in paths],'common_cells':sorted(common)},ensure_ascii=False))
