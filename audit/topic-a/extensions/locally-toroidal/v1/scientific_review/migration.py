"""Independent exact transport of the four already accepted proof bodies."""
import hashlib,json,re
from pathlib import Path

def need(t,m):
 if not t:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(t):return hashlib.sha256(t.encode()).hexdigest()
def read(p):return json.loads(p.read_text())
def replace(s,a,b):
 need(a in s,'declared old passage '+a[:50]);return s.replace(a,b)

def expected_bodies(base,p):
 m=read(p/'migration_draft.json');old={}
 for key,x in m['origins'].items():
  f=base/x['path'];need(sha(f)==x['sha256'],'exact accepted origin '+key);s=f.read_text();body=s[s.index(x['start']):s.index(x['end'])];need(digest(body)==x['retained_body_sha256'],'complete original proof-body span '+key);old[key]=body
 c=old['cubic'];c=replace(c,r'\section{The actual universal group and its periods}',r'\section{The cubic family and its period lattice}')
 for name in ['kernel_certificate.g','certificate.py']:c=replace(c,'\\path{'+name+'}','\\path{cubic/'+name+'}')
 c=replace(c,'[FLPW, p.~6]',r'\cite[p.~6]{source}');c=replace(c,'[FLPW, Theorem 3.1]',r'\cite[Theorem~3.1]{source}')
 s=old['square'];s=r'\section{The square family and its affine group}'+'\n'+s;s=replace(s,r'\section{The fixed affine group}'+'\n','')
 s=re.sub(r'\\tag\{(\d+)\}',lambda m:r'\tag{S.'+m[1]+'}',s)
 for n in [2,5,6,8,9,10]:s=replace(s,'('+str(n)+')','(S.'+str(n)+')')
 f=old['finite']
 for name in ['countermodel.py','formal/SectionFive.lean','exact_groups.g','model_data.json','finite_models.py']:f=replace(f,'\\path{'+name+'}','\\path{finite/'+name+'}')
 f=replace(f,'[FLPW]',r'\cite{source}')
 start=f.index('For completeness, (3) identifies each residue stabilizer');end=f.index('\n\nThe modified presentation',start)
 removed=f[start:end]
 need(digest(removed+'\n\n')==m['modifications'][0]['removed_text_sha256'],'exact removed generic proof')
 replacement='''The markers are nontrivial involutions. Equation (3) and the full typed
coset Helly property therefore satisfy UA.Geometry of the common paper.
The coset system is thin, residually connected and flag-transitive, and
the displayed group is its full type-preserving automorphism group.'''
 f=f[:start]+replacement+f[end:]
 f=re.sub(r'\\tag\{(\d+)\}',lambda m:r'\tag{F.'+m[1]+'}',f)
 for n in [1,2,3]:f=replace(f,'('+str(n)+')','(F.'+str(n)+')')
 rel=r'\section{The relation with the full cubic toroid}'+'\n'+old['cubic_toroid_relation']
 for a,b in [('[L003, pp.14--15]',r'\cite[pp.~14--15]{earlier}'),('[L003]',r'\cite{earlier}'),('[L121]',r'\cite{source}')]:rel=replace(rel,a,b)
 return dict(zip(['sections/01-cubic.tex','sections/02-square.tex','sections/03-finite.tex','sections/04-cubic-relation.tex'],[v.strip()+'\n' for v in [c,s,f,rel]]))

def validate(base,p,bodies=None):
 expected=expected_bodies(base,p)
 if bodies is None:bodies={f:(p/f).read_text() for f in expected}
 need(bodies==expected,'exact accepted proof transport plus one declared common-interface substitution')
 text='\n'.join(bodies.values());need(text.count('\\label{lem:group}')==1 and text.count('\\label{lem:helly}')==1,'unique migrated theorem labels')
 # Required hypotheses of the common geometry theorem remain in the finite route.
 finite=bodies['sections/03-finite.tex']
 for s in ['The markers are nontrivial involutions.','G_J\\cap G_K=G_{J\\cap K}','full typed\ncoset Helly property','four triples of maximal parabolics','four more tests']:
  need(s in finite,'finite UA.Geometry premise '+s)
 return {'complete_proof_bodies':4,'changed_generic_arguments':1,'changed_generic_interface':'UA.Geometry','unchanged_mathematical_body_except_that_call':True,'full_marking_IP_Helly_hypotheses_present':True,'source_word_and_marker_conventions_preserved':True}
