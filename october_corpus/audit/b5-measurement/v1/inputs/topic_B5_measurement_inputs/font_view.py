from pathlib import Path
import json,os,argparse
import pypdf
from font_tools import embedded,font_identity,need
from fontTools.agl import toUnicode
from fontTools.pens.basePen import BasePen
O=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();out=args.out;need(not out.exists(),'fresh visual directory');out.mkdir(parents=True)
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
p=json.loads((O/'policy.json').read_text());audits=json.loads((O/'font_audit.json').read_text());records=[]
for key,a in audits.items():
 row=({'L040':p['source']}|p['replacements'])[key];file={'public':args.public_root,'sources':args.sources_root,'packet':O}[row['root']]/row['path']
 wanted={(r['font_identity'],r['encoded_byte']):r for r in a['encoded_glyph_classes'] if toUnicode(r['glyph_name'])!=r['decoded_text'] or 'CMSY' in r['font'] and r['glyph_name'].isascii() and r['glyph_name'].isupper()};seen=set()
 for page in pypdf.PdfReader(file).pages:
  for ref in page['/Resources']['/Font'].values():
   f=ref.get_object();fid,_=font_identity(f)
   if fid in seen:continue
   seen.add(fid)
   for (identity,byte),r in wanted.items():
    if identity!=fid:continue
    _,m,g=embedded(f);pen=Pen();g[r['glyph_name']].draw(pen);records.append((dict(document=key,**r),pen))
index=[]
for start in range(0,len(records),12):
 fig,axes=plt.subplots(3,4,figsize=(12,9))
 for ax in axes.flat:ax.axis('off')
 for ax,(r,pen) in zip(axes.flat,records[start:start+12]):
  ax.add_patch(PathPatch(MP(pen.v,pen.c),facecolor='black'));ax.autoscale_view();ax.set_aspect('equal');ax.set_title(r['document']+' '+r['font']+' '+str(r['encoded_byte'])+' '+r['glyph_name']+'\n'+repr(r['decoded_text']),fontsize=8)
 fig.tight_layout();path=out/f'panel-{start//12+1}.png';fig.savefig(path,dpi=110);plt.close(fig);index.append(dict(path=str(path),classes=[r for r,_ in records[start:start+12]]))
(out/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n');print(len(records),'classes',len(index),'panels')
