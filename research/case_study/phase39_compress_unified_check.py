#!/usr/bin/env python3
"""Read-only source/span/census and internal-reference checker; no proof claims."""
import hashlib,json,re,sys
from pathlib import Path
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def checked(b):
 data=(P/b['path']).read_bytes();assert sha(data)==b['sha256'],b['path'];return data
c=json.loads((P/'phase39_compress_unified_intake.json').read_text());t=checked(c['manuscript']).decode()
for b in c['source_files']+c['component_provenance']+c['proof_census_costs']:checked(b)
for row in c['targets']:
 for text,s in [((P/row['source_file']).read_text(),row['source_span']),(t,row['replacement_span'])]:
  a,b=s['start_codepoint'],s['end_codepoint_exclusive'];assert 0<=a<b<=len(text);assert sha(text[a:b].encode())==s['sha256_utf8'],row['adapter']
expected=[f'A{i}' for i in range(1,5)]+[f'B{i}' for i in range(1,9)]+[f'C{i}' for i in range(1,12)]+[f'D{i}' for i in range(1,12)]
assert re.findall(r'\*\*Corollary ([ABCD]\d+) —',t)==expected
assert len(c['B_clause_rows'])==17
assert len(c['complete_N008_numbered_inventory'])==10
labels=re.findall(r'\\tag\{([^}]+)\}',t);assert len(labels)==len(set(labels))
refs=set(re.findall(r'\b(?:Lemma|Theorem|Corollary) (Q\d+\.\d+)',t));defs=set(re.findall(r'\*\*(?:Lemma|Theorem|Corollary) (Q\d+\.\d+)',t));assert refs<=defs,refs-defs
for eq in re.findall(r'\((A\d+\.\d+|Q\d+\.\d+|S\.\d+)\)',t):assert eq in labels,eq
old=(P/'phase37_compress_twogroups_manuscript.md').read_text();newcode=re.findall(r'```gap\n(.*?)\n```',t,re.S);oldcode=re.findall(r'```gap\n(.*?)\n```',old,re.S);assert len(newcode)==1 and newcode==oldcode
for token in ['CFSG-dependent W2','nontrivial transposition','Prüfer','Theorem S','Theorem K']:
 assert token in t,token
print(json.dumps({'status':'PASS_read_only_integrity_not_mathematical_review','manuscript_sha256':sha(t.encode()),'intake_sha256':sha((P/'phase39_compress_unified_intake.json').read_bytes()),'primary_files':len(c['source_files']),'source_and_adapter_spans':len(c['targets']),'clause_rows_B':17,'N008_numbered_inventory':10,'equation_labels':len(labels),'all_internal_Q_references_resolve':True,'full_AppA_code_exact':True,'infinite_correction_and_CFSG_boundary_present':True,'seven_source_factor':None},indent=2))
