#!/usr/bin/env python3
"""Validate the frozen three-application Topic E boundary; optionally measure.
Default: binding, scope, glyph and complete-program checks only, no length factors.
Use --measure only after independent/root boundary review. No Markdown dependency.
Requires pypdf 6.13.0. Primary PDFs remain private and are not emitted.
"""
import argparse,copy,hashlib,json,re,unicodedata
from pathlib import Path
import pypdf
PROTOCOL_SHA256='2f4f5aa3e6771efea45bcc58a6dbc9e4b7da99eab19825c9c543b707d0a35dd3'
ROOT=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError('TOPIC_E_THREE_REJECT '+message)
def sha(data):return hashlib.sha256(data).hexdigest()
def bound(root,row):
    path=root/row['path'];data=path.read_bytes();need(sha(data)==row['sha256'],'binding '+row['path'])
    if 'bytes' in row:need(len(data)==row['bytes'],'byte count '+row['path'])
    return data

def spans(raw,binding):
    for group in ('included_spans','excluded_furniture'):
        previous=-1
        for s in binding[group]:
            a,b=s['start'],s['end'];need(previous<=a<b<=len(raw),'span order '+group)
            need(sha(raw[a:b].encode())==s['sha256'],'span hash '+group);previous=b
    for f in binding['excluded_furniture']:
        need(any(s['start']<=f['start']<f['end']<=s['end'] for s in binding['included_spans']),'excluded furniture containment')

def selected(raw,binding):
    pieces=[]
    for span in binding['included_spans']:
        start=span['start']
        for f in binding['excluded_furniture']:
            if span['start']<=f['start']<f['end']<=span['end']:
                pieces.append(raw[start:f['start']]);start=f['end']
        pieces.append(raw[start:span['end']])
    return '\n'.join(pieces)

def calibrate(raw,binding,key):
    changes=binding['glyph_substitutions'];positions=[];chars=list(raw)
    for row in changes:
        at=row['offset'];need(at not in positions,'duplicate glyph occurrence');positions.append(at)
        expected=chr(int(row['input_codepoint'][2:],16));need(raw[at]==expected,'glyph occurrence value')
        page=binding['page_bindings'][row['page']-1]
        need(at==page['start']+row['page_offset'] and page['start']<=at<page['end'],'glyph page locator')
        a,b=row['context_start'],row['context_end'];need(a<=at<b and sha(raw[a:b].encode())==row['context_sha256'],'glyph context')
        need(key=='L021' and row['page']==8 and (expected,row['output']) in [('\x12','('),('\x13',')')],'authorized delimiter substitution')
        # Same character classification gives invariance of all five declared metrics.
        x,y=expected,row['output']
        for form in ('NFC','NFKC'):
            need(unicodedata.normalize(form,x)==x and unicodedata.normalize(form,y)==y,'normalization classification')
        need(len(x)==len(y)==1 and len(x.encode())==len(y.encode())==1,'delimiter length')
        need(not x.isspace() and not y.isspace() and not x.isalnum() and not y.isalnum(),'delimiter classification')
        chars[at]=y
    controls=[i for i,c in enumerate(raw) if ord(c)<32 and c not in '\n\r\t']
    need(controls==positions,'unclassified or reordered control glyph '+key)
    need(not any(c=='\ufffd' or unicodedata.category(c)=='Co' for c in raw),'unclassified replacement/private-use glyph '+key)
    if key=='L021':need(len(changes)==8,'all eight glyph occurrences')
    else:need(not changes,'unexpected glyph mapping '+key)
    return ''.join(chars)

def document(root,key,row):
    path=root/row['path'];need(sha(path.read_bytes())==row['pdf_sha256'],'PDF '+key)
    texts=[p.extract_text() or '' for p in pypdf.PdfReader(path).pages];need(len(texts)==row['pages'],'page count '+key)
    raw='\n'.join(texts);need(sha(raw.encode())==row['extraction_sha256'],'extraction '+key)
    at=0;expected=[]
    for i,t in enumerate(texts,1):expected.append(dict(page=i,start=at,end=at+len(t),sha256=sha(t.encode())));at+=len(t)+1
    need(expected==row['page_bindings'],'page bindings '+key);spans(raw,row)
    calibrated=calibrate(raw,row,key)
    return raw,selected(raw,row),selected(calibrated,row)

