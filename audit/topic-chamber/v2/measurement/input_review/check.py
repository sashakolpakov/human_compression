#!/usr/bin/env python3
"""Independent complete input extraction, source-glyph checks and integer counts."""
import argparse,copy,hashlib,json,re,sys,unicodedata
from pathlib import Path
import pypdf,fontTools
from fonts import audit,require,digest
PIN='5d37d8ad6e775792c0d8750c6984b04023ba4c657ed82625e650251da5201305'
def load(p):return json.loads(p.read_text())
def metric(s,form):
    s=unicodedata.normalize(form,s);words=alnums=chars=0;inword=inalnum=False;out=[];pending=False
    for c in s:
        nonspace=not c.isspace();an=c.isalnum()
        words+=int(nonspace and not inword);alnums+=int(an and not inalnum)
        if nonspace:
            chars+=1
            if pending and out:out.append(' ')
            out.append(c);pending=False
        else:pending=True
        inword=nonspace;inalnum=an
    compact=''.join(out)
    return {'whitespace_tokens':words,'alphanumeric_units':alnums,'characters_without_whitespace':chars,'characters_with_collapsed_whitespace':len(compact),'utf8_bytes_with_collapsed_whitespace':len(compact.encode()),'collapsed_text_sha256':digest(compact.encode())}

def boundary(raw,row,key,pages):
    require(row['included_spans']==[{'start':0,'end':len(raw),'sha256':digest(raw.encode()),'role':row['included_spans'][0]['role']}],'Whole document selection')
    require(len(row['excluded_furniture'])==len(pages),'One declared furniture cut on every page')
    spans=[];last=0
    for no,(f,p) in enumerate(zip(row['excluded_furniture'],pages),1):
        a,b=f['start'],f['end'];literal=f['literal']
        require(f['page']==no and p['start']<=a<b<=p['end'] and a>=last,'Furniture belongs to exact physical page')
        require(raw[a:b]==literal and digest(literal.encode())==f['sha256'],'Literal furniture bytes')
        if key=='L008':
            expected=(str(no)+'\n') if no==1 else (f'{no} WEI-JUAN ZHANG AND DIMITRI LEEMANS\n' if no%2==0 else f'TESTING CHIRALITY ON HYPERTOPES {no}\n')
            require(literal==expected,'Only actual repeated author/title/page header')
            if no>1:require(a==p['start'],'Repeated running header at page start')
        else:
            require(literal==str(no) and not raw[b:p['end']].strip(),'Only isolated trailing physical page number')
            require(a==p['start'] or raw[a-1].isspace(),'Page number separated from body')
        spans.append((a,b));last=b
    def select(text):
        out=[];start=0
        for a,b in spans:out.append(text[start:a]);start=b
        out.append(text[start:]);return '\n'.join(out)
    return select

def extract(path,row,key,expected_fonts=None):
    require(digest(path.read_bytes())==row['pdf_sha256'],'Exact complete original/published PDF '+key)
    reader=pypdf.PdfReader(path);text=[];font_names=[];pages=[];at=0
    for no,page in enumerate(reader.pages,1):
        chunks=[];names=[]
        def visitor(s,cm,tm,font,size):
            chunks.append(s);names.extend([str(font.get('/BaseFont',font.get('/Name',''))) if font else '']*len(s))
        s=page.extract_text(visitor_text=visitor) or ''
        require(s==''.join(chunks),'Literal visitor text is full extraction')
        pages.append({'page':no,'start':at,'end':at+len(s),'sha256':digest(s.encode()),'empty_extraction':not s});at+=len(s)+1
        text.append(s);font_names.extend(names+[''])
    raw='\n'.join(text);font_names=font_names[:-1]
    require(pages==row['page_bindings'] and len(pages)==row['pages'],'Every physical page bound')
    require(digest(raw.encode())==row['extraction_sha256'],'Full raw extraction hash')
    select=boundary(raw,row,key,pages);chars=list(raw);seen=set()
    for x in row['glyph_substitutions']:
        pos=x['offset'];require(pos not in seen,'Unique occurrence repair');seen.add(pos)
        require(raw[pos]==chr(int(x['input_codepoint'][2:],16)) and font_names[pos]==x['input_font'],'Original decoded character/font')
        require(len(x['output'])==1,'One glyph, no deletion/expansion')
        require(digest(raw[x['context_start']:x['context_end']].encode())==x['context_sha256'],'Original occurrence context')
        require(pos==pages[x['page']-1]['start']+x['page_offset'],'Exact occurrence page/offset');chars[pos]=x['output']
    audit_result=audit(path,key,raw,font_names,pages,expected_fonts,row['glyph_substitutions']) if expected_fonts else None
    if expected_fonts is None:require(not seen,'No unreviewed replacement glyph changes')
    variants={n:{f:metric(s,f) for f in ['NFC','NFKC']} for n,s in [('raw_untrimmed',raw),('raw_selected',select(raw)),('calibrated_selected',select(''.join(chars)))]}
    return variants,audit_result,raw,select(raw),pages,font_names

