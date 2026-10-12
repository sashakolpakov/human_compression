"""Independent expected geometry from accepted costs and fixed chart dimensions."""
from geometry_parser import svg_rectangles,pdf_rectangles,compare_geometry,compare_pdf
from derive import SOURCES,PAIRS

def expected(oracle,stem):
 p=oracle['primary'];d=p['document_costs'];out={}
 if stem=='costs':
  W=H=648.;maxcost=max(p['source_sum'],p['whole_written'])*1.12
  def top(name,y,left,value):
   x=.21*W+left/maxcost*.70*W;top=H-(.75*H+(y+.18+.55)/2.10*.14*H)
   out[name]=[x,top,value/maxcost*.70*W,.36/2.10*.14*H]
  top('bar-whole-source',1,0,p['source_sum']);left=0
  for key in ['U']+list(PAIRS.values()):top('bar-whole-'+key,0,left,d[key]);left+=d[key]
  limit=max(d['U'],*[d[k]for k in SOURCES],*[d[k]for k in PAIRS.values()])*1.12
  def bottom(name,y,value):out[name]=[.21*W,H-(.10*H+(y+.18+.60)/10.20*.53*H),value/limit*.70*W,.36/10.20*.53*H]
  bottom('bar-acquire-U',9,d['U'])
  for i,k in enumerate(SOURCES):bottom('bar-source-'+k,8-i+.2,d[k]);bottom('bar-application-'+k,8-i-.2,d[PAIRS[k]])
 else:
  W,H=648.,338.4;limit=max(p['source_sum'],p['whole_written'])*1.12
  for row in oracle['stages']:
   i=row['stage']
   for name,dx,key in [('source',-.19,'source_written'),('replacement',.19,'replacement_written')]:
    value=row[key]
    if value:
     out[f'bar-cumulative-{name}-{i}']=[.13*W+(i+dx-.16+.65)/10.30*.82*W,H-(.19*H+value/limit*.61*H),.32/10.30*.82*W,value/limit*.61*H]
 return out

def inspect(packet,oracle):
 out={}
 for stem in ['costs','cumulative']:
  want=expected(oracle,stem);svg=svg_rectangles((packet/(stem+'.svg')).read_text());compare_geometry(svg,want);pdf,height=pdf_rectangles(packet/(stem+'.pdf'));compare_pdf(pdf,height,want,0)
  out[stem]={'SVG_bars':len(svg),'PDF_bars':len(pdf),'independent_rectangles':want}
 return out
