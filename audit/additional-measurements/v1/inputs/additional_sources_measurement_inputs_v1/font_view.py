"""Render actual audited glyph outlines in bounded private panels."""
from pathlib import Path
import argparse,json,os
import pypdf
from font_tools import embedded,font_identity,need,sha
from fontTools.agl import toUnicode
from fontTools.pens.basePen import BasePen

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);args=ap.parse_args()
    O=Path(__file__).resolve().parent;R=O.parent;args.out.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR','/private/tmp/additional-input-mpl')
    import matplotlib;matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch
    class Pen(BasePen):
        def __init__(self):super().__init__(None);self.vertices=[];self.codes=[]
        def _moveTo(self,p):self.vertices.append(p);self.codes.append(MPath.MOVETO)
        def _lineTo(self,p):self.vertices.append(p);self.codes.append(MPath.LINETO)
        def _curveToOne(self,a,b,c):self.vertices.extend([a,b,c]);self.codes.extend([MPath.CURVE4]*3)
        def _closePath(self):self.vertices.append((0,0));self.codes.append(MPath.CLOSEPOLY)
        def _endPath(self):pass
    from extract_inputs import resolve
    pub=json.loads((O/'publication_binding.json').read_text())
    policy=json.loads((O/'policy.json').read_text());audits=json.loads((O/'font_audit.json').read_text());aliases=json.loads((O/'proposed_aliases.json').read_text())['aliases']
    records=[]
    for key,a in audits.items():
        row=(policy['source_roster']|policy['replacement_roster'])[key];pdf=resolve(row['path'],args,pub);need(sha(pdf.read_bytes())==row['sha256'],'exact PDF')
        wanted={}
        for r in a['encoded_glyph_classes']:
            alias=next((x for x in aliases if x['document']==key and x['font_identity']==r['font_identity'] and x['encoded_byte']==r['encoded_byte']),None)
            if alias or toUnicode(r['glyph_name'])!=r['decoded_text']:
                wanted[r['font_identity'],r['encoded_byte']]=(r,alias)
        seen=set()
        for page in pypdf.PdfReader(pdf).pages:
            for ref in page['/Resources']['/Font'].values():
                f=ref.get_object();fid,_=font_identity(f)
                if fid in seen:continue
                seen.add(fid)
                for (rid,byte),(r,alias) in wanted.items():
                    if rid!=fid:continue
                    _,mapping,strings=embedded(f);need(mapping[byte]==r['glyph_name'],'exact glyph')
                    obj=strings[r['glyph_name']];need(not isinstance(obj,dict),'outline expected')
                    pen=Pen();obj.draw(pen)
                    records.append(dict(key=key,font=r['font'],byte=byte,glyph=r['glyph_name'],input=r['decoded_text'],output=alias['output'] if alias else r['decoded_text'],vertices=pen.vertices,codes=pen.codes))
    inventory=[]
    for start in range(0,len(records),12):
        fig,axes=plt.subplots(3,4,figsize=(12,9))
        for ax in axes.flat:ax.axis('off')
        for ax,r in zip(axes.flat,records[start:start+12]):
            ax.add_patch(PathPatch(MPath(r['vertices'],r['codes']),facecolor='black'));ax.autoscale_view();ax.set_aspect('equal')
            ax.set_title(r['key']+' '+r['font']+' byte '+str(r['byte'])+'\n'+r['glyph']+' -> '+' '.join(f'U+{ord(c):04X}' for c in r['output']),fontsize=7)
        fig.tight_layout();path=args.out/f'panel-{start//12+1}.png';fig.savefig(path,dpi=110);plt.close(fig)
        inventory.append(dict(path=str(path),classes=[{k:v for k,v in r.items() if k not in ['vertices','codes']} for r in records[start:start+12]]))
    (args.out/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    print(len(records),'classes;',len(inventory),'actual-outline panels; private only')

if __name__=='__main__':main()