def scopes(s,r,c,pub,repo):
    require(set(s['sources'])=={'L008','N016'} and set(r['ours'])=={'U_H','H1','H2','CODE'},'Complete six-document roster')
    require(s['N016_publisher_pdf_available'] is False,'N016 author edition only')
    bound_scope=load(repo/'papers/topic-chamber/v2/scope.json'); q=load(repo/'papers/topic-chamber/v2/question_map.json');f=load(repo/'papers/topic-chamber/v2/formal/scope.json')
    for x,y in [('source_rows','rows'),('proof_spans','proof_spans'),('source_bindings','source_bindings'),('principal_contracts','principal_contracts')]:require(c[x]==bound_scope[y],'Exact inherited '+x)
    require(c['row_count']==len(c['source_rows'])==27 and len(c['proof_spans'])==22,'All admitted source rows/contexts')
    require(c['question_map']==q and c['formal_scope']==f,'Exact limited formal / separate question maps')
    programs=r['complete_mathematical_programs'];drivers=r['complete_operational_drivers'];formal=r['complete_formal_files']
    require({Path(x['path']).name:(x['classification'],x['required_mathematical_premise']) for x in programs}=={'chiral_cover.g':('required',True),'reflection_models.py':('diagnostic',False)},'Required GAP and diagnostic remain distinct')
    require(len(programs)==2 and all(x['complete_original_file'] and x['printed'] for x in programs),'Both whole programs printed')
    require(len(drivers)==3 and all(x['complete_original_file'] and not x['printed'] and not x['required_mathematical_premise'] for x in drivers),'Three separate whole drivers')
    require({Path(x['path']).name:x['reports'] for x in formal}=={'LiftCertificate.lean':4,'ChamberOrbit.lean':3,'TwoOrbitReflection.lean':7},'Fourteen scoped declarations in three full files')
    require(c['new_source_credit']==c['new_question_credit']==0 and c['whole_manuscript_all_assertions_claim'] is False,'No credit / ancillary overclaim')
    require(all(c[k] is None for k in ['retained_external_cost','graphics_cost','historical_software_cost','ratio']),'Unknown costs and factors remain null')
    require(r['retained_external_cost'] is None and r['graphics_cost'] is None,'Unknown replacement expanded costs')
    tex=(repo/r['appendix_tex']['path']).read_text();files=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',tex)
    require(files==['programs/chiral_cover.g','programs/reflection_models.py'] and not any(x in tex for x in ['firstline','lastline','firstnumber','lastnumber']),'Exactly both complete files in appendix')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    require(not a.out.exists(),'Fresh independent output');a.out.mkdir(parents=True)
    require(pypdf.__version__=='6.13.0' and fontTools.__version__=='4.63.0','Pinned library versions')
    packet=a.study_root/'topic_Chamber_measurement_inputs';require(digest((packet/'manifest.json').read_bytes())==PIN,'Exact frozen author packet')
    for row in load(packet/'manifest.json')['exports']:
        b=(packet/row['path']).read_bytes();require(digest(b)==row['sha256'] and len(b)==row['bytes'],'Exact author export '+row['path'])
    s=load(packet/'source_input_spec.json');r=load(packet/'replacement_input_spec.json');c=load(packet/'source_contract_boundary.json');pub=load(packet/'publication_binding.json');audit_doc=load(packet/'font_audit.json');expected=load(packet/'input_counts.json')
    for row in pub['bindings'].values():
        b=(a.public_root/row['path']).read_bytes();require(digest(b)==row['sha256'] and len(b)==row['bytes'],'Exact scientific provenance')
    scopes(s,r,c,pub,a.public_root);docs={};fonts={};rawfiles={};cache={}
    for key,row in (s['sources']|r['ours']).items():
        path=(a.study_root if key in s['sources'] else a.public_root)/row['path']
        vals,af,raw,selected,pages,font_names=extract(path,row,key,audit_doc.get(key));cache[key]=(raw,pages,row,font_names)
        require(vals==expected['documents'][key]['variants'],'All independent PDF metric cells '+key)
        docs[key]={'pdf_sha256':row['pdf_sha256'],'pages':row['pages'],'variants':vals,'furniture_cuts':len(row['excluded_furniture']),'repairs':len(row['glyph_substitutions'])}
        if af:fonts[key]=af
    for category in ['complete_mathematical_programs','complete_operational_drivers','complete_formal_files']:
        rawfiles[category]={}
        for row in r[category]:
            data=(a.public_root/row['path']).read_bytes();require(digest(data)==row['sha256'] and len(data)==row['bytes'],'Whole raw file '+row['path'])
            result={f:metric(data.decode(),f) for f in ['NFC','NFKC']};name=Path(row['path']).name
            require(result==expected[category][name]['metrics'],'Independent raw-file metric cells')
            rawfiles[category][name]={'sha256':digest(data),'bytes':len(data),'metrics':result,'role':row['role']}
    controls=[]
    mutations=[('omit_required',lambda ss,rr,cc:rr['complete_mathematical_programs'].pop(0)),('promote_diagnostic',lambda ss,rr,cc:rr['complete_mathematical_programs'][1].update(required_mathematical_premise=True)),('prune_diagnostic',lambda ss,rr,cc:rr['complete_mathematical_programs'][1].update(complete_original_file=False)),('omit_driver',lambda ss,rr,cc:rr['complete_operational_drivers'].pop()),('claim_full_formal',lambda ss,rr,cc:cc['formal_scope'].update(full_application_verified=True)),('omit_clause',lambda ss,rr,cc:cc['source_rows'].pop()),('new_question',lambda ss,rr,cc:cc.update(new_question_credit=1)),('unknown_graphics_zero',lambda ss,rr,cc:cc.update(graphics_cost=0)),('pretend_publisher',lambda ss,rr,cc:ss.update(N016_publisher_pdf_available=True))]
    for name,mut in mutations:
        ss,rr,cc=copy.deepcopy(s),copy.deepcopy(r),copy.deepcopy(c);mut(ss,rr,cc)
        try:scopes(ss,rr,cc,pub,a.public_root)
        except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('Control accepted '+name)
    for key in ['L008','N016']:
        raw,pages,row,_=cache[key]
        for name,mut in [('drop_first_body_character',lambda x:x['included_spans'][0].update(start=1)),('remove_body_as_furniture',lambda x:x['excluded_furniture'][0].update(literal='body')),('omit_last_furniture_binding',lambda x:x['excluded_furniture'].pop())]:
            rr=copy.deepcopy(row);mut(rr)
            try:boundary(raw,rr,key,pages)
            except ValueError as e:controls.append({'name':key+'_'+name,'rejected':True,'reason':str(e)})
            else:raise ValueError('Boundary control accepted')
    for key in ['L008','N016']:
        raw,pages,row,font_names=cache[key]
        special=next(i for i,x in enumerate(row['glyph_substitutions']) if x['output']==('⏐' if key=='L008' else '•'))
        mutations=[('drop_visible_glyph_repair',lambda ef,ss:ss.pop(special)),('change_visible_glyph_identity',lambda ef,ss:ss[special].update(output='X')),('forge_encoded_byte',lambda ef,ss:ss[special]['pdf_event'].update(encoded_byte=0)),('forge_font_dictionary',lambda ef,ss:ss[special]['pdf_event'].update(font_dictionary_sha256='0'*64)),('change_class_multiplicity',lambda ef,ss:ef['encoded_glyph_classes'][0].update(occurrences=0)),('erase_actual_outline',lambda ef,ss:ef['encoded_glyph_classes'][0]['glyph_evidence'].update(visible=False))]
        for name,mut in mutations:
            ef,ss=copy.deepcopy(audit_doc[key]),copy.deepcopy(row['glyph_substitutions']);mut(ef,ss)
            try:audit(a.study_root/row['path'],key,raw,font_names,pages,ef,ss)
            except ValueError as e:controls.append({'name':key+'_'+name,'rejected':True,'reason':str(e),'hash_gate_bypassed':True})
            else:raise ValueError('Glyph control accepted '+key+' '+name)
    report={'status':'PASS_INDEPENDENT_INPUT_RECOUNT_AND_FONT_AUDIT','author_manifest_sha256':PIN,'documents':docs,'font_reconstruction':fonts,'raw_files':rawfiles,'pdf_metric_cells':180,'raw_metric_cells':80,'controls':controls,'science_author_role_disclosed':True,'scientific_scope_readjudicated':False,'ratios':None,'no_primary_text_exported':True,'no_GAP_or_Lean_run':True}
    (a.out/'recount.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['documents','raw_files','controls']}))
if __name__=='__main__':main()
