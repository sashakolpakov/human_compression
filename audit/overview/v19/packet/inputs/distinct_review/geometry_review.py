"""Independent bar dimensions from accepted cells and inspected fixed axes; no plotter import."""
from geometry_parser import svg_rectangles,pdf_rectangles,compare_geometry,compare_pdf
from derive import SOURCES,PAIRS,COMMON,need

def expected(o,stem):
 p=o['primary'];d=p['document_costs'];apps=p['application_costs'];out={}
 if stem=='costs':
  W=H=648.;top_limit=max(p['source_sum'],p['whole_written'])*1.12
  def top(name,y,left,value):out[name]=[.21*W+left/top_limit*.70*W,H-(.75*H+(y+.18+.55)/2.10*.14*H),value/top_limit*.70*W,.36/2.10*.14*H]
  top('bar-whole-source',1,0,p['source_sum']);left=0
  for key in COMMON+list(PAIRS.values()):
   value=d[key]if key in COMMON else apps[key];top('bar-whole-'+key,0,left,value);left+=value
  bottom_limit=max(p['whole_common'],*[d[k]for k in SOURCES],*apps.values())*1.12
  def bottom(name,y,value):out[name]=[.21*W,H-(.10*H+(y+.18+.60)/11.20*.53*H),value/bottom_limit*.70*W,.36/11.20*.53*H]
  bottom('bar-acquire-U',10,p['whole_common'])
  for i,s in enumerate(SOURCES):bottom('bar-source-'+s,9-i+.2,d[s]);bottom('bar-application-'+s,9-i-.2,apps[PAIRS[s]])
 else:
  W,H=648.,338.4;limit=max(p['source_sum'],p['whole_written'])*1.12
  for row in o['stages']:
   i=row['stage']
   for name,dx,key in [('source',-.19,'source_written'),('replacement',.19,'replacement_written')]:
    value=row[key]
    if value:out[f'bar-cumulative-{name}-{i}']=[.13*W+(i+dx-.16+.65)/11.30*.82*W,H-(.19*H+value/limit*.61*H),.32/11.30*.82*W,value/limit*.61*H]
 return out

def inspect(packet,o):
 out={}
 for stem,count in [('costs',35),('cumulative',21)]:
  want=expected(o,stem);actual=svg_rectangles((packet/(stem+'.svg')).read_text());compare_geometry(actual,want);rect,H=pdf_rectangles(packet/(stem+'.pdf'));compare_pdf(rect,H,want,0);need(len(actual)==len(rect)==count,'full actual vector rectangles')
  out[stem]=dict(SVG_bars=len(actual),PDF_bars=len(rect),expected_rectangles=want)
 return out
