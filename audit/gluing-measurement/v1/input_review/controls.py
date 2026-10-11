#!/usr/bin/env python3
"""Independent semantic controls over the reviewed selection and boundaries."""
from copy import deepcopy
from pathlib import Path
import argparse, json
import pypdf
import recount as R

def run(packet, sources):
    spec=R.read(packet/'input_spec.json');policy=R.read(packet/'policy.json')
    pages=[p.extract_text() or '' for p in pypdf.PdfReader(sources/spec['L010']['path']).pages]
    tests=[]
    def rejected(label, fn):
        try: fn()
        except (ValueError,KeyError,IndexError) as e:
            tests.append(dict(name=label,rejected=True,reason=str(e)));return
        raise ValueError('Control incorrectly accepted: '+label)
    def selection_control(label, mutate):
        s=deepcopy(spec['L010']);mutate(s)
        rejected(label,lambda:R.selection('L010',pages,s))
    selection_control('omit final reference page',lambda s:s['page_bindings'].pop())
    selection_control('prune body span',lambda s:s['included_spans'][0].update(start=100))
    selection_control('remove source identification banner',lambda s:s['excluded_furniture'].append(dict(page=1,start=0,end=100,literal='x',sha256='x')))
    selection_control('erase visible script glyph',lambda s:s['glyph_substitutions'][0].update(output=''))
    selection_control('restore erroneous plain G glyph',lambda s:s['glyph_substitutions'][0].update(output='G'))
    selection_control('wrong actual dictionary',lambda s:s['glyph_substitutions'][0]['pdf_events'][0].update(font_dictionary_sha256='0'*64))
    selection_control('wrong effective encoding',lambda s:s['glyph_substitutions'][0]['pdf_events'][0].update(effective_encoding_sha256='0'*64))
    selection_control('wrong occurrence context',lambda s:s['glyph_substitutions'][0].update(context_sha256='0'*64))
    def policy_control(label, mutate):
        p=deepcopy(policy);mutate(p);rejected(label,lambda:R.boundary(p))
    policy_control('unpaid second common paper',lambda p:p['replacements'].pop('U2'))
    policy_control('omit complete validation program',lambda p:p['programs'].pop())
    policy_control('turn sample validation into general premise',lambda p:p['programs'][0].update(uniform_mathematical_premise=True))
    policy_control('omit code prepayment',lambda p:p.update(all_declared_code_prepurchased_for_conditional_results=False))
    policy_control('graphics unknown set to zero',lambda p:p['unknown_costs'].update(full_graphics=0))
    policy_control('inflate formal coverage',lambda p:p.update(whole_source_formalized=True))
    policy_control('introduce input-stage ratio',lambda p:p.update(ratio=1.5))
    rejected('overlapping cuts',lambda:R.changes('abcdef',[(0,3,''),(2,4,'')]))
    return dict(status='PASS',independent_controls=tests,count=len(tests),author_code_imported=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--sources-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    R.need(not a.out.exists(),'fresh output');a.out.write_text(json.dumps(run(a.packet,a.sources_root),indent=2)+'\n')
