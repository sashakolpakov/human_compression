#!/usr/bin/env python3
"""Independent literal source-body reconstruction and counts, without author imports."""
import argparse,collections,copy,hashlib,json,unicodedata
from pathlib import Path
BOUNDS={'N001':(181,220),'L108':(1,36)}
RECORDS={'N001':['sources/phase16_N001_browser_record.txt','sources/recovery_20261011/N001_fresh_web.txt'],'L108':['sources/phase25_L108_rendered_primary.txt','sources/recovery_20261011/L108_fresh_complete_web.txt']}
PINS=['222d5742392a4c40c0468d473bfba99b50f34a70eb0ac90200006314d3c5b207','8c6b0ecf4d992b03710db9067b03ee4263abc6751034afb329da4f6b066558bc','e9874c5c958a056b095861fcbf60d52f0aca33335cd7dfdfa82f606bebb7499a','d5c943a335e37347dd08f4ea8dc927f846aceae96c4e9e18ff7589f7edbdede7']
def need(x,m):
    if not x:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def remove_link_wrapper(s):
    out='';marker='\ue200cite\ue202'
    while marker in s:
        before,_,tail=s.partition(marker);body,close,suffix=tail.partition('\ue201');need(bool(close),'Closed annotation');parts=body.split('†');need(len(parts)==2 and parts[0]=='0' and parts[1]=='[email\xa0protected]','Exactly the known displayed masked-address wrapper');out+=before+parts[1];s=suffix
    out+=s;need(not any(x in out for x in ['\ue200','\ue201','\ue202']),'No other tool annotation');return out

def select(record,key):
    first,last=BOUNDS[key];found=[];offset=0
    for line in record.split('\n'):
        label,sep,body=line.partition(':')
        if sep and label.startswith('L') and label[1:].isdigit() and first<=int(label[1:])<=last:
            start=offset+len(label)+1
            if body.startswith(' '):body=body[1:];start+=1
            shown=remove_link_wrapper(body);found.append((int(label[1:]),shown,{'line':int(label[1:]),'start':start,'end':offset+len(line),'sha256':digest(body.encode()),'displayed_sha256':digest(shown.encode())}))
        offset+=len(line)+1
    need([r[0] for r in found]==list(range(first,last+1)),'All body lines exactly once and in order')
    whole='\n'.join(r[1] for r in found);pre=whole;cuts=[]
    if key=='N001':
        suffix=' View publication stats';need(whole.endswith('pcara@vub.ac.be'+suffix) and whole.count('View publication stats')==1,'Only exact nonauthor trailer after complete address');whole=whole[:-len(suffix)];cuts=[{'reason':'nonauthor platform trailer','exact_text':'View publication stats','first_codepoint':len(whole),'last_codepoint':len(pre),'removed_codepoints':len(suffix)}]
        need(whole.startswith('Some properties of inductively minimal geometries') and 'References [1]' in whole and all('Lemma '+str(i) in whole for i in range(1,8)) and 'Theorem 1' in whole,'Complete N001 body landmarks')
    else:need(whole.startswith('J. geom. 71 (2001)') and 'References [1]' in whole and whole.endswith('Received 12 October 1999; revised 25 March 2000.'),'Complete L108 body landmarks')
    return whole,pre,[r[2] for r in found],cuts

def measure(s,form):
    s=unicodedata.normalize(form,s);tokens=alnum=nonspace=0;word=False;anum=False;out=[];space=False
    for c in s:
        w=not c.isspace();a=c.isalnum();tokens+=w and not word;alnum+=a and not anum;nonspace+=w
        if w:
            if space and out:out.append(' ')
            out.append(c);space=False
        else:space=True
        word=w;anum=a
    collapsed=''.join(out)
    return {'whitespace_tokens':tokens,'alphanumeric_units':alnum,'characters_without_whitespace':nonspace,'characters_with_collapsed_whitespace':len(collapsed),'utf8_bytes_with_collapsed_whitespace':len(collapsed.encode()),'collapsed_text_sha256':digest(collapsed.encode())}

def compare(got,expected,policy):
    need(got['documents']==expected,'All literal spans, cuts, glyphs and twenty metrics')
    need(got['original_manuscripts']==2 and got['metric_cells']==20 and not got['source_PDF_claim'] and not got['factors_admitted'] and not got['source_or_question_credit_added'] and not got['primary_body_exported'],'Input-only claim boundary')
    need(policy['primary_coordinate']==['NFC','characters_without_whitespace'] and policy['normalizations']==['NFC','NFKC'],'Fixed coordinates')
    need(not policy['source_PDF_claim'] and not policy['PDF_only_historical_comparisons_changed'] and not policy['numerical_admission'],'Separate immutable PDF comparisons')
    need('raw_untrimmed complete PDF measurements for every remaining original and all our papers' in policy['comparison_requirement'] and 'sensitivities only' in policy['comparison_requirement'],'Untrimmed entire comparison primary; mixed trimming only named sensitivities')

