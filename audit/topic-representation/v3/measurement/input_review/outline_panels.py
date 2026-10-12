#!/usr/bin/env python3
"""Private embedded-source outline viewer; raster/font bytes are not exports."""
import argparse,json,pathlib,sys,unicodedata
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from fontTools.pens.basePen import BasePen
from pypdf import PdfReader
from font_events import encoded_face
from recount import SOURCE_ALIASES
class Draw(BasePen):
    def __init__(self):super().__init__(None);self.vertices=[];self.codes=[]
    def _moveTo(self,p):self.vertices.append(p);self.codes.append(MPath.MOVETO)
    def _lineTo(self,p):self.vertices.append(p);self.codes.append(MPath.LINETO)
    def _curveToOne(self,a,b,c):self.vertices.extend([a,b,c]);self.codes.extend([MPath.CURVE4]*3)
    def _qCurveToOne(self,a,b):self.vertices.extend([a,b]);self.codes.extend([MPath.CURVE3]*2)
    def _closePath(self):self.vertices.append((0,0));self.codes.append(MPath.CLOSEPOLY)
    def _endPath(self):pass
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pdf',type=pathlib.Path,required=True);p.add_argument('--audit',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();a.out.mkdir();r=PdfReader(a.pdf);data=json.loads(a.audit.read_text());classes=data['classes'];extra={'negationslash','angbracketleft','angbracketright','unionsq','square','dblarrowheadright','prime','multicloseright'}
    rows=[x for x in classes if (x['font'].split('+')[-1],x['glyph_name'])in SOURCE_ALIASES or x['glyph_name']in extra];fig,axes=plt.subplots(4,4,figsize=(12,10));assert len(rows)==16
    for ax,x in zip(axes.flat,rows):
        font=r.get_object(x['font_dictionary'][0]);_,_,strings=encoded_face(font);pen=Draw();strings[x['glyph_name']].draw(pen);path=MPath(pen.vertices,pen.codes);ax.add_patch(PathPatch(path,color='black'));box=path.get_extents();pad=max(box.width,box.height)*.15;ax.set_xlim(box.xmin-pad,box.xmax+pad);ax.set_ylim(box.ymin-pad,box.ymax+pad);ax.set_aspect('equal');ax.axis('off');ax.set_title(f"obj{x['font_dictionary'][0]} byte{x['encoded_byte']} {x['glyph_name']}\nn={x['occurrences']}",fontsize=9)
    fig.tight_layout();fig.savefig(a.out/'L126_special_outlines.png',dpi=140);plt.close(fig);(a.out/'classes.json').write_text(json.dumps(rows,indent=2)+'\n');print(a.out/'L126_special_outlines.png')
