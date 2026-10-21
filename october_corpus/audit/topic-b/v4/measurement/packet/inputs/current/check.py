#!/usr/bin/env python3
"""Whole enlarged-B input replay. No group computation or formal build is run."""
from pathlib import Path
import argparse,copy,csv,io,json,subprocess,sys
import pypdf
from extract_inputs import H,load,need,sha,replay,validate_one,code_inclusion,bound
from build_reader import reader,build

def semantic(c):
 p=load('policy.json');old=load('precount/baseline/author_counts.json');src=load('precount/baseline/retained_source_counts.json')
 need(c['originals']==p['originals']and set(c['documents'])==set(old['documents'])|{'L047','U_B6','B6','CODE6'},'complete six-source document boundary')
 need(all(c['documents'][k]==v for k,v in old['documents'].items())and c['raw_files']==old['raw_files']and c['retained_source_coordinates']==src,'all inherited whole inputs exactly retained')
 need(set(c['new_raw_files'])=={r['id']for r in load('precount/raw_inventory.json')['files']if not r['inherited']},'all nine whole new files')
 need((c['total_main_document_cells'],c['total_raw_cells'],c['whole_programs'],c['drivers'],c['partial_Lean_files'],c['partial_declarations'],c['new_declarations'])==(480,170,10,5,2,14,0),'complete dimension and evidence inventory')
 need(c['factors']is None and c['software_inclusive_comparison']is None and c['source_software_cost']is None and c['full_graphics_cost']is None and c['external_proofs_cost']is None,'no factors or invented unknown costs')
 need(c['science_adopted']and not c['input_accepted']and c['source_credit']==c['question_credit']==0,'distinct scientific and metric statuses')
 for k,pages,repairs in [('L047',12,2),('U_B6',10,312),('B6',3,0),('CODE6',7,0)]:
  d=c['documents'][k];need(d['pages']==pages and d['glyph_repairs']==repairs,'all pages and bound aliases '+k)
  need(set(d['metrics'])==set(p['variants']),'three variants')
  for v in p['variants']:
   need(set(d['metrics'][v])==set(p['normalizations']),'two normalizations')
   for n in p['normalizations']:need(set(d['metrics'][v][n])==set(p['units'])|{'normalized_text_sha256','collapsed_text_sha256'},'five units with full hashes')
 for r,oldr in zip(c['source_coordinates'],src['coordinates']):
  q=copy.deepcopy(r);need(q['sources'].pop('L047')==c['documents']['L047']['metrics'][r['variant']][r['normalization']][r['unit']],'one source cost view, no duplicate charge');q['source_representations'].pop('L047');need(q==oldr,'all old source and article-only costs exact')
 need(len(c['source_coordinates'])==30 and c['program_inclusion']['files']==6 and c['program_inclusion']['all_lines_included']and c['program_inclusion']['wrap_glyphs_retained_in_all_measured_variants'],'all complete coordinates and code')

def tables(c):
 def csvtext(head,rows):
  o=io.StringIO(newline='');w=csv.writer(o,lineterminator='\n');w.writerow(head);w.writerows(rows);return o.getvalue()
 p=load('policy.json');rows=[]
 for k,d in c['documents'].items():
  for v in p['variants']:
   for n in p['normalizations']:
    for u in p['units']:rows.append([k,v,n,u,d['metrics'][v][n][u]])
 for r in c['retained_source_coordinates']['coordinates']:
  for k,v in r['sources'].items():rows.append([k,r['variant'],r['normalization'],r['unit'],v])
 raw=[]
 for cat,files in c['raw_files'].items():
  for k,d in files.items():
   for n in p['normalizations']:
    for u in p['units']:raw.append([cat,k,n,u,d['metrics'][n][u]])
 for k,d in c['new_raw_files'].items():
  for n in p['normalizations']:
   for u in p['units']:raw.append([d['category'],k,n,u,d['metrics'][n][u]])
 article=[[r['variant'],r['normalization'],r['unit'],r['L040_article_only']]for r in c['retained_source_coordinates']['coordinates']]
 return {'document_counts.csv':csvtext(['document','variant','normalization','unit','count'],rows),'raw_counts.csv':csvtext(['category','file','normalization','unit','count'],raw),'L040_article_sensitivity.csv':csvtext(['variant','normalization','unit','count'],article)}

