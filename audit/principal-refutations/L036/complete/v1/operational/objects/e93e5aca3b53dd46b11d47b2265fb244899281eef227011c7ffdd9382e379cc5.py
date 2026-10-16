"""Transcribe source Tables3 and4 without group calculations or normalization."""
from pathlib import Path
import hashlib,json,re
from pypdf import PdfReader
H=Path(__file__).resolve().parent
SOURCE=H.parents[2]/'sources/catalogue_L036.pdf'
def need(b,m):
 if not b:raise ValueError(m)
def extract():
 pages=PdfReader(SOURCE).pages
 text3=pages[6].extract_text();text4=pages[7].extract_text()
 name=r'(GL2\(3\)|S5|L2\(11\)|M9\s*:\s*2|M10)'
 pattern=r'(?m)^\s*(\d+)\s+'+name+r'\s+'+name+r'\s+(.+?)\s+\[(\d+),\s*(\d+),\s*(\d+)\]\s*$'
 table3=[]
 for row,h,k,meet,dp,g,dl in re.findall(pattern,text3):
  table3.append(dict(row=int(row),G1=' '.join(h.split()),G2=' '.join(k.split()),intersection=' '.join(meet.split()),point_diameter=int(dp),gonality=int(g),line_diameter=int(dl)))
 need([r['row'] for r in table3]==list(range(1,38)),'37 exact printed geometry rows')
 table4=[]
 for row,star,lam,t,k,v in re.findall(r'(?m)^\s*(\d+)(∗?)\s+S(\d+)\((\d+),\s*(\d+),\s*(\d+)\)\s*$',text4):
  table4.append(dict(row=int(row),dual=bool(star),lambda_value=int(lam),t=int(t),k=int(k),v=int(v)))
 need(len(table4)==70 and {(r['row'],r['dual']) for r in table4}=={(i,d) for i in range(1,38) if i not in [31,32] for d in [False,True]},'70 exact printed design rows')
 table4.sort(key=lambda r:(r['row'],r['dual']))
 return dict(source_pdf_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),physical_pages=[7,8],table3=table3,table4=table4,printed_design_omissions=[31,32]),[text3,text4]
if __name__=='__main__':
 result,texts=extract()
 out=H/'printed.json';need(not out.exists(),'Fresh source transcription')
 out.write_text(json.dumps(result,indent=2)+'\n')
 for i,t in zip([7,8],texts):(H/f'source-page{i:02d}.txt').write_text(t)
 print(json.dumps({'table3_rows':37,'table4_rows':70,'source_comparison_performed':False}))
