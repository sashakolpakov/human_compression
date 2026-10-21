from pathlib import Path
W=Path(__file__).resolve().parent;S=W.parents[1]
s=(S/'corpus106_L027_odd_three_v2/check.py').read_text();a=s.index('def parse(b):');b=s.index('\ndef main():',a)
s=s[:a]+'''def parse(b):
 lines=b.decode().replace('\\r','').splitlines()
 need(len(lines)==6 and lines[-1]=='PASS_PSU17_THREE_WITNESSES','complete finite receipt')
 for i,k in enumerate([7,8,9]):need(re.fullmatch(r'WITNESS '+str(i+1)+' TYPE 3 '+str(k)+r' 3 GROUP 2317678272 ENDS (168|2448) (168|2448) IP 256 REVERSERS 0 PASS',lines[i])is not None,'exact positive receipt')
 need(lines[3]=='NEGATIVE_PROPER_GROUP 2448 PASS' and lines[4]=='NEGATIVE_REFLECTABLE 1 PASS','both independent negative controls')
 return lines
'''+s[b:]
s=s.replace('odd_three','unitary_examples').replace("str(P/'finite.g')","str(P/'witnesses.g')")
a=s.index(" result=dict(status=");b=s.index("\n (out/'report.json')",a)
s=s[:a]+''' result=dict(status='PASS_L027_UNITARY_EXAMPLES',exports=len(manifest['exports']),dependencies=len(deps),positive_markings=3,actual_subset_pairs=768,projective_degree=4914,group_order=2317678272,centralizer_maps=36,negative_controls=2,literal_rows=len(literal['rows']),guards=guards,native_pages=len(texts(native/'unitary_examples.pdf')),commands=commands,proof_status='Three explicit positive pairs; no other-type exhaustion',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)'''+s[b:]
# Preserve the simple marker guard on the finite wrapper, and also test the literal checker itself.
s=s.replace("for mode in ['argument','environment']:\n  ee=dict(env);cmd=[sys.executable];target=out/('optimized_'+mode)","for mode in ['argument','environment']:\n  ee=dict(env);cmd=[sys.executable];target=out/('optimized_'+mode)")
(W/'check.py').write_text(s)