def controls(c,cache):
 done=[]
 def reject(name,f):
  try:f()
  except(ValueError,KeyError,AssertionError,TypeError):done.append(name)
  else:raise ValueError('control survived '+name)
 def cm(name,f):
  q=copy.deepcopy(c);f(q);reject(name,lambda:semantic(q))
 cm('drop complete old common',lambda q:q['documents'].pop('U_B'))
 cm('drop complete new common',lambda q:q['documents'].pop('U_B6'))
 cm('remove old application',lambda q:q['documents'].pop('B2'))
 cm('delete new references page',lambda q:q['documents']['B6'].update(pages=2))
 cm('change old PDF vector',lambda q:q['documents']['U_B']['metrics']['raw_untrimmed']['NFC'].update(characters_without_whitespace=0))
 cm('change old raw vector',lambda q:q['raw_files']['programs']['programs/primitive_bound.g']['metrics']['NFC'].update(whitespace_tokens=0))
 cm('remove whole required roster',lambda q:q['new_raw_files'].pop('NEW_PROGRAM_6'))
 cm('drop sensitivity',lambda q:q['documents']['L047']['metrics'].pop('raw_selected'))
 cm('source count differs from one document',lambda q:q['source_coordinates'][0]['sources'].update(L047=0))
 cm('omit source coordinate',lambda q:q['source_coordinates'].pop())
 cm('unknown source software as zero',lambda q:q.update(source_software_cost=0))
 cm('software scalar invented',lambda q:q.update(software_inclusive_comparison=1))
 cm('premature factor',lambda q:q.update(factors=1))
 cm('premature count acceptance',lambda q:q.update(input_accepted=True))
 cm('new source credit',lambda q:q.update(source_credit=1))
 cm('full new formal claim',lambda q:q.update(new_declarations=14))
 cm('code wrap erased from metric boundary',lambda q:q['program_inclusion'].update(wrap_glyphs_retained_in_all_measured_variants=False))
 spec=load('input_spec.json')
 def rm(name,k,f):
  q=copy.deepcopy(spec[k]);f(q);reject(name,lambda:validate_one(k,q,*cache[k]))
 rm('wrong actual epsilon','L047',lambda q:q['glyph_substitutions'][0].update(output='e'))
 rm('drop a visible source event','L047',lambda q:q['glyph_substitutions'].pop())
 rm('wrong encoded byte','U_B6',lambda q:q['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=1))
 rm('wrong actual font dictionary','U_B6',lambda q:q['glyph_substitutions'][0]['pdf_events'][0].update(font_dictionary_sha256='0'*64))
 rm('merge mapsto components','U_B6',lambda q:next(g for g in q['glyph_substitutions']if g['pdf_events'][0]['glyph_name']=='mapsto').update(end=next(g for g in q['glyph_substitutions']if g['pdf_events'][0]['glyph_name']=='mapsto')['end']+1,output='↦'))
 rm('delete references as furniture','L047',lambda q:q['excluded_furniture'][-1].update(end=q['page_bindings'][-1]['end']))
 rm('drop physical footer','B6',lambda q:q['excluded_furniture'].pop())
 rm('erase algorithm prose as executable listing','U_B6',lambda q:q['excluded_listings'].append(dict(page=9)))
 files={f'{i}.g':f'Print("required-{i}");\n'for i in range(6)};tex='\n'.join('\\VerbatimInput{'+k+'}'for k in files);text=''.join(files.values());code_inclusion(tex,text,files)
 reject('truncated printed complete file',lambda:code_inclusion(tex,text[:-8],files))
 reject('line-pruned executable appendix',lambda:code_inclusion(tex.replace('VerbatimInput{','VerbatimInput[firstline=2]{',1),text,files))
 return done

def main():
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--public-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');v=a.parse_args();need(not v.out.exists(),'fresh output');v.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for e in load('manifest.json')['exports']:bound(H/e['path'],e)
 for e in load('helper_provenance.json'):bound(H/e['path'],e)
 r=subprocess.run([sys.executable,'-B','-O',str(H/'precount/check.py'),'--study-root',str(v.study_root),'--public-root',str(v.public_root),'--out',str(v.out/'precount_report.json')],capture_output=True,text=True);need(r.returncode==0,'precount binding replay '+r.stdout+r.stderr)
 for r in load('precount/source_editions.json')['inherited']:
  bound(v.study_root/r['declared_source_or_paper_path'],r)
 for r in load('inherited_visual_evidence.json').values():
  if isinstance(r,dict)and 'sha256'in r:bound(v.study_root/r['path'],r)
 c,cache=replay(v.study_root,v.public_root);semantic(c);need(c==load('author_counts.json'),'all new/inherited metric cells and hashes')
 for name,t in tables(c).items():need(t==(H/name).read_text(),'all exact CSV rows '+name)
 need(reader()==(H/'reader.tex').read_text(),'exact reader text from inputs');tests=controls(c,cache);rr=None
 if v.render:
  rr=build(v.out/'reader',v.xelatex);a=pypdf.PdfReader(H/'reader.pdf');b=pypdf.PdfReader(v.out/'reader/reader.pdf');need([p.extract_text()for p in a.pages]==[p.extract_text()for p in b.pages],'exact reader pages')
 report=dict(status='PASS_COMPLETE_INPUT_REPLAY',whole_document_cells=480,PDF_cells=450,literal_rendering_cells=30,retained_article_sensitivity_cells=30,whole_raw_cells=170,new_PDF_cells=120,new_raw_cells=90,old_document_cells_unchanged=360,old_raw_cells_unchanged=80,physical_PDF_pages=134,new_PDF_pages=32,precount_controls=15,controls=tests,reader=rr,programs_executed=False,formal_executed=False,factors=None,software_inclusive_comparison=None)
 (v.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
