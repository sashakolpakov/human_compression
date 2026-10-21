#!/usr/bin/env python3
"""Independent affine measurement boundary and unknown-cost checks.

The exact scientific admission is reused. This does not repeat its mathematics,
GAP computations or Lean compilation. Visual selection review is separate.
"""
import argparse,copy,hashlib,json,re
from pathlib import Path
from collections import Counter
from pypdf import PdfReader
from pypdf.generic import ContentStream

PIN='4f322184f2d3d67abfc29841567b51b984e7f6d28788b9e3a475faa0c18ae911'
ADMISSION='23a61a1e913943c4a68234a5af31f2da7fadd6b123a1cd5788f64baf24dd4695'
REQUIRED={'phase250_affine64_kernel.g','phase250_affine_check.py','phase250_base384_census.g',
          'phase250_fixed_groups.g','phase2_cubic_kernel_check.g','phase2_cubic_lattice_check.py'}
def need(ok,why):
    if not ok: raise ValueError(why)
def sha(data): return hashlib.sha256(data).hexdigest()
def read(p): return json.loads(p.read_text())

def validate(d,scope,raw,expected_glyphs):
    source=d['source_input_spec'];replacement=d['replacement_input_spec'];policy=d['policy']
    contract=d['source_contract_boundary'];pub=d['publication_binding'];graphics=d['graphic_inventory']
    rows=source['sources']|replacement['ours']
    need(set(source['sources'])=={'L012'} and set(replacement['ours'])=={'U_Affine','AF1','CODE'},'whole source and all replacement documents')
    need({k:r['pages'] for k,r in rows.items()}=={'L012':17,'U_Affine':7,'AF1':9,'CODE':8},'all41 pages')
    removed=0
    for key,row in rows.items():
        text=raw[key]
        need(row['included_spans']==[dict(start=0,end=len(text),sha256=sha(text.encode()),role=row['included_spans'][0]['role'])],
             'whole document, including front and references')
        need(len(row['excluded_furniture'])==row['pages'],'one reviewed furniture item per page')
        for number,(page,item) in enumerate(zip(row['page_bindings'],row['excluded_furniture']),1):
            need(item['page']==number,'furniture physical page')
            if key=='L012' and number>1:
                literal=(f'{number} DONG-DONG HOU, YAN-QUAN FENG, AND DIMITRI LEEMANS\n' if number%2==0
                         else f'REGULAR 3-POLYTOPES OF ORDER 2 np {number}\n')
                start=page['start']
            else:
                literal=str(number);start=page['end']-len(literal)
            need(item['literal']==literal and item['start']==start and item['end']==start+len(literal) and
                 text[start:item['end']]==literal and item['sha256']==sha(literal.encode()),
                 'only independently reviewed header or final page number')
            removed+=1
        glyphs=row['glyph_substitutions'];actual=expected_glyphs.get(key,{})
        need(len(glyphs)==len(actual),'all visible glyph substitutions')
        for g in glyphs:
            need(g['offset'] in actual,'known glyph occurrence');event=actual[g['offset']]
            need(g['output']==event['expected_output'] and g['input_font']==event['font'] and
                 g['pdf_event']==event['pdf_event'],'actual glyph, encoded byte and font identity')
    need(removed==41,'all41 furniture exclusions')
    for field in ['source_rows','exclusions','source_bindings','proof_dependencies','formal_scope']:
        need(contract[field]==scope[field],'unchanged admitted '+field)
    need(contract['source']=='L012' and contract['row_count']==len(contract['source_rows'])==33 and
         contract['principal_contracts']==1 and contract['project_total_preserved']==27 and
         contract['new_source_credit']==contract['new_question_credit']==0,'existing principal contract and credit')
    need(replacement['formal_scope']==scope['formal_scope'] and replacement['formal_scope']['new']==2 and
         replacement['formal_scope']['reused']==7 and not replacement['formal_scope']['end_to_end'],
         'nine supporting declarations only')
    programs=replacement['complete_mathematical_programs'];aux=replacement['complete_auxiliary_scripts']
    need(len(programs)==6 and {Path(r['path']).name for r in programs}==REQUIRED and
         all(r['classification']=='required' for r in programs),'six complete required programs')
    need(len(aux)==3 and {Path(r['path']).name for r in aux}=={'check.py','integrity_controls.py','controls.py'},
         'complete union of the two auxiliary lists')
    need(pub['complete_mathematical_programs']==programs and pub['complete_auxiliary_scripts']==aux and
         pub['complete_formal_files']==replacement['complete_formal_files'],'same public file inventory')
    need(replacement['auxiliary_list_discrepancy']['original_scope_drivers']==scope['drivers'] and
         replacement['auxiliary_list_discrepancy']['original_cost_boundary_drivers']==scope['cost_boundary']['drivers'],
         'record original auxiliary discrepancy exactly')
    need(replacement['program_representation']['diagnostic_pruning'] is False and
         replacement['program_representation']['auxiliary_count']==3 and
         replacement['program_representation']['auxiliary_in_appendix'] is False,'no code pruning or hidden driver addition')
    need(replacement['comparison_policy']==policy['comparison_policy'] and
         policy['comparison_policy']['cross_topic_deduplication'] is False and
         policy['comparison_policy']['conditional']=='whole L012 / whole AF1, after acquiring the WHOLE U_Affine and ALL SIX complete required programs',
         'whole theory and full programs acquired for conditional comparison')
    need(source['historical_program_cost'] is None and source['graphic_cost'] is None and
         replacement['retained_external_cost'] is None and replacement['graphics_cost'] is None and
         graphics['graphic_cost'] is None and graphics['raster_text_cost'] is None and
         policy['retained_external_cost'] is None and policy['diagram_and_layout_cost'] is None and
         policy['historical_program_cost'] is None,'unknown external, graphic and historical program costs')
    need(all(d[k]['ratio'] is None for k in ['policy','source_input_spec','replacement_input_spec','protocol']) and
         not policy['factors_permitted_at_this_stage'],'input admission does not invent a factor')
    return {'physical_pages':41,'furniture_occurrences':removed,'source_rows':33,'required_programs':6,'auxiliary_scripts':3,'formal_declarations':9}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--proposal',type=Path,required=True)
    ap.add_argument('--study',type=Path,required=True);ap.add_argument('--public',type=Path,required=True)
    ap.add_argument('--font-report',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();need(not a.out.exists(),'fresh report')
    need(sha((a.proposal/'manifest.json').read_bytes())==PIN,'exact frozen proposal')
    manifest=read(a.proposal/'manifest.json')
    for r in manifest['exports']:
        data=(a.proposal/r['path']).read_bytes();need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen export')
    d={k:read(a.proposal/(k+'.json')) for k in ['policy','source_input_spec','replacement_input_spec','source_contract_boundary','publication_binding','graphic_inventory','protocol']}
    need(sha((a.public/'audit/topic-affine/v2/admission.json').read_bytes())==ADMISSION,'exact scientific admission')
    scope=read(a.public/'papers/topic-affine/v2/scope.json')
    need(sha((a.public/'papers/topic-affine/v2/scope.json').read_bytes())==d['replacement_input_spec']['accepted_scope']['sha256'],'exact mathematical scope')
    fonts=read(a.font_report);need(fonts['status']=='PASS_INDEPENDENT_GLYPH_IDENTITIES' and
         fonts['proposal_manifest_sha256']==sha((a.proposal/'manifest.json').read_bytes()),'independent actual font acceptance')
    glyphs={key:{r['offset']:r for r in value['calibrated_occurrences']} for key,value in fonts['documents'].items()}
    raw={};actual_images={};inline_counts={}
    for key,row in (d['source_input_spec']['sources']|d['replacement_input_spec']['ours']).items():
        path=a.study/row['path'] if key=='L012' else a.public/d['publication_binding']['documents'][key]['public_path']
        need(sha(path.read_bytes())==row['pdf_sha256'],'exact input PDF')
        pages=PdfReader(path).pages;raw[key]='\n'.join(p.extract_text() or '' for p in pages)
        need(sha(raw[key].encode())==row['extraction_sha256'],'exact complete extraction')
        images=[];inline=0
        for number,page in enumerate(pages,1):
            for im in page.images:
                images.append(dict(page=number,name=im.name,width=im.image.width,height=im.image.height,sha256=sha(im.data)))
            for operands,op in ContentStream(page.get_contents(),page.pdf).operations:
                if op==b'INLINE IMAGE':
                    need(operands['settings']['/W']==operands['settings']['/H']==1,'one pixel inline marks');inline+=1
        expected=[{k:v for k,v in row.items() if k!='classification'} for row in d['graphic_inventory']['documents'][key]]
        need(images==expected,'complete image inventory')
        actual_images[key]=len(images);inline_counts[key]=inline
    need(actual_images=={'L012':163,'U_Affine':0,'AF1':0,'CODE':0} and inline_counts['L012']==163,'all inline graphic strokes')
    result=validate(d,scope,raw,glyphs)
    for key in ['complete_mathematical_programs','complete_auxiliary_scripts','complete_formal_files']:
        for r in d['publication_binding'][key]:
            data=(a.public/r['public_path']).read_bytes();need(len(data)==r['bytes'] and sha(data)==r['sha256'],'whole bound program or formal file')
    appendix=d['replacement_input_spec']['appendix_tex'];text=(a.public/appendix['public_path']).read_text()
    need(sha(text.encode())==appendix['sha256'],'accepted appendix TeX')
    includes=re.findall(r'\\VerbatimInput\[([^\]]*)\]\{([^}]+)\}',text)
    need(len(includes)==6 and {Path(path).name for options,path in includes}==REQUIRED and
         not any(re.search(r'firstline|lastline|firstnumber|lastnumber',options) for options,path in includes),'six whole untruncated listings')
    mutations=[
      ('partial_document',lambda z:z['source_input_spec']['sources']['L012']['included_spans'][0].update(start=1)),
      ('body_one_as_footer',lambda z:z['source_input_spec']['sources']['L012']['excluded_furniture'][0].update(start=1,end=2)),
      ('missing_page_furniture',lambda z:z['replacement_input_spec']['ours']['CODE']['excluded_furniture'].pop()),
      ('wrong_glyph',lambda z:z['source_input_spec']['sources']['L012']['glyph_substitutions'][0].update(output='x')),
      ('lost_glyph',lambda z:z['source_input_spec']['sources']['L012']['glyph_substitutions'].pop()),
      ('wrong_encoded_byte',lambda z:z['source_input_spec']['sources']['L012']['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=255)),
      ('lost_source_clause',lambda z:z['source_contract_boundary']['source_rows'].pop()),
      ('lost_exclusion',lambda z:z['source_contract_boundary']['exclusions'].pop()),
      ('formal_overclaim',lambda z:z['replacement_input_spec']['formal_scope'].update(end_to_end=True)),
      ('missing_required_program',lambda z:z['replacement_input_spec']['complete_mathematical_programs'].pop()),
      ('demoted_program',lambda z:z['replacement_input_spec']['complete_mathematical_programs'][0].update(classification='diagnostic')),
      ('missing_auxiliary',lambda z:z['replacement_input_spec']['complete_auxiliary_scripts'].pop()),
      ('pruned_diagnostics',lambda z:z['replacement_input_spec']['program_representation'].update(diagnostic_pruning=True)),
      ('cross_topic_discount',lambda z:z['policy']['comparison_policy'].update(cross_topic_deduplication=True)),
      ('unpaid_common_theory',lambda z:z['policy']['comparison_policy'].update(conditional='source / application without common theory')),
      ('graphics_zero',lambda z:z['graphic_inventory'].update(graphic_cost=0)),
      ('historical_program_zero',lambda z:z['source_input_spec'].update(historical_program_cost=0)),
      ('invented_factor',lambda z:z['protocol'].update(ratio=2))]
    controls=[]
    for name,change in mutations:
        bad=copy.deepcopy(d);change(bad)
        try:validate(bad,scope,raw,glyphs)
        except (ValueError,KeyError) as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('missed corruption '+name)
    report=dict(status='PASS_INDEPENDENT_INPUT_BOUNDARY',proposal_manifest_sha256=sha((a.proposal/'manifest.json').read_bytes()),
        checker_sha256=sha(Path(__file__).read_bytes()),**result,graphic_objects=actual_images,inline_images=inline_counts,
        controls=controls,author_functions_imported=False,mathematical_replay_repeated=False,primary_text_exported=False,ratio=None)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','physical_pages','furniture_occurrences','source_rows','required_programs']}))
if __name__=='__main__':main()
