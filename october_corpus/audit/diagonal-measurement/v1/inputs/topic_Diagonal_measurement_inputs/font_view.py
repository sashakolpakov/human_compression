from pathlib import Path
import json,os,argparse
import pypdf
from font_tools import embedded,font_identity
from fontTools.agl import toUnicode
from fontTools.pens.basePen import BasePen
O=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();R=args.sources_root;out=args.out
if out.exists():raise ValueError('fresh glyph output required')
out.mkdir(parents=True)
os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
import matplotlib;matplotlib.use('Agg');from matplotlib import pyplot as plt
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch
class Pen(BasePen):
 def __init__(self):super().__init__(None);self.v=[];self.c=[]
 def _moveTo(self,p):self.v.append(p);self.c.append(MP.MOVETO)
 def _lineTo(self,p):self.v.append(p);self.c.append(MP.LINETO)
 def _curveToOne(self,a,b,c):self.v.extend([a,b,c]);self.c.extend([MP.CURVE4]*3)
 def _closePath(self):self.v.append((0,0));self.c.append(MP.CLOSEPOLY)
 def _endPath(self):pass
p=json.loads((O/'policy.json').read_text());a=json.loads((O/'font_audit.json').read_text())['N007'];wanted={(r['font_identity'],r['encoded_byte']):r for r in a['encoded_glyph_classes'] if toUnicode(r['glyph_name'])!=r['decoded_text'] or 'CMSY' in r['font'] and r['glyph_name']=='G'};records=[];seen=set()
for page in pypdf.PdfReader(R/p['source']['path']).pages:
 for ref in page['/Resources']['/Font'].values():
  f=ref.get_object();fid,_=font_identity(f)
  if fid in seen:continue
  seen.add(fid)
  for (key,byte),row in wanted.items():
   if key!=fid:continue
   _,m,g=embedded(f);pen=Pen();g[row['glyph_name']].draw(pen);records.append((row,pen))
if len(records)!=34:raise ValueError('all34 exceptional classes must be displayed')
index=[]
for start in range(0,len(records),12):
 fig,axes=plt.subplots(3,4,figsize=(12,9))
 for ax in axes.flat:ax.axis('off')
 for ax,(r,pen) in zip(axes.flat,records[start:start+12]):
  ax.add_patch(PathPatch(MP(pen.v,pen.c),facecolor='black'));ax.autoscale_view();ax.set_aspect('equal');ax.set_title(r['font']+' '+str(r['encoded_byte'])+' '+r['glyph_name']+'\n'+repr(r['decoded_text']),fontsize=8)
 fig.tight_layout();path=out/f'panel-{start//12+1}.png';fig.savefig(path,dpi=110);plt.close(fig);index.append(dict(path=str(path),classes=[r for r,_ in records[start:start+12]]))
(out/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n');print(len(records),'classes',len(index),'panels')