def main():
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--counts',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'Fresh output');need(digest((a.author/'manifest.json').read_bytes())=='9bd3fd3a79b84e60d445b51bf03268b006965d1416c11484f2e0bd9af76187f2','Exact final author freeze')
    for row in read(a.author/'manifest.json')['exports']:
        data=(a.author/row['path']).read_bytes();need(len(data)==row['bytes'] and digest(data)==row['sha256'],'Exact author export '+row['path'])
    policy=read(a.author/'policy.json');got=read(a.counts);need(got==read(a.author/'counts.json'),'Exact corrected frozen counts');need(got['policy_sha256']==digest((a.author/'policy.json').read_bytes()) and got['implementation_sha256']==digest((a.author/'extract.py').read_bytes()),'Exact reviewed author implementation');expected={};raw={};idx=0
    for key,files in RECORDS.items():
        selected=[];binds=[]
        for f in files:
            b=(a.study_root/f).read_bytes();need(digest(b)==PINS[idx],'Pinned original record');idx+=1;record=b.decode();raw[key]=record;selected.append(select(record,key));binds.append(dict(path=f,bytes=len(b),sha256=digest(b)))
        (text,pre,oldspans,cuts),(fresh,freshpre,newspans,newcuts)=selected;need(text==fresh and pre==freshpre and cuts==newcuts,'Historical/fresh authored bodies identical')
        controls=dict(collections.Counter('U+'+format(ord(c),'04X') for c in text if unicodedata.category(c).startswith('C')))
        expected[key]=dict(representation='complete_literal_authored_rendering',primary_url=policy['originals'][key]['primary_url'],original_PDF_retrieved=False,historical_record=binds[0],fresh_record=binds[1],historical_body_spans=oldspans,fresh_body_spans=newspans,complete_body_sha256=digest(text.encode()),pre_trailer_cut_sha256=digest(pre.encode()),pre_trailer_cut_metrics={f:measure(pre,f) for f in ['NFC','NFKC']},nonauthor_trailer_cuts=cuts,complete_body_codepoints=len(text),body_lines=len(oldspans),fresh_complete_body_identical=True,printed_pages=list(range(213,220) if key=='N001' else range(19,26)),running_furniture_removed=False,nonprinting_characters=controls,metrics={f:measure(text,f) for f in ['NFC','NFKC']},unmeasured_graphics_cost=None,full_original_PDF_glyph_identity_verified=False)
    before=read(a.author/'before_trailer_correction.json')
    for key in RECORDS:need(before['documents'][key]['metrics']==expected[key]['pre_trailer_cut_metrics'] and before['documents'][key]['complete_body_sha256']==expected[key]['pre_trailer_cut_sha256'],'Preserved exact pre-correction record')
    compare(got,expected,policy);tests=[]
    mutations=[('change_nonspace_count',lambda x:x['documents']['N001']['metrics']['NFC'].update(characters_without_whitespace=0)),('reinsert_platform_trailer',lambda x:x['documents']['N001'].update(complete_body_sha256=x['documents']['N001']['pre_trailer_cut_sha256'])),('repair_Petrial_symbol',lambda x:x['documents']['L108']['nonprinting_characters'].update({'U+0001':0})),('zero_unknown_graphics',lambda x:x['documents']['L108'].update(unmeasured_graphics_cost=0)),('claim_PDF_identity',lambda x:x['documents']['L108'].update(full_original_PDF_glyph_identity_verified=True)),('omit_final_line',lambda x:x['documents']['N001']['historical_body_spans'].pop()),('claim_ratio_admitted',lambda x:x.update(factors_admitted=True))]
    for name,mut in mutations:
        x=copy.deepcopy(got);mut(x)
        try:compare(x,expected,policy)
        except ValueError as e:tests.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('Mutation accepted')
    for key in RECORDS:
        first,last=BOUNDS[key];lines=raw[key].split('\n');firstline=next(x for x in lines if x.startswith('L'+str(first)+':'));lastline=next(x for x in lines if x.startswith('L'+str(last)+':'))
        for name,text in [('drop_first',raw[key].replace(firstline+'\n','',1)),('duplicate_last',raw[key]+'\n'+lastline),('omit_last',raw[key].replace(lastline,'',1))]:
            try:select(text,key)
            except ValueError as e:tests.append(dict(name=key+'_'+name,rejected=True,reason=str(e)))
            else:raise ValueError('Boundary mutation accepted')
    for name,mut in [('selected_primary',lambda x:x.update(comparison_requirement='Use calibrated_selected PDFs as primary')),('overwrite_PDF_coordinate',lambda x:x.update(PDF_only_historical_comparisons_changed=True))]:
        x=copy.deepcopy(policy);mut(x)
        try:compare(got,expected,x)
        except ValueError as e:tests.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('Policy mutation accepted')
    a.out.mkdir(parents=True);report=dict(status='PASS_INDEPENDENT_LITERAL_RENDERING_INPUT_RECOUNT',documents=expected,metric_cells=20,body_lines=76,controls=tests,imported_author_implementation=False,source_PDF_coordinate_filled=False,numerical_factors_admitted=False,primary_body_exported=False);write(a.out/'recount.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ['documents','controls']}))
if __name__=='__main__':main()
