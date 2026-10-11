#!/usr/bin/env python3
"""Portable complete-topic and conditional counts, with explicit qualifications."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,json,re
import extract_inputs as extract
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def ratio(n,d):
    need(n>=0 and d>0,'Ratio domain');f=Fraction(n,d)
    return {'numerator':n,'denominator':d,'reduced_fraction':str(f),'decimal':float(f)}
def count_documents(spec,sources_root,public_root):
    docs={};text={}
    for key,row in (spec['sources']|spec['ours']).items():
        raw,before,after,_=extract.document(sources_root if key in spec['sources'] else public_root,key,row)
        text[key]=after
        docs[key]={'pages':row['pages'],'glyph_changes':len(row['glyph_substitutions']),
          'metrics':{form:{variant:extract.metrics(value,form) for variant,value in [('untrimmed',raw),('raw_selected',before),('calibrated_selected',after)]} for form in spec['normalizations']}}
    return docs,text
def factors(spec,docs,programs):
    sources=spec['source_sequence'];apps=spec['application_sequence'];result={}
    for form in spec['normalizations']:
        result[form]={}
        for variant in spec['variants']:
            result[form][variant]={}
            for metric in spec['metrics']:
                c=lambda k:docs[k]['metrics'][form][variant][metric]
                source_total=sum(c(k) for k in sources);local_total=sum(c(k) for k in apps)
                common=c('U_A');printed=c('code');raw_program=sum(p['metrics'][form][metric] for p in programs)
                result[form][variant][metric]={
                  'costs':{'full_sources':source_total,'full_umbrella':common,'six_applications':local_total,
                    'full_written_papers':common+local_total,'complete_printed_program_appendix':printed,
                    'full_program_inclusive':common+local_total+printed,'complete_raw_program_files':raw_program},
                  'written_topic':ratio(source_total,common+local_total),
                  'program_inclusive_topic':ratio(source_total,common+local_total+printed),
                  'raw_program_representation_sensitivity':ratio(source_total,common+local_total+raw_program),
                  'printed_program_to_written_papers':ratio(printed,common+local_total),
                  'conditional_applications':[{'source_id':s,'application_id':a,
                     'factor':ratio(c(s),c(a)),
                     'given':'Whole U_A and whole complete required program appendix already acquired.'}
                    for s,a in zip(sources,apps)]}
    return result
def human(result,spec):
    p=result['factors']['NFC']['calibrated_selected']['characters_without_whitespace'];c=p['costs']
    lines=['Topic A: lengths of the manuscripts',
      '===================================','',
      'The six applications, common paper and final attribution correction have',
      'passed independent review. These private numerical results bind their',
      'final editions and await root review before admission.','',
      'Primary coordinate: NFC characters other than whitespace, after only',
      'reviewed page-furniture exclusions and font-aware glyph calibration.','',
      f"Six complete sources: {c['full_sources']:,} characters.",
      f"Full umbrella: {c['full_umbrella']:,}; six complete applications: {c['six_applications']:,}.",
      f"Full printed four-program appendix: {c['complete_printed_program_appendix']:,}.",'',
      f"Written papers: {p['written_topic']['numerator']:,}/{p['written_topic']['denominator']:,} = {p['written_topic']['decimal']:.6f}.",
      f"Including the required program: {p['program_inclusive_topic']['numerator']:,}/{p['program_inclusive_topic']['denominator']:,} = {p['program_inclusive_topic']['decimal']:.6f}.",'',
      'The second denominator includes the entire printed appendix exactly once.',
      'The same raw program files are not added again. Their complete raw-text',
      'costs and the alternative denominator are reported as a sensitivity.','',
      'Conditional applications','------------------------','',
      'Each following factor is c(source manuscript)/c(application), after',
      'acquiring the whole umbrella and the whole complete program appendix.',
      'Those common costs remain included in the topic comparison above.','']
    for row in p['conditional_applications']:
        q=row['factor'];lines.append(f"{row['source_id']} -> {row['application_id']}: {q['numerator']:,}/{q['denominator']:,} = {q['decimal']:.6f}")
    lines+=['','Calibrated metric sensitivity','-----------------------------','',
      'Each row uses the named unit throughout. The five units are reported',
      'separately under each normalization.','',
      'Form  Metric                                  Written    With full code',
      '====  ======================================  =========  ==============']
    for form in spec['normalizations']:
        for metric in spec['metrics']:
            value=result['factors'][form]['calibrated_selected'][metric]
            lines.append(f"{form:4}  {metric:38}  {value['written_topic']['decimal']:9.6f}  {value['program_inclusive_topic']['decimal']:14.6f}")
    lines+=['====  ======================================  =========  ==============']
    lines+=['','Scope and sensitivity','---------------------','',
      'All source pages, including titles, abstracts and references, belong to',
      'the numerator under the reviewed main-result contracts and their explicit',
      'corrections/retained inputs. No all-assertions equivalence is claimed.',
      'This is an extracted-text comparison, not complete visible-text cost:',
      'L035 pages 9, 10, 12 and 22 contain image-only scientific labels and diagrams;',
      'its page 22 embedded image is clipped. N009 page 1 also has an image-only',
      'journal banner. Their missing visible text and graphical construction',
      'costs remain unknown, not zero. No private raster transcription is counted.','',
      'Every one of the five metrics is supplied under NFC and NFKC, with',
      'untrimmed, raw selected and calibrated selected text. Glyph corrections',
      'can change byte and alphanumeric counts. Per-document costs are summed;',
      'no artificial inter-document separator is added.','',
      'Physical extents are separately recorded: 93 source pages; 17 umbrella pages,',
      '33 application pages and 21 pages of complete programs. They are not substituted',
      'for the text factors. Retained outside proofs, historical external code',
      'and library/diagram complexity remain separately unpriced. Formal proof',
      'coverage and verification costs are not collapsed into these ratios.','',
      'Reproduction','------------','',
      'Install the pinned pypdf version 6.13.0. Supply the primary files privately',
      'under a sources-root containing the sources/ paths in input_spec.json;',
      'public-root must contain the declared papers/topic-a/v2 artifacts. Run::','',
      '  python3 -B -O recount.py --sources-root /private/study \\',
      '    --public-root /path/to/repository --out /fresh/output','',
      'No original PDF text, primary image or private label transcription is',
      'written to the result packet. No new source or question credit is assigned.','']
    return '\n'.join(lines)
def main():
    p=argparse.ArgumentParser();p.add_argument('--sources-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'Fresh output required');a.out.mkdir(parents=True)
    specdata=(HERE/'input_spec.json').read_bytes();spec=json.loads(specdata);pins=json.loads((HERE/'baseline_bindings.json').read_text())
    need(sha(specdata)==pins['input_spec_sha256'],'Input specification binding')
    need(sha((HERE/'extract_inputs.py').read_bytes())==pins['extractor_sha256'],'Accepted extraction helper binding')
    olddata=(HERE/pins['independent_recount_file']).read_bytes();need(sha(olddata)==pins['independent_recount_sha256'],'Independent count binding')
    independent=json.loads(olddata)
    for file_key,hash_key in [('baseline_file','baseline_sha256'),('final_A6_file','final_A6_sha256')]:
        need(sha((HERE/independent['provenance'][file_key]).read_bytes())==independent['provenance'][hash_key],'Independent original report binding')
    original=json.loads((HERE/independent['provenance']['baseline_file']).read_text())['documents']
    final_a6=json.loads((HERE/independent['provenance']['final_A6_file']).read_text())
    need(set(independent['documents'])==set(original),'Independent complete document set')
    for key,row in independent['documents'].items():
        need(row==(final_a6['document'] if key=='A6' else original[key]),'Independent unchanged-record assembly '+key)
    need(sha((HERE/'source_contract_scope.json').read_bytes())==pins['source_contract_scope_sha256'],'Accepted source-contract scope binding')
    for row in spec['published_artifacts']:
        data=(a.public_root/row['path']).read_bytes()
        need(sha(data)==row['sha256'] and len(data)==row['bytes'],'Published artifact binding '+row['path'])
    need(extract.pypdf.__version__==spec['pypdf_version'],'pypdf version')
    need(spec['source_sequence']==['L032','L034','F016','F013','L035','N009'] and spec['application_sequence']==['A1','A2','A3','A4','A5','A6'],'Complete six-source contract')
    docs,selected=count_documents(spec,a.sources_root,a.public_root)
    accepted=independent['documents'];agreement=0;hashes=0
    for key,d in docs.items():
        for form in spec['normalizations']:
            for variant in spec['variants']:
                for metric in spec['metrics']:
                    need(d['metrics'][form][variant][metric]==accepted[key]['metrics'][form][variant][metric],'Independent metric mismatch '+key);agreement+=1
                need(d['metrics'][form][variant]['collapsed_text_sha256']==accepted[key]['metrics'][form][variant]['collapsed_text_sha256'],'Independent text mismatch '+key);hashes+=1
    need(len(spec['required_programs'])==4,'All four whole programs');programs=[]
    for row in spec['required_programs']:
        data=(a.public_root/row['path']).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'Required program binding')
        t=data.decode();need(re.sub(r'\s+','',t) in re.sub(r'\s+','',selected['code']),'Full program missing from charged appendix')
        programs.append({'path':row['path'],'sha256':row['sha256'],'bytes':len(data),'metrics':{form:extract.metrics(t,form) for form in spec['normalizations']}})
    result={'status':'PASS_PRIVATE_NUMERICAL_REPLAY_PENDING_ROOT_ADMISSION','input_spec_sha256':sha(specdata),
      'checker_sha256':sha(Path(__file__).read_bytes()),'independent_metric_agreements':agreement,'independent_text_hash_agreements':hashes,
      'published_commit':spec['published_commit'],'published_artifact_bindings_checked':len(spec['published_artifacts']),
      'independent_count_provenance':independent['provenance'],
      'documents':docs,'complete_raw_program_files':programs,'factors':factors(spec,docs,programs),
      'source_pages':sum(docs[k]['pages'] for k in spec['source_sequence']),
      'replacement_pages':{'umbrella':docs['U_A']['pages'],'applications':sum(docs[k]['pages'] for k in spec['application_sequence']),'complete_program_appendix':docs['code']['pages']},
      'definitions':spec['factor_definitions'],'scope':spec['mathematical_status'],
      'missing_visible_text_cost':None,'graphical_structure_cost':None,'external_proof_library_cost':None,'historical_external_program_cost':None,
      'no_whole_visible_text_claim':True,'primary_images_or_text_redistributed':False,'new_source_credit':0,'new_question_credit':0}
    (a.out/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');(a.out/'REPORT.rst').write_text(human(result,spec))
    print(json.dumps({'status':result['status'],'independent_metric_agreements':agreement,'independent_text_hash_agreements':hashes,'normalizations':2,'metrics':5,'raw_sensitivity_variants':3,'conditional_application_count':6,'programs_charged_once':4}))
if __name__=='__main__':main()
