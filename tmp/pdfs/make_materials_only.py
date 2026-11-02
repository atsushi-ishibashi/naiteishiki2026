from pathlib import Path
p=Path('tmp/pdfs/build_materials.py');lines=p.read_text().splitlines()
remove=set(range(58,66))|{67,68,73,87,96,112,116,125,133,134,180,187,188}|set(range(236,241))|{244,248,289,292,293,294,299,305,306,307}|set(range(309,315))|{320,326,327,334,335}
new=[]
for no,line in enumerate(lines,1):
 if no in remove:continue
 if no==66:line="D.page('参考資料','START');y=730"
 if no==111:line="D.page('部署メモ','A FIRST')"
 if no==132:line="D.page('沿革の断片','B FIRST')"
 if no==137:line=line.replace('top=350-i*91','top=720-i*190')
 if no==186:line="D.page('記録の復元台紙','C FIRST');D.text('法人化＝0',40,720,20,TEAL)"
 if no==243:line=line.replace('y=D.block(title,body,y)-20',"y=D.block(title,body.split('\\n回答には')[0],y)-20")
 if no==247:line=line.replace('y=D.block(title,body,y)-14',"y=D.block(title,body.split('\\n')[0],y)-14")
 if no==245:line="D.page('公開テスト / 問い合わせ','B SECOND')"
 if no==284:line="y=W.block('呼出番号','2・4・8をそれぞれ1回ずつ使う3桁。',330)"
 if "D.text('読む順：" in line:continue
 if "D.text('主線は →" in line:continue
 if "D.text('全件で、同じカード" in line:continue
 if "D.box(35,230" in line:line="D.box(35,230,772,630,fill=PALE)"
 if "D.text('← 切り取って" in line:line=line.split(";D.text('←")[0]
 if "D.para('この記録が歴史の何番目か" in line:continue
 if "W.text('最初はPのみ操作可能" in line:line=line.split(";W.text('最初はPのみ操作可能")[0]
 # Keep only section names in small headers, no production/progression instructions.
 if 'self.text(tag,32' in line:line=line.replace('self.text(tag,32','self.text(tag.split(" / ")[0],32')
 new.append(line)
Path('tmp/pdfs/materials_only.py').write_text('\n'.join(new)+'\n')
