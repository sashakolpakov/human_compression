from pathlib import Path
W=Path(__file__).resolve().parent
S=W.parents[1]
s=(S/'corpus106_L027_rank_obstruction_v1/check.py').read_text()
a=s.index('def parse(b):');b=s.index('\ndef main():',a)
s=s[:a]+'''def parse(b):
 lines=b.decode().replace('\\r','').splitlines()
 need(len(lines)==68 and lines[-1]=='PASS_ALL_ODD_THREE_CONTROLS','complete finite receipt')
 need(sum(t.startswith('GENERIC ') for t in lines)==50,'exact affine roster')
 need(sum(t.startswith('TRIANGULAR ') for t in lines)==9,'exact triangular roster')
 need(sum(t.startswith('CONIC ') for t in lines)==4,'exact conic roster')
 need(sum(t.startswith('UNIPOTENT ') for t in lines)==4,'exact unipotent roster')
 for t in lines[:-1]:need(t.endswith(' PASS'),'explicit successful receipt')
 return lines
'''+s[b:]
s=s.replace("str(P/'finite.g')],60)","str(P/'finite.g')],120)")
s=s.replace('rank_obstruction','odd_three')
a=s.index(" result=dict(status=");b=s.index("\n (out/'report.json')",a)
s=s[:a]+''' result=dict(status='PASS_L027_ODD_THREE_CONTROLS',exports=len(manifest['exports']),dependencies=len(deps),identities=literal['count'],affine_models=50,triangular_models=9,conic_markings=4,actual_subset_pairs=11584,unipotent_fields=4,guards=guards,native_pages=len(texts(native/'odd_three.pdf')),commands=commands,proof_status='Uniform written proof, bounded controls only',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)'''+s[b:]
(W/'check.py').write_text(s)
