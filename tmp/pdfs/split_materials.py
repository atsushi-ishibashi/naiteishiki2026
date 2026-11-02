from pathlib import Path
from pypdf import PdfReader,PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import json
root=Path.cwd();temp=root/'tmp/pdfs';out=root/'output/pdf'
pdfmetrics.registerFont(TTFont('JP','/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))
paper=PdfReader(out/'01_紙の試遊キット.pdf');web=PdfReader(out/'02_Web画面イメージとルール.pdf')
meta={k:dict(json.loads((temp/(k+'_pages.json')).read_text())) for k in ['paper','web']}
plans=[
 ('start_mission','最初のオフィスはどこ？',list(range(2,9)),[], '10枚の創業の記録カードと、共有の宛先台紙です。カードは枠で切り分け、1人1枚配ります。noteのリンクはルール説明のタイトルから開けます。', '最終ページの宛先台紙はA3。ほかはA4。'),
 ('teama_first_mission','最初の顧客はどこにいる？',[12,9,10,11,13,14],[], 'カードは左右の表と裏をセットで切り、中央で折って背中合わせに貼ります。▲の向きをそろえてください。部署メモは枠で切り分けます。封筒型ケースは外形を切り、印刷面を内側にして破線で折ります。左右、下、上の順に折り込み、テープで封をせず開ける状態で、カード・メモ・配置台紙を包んでください。','最終ページの封筒型ケースはA3。ほかはA4。'),
 ('teamb_first_mission','4つのサービス、1つの正体',[15,16,17,18,19,20],[], '4枚の迷路を1人1枚ずつ担当し、共通の文字盤に経路を記録します。沿革の断片は枠で切り分けられます。○・△・□・☆の4種類の印を使います。迷路の薄い点線はマスの境界、濃い実線は壁です。','全ページA4。'),
 ('teamc_first_mission','会社が存在しない会社の記録',list(range(21,27)),[], '9枚の観測記録カードを枠で切り分け、混ぜて渡してください。台紙の0マーカーも切り取ります。記録位置を書き直せるよう、鉛筆と消しゴムを用意します。カードのグラフはゲーム用の架空データです。','全ページA4。'),
 ('teama_second_mission','認証室',[],[1,2,3,4], 'チーム全員が同じ「あなた」の視点で考えます。各ページの上部に書かれた段階で、その画面を提示してください。先のページをまとめて見ないよう、1ページずつ使います。','全ページA4。画面表示でも使えます。'),
 ('teamb_second_mission','12ポイントで回答を届ける',list(range(27,35)),[5], '工程カード14枚を枠で切り分けます。目的・接続ルールと5件の公開テストを共有し、作業台紙にカードと矢印を置いて構成を考えます。最後のページはWeb画面のイメージです。','作業台紙（9ページ目）はA3。ほかはA4。'),
 ('teamc_second_mission','配信室の復旧',[],[6,7,8,9], '共通の案内を確認した後、FIELD・RULE・CONTROLの役割ページを1人1枚ずつ配ります。各自の資料だけを見て、離れた席から音声で相談します。メモ用紙と筆記具を用意してください。','全ページA4。画面表示でも使えます。'),
]
for folder,title,pp,wp,prep,printing in plans:
 cover=temp/(folder+'_cover.pdf');c=canvas.Canvas(str(cover),pagesize=A4);w,h=A4
 c.setFillColor(HexColor('#167C80'));c.rect(0,h-13,w,13,fill=1,stroke=0)
 def text(t,x,y,size=12,color='#172F3D'):
  c.setFont('JP',size);c.setFillColor(HexColor(color));c.drawString(x,y,t)
 def para(t,y,size=12):
  p=Paragraph(t,ParagraphStyle('p',fontName='JP',fontSize=size,leading=size*1.7,wordWrap='CJK',textColor=HexColor('#172F3D')));_,hh=p.wrap(515,900);p.drawOn(c,40,y-hh);return y-hh
 text(folder.upper().replace('_',' '),40,790,10,'#167C80');text(title,40,746,23)
 text('試遊素材',40,708,17);text('印刷・配布の準備 / このページは参加者への配布前に外せます',40,678,10,'#617581')
 text('用意するもの',40,624,14,'#167C80');y=para(prep,605)
 text('印刷設定',40,y-36,14,'#167C80');y=para('片面・実際のサイズ（100%）で印刷してください。'+printing,y-54)
 if wp:y=para('Web画面は静止画のイメージです。ボタンや自動判定は動作しません。',y-25)
 y-=42;text('収録ページ',40,y,14,'#167C80');y-=25
 for index,(kind,page) in enumerate([('paper',p) for p in pp]+[('web',p) for p in wp],start=2):
  text(str(index).rjust(2)+'  '+meta[kind][page],40,y,10);y-=20
 text('解答・解説・運営用の進行ガイドは収録していません。',40,52,9,'#617581');c.save()
 writer=PdfWriter();writer.add_page(PdfReader(cover).pages[0]);writer.add_outline_item('印刷・配布の準備',0)
 for i,(kind,page) in enumerate([('paper',p) for p in pp]+[('web',p) for p in wp],start=1):
  writer.add_page((paper if kind=='paper' else web).pages[page-1]);writer.add_outline_item(meta[kind][page],i)
 writer.add_metadata({'/Title':title+' / 試遊素材','/Author':'Finatext 内定式企画','/Subject':'参加者用素材・画面イメージ（解答なし）'})
 dest=root/folder/'試遊素材.pdf';writer.write(dest);print(str(dest),len(writer.pages))
# Consolidated files are intermediate, only mission files are deliverables.
for filename in ['01_紙の試遊キット.pdf','02_Web画面イメージとルール.pdf']:
 (out/filename).replace(temp/filename)
