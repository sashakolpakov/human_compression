"""Literal adaptation of RunBorel: load complete levels; begin the next level."""
import difflib,hashlib,json
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
HERE=Path(__file__).resolve().parent
P=HERE.parent/'exhaustion_component_v2'
def derive(old):
 start=old.index('RunBorel:=function(bid)');s=old[start:]
 s=s.replace('RunBorel:=function(bid)','RunBorelFromLevel:=function(bid,resume)',1)
 marker=' else panels:=OvergroupsFromInclusions(B,maxinclusions);fi;\n'
 assert s.count(marker)==1
 s=s.replace(marker,marker+' if Set(panels)<>Set(resume.panels) then Error("saved panel inventory changed");fi;\n panels:=resume.panels;\n',1)
 a=s.index(' levels:=[List(Orbits(A,');b=s.index(' maxrank:=',a)
 s=s[:a]+''' levels:=ShallowCopy(resume.levels);allFull:=ShallowCopy(resume.geometries);
 Print("BOREL_RESUME id=",bid," completed_levels=",List(levels,Length)," next_rank=",Length(levels)+1,"\\n");
'''+s[b:]
 assert s.count(' for rank in [2..maxrank] do')==1
 s=s.replace(' for rank in [2..maxrank] do',' for rank in [Length(levels)+1..maxrank] do',1)
 return s
if __name__=='__main__':
 old=(P/'legacy_functions.g').read_text();new=derive(old);(HERE/'resume_borel.g').write_text(new)
 (HERE/'resume_delta.diff').write_text(''.join(difflib.unified_diff(old[old.index('RunBorel:=function(bid)'):].splitlines(True),new.splitlines(True),fromfile='accepted RunBorel',tofile='RunBorelFromLevel')))
 print(hashlib.sha256(new.encode()).hexdigest())
