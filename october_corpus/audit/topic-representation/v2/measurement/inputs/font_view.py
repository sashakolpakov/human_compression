#!/usr/bin/env python3
"""Private render of the bound source font outlines; do not redistribute output."""
from pathlib import Path
import argparse
import json
import pypdf
from extract_inputs import embedded, need, sha
from calibration import ALIASES


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh private outline output')
    source=json.loads((Path(__file__).parent/'policy.json').read_text())['source_roster']['F010']
    pdf=args.study_root/source['path'];need(sha(pdf.read_bytes())==source['sha256'],'exact source')
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib.path import Path as MPath
    from matplotlib.patches import PathPatch
    from matplotlib import pyplot as plt
    from fontTools.pens.basePen import BasePen
    class Pen(BasePen):
        def __init__(self):super().__init__(None);self.vertices=[];self.codes=[]
        def _moveTo(self,p):self.vertices.append(p);self.codes.append(MPath.MOVETO)
        def _lineTo(self,p):self.vertices.append(p);self.codes.append(MPath.LINETO)
        def _curveToOne(self,a,b,c):self.vertices.extend([a,b,c]);self.codes.extend([MPath.CURVE4]*3)
        def _closePath(self):self.vertices.append((0,0));self.codes.append(MPath.CLOSEPOLY)
        def _endPath(self):pass
    wanted=[(font,byte,raw,out,name) for (key,font,byte,raw),(out,name) in ALIASES.items()]

    wanted.extend([
        ('/IPSOSC+CMMI10',39,'φ','φ','phi1'),
        ('/WUERPZ+MSBM10',12,'⪇','⪇','lessnotequal'),
        ('/HANKPV+CMSY7',48,'′','′','prime'),
        ('/KSWBZS+MSAM10',3,'□','□','square'),
        ('/KSWBZS+MSAM10',69,'⊴','⊴','triangleleftequal'),
        ('/TUCRSU+CMSY10',54,'̸','̸','negationslash'),
        ('/TUCRSU+CMSY10',116,'⊔','⊔','unionsq')])
    faces={}
    for page in pypdf.PdfReader(pdf).pages:
        for f in page['/Resources']['/Font'].values():
            f=f.get_object();name=str(f['/BaseFont'])
            if any(x[0]==name for x in wanted):faces[name]=embedded(f)
    fig,axes=plt.subplots(6,4,figsize=(14,17))
    for ax,(font,byte,raw,out,name) in zip(axes.flat,wanted):
        stream,mapping,strings=faces[font];need(mapping[byte]==name,'expected actual outline name')
        pen=Pen();strings[name].draw(pen)
        ax.add_patch(PathPatch(MPath(pen.vertices,pen.codes),facecolor='black'))
        ax.autoscale_view();ax.set_aspect('equal');ax.axis('off')
        ax.set_title(font+' byte '+str(byte)+'\n'+name+' -> U+'+format(ord(out),'04X'),fontsize=9)
    fig.tight_layout();fig.savefig(args.out,dpi=150)
    print('Private embedded-outline render only; source glyph images are not packet exports.')


if __name__=='__main__':main()
