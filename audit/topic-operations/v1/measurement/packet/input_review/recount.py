#!/usr/bin/env python3
"""Independent whole-document recount. No author module is imported.

Glyph choices are the visually reviewed, actual-font-bound declarations;
the author's separately replayed event walker checks their byte origins.
This checker independently extracts all page text and font labels, verifies
the complete boundaries, and recounts every declared cost coordinate.
"""
import argparse, copy, hashlib, json, pathlib, re, unicodedata
import pypdf

PIN='3b0d503dcdd3fe778a05213523fa248109b06f6639df31a6ddbc9196cd1b8b03'
BANNER='arXiv:2608.23223v1  [math.CO]  24 Aug 2026'
BANNER6='arXiv:2605.04646v2  [math.GR]  28 May 2026'
def need(t,s):
    if not t: raise ValueError('INPUT_RECOUNT_REJECT '+s)
def sha(b): return hashlib.sha256(b).hexdigest()
def counts(s,norm):
    s=unicodedata.normalize(norm,s)
    words=s.split();flat=' '.join(words)
    runs=0;previous=False
    for c in s:
        current=c.isalnum()
        if current and not previous:runs+=1
        previous=current
    return {'whitespace_tokens':len(words),'alphanumeric_units':runs,
            'characters_without_whitespace':len(''.join(words)),
            'characters_with_collapsed_whitespace':len(flat),
            'utf8_bytes_with_collapsed_whitespace':sum(len(c.encode('utf-8')) for c in flat),
            'collapsed_text_sha256':sha(flat.encode())}

def document(path,key,spec,aliases):
    need(sha(path.read_bytes())==spec['sha256'],'PDF identity')
    text=[];fonts=[];bindings=[];offset=0;cuts=[]
    for number,page in enumerate(pypdf.PdfReader(path).pages,1):
        pieces=[];names=[]
        def visit(t,cm,tm,font,size):
            if key=='N007' and number==1 and font is None and t==BANNER and pieces and pieces[-1]==BANNER:return
            pieces.append(t);names.extend([str(font.get('/BaseFont',font.get('/Name',''))) if font else '']*len(t))
        raw=page.extract_text(visitor_text=visit) or ''
        need(raw==''.join(pieces) and raw,'whole nonempty page')
        bindings.append({'page':number,'start':offset,'end':offset+len(raw),
                         'sha256':sha(raw.encode()),'empty_extraction':False})
        start=end=None
        if key=='N005':
            if number==1:
                match=re.search(r'\n1\s*\Z',raw)
                need(match is not None,'N005 first-page isolated folio')
                start=match.start()+1;end=len(raw)
            else:
                header=(f'{number} CLAUDIO ALEXANDRE PIEDADE AND PHILIPPE TRANCHIDA\n'
                        if number%2==0 else f'FROM GROUP OPERATIONS TO GEOMETRIC STRUCTURES {number}\n')
                need(raw.startswith(header),'N005 literal running header');start=0;end=len(header)
        elif key=='N007':
            if number==1:
                need(raw.count(BANNER)==1,'one original version stamp')
                start=raw.rfind('\n1\n'+BANNER)+1
                need(start>0,'page-one isolated folio before stamp');end=start+1
            else:
                header=(f'{number} CLAUDIO ALEXANDRE PIEDADE AND PHILIPPE TRANCHIDA\n'
                        if number%2==0 else f'THEj-DIAGONALS TWISTING {number}\n')
                need(raw.startswith(header),'running source header');start=0;end=len(header)
        elif key=='N006':
            if number==1:
                need(raw.count(BANNER6)==1,'one N006 version stamp')
                start=raw.rfind('\n1\n'+BANNER6)+1
                need(start>0,'N006 page-one isolated folio');end=start+1
            else:
                header=f'{number}\n'
                need(raw.startswith(header),'N006 initial isolated folio')
                start=0;end=len(header)
        else:
            match=re.search(r'(?:^|\n)'+str(number)+r'\s*$',raw)
            need(match is not None,'isolated folio')
            start=match.start()+int(raw[match.start()]=='\n');end=len(raw)
        if start is not None:
            literal=raw[start:end]
            cuts.append({'page':number,'start':offset+start,'end':offset+end,
                         'literal':literal,'sha256':sha(literal.encode())})
        offset+=len(raw)+1;text.append(raw);fonts.extend(names);fonts.append('')
    raw='\n'.join(text);fonts=fonts[:-1]
    need(spec['page_bindings']==bindings and spec['pages']==len(bindings),'all physical pages')
    need(spec['extraction_sha256']==sha(raw.encode()),'entire extracted text')
    need(len(spec['included_spans'])==1,'one full span')
    span=spec['included_spans'][0]
    need(span['start']==0 and span['end']==len(raw) and span['sha256']==sha(raw.encode()),'whole span')
    need([{k:c[k] for k in cuts[0]} for c in spec['excluded_furniture']]==cuts,'exact furniture only')
    calibrated=list(raw);used=set();proxy_offsets=[]
    for g in spec['glyph_substitutions']:
        i=g['offset'];need(i not in used,'unique glyph');used.add(i)
        need(g['input_codepoint']==f'U+{ord(raw[i]):04X}' and fonts[i]==g['input_font'],'actual input glyph/font')
        event=g['pdf_event']
        matches=[a for a in aliases if a['font_identity']==event['font_identity'] and
                 a['encoded_byte']==event['encoded_byte'] and a['glyph_name']==event['glyph_name'] and
                 a['input']==raw[i] and a['font']==fonts[i]]
        need(len(matches)==1 and matches[0]['output']==g['output'] and len(g['output'])==1,'reviewed visible glyph')
        need(matches[0]['source']==key and matches[0]['kind']==g['kind'],'glyph role/source')
        if g['kind']=='graphical_proxy':proxy_offsets.append(i)
        else:need(g['kind']=='visible_symbol','only declared symbol/proxy roles')
        need(sha(raw[g['context_start']:g['context_end']].encode())==g['context_sha256'],'glyph context')
        need(not any(c['start']<=i<c['end'] for c in cuts),'glyph not in removed furniture')
        calibrated[i]=g['output']
    def select(s):
        chunks=[];at=0
        for c in cuts:chunks.append(s[at:c['start']]);at=c['end']
        chunks.append(s[at:]);return '\n'.join(chunks)
    variants={'raw_untrimmed':raw,'raw_selected':select(raw),'calibrated_selected':select(''.join(calibrated))}
    text_only=list(calibrated)
    for i in proxy_offsets:text_only[i]=' '
    alternatives={n:counts(select(''.join(text_only)),n) for n in ['NFC','NFKC']}
    return ({v:{n:counts(t,n) for n in ['NFC','NFKC']} for v,t in variants.items()},alternatives,len(proxy_offsets))

