#!/usr/bin/env python3
"""Independent whole-document recount. No author module is imported.

Glyph choices are the visually reviewed, actual-font-bound declarations;
the author's separately replayed event walker checks their byte origins.
This checker independently extracts all page text and font labels, verifies
the complete boundaries, and recounts every declared cost coordinate.
"""
import argparse, copy, hashlib, json, pathlib, re, unicodedata
import pypdf

PIN='4e7991712d5e186c5d0eca9a8173f245a2d1a584eadb1187ef952cef48caec04'
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
        if key=='N007':
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
    a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    def load(name):return json.loads((a.author/name).read_text())
    need(sha((a.author/'manifest.json').read_bytes())==PIN,'frozen author manifest')
    for r in load('manifest.json')['exports']:
        data=(a.author/r['path']).read_bytes();need(len(data)==r['bytes'] and sha(data)==r['sha256'],'exact export')
    policy=load('policy.json')
    def resolve(row):
        return {'public':a.public_root,'sources':a.sources_root,'prior':a.sources_root}[row['root']]/row['path']
    for row in policy['scientific_bindings']+policy['prior_input_bindings']:
        data=resolve(row).read_bytes()
        need(len(data)==row['bytes'] and sha(data)==row['sha256'],'exact scientific/prior binding '+row['path'])
    specs=load('input_spec.json')
    aliases=load('glyph_aliases.json')['aliases'];expected=load('author_counts.json')
    need(set(specs)=={'N007','N006','U','A1','A2','A2nine','A2HN','CODEold'},'all eight complete PDFs')
    need(policy['original_manuscripts']==2 and policy['ratio'] is None and not policy['factors_permitted'],'inputs only')
    need(policy['unknown_costs']==dict(retained_classification_proofs=None,source_historical_software=None,full_graphics=None,full_formalization=None),'unmeasured costs remain null')
    need(policy['source_rows']==dict(N007=32,N006=27),'unchanged scientific scope')
    docs={};sensitivities={};proxies={}
    for key,spec in specs.items():
        row={**policy['sources'],**policy['replacements']}[key]
        need(all(spec[k]==v for k,v in row.items()),'policy and input identity '+key)
        docs[key],sensitivities[key],proxies[key]=document(resolve(spec),key,spec,aliases)
        need(docs[key]==expected['documents'][key]['metrics'],'all30 PDF coordinates '+key)
        need(sensitivities[key]==expected['text_only_sensitivity'][key]['metrics'],'all10 text-only coordinates '+key)
        need(proxies[key]==expected['text_only_sensitivity'][key]['proxy_events_removed'],'all proxy events '+key)
    need(sum(s['pages'] for s in specs.values())==66,'all66 physical pages')
    need(proxies==dict(N007=152,N006=288,U=0,A1=0,A2=0,A2nine=0,A2HN=0,CODEold=0),'exact declared proxy boundary')
    raw={};raw_count=0
    for category in ['programs','required_drivers','drivers','formal']:
        for row in policy[category]:
            data=resolve(row).read_bytes()
            need(sha(data)==row['sha256'] and len(data)==row['bytes'],'full raw-file identity')
            metrics={n:counts(data.decode(),n) for n in ['NFC','NFKC']}
            need(metrics==expected['raw_files'][category][row['path']]['metrics'],'all10 raw-file coordinates')
            raw[row['path']]=metrics;raw_count+=1
    need(raw_count==28 and len(raw)==28,'all28 unique complete raw files')
    need([len(policy[k]) for k in ['programs','required_drivers','drivers','formal']]==[19,2,4,3],'complete software and scoped evidence')
    need(sum(r['role']=='required_finite_proof_or_complete_witness' for r in policy['programs'])==16,'sixteen required proof/witness files')
    boundary=json.loads((a.public_root/'papers/topic-diagonal/v2/cost_boundary.json').read_text())
    prefix='papers/topic-diagonal/v2/'
    need({r['path'] for r in policy['programs']}=={prefix+p for p in boundary['whole_program_files']}|{'papers/topic-diagonal/v1/programs/diagonal_models.g'},'every complete program in accepted scientific boundary')
    need({r['path'] for r in policy['required_drivers']}=={prefix+p for p in boundary['required_input_decoding_drivers']},'every mathematical decoding driver')
    need({policy['replacements'][k]['path'] for k in ['A2','A2nine','A2HN']}=={prefix+p for p in boundary['whole_application_pdfs']},'all three complete N006 companions')
    need(policy['replacements']['U']['path']==prefix+boundary['whole_common_pdf'],'whole enlarged common paper once')
    need({r['path'] for r in policy['programs'] if r['role']=='required_finite_proof_or_complete_witness'}=={prefix+p for p in boundary['roles']['required_finite_proofs']},'inherited finite proof roles')
    external=load('external_data.json')
    ledgers=[json.loads((a.public_root/prefix/p).read_text()) for p in boundary['external_data_ledgers']]
    atlas=ledgers[0]['external_atlas_inputs']+ledgers[1]['binary_files']
    need(len(atlas)==len(external['inputs']),'all eight provenance/input entries')
    for old in atlas:
        current=[r for r in external['inputs'] if r['filename']==old['filename']]
        need(len(current)==1 and all(current[0].get(k)==v for k,v in old.items()),'exact inherited external representation')
    required=[r for r in external['inputs'] if r['stage_role'].startswith('required')]
    need(len(required)==external['required_representation_files']==4 and sum(r['bytes'] for r in required)==external['required_representation_bytes']==21960689,'whole required external bytes')
    installed={r['sha256']:r['bytes'] for r in ledgers[0]['files']+ledgers[1]['installed_catalogue_inputs']}
    need(len(installed)==16 and installed=={r['sha256']:r['bytes'] for r in external['installed_files_once_by_identical_hash']},'exact union of installed catalogue and algorithm files')
    need(sum(installed.values())==external['installed_file_bytes_once']==2516249,'whole installed bytes once within topic')
    need(external['unknown_proof_cost'] is None and not external['cross_topic_overlap_discount'] and not external['compact_word_discount'],'no invented external-proof or compact-word savings')
    scope=load('source_boundary.json')
    need(scope['N006']['contract']==json.loads((a.public_root/'audit/topic-diagonal/v2/source_contract.json').read_text()),'exact N006 source contract')
    need(scope['N007']['source_clause_map']==json.loads((a.public_root/'papers/topic-diagonal/v1/source_clause_map.json').read_text()),'exact N007 source contract')
    prior=json.loads((a.sources_root/'topic_Diagonal_measurement_inputs/author_counts.json').read_text())
    for new,old in [('N007','N007'),('A1','A1'),('CODEold','CODE')]:
        need(docs[new]==prior['documents'][old]['metrics'],'unchanged prior measured document '+new)
    controls=[]
    for name,fn in [
        ('drop physical page',lambda s:s['page_bindings'].pop()),
        ('select only a proof',lambda s:s['included_spans'][0].update(start=100)),
        ('remove body as furniture',lambda s:s['excluded_furniture'][0].update(start=0)),
        ('alter actual glyph font',lambda s:s['glyph_substitutions'][0].update(input_font='fake')),
        ('erase version stamp as furniture',lambda s:s['excluded_furniture'][0].update(end=s['excluded_furniture'][0]['end']+50)),
        ('change visible left angle',lambda s:next(x for x in s['glyph_substitutions'] if x['input_codepoint']=='U+000A').update(output=' '))]:
        changed=copy.deepcopy(specs['N007']);fn(changed)
        try:document(resolve(changed),'N007',changed,aliases)
        except ValueError:controls.append(name)
        else:raise ValueError('control accepted '+name)
    for name,fn in [
        ('N006 omit a physical page',lambda s:s['page_bindings'].pop()),
        ('N006 select only one companion',lambda s:s['included_spans'][0].update(end=1000)),
        ('N006 erase version stamp',lambda s:s['excluded_furniture'][0].update(end=s['excluded_furniture'][0]['end']+40)),
        ('N006 mislabel graphical proxy as symbol',lambda s:next(g for g in s['glyph_substitutions'] if g['kind']=='graphical_proxy').update(kind='visible_symbol')),
        ('N006 alter circle fragment',lambda s:next(g for g in s['glyph_substitutions'] if 'XYCIRC' in g['input_font']).update(output='O')),
        ('N006 alter actual font binding',lambda s:s['glyph_substitutions'][0]['pdf_event'].update(font_identity='0'*64))]:
        changed=copy.deepcopy(specs['N006']);fn(changed)
        try:document(resolve(changed),'N006',changed,aliases)
        except ValueError:controls.append(name)
        else:raise ValueError('control accepted '+name)
    result={'status':'PASS_INDEPENDENT_RECOUNT','pdf_metric_cells':240,'raw_metric_cells':280,'text_only_sensitivity_cells':80,
            'documents':docs,'text_only_sensitivity':sensitivities,'graphical_proxy_events':proxies,'raw_files':raw,'negative_controls':controls,
            'font_event_walker':'separate fresh author replay; not independently reimplemented here',
            'boundary':'accepted scientific edition: whole8-pageU replaces oldU, unchangedN007app, all3N006companions, all19programs and both required decoding drivers',
            'external_boundary':{'required_representation_bytes':21960689,'listed_installed_bytes':2516249,'actual_external_files_replayed':False,'inherited_accepted_ledgers_rechecked':True},
            'graphics_limit':'XYDASH, XYCIRC and underbrace aliases are encoded-event counting proxies, not literal Unicode extraction or full graphic geometry.',
            'compression_factor':None,'new_original_credit':0,'new_question_credit':0}
    (a.out/'recount.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','pdf_metric_cells','raw_metric_cells','negative_controls']}))
if __name__=='__main__':main()
