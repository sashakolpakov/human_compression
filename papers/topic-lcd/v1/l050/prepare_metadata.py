#!/usr/bin/env python3
"""Author-side metadata generation; never changes retained packet bytes."""
from pathlib import Path
import collections,hashlib,json,re

HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def record(p,role):return dict(path=str(p.relative_to(HERE)),bytes=p.stat().st_size,sha256=sha(p),role=role)

def main():
 source=json.loads((HERE/'source_map.json').read_text())
 source['status']='AUTHOR_COMPLETE_CORRECTED_CONTRACT_DISTINCT_REVIEW_PENDING'
 for row in source['records']:
  if row['id'] in ['P2group','P2groupS']:
   row['disposition']='PROVED';row['proof_files']=['sections/04-graph120.tex','sections/04b-group120.tex']
   row['premises']=['group120 complete actual projector/support/refinement certificate','enumerations complete112 minimum words','module120 abstract group identification']
  row['proof_file_hashes']={p:sha(HERE/p)for p in row['proof_files']}
 save('source_map.json',source)
 # Disjoint local proof contexts; the source-row correspondence may use several.
 contexts=[]
 for p in sorted((HERE/'sections').glob('*.tex')):
  lines=p.read_text().splitlines(True)
  cuts=[i for i,s in enumerate(lines)if re.match(r'\\(?:section|subsection|paragraph)\{',s)]
  if not cuts or cuts[0]!=0:cuts=[0]+cuts
  for n,i in enumerate(cuts):
   j=cuts[n+1]if n+1<len(cuts)else len(lines)
   text=''.join(lines[i:j]);title=lines[i].strip()
   contexts.append(dict(id=p.stem+'.'+str(n+1),path=str(p.relative_to(HERE)),start_line=i+1,end_line=j,sha256=hashlib.sha256(text.encode()).hexdigest(),heading=title))
 save('proof_contexts.json',{'status':'EXACT_CURRENT_PROOF_CONTEXTS','contexts':contexts,'count':len(contexts),'not_exclusive_complexity_owners':True})
 old=json.loads((HERE/'program_inventory.json').read_text())
 roles={r['path']:r['role']for r in old['whole_executable_files']}
 roles.update({'inputs/common_scalar/check_association_counts.py':'REQUIRED_COMMON_SCALAR_CERTIFICATE',
               'inputs/group120/check.py':'REQUIRED_COMPLETE_MATHEMATICAL_PROGRAM',
               'inputs/group120/retained/steiner_construction.py':'REQUIRED_COMPLETE_MATHEMATICAL_PROGRAM',
               'inputs/group120/retained/enumerate_ternary.c':'REQUIRED_RETAINED_COMPLETE_ENUMERATOR',
               'assemble.py':'OPERATIONAL_MIGRATION', 'prepare_metadata.py':'OPERATIONAL_INVENTORY',
               'check.py':'OPERATIONAL_REPLAY_AND_OPTIONAL_CONTROLS'})
 files=[]
 for root in ['inputs','programs']:
  for p in sorted((HERE/root).rglob('*')):
   if p.is_file()and p.suffix in ['.py','.g','.c']:
    key=str(p.relative_to(HERE));files.append(record(p,roles.get(key,'OPERATIONAL_OR_PROVENANCE_PROGRAM')))
 for f in ['assemble.py','prepare_metadata.py','check.py']:
  p=HERE/f
  if p.exists():files.append(record(p,roles[f]))
 data={r['path']:r for r in old.get('literal_data_and_retained_outputs',old.get('literal_or_retained_required_data',[]))}
 additions=[('inputs/common_scalar/counts.json','REQUIRED_COMMON_SCALAR_OUTPUT'),('inputs/group120/certificate_data.json','REQUIRED_LITERAL_SEED_AND_REFINEMENT'),('inputs/module120/author_replay/K_enumeration.json','RETAINED_COMPLETE_ENUMERATION_OUTPUT'),('inputs/module120/author_replay/N_enumeration.json','RETAINED_COMPLETE_ENUMERATION_OUTPUT')]
 for name,role in additions:data[name]=record(HERE/name,role)
 # Every bound literal basis, generator and full module data is an actual premise.
 for p in sorted((HERE/'inputs').rglob('*')):
  if p.is_file()and(p.name in ['module_data.json','generators.json','certificate_data.json']or p.name.endswith('_basis.txt')or('bases'in p.parts and p.suffix=='.txt')):
   data[str(p.relative_to(HERE))]=record(p,'REQUIRED_LITERAL_BASIS_OR_ACTION')
 identical=collections.defaultdict(list)
 for r in files:identical[r['sha256']].append(r['path'])
 old.update(status='COMPLETE_WHOLE_FILE_ROLE_INVENTORY',whole_executable_files=files,literal_data_and_retained_outputs=list(data.values()),identical_content_occurrences=[dict(sha256=k,paths=v)for k,v in identical.items()if len(v)>1])
 old.pop('common_required_program_followup',None)
 old.pop('literal_or_retained_required_data',None)
 old['acceptance_packet_tools']='Complete distinct-review archives are provenance/evidence; their checkers are not additional mathematical programs used by this application.'
 old['common_program_scope']='The scalar certificate is included because the entire common paper is retained, even though L050 does not invoke its subset-family classification.'
 old['large_enumeration_scope']='The full seven completed distributions and both K/N distributions are retained finite inputs; their exact full C programs and bases remain present. This assembly does not rerun them or claim that a pre-completion method review reviewed later histograms.'
 save('program_inventory.json',old)
 migration=json.loads((HERE/'migration.json').read_text());migration['status']='EXACT_PROOF_MIGRATION_WITH_LOCAL_ADDITIONS';save('migration.json',migration)
 dep=json.loads((HERE/'dependencies.json').read_text());dep['status']='COMPLETE_EXACT_RETAINED_CLOSURE';save('dependencies.json',dep)
 save('retained_inputs.json',{'classifications':[{'name':'Coolsaet Theorem3','use':'Identify actual105 graph with intended source graph via complement SRG uniqueness','proved_here':False},{'name':'Atlas of Brauer Characters source[13]','use':'Three faithful15dimensional L3(4) modules; M22 unique21 and minimum nontrivial degree; M23 listed absolute degrees and finite-field descent','proved_here':False},{'name':'Specified Witt system and source subgraph identifications','use':'Actual binary construction exhaustively checked; comparison to named McLaughlin subgraphs retained from source attribution','proved_here':'actual design and adjacency construction only'},{'name':'Historical optimal-code tables and Sendrier','use':'Attributed historical comparisons and asymptotic class result; no local dimension, distance or group proof depends on a table optimality assertion','proved_here':False}], 'source_software_unknown':True,'source_software_length':None,'source_embedded_executable_listing':False,'source_listing_screen_pages':list(range(1,12)),'unresolved':['Uniqueness of every SRG(253,140,87,65)','Construction of the other two faithful15dimensional L3(4) modules mentioned in Remark3'],'no_new_question_credit':True})
 print(json.dumps({'source_rows':len(source['records']),'proof_contexts':len(contexts),'executable_occurrences':len(files),'mathematical_data_occurrences':len(data)}))
if __name__=='__main__':main()