def main():
    ap=argparse.ArgumentParser()
    for n in ['author','public-root','sources-root','out']:ap.add_argument('--'+n,type=pathlib.Path,required=True)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
    def load(name):return json.loads((a.author/name).read_text())
    need(sha((a.author/'manifest.json').read_bytes())==PIN,'frozen author manifest')
    exports=load('manifest.json')['exports'];need(len(exports)==30,'thirty exports')
    for r in exports:
        path=pathlib.Path(r['path']);need(not path.is_absolute() and '..' not in path.parts,'relative export')
        data=(a.author/path).read_bytes();need(len(data)==r['bytes'] and sha(data)==r['sha256'],'exact export')
    policy=load('policy.json')
    def resolve(row):return {'public':a.public_root,'sources':a.sources_root}[row['root']]/row['path']
    for row in policy['scientific_bindings']:
        data=resolve(row).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'scientific binding')
    specs=load('input_spec.json');aliases=load('glyph_aliases.json')['aliases'];expected=load('author_counts.json')
    need(set(specs)=={'N005','N006','N007','U','A0','A1','A2','A2nine','A2HN','CODEold','CODEnew'},'eleven whole PDFs')
    need(policy['original_manuscripts']==3 and policy['source_rows']=={'N005':81,'N006':27,'N007':32},'three whole originals')
    need(policy['ratio'] is None and not policy['factors_permitted'],'input stage only')
    need(all(x is None for x in policy['unknown_costs'].values()),'unknown costs null')
    need(policy['written_documents']==['U','A0','A1','A2','A2nine','A2HN'],'whole common and all applications')
    need(policy['application_bundles']=={'N005':['A0'],'N006':['A2','A2nine','A2HN'],'N007':['A1']},'all conditional companions')
    docs={};sensitivities={};proxies={}
    for key,spec in specs.items():
        row={**policy['sources'],**policy['replacements']}[key]
        need(all(spec[k]==v for k,v in row.items()),'policy/spec identity')
        docs[key],sensitivities[key],proxies[key]=document(resolve(spec),key,spec,aliases)
        need(docs[key]==expected['documents'][key]['metrics'],'all30 PDF cells '+key)
        need(sensitivities[key]==expected['text_only_sensitivity'][key]['metrics'],'all10 sensitivity cells '+key)
    need(sum(s['pages'] for s in specs.values())==161,'all physical pages')
    need(proxies==dict(N005=138,N006=288,N007=152,U=0,A0=0,A1=0,A2=0,A2nine=0,A2HN=0,CODEold=0,CODEnew=0),'all and only proxies')
    old=load('prior_count_reference.json')
    for k in ['N006','N007','A2nine','A2HN','CODEold']:need(docs[k]==old['documents'][k]['metrics'],'unchanged historical whole PDF')
    raw={};raw_count=0
    for category in ['programs','required_drivers','drivers','formal']:
        for row in policy[category]:
            data=resolve(row).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'whole raw identity')
            metrics={n:counts(data.decode(),n) for n in ['NFC','NFKC']}
            need(metrics==expected['raw_files'][category][row['id']]['metrics'],'all10 raw cells')
            raw[row['id']]=metrics;raw_count+=1
    need(raw_count==len(raw)==33,'all33 unique files')
    need([len(policy[k]) for k in ['programs','required_drivers','drivers','formal']]==[23,2,5,3],'whole software boundary')
    need(sum(r['logical_premise'] for r in policy['programs'])==17,'finite premise/witness roles')
    need(sum(not r['logical_premise'] for r in policy['programs'])==6,'six whole validation files')
    need(all(r['whole_file'] for k in ['programs','required_drivers','drivers'] for r in policy[k]),'no selected code ranges')
    sw=load('software_inventory.json')
    for oldkey,newkey in [('programs','programs'),('required_input_drivers','required_drivers'),('operational_drivers','drivers'),('formal_files','formal')]:
        for oldrow,newrow in zip(sw[oldkey],policy[newkey],strict=True):
            for k,v in oldrow.items():
                if k=='path':need(pathlib.Path(v).parts[-len(pathlib.Path(newrow[k]).parts):]==pathlib.Path(newrow[k]).parts,'same software path')
                else:need(v==newrow[k],'same semantic role and full file')
    boundary=json.loads((a.public_root/'papers/topic-diagonal/v2/cost_boundary.json').read_text());prefix='papers/topic-diagonal/v2/'
    newprograms={r['path'] for r in policy['programs'] if r['original']=='N006'}
    need(newprograms=={prefix+p for p in boundary['whole_program_files']},'all eighteen inherited N006 files')
    need({r['path'] for r in policy['required_drivers']}=={prefix+p for p in boundary['required_input_decoding_drivers']},'both full decoders')
    need({r['path'] for r in policy['programs'] if r['original']=='N005'}=={'corpus161_N005_integrated/programs/'+n+'.py' for n in ['affine_example','presentation_identities','literal_twist']}|{'corpus161_N005_integrated/controls.py'},'all four N005 files')
    external=load('external_data.json');ledgers=[json.loads((a.public_root/prefix/p).read_text()) for p in boundary['external_data_ledgers']]
    atlas=ledgers[0]['external_atlas_inputs']+ledgers[1]['binary_files'];need(len(atlas)==len(external['inputs']),'all external inputs')
    for old in atlas:
        current=[r for r in external['inputs'] if r['filename']==old['filename']]
        need(len(current)==1 and all(current[0].get(k)==v for k,v in old.items()),'literal inherited external pin')
    required=[r for r in external['inputs'] if r['stage_role'].startswith('required')]
    need(len(required)==4 and sum(r['bytes'] for r in required)==21960689,'whole external representations')
    installed={r['sha256']:r['bytes'] for r in ledgers[0]['files']+ledgers[1]['installed_catalogue_inputs']}
    need(len(installed)==16 and installed=={r['sha256']:r['bytes'] for r in external['installed_files_once_by_identical_hash']},'whole installed files once within topic')
    need(sum(installed.values())==2516249 and external['unknown_proof_cost'] is None,'external cost boundary')
    need(not external['cross_topic_overlap_discount'] and not external['compact_word_discount'],'no unpaid dependencies')
    scope=load('source_boundary.json')
    need(scope['N005']['contract']==json.loads((a.sources_root/'corpus161_N005_integrated/source_migration.json').read_text()),'all81 N005 dispositions')
    need(scope['N006']['contract']==json.loads((a.public_root/'audit/topic-diagonal/v2/source_contract.json').read_text()),'all27 N006 dispositions')
    need(scope['N007']['source_clause_map']==json.loads((a.public_root/'papers/topic-diagonal/v1/source_clause_map.json').read_text()),'all32 N007 dispositions')
    controls=[]
    for key in ['N005','N006','N007']:
        mutations=[('drop last page',lambda s:s['page_bindings'].pop()),('select proof only',lambda s:s['included_spans'][0].update(start=100)),('remove body',lambda s:s['excluded_furniture'][0].update(end=s['excluded_furniture'][0]['end']+50)),('fake font identity',lambda s:s['glyph_substitutions'][0]['pdf_event'].update(font_identity='0'*64)),('proxy mislabel',lambda s:next(g for g in s['glyph_substitutions'] if g['kind']=='graphical_proxy').update(kind='visible_symbol'))]
        if key=='N005':mutations += [('visible CR stroke blank',lambda s:next(g for g in s['glyph_substitutions'] if g['input_codepoint']=='U+000D').update(output=' '))]
        for name,fn in mutations:
            changed=copy.deepcopy(specs[key]);fn(changed)
            try:document(resolve(changed),key,changed,aliases)
            except ValueError:controls.append(key+': '+name)
            else:raise ValueError('control accepted '+name)
    result=dict(status='PASS_INDEPENDENT_RECOUNT',pdf_metric_cells=330,raw_metric_cells=330,text_only_sensitivity_cells=110,documents=docs,text_only_sensitivity=sensitivities,graphical_proxy_events=proxies,raw_files=raw,negative_controls=controls,font_event_walker='Fresh author replay separately; root read but did not independently reimplement the font/event decoder.',author_code_imported=False,full_graphics_cost=None,ratio=None,new_source_credit=0,new_question_credit=0,external_files_refetched=False)
    (a.out/'recount.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','pdf_metric_cells','raw_metric_cells','text_only_sensitivity_cells','negative_controls']}))
if __name__=='__main__':main()