def metrics(text,form):
    t=unicodedata.normalize(form,text);collapsed=' '.join(t.split())
    return dict(whitespace_tokens=len(collapsed.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),
        characters_without_whitespace=sum(not c.isspace() for c in t),characters_with_collapsed_whitespace=len(collapsed),
        utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),collapsed_text_sha256=sha(collapsed.encode()))

def controls(protocol,raw,selected_text,code):
    cases=[];b=copy.deepcopy(protocol['sources']['L021']);b['glyph_substitutions'][0]['output']=''
    cases.append(('deleted_visible_delimiter',lambda:calibrate(raw['L021'],b,'L021')))
    b2=copy.deepcopy(protocol['sources']['L021']);b2['glyph_substitutions'][0]['offset']+=1
    cases.append(('shifted_glyph_occurrence',lambda:calibrate(raw['L021'],b2,'L021')))
    b3=copy.deepcopy(protocol['sources']['L021']);b3['included_spans'][0]['end']-=1
    cases.append(('changed_full_manuscript_boundary',lambda:spans(raw['L021'],b3)))
    code_row=protocol['required_programs'][1]
    cases.append(('changed_required_program',lambda:need(sha(code[code_row['path']]+b' ') == code_row['sha256'],'program changed')))
    altered=copy.deepcopy(protocol);altered['required_programs'].pop()
    cases.append(('omitted_required_program_from_protocol',lambda:need(sha((json.dumps(altered,indent=2,ensure_ascii=False)+'\n').encode())==PROTOCOL_SHA256,'protocol changed')))
    cases.append(('missing_complete_code_appendix',lambda:need(re.sub(r'\s+','',code[code_row['path']].decode()) in re.sub(r'\s+','','no program here'),'full program absent')))
    passed=[]
    for label,action in cases:
        try:action()
        except ValueError:passed.append(label)
        else:raise ValueError('negative control accepted '+label)
    return passed

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--sources-root',type=Path);ap.add_argument('--public-root',type=Path,required=True)
    ap.add_argument('--protocol',type=Path,default=ROOT/'topic_E_three_protocol.json');ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--measure',action='store_true',help='Evaluate all factors after the proposed boundary has received independent/root review.')
    args=ap.parse_args();need(not args.out.exists() and not args.out.is_symlink(),'fresh output required')
    sources_root=args.sources_root or args.root
    data=args.protocol.read_bytes();need(sha(data)==PROTOCOL_SHA256,'frozen protocol');protocol=json.loads(data)
    need(pypdf.__version__==protocol['pypdf_version'],'pypdf version')
    need(protocol['source_sequence']==['L083','L079','L021'] and protocol['third_application_included'],'three-application scope')
    need(len(protocol['required_programs'])==3,'exact three complete programs')
    for key in ['prior_two_source_protocol','prior_two_source_measurement','dependency_review','conversion_report']:
        bound(args.root,protocol[key])
    bound(args.public_root,protocol['prior_two_source_public_protocol'])
    for row in protocol['scientific_bindings']:
        bound(sources_root if row['path'].startswith('sources/') else args.root,row)
    for row in protocol['tex_bindings']:bound(args.public_root if row['path'].startswith('papers/') else args.root,row)
    raw={};before={};after={}
    for key,row in (protocol['sources']|protocol['ours']).items():
        raw[key],before[key],after[key]=document(sources_root if key in protocol['sources'] else args.root,key,row)
    code={};included=[]
    for row in protocol['required_programs']:
        b=bound(args.root,row);code[row['path']]=b
        need(re.sub(r'\s+','',b.decode()) in re.sub(r'\s+','',after[row['appendix']]),'full required program in charged appendix '+row['path'])
        included.append(dict(path=row['path'],sha256=row['sha256'],appendix=row['appendix'],complete=True))
    result=dict(status='PASS_BOUNDARY_VALIDATION_ONLY' if not args.measure else 'PASS_PRIVATE_MEASUREMENT_PENDING_ADOPTION',
      protocol_sha256=PROTOCOL_SHA256,checker_sha256=sha(Path(__file__).read_bytes()),pypdf_version=pypdf.__version__,
      scope='Three admitted corrected principal contracts; all full source/replacement manuscripts and every required code line. No new result credit.',
      glyph_occurrences=8,all_unclassified_glyphs_rejected=True,glyph_metric_invariance_by_character_classification=True,
      complete_required_programs=included,negative_controls=controls(protocol,raw,after,code),
      new_credit=protocol['new_credit'],factors_evaluated=args.measure,
      historical_program_cost=None,unconditional_retained_library_cost=None,exact_all_artifact_factor=None)
    if args.measure:
        costs={key:{form:metrics(text,form) for form in protocol['normalizations']} for key,text in after.items()}
        raw_costs={key:{form:metrics(text,form) for form in protocol['normalizations']} for key,text in before.items()}
        for key in costs:
            for form in protocol['normalizations']:
                need(all(costs[key][form][m]==raw_costs[key][form][m] for m in protocol['metrics']),'raw/calibrated metric invariance '+key)
        result['costs']=costs;result['raw_glyph_sensitivity']=raw_costs
        result['untrimmed_source_sensitivity']={key:{f:metrics(raw[key],f) for f in protocol['normalizations']} for key in protocol['sources']}
        result['comparisons']={}
        for form in protocol['normalizations']:
            result['comparisons'][form]={}
            for metric in protocol['metrics']:
                c={key:v[form][metric] for key,v in costs.items()};s=sum(c[x] for x in protocol['source_sequence']);w=sum(c[x] for x in ['U_E','A1','A2','A3']);k=w+c['Code_shared']+c['Code_A3']
                result['comparisons'][form][metric]=dict(full_source_manuscripts=s,replacement_complete_manuscripts=w,replacement_manuscripts_and_all_required_programs=k,
                  written_factor=s/w,known_cost_coordinate=s/k,exact_all_artifact_factor=None,
                  acquisition_written=c['U_E'],acquisition_with_shared_program=c['U_E']+c['Code_shared'],
                  source_sequence=[c[x] for x in ['L083','L079','L021']],source_cumulative=[c['L083'],c['L083']+c['L079'],s],
                  application_sequence=[c['A1'],c['A2'],c['A3']],marginal_with_required_code=[c['A1'],c['A2'],c['A3']+c['Code_A3']],
                  replacement_written_cumulative=[c['U_E']+c['A1'],c['U_E']+c['A1']+c['A2'],w],
                  replacement_with_code_cumulative=[c['U_E']+c['Code_shared']+c['A1'],c['U_E']+c['Code_shared']+c['A1']+c['A2'],k],
                  local_written_conditioned_on_acquisition={l:c[l]/c[a] for l,a in [('L083','A1'),('L079','A2'),('L021','A3')]},
                  local_known_cost_conditioned_on_acquisition={'L083':c['L083']/c['A1'],'L079':c['L079']/c['A2'],'L021':c['L021']/(c['A3']+c['Code_A3'])})
        result['interpretation']='Written factors use complete historical manuscripts under declared main-result contracts. The known-cost coordinate includes all our required programs, but historical code is unknown. Retained library remains conditional and symmetrically available. No all-assertions, full Lean, minimum complexity or long-run sawtooth claim.'
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(status=result['status'],protocol_sha256=PROTOCOL_SHA256,checked_documents=len(raw),complete_programs=len(included),factors_evaluated=args.measure,controls=len(result['negative_controls'])),indent=2))
if __name__=='__main__':main()
