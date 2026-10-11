"""Semantic negative controls; no Python assert, no scientific computation."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import json,re
import extract_inputs as E
from font_tools import embedded, validate_unembedded_banner, need

def run(args,cache):
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError) as e:rejected.append(dict(name=name,message=str(e)));return
        raise ValueError('CONTROL_ACCEPTED: '+name)
    p=E.load('policy.json')
    def policy(name,edit):
        q=deepcopy(p);edit(q);reject(name,lambda:E.validate_policy(q))
    policy('omit first whole common paper',lambda q:q['replacements'].pop('U1'))
    policy('omit second whole common paper',lambda q:q['replacements'].pop('U2'))
    policy('shorten application',lambda q:q['replacements']['A1'].__setitem__('pages',4))
    policy('drop original page',lambda q:q['source'].__setitem__('pages',14))
    policy('discount common theory',lambda q:q.__setitem__('whole_common_papers_charged',False))
    policy('import old B for free',lambda q:q.__setitem__('existing_B_common_is_not_a_prerequisite',False))
    policy('cross-topic discount',lambda q:q.__setitem__('cross_topic_discount',True))
    policy('drop complete diagnostic',lambda q:q['programs'].pop())
    policy('promote samples to uniform premise',lambda q:q['programs'][0].__setitem__('uniform_mathematical_premise',True))
    policy('omit driver inventory',lambda q:q['drivers'].pop())
    policy('claim full formalization',lambda q:q.__setitem__('whole_source_formalized',True))
    policy('omit code from prepayment',lambda q:q.__setitem__('all_declared_code_prepurchased_for_conditional_results',False))
    policy('charge printed and raw code together',lambda q:q.__setitem__('raw_and_printed_code_are_alternatives',False))
    policy('turn unknown graphics into zero',lambda q:q['unknown_costs'].__setitem__('full_graphics',0))
    policy('omit unknown graphics qualification',lambda q:q['unknown_costs'].pop('full_graphics'))
    policy('permit early factor',lambda q:q.__setitem__('factors_permitted',True))
    policy('invent scientific credit',lambda q:q.__setitem__('new_scientific_credit',1))
    policy('omit raw sensitivity',lambda q:q['variants'].remove('raw_untrimmed'))
    spec=E.load('input_spec.json');aliases=E.load('glyph_aliases.json')['aliases'];c=cache['L010'];r=spec['L010']
    def selection(name,edit):
        q=deepcopy(r);edit(q);reject(name,lambda:E.validate_selection('L010',c['raw'],q,c['pages'],c['meta']))
    selection('drop full-document span',lambda q:q.__setitem__('included_spans',[]))
    selection('omit physical page',lambda q:q['page_bindings'].pop())
    selection('cut arbitrary source text',lambda q:q['excluded_furniture'][0].__setitem__('end',q['excluded_furniture'][0]['end']+10))
    selection('alter source extraction',lambda q:q.__setitem__('extraction_sha256','0'*64))
    def glyph(name,edit):
        q=deepcopy(r);edit(q);reject(name,lambda:E.validate_glyphs('L010',c['raw'],c['fonts'],c['pages'],c['events'],q,aliases))
    glyph('change visible glyph output',lambda q:q['glyph_substitutions'][0].__setitem__('output','X'))
    glyph('drop actual alias occurrence',lambda q:q['glyph_substitutions'].pop())
    glyph('duplicate actual glyph occurrence',lambda q:q['glyph_substitutions'].append(deepcopy(q['glyph_substitutions'][0])))
    glyph('alter actual font event',lambda q:q['glyph_substitutions'][0]['pdf_events'][0].__setitem__('encoded_byte',0))
    glyph('alter local context',lambda q:q['glyph_substitutions'][0].__setitem__('context_sha256','0'*64))
    glyph('invent multicharacter glyph output',lambda q:q['glyph_substitutions'][0].__setitem__('output','GG'))
    reject('unsupported unembedded font',lambda:embedded({'/Subtype':'/Type1','/BaseFont':'/Helvetica'}))
    reject('unsupported standard font encoding',lambda:embedded({'/Subtype':'/Type1','/BaseFont':'/Times-Roman','/Encoding':'/MacRomanEncoding'}))
    reject('nonASCII unembedded byte',lambda:validate_unembedded_banner(200,'È'))
    reject('incorrect banner decoding',lambda:validate_unembedded_banner(65,'B'))
    validate_unembedded_banner(65,'A');embedded({'/Subtype':'/Type1','/BaseFont':'/Times-Roman'})
    tex=(E.H/'programs.tex').read_text();cc=cache['CODE'];pr={x['printed_path']:E.bound(x,args)[1].decode()for x in p['programs']}
    def printed(t=tex,raw=None,programs=pr):return E.code_inclusion(t,cc['raw'] if raw is None else raw,programs,cc['events'],spec['CODE']['excluded_furniture'])
    reject('drop printed program',lambda:printed(re.sub(r'\\VerbatimInput(?:\[[^\]]*\])?\{programs/check_applications.g\}', '', tex)))
    reject('print only part of file',lambda:printed(tex.replace('fontsize=\\scriptsize','firstline=2,fontsize=\\scriptsize',1)))
    q=deepcopy(pr);q[next(iter(q))]+='\nMISSING_WHOLE_PROGRAM_SENTINEL;';reject('omitted raw program content',lambda:printed(programs=q))
    q=deepcopy(p['source']);q['sha256']='0'*64;reject('changed complete source bytes',lambda:E.bound(q,args))
    return dict(status='PASS',python_optimization_safe=True,rejected=len(rejected),controls=rejected,scientific_programs_executed=False,scope='Selection, exact original events, safe banner decoding, complete programs, roles and independent-topic boundary; not a mathematical proof or distinct input acceptance.')
