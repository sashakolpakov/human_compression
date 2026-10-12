"""In-memory failure controls: no mutation of source or frozen science files."""
from copy import deepcopy
from types import SimpleNamespace
from extract_inputs import load,validate_policy,validate_selection,validate_glyphs,bound
from font_tools import need

def controls(args,cache):
 result=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,TypeError):result.append(dict(name=name,rejected=True));return
  raise ValueError('Accepted negative control '+name)
 p=load('policy.json');d=load('document_map.json');r=load('raw_file_map.json')
 for name,change in [
 ('change inherited primary',lambda x:x['primary'].update(variant='raw_untrimmed')),
 ('invent software factor',lambda x:x['symmetric_program_rule'].update(software_inclusive_factor=1)),
 ('zero unknown source software',lambda x:x['unknowns'].update(source_programs=0))]:
  x=deepcopy(p);change(x);reject(name,lambda x=x:validate_policy(x,d,r))
 for name,change in [
 ('drop complete R1 application',lambda x:x['documents'].pop(3)),
 ('reuse old changed R1 cells',lambda x:x['reusable_exact_rows'].append('R1')),
 ('restore sibling premise',lambda x:x['pair_map'][1]['prepaid_documents'].append('R1')),
 ('omit required graph data',lambda x:x['pair_map'][1]['required_files'].pop()),
 ('drop bibliography page',lambda x:x['documents'][4].update(pages=11))]:
  x=deepcopy(d);change(x);reject(name,lambda x=x:validate_policy(p,x,r))
 for name,change in [
 ('drop graph data file',lambda x:x['files'].pop(10)),
 ('promote optional diagnostic',lambda x:x['files'][0].update(role='required_finite_certificate')),
 ('prune full raw program',lambda x:x['files'][0].update(whole_file=False)),
 ('overclaim formal coverage',lambda x:x.update(partial_declarations=23))]:
  x=deepcopy(r);change(x);reject(name,lambda x=x:validate_policy(p,d,x))
 row=load('input_spec.json')['L126'];c=cache['L126'];aliases=load('glyph_aliases.json')['aliases']
 for name,change in [
 ('omit actual alias',lambda x:x['glyph_substitutions'].pop()),
 ('erase actual outline',lambda x:x['glyph_substitutions'][0].update(output='')),
 ('invent full mapsto arrow',lambda x:next(g for g in x['glyph_substitutions']if g['input']=='7').update(output='↦')),
 ('wrong encoded byte',lambda x:x['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=255)),
 ('wrong actual dictionary',lambda x:x['glyph_substitutions'][0]['pdf_events'][0].update(font_identity='bad')),
 ('wrong effective encoding',lambda x:x['glyph_substitutions'][0]['pdf_events'][0].update(effective_encoding_sha256='bad')),
 ('wrong visible context',lambda x:x['glyph_substitutions'][0].update(context_sha256='bad'))]:
  x=deepcopy(row);change(x);reject(name,lambda x=x:validate_glyphs('L126',c['raw'],c['fonts'],c['pages'],c['events'],x,aliases))
 for name,change in [
 ('drop first source character',lambda x:x['included_spans'][0].update(start=1)),
 ('erase source arXiv banner',lambda x:x['excluded_furniture'].insert(0,dict(start=0,end=39))),
 ('invent source header',lambda x:x['excluded_furniture'][1].update(literal='invented'))]:
  x=deepcopy(row);change(x);reject(name,lambda x=x:validate_selection('L126',c['raw'],x,c['pages'],c['meta']))
 data=next(x for x in r['files']if x['role']=='required_graph_data');x=dict(root='sources',**data);x['bytes']-=1;reject('truncated whole graph input',lambda:bound(x,args))
 x=dict(root='sources',path='../outside',bytes=1,sha256='bad');reject('traversal input route',lambda:bound(x,args))
 return result
