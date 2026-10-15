"""Join accepted L100 interfaces; no group, graph or geometry enumeration."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,collections,copy,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent;S=G.parents[1]
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')

def execution_join(receipts=None):
    names=['exhaustion_target01','exhaustion_target02','exhaustion_target03_anchor2','exhaustion_target05_level_resume']
    receipts=receipts if receipts is not None else [read(G/n/'receipt.json') for n in names]
    anchors=[];families=[];boundary=[]
    for n,r in zip(names,receipts):
        need(r['status'] in ['PARTIAL_DEADLINE','COMPLETE_REQUEST'],'actual returned-scope status')
        need(r['audit']['returncode']==0 and r['audited_returned_rows']==r['reported_completed_rows'],'clean independent returned-anchor audit')
        rows=r['audited_returned_rows'];need([x[0] for x in rows]==r['completed_anchors'],'every claimed anchor actually audited')
        for a,levels,ranks in rows:
            need(a not in anchors and ((a==95 and levels==[] and ranks==[]) or (levels and levels[-1]==0)),'unique anchor with actual empty next level')
            anchors.append(a);families+=ranks;boundary.append(dict(anchor=a,receipt=n,completed_levels=levels,full_family_ranks=ranks))
    need(sorted(anchors)==list(range(1,96)),'all95 anchors exactly once')
    counts=collections.Counter(k for k in families if k>=2);need(dict(counts)=={2:21,3:25,4:63,5:36},'actual audited full families')
    inc=read(G/'incremental_target02/receipt.json');need(inc['status']=='COMPLETE_INCREMENTAL_FUSION' and inc['execution']['returncode']==0 and inc['old_member_count']==103 and inc['new_member_count']==42 and inc['total_input_members']==145,'exact completed full-Aut join')
    palette=read(G/'palette_serialization_v1/derived/result.json');need(palette['status']=='COMPLETE_LITERAL_INCIDENCE_AND_PALETTE_CATALOGUE' and palette['completed']==palette['classes']==list(range(1,30)),'all29 actual palette results')
    need(palette['counts']==[[2,7,7],[3,7,7],[4,11,11],[5,4,4]],'literal palette rank partition')
    return dict(status='COMPLETE_ACQUIRED_95_ANCHOR_145_FAMILY_29_MODEL_JOIN',anchors=boundary,rank_family_counts=dict(counts),incremental_receipt='geometry/psl3_4/incremental_target02/receipt.json',palette_result='geometry/psl3_4/palette_serialization_v1/derived/result.json',no_target_replay=True)

def catalogue():
    D=G/'source_join_component_v2'
    inv=read(D/'diagram_inventory02.json')['rows'];cmp=read(D/'diagram_comparison01.json')['rows']
    records={x['index']:x for x in read(D/'literal_diagrams01/diagrams.json')['records']}
    names={x['label']:x for x in read(G/'parabolic_component_v2/source_names.json')['rows']}
    aut={x['source_label']:x for x in read(G/'aut_cor_structure_component_v1/source_names.json')['rows']}
    fusion={x['label']:x for x in read(G/'doubling_component_v1/source_routes.json')['source_fusion_multiplicities']}
    out=[]
    for r,c in zip(inv,cmp):
        label=r['label'];need(c['label']==label,'exact source row order');cs=c['candidates'];ids={x['catalogue_index'] for x in cs};need(len(ids)==1,'unique catalogue index among documented node choices');k=next(iter(ids));m=cs[0]['source_node_to_catalogue_type'];a=records[k];n=names[label];u=aut[label];f=fusion[label]
        need(n['catalogue']==u['catalogue_index']==k and f['match'] and f['printed']==f['actual'],'exact model/name/fusion join')
        nodes=[]
        for node in r['nodes']:
            pos=node['position'];t=m[pos];hn=next(x for x in n['nodes'] if x['type']==t);need(hn['source_node']==pos and hn['type_size']==node['type_size']==a['type_sizes'][t-1],'exact source node transport')
            nodes.append(dict(source_node=pos,catalogue_type=t,type_size=node['type_size'],printed_panel_order=node['printed_panel_order'],actual_panel_order=a['panel_orders'][t-1],local_two_transitive=a['panel_two_transitive'][t-1],parabolic=hn['parabolic'],kernel=hn['kernel'],extension=hn['extension']))
        out.append(dict(label=label,rank=len(nodes),catalogue_index=k,source_pages=r['physical_pages'],nodes=nodes,borel=n['borel'],fusion_multiplicity=f['actual'],aut_cor=u['profiles'],printed_edges=r['edges'],printed_absent_edges=r['absent_edges'],actual_rank_two_residues=a['pairs'],source_node_map=m,construction_route=r['construction_route']))
    return out

def corrections():
    return [
      dict(id='C01',clauses=['Diagram-5.1','Diagram-5.2'],kind='numeric diagram correction',claim='At the 210-object node the panel order is1, not the printed2.',proof='source_join_component_v2'),
      dict(id='C02',clauses=['Diagram-3.6'],kind='truncation-link correction',claim='The printed parent5.3 has no210-object type and cannot truncate to3.6; the explicit corrected parent5.2 map is supplied.',proof='doubling_component_v1'),
      dict(id='C03',clauses=['Construction-3.3','Diagram-3.3'],kind='ancillary incidence-rule correction',claim='The printed point-pair/line-pair relation has degree18 and a nonextendible flag. Requiring a common Baer subplane in the selected orbit gives degree6 and the exact construction.',proof='baer_component_v1'),
      dict(id='C04',clauses=['Diagram-3.5'],kind='qualified group-name correction',claim='Under the explicit field convention for PSigmaL, typed Aut is the field-graph extension U, not the printed field extension Sigma.',proof='aut_cor_structure_component_v1'),
      dict(id='C05',clauses=['Diagram-4.11'],kind='qualified group-name correction',claim='Under the same field convention, Cor is the graph extension T, not the printed field extension Sigma.',proof='aut_cor_structure_component_v1'),
      dict(id='C06',clauses=['Diagram-2.3'],kind='split-extension notation correction',claim='The actual index-two kernel3^2:C4 in3^2:Q8 has no complement: replace the displayed outer split colon by a generic extension dot.',proof='parabolic_component_v2')]

def retained():
    return [
      dict(id='R01',source_refs=[45],claim='The quoted strongly-Boolean connectivity criterion, with its source hypotheses; retained attribution. The present proof uses the separately acquired full panel-recognition theorem, not a weaker reading of this sentence.'),
      dict(id='R02',source_refs=[16],claim='The quoted anchored-coset Helly criterion; its actual general implementation and proof are acquired in the common theory and broad primitive preparation.'),
      dict(id='R03',source_refs=[28,29,30,42],claim='Classical PG(2,4) terminology and uniqueness of the plane are retained. Concrete hyperoval/Baer sets, orbits, butterfly completions and actions used here are separately certified.'),
      dict(id='R04',source_refs=[40,42],claim='The exact rank>=3 doubling antecedent with its I12 condition is retained, not strengthened to Pasini full intersection property or extended to rank2. Four finite doubles have actual maps; the rank2 case has a separate elementary proof.'),
      dict(id='R05',source_refs=[27,15,25,24,4,20],claim='Historical thesis reduction, earlier subgroup-geometry classification and Cayley/Magma calculations remain attributed history. The present completeness proof uses the acquired broad panel enumeration and does not claim to replay those older programs.'),
      dict(id='R06',source_refs=[23],claim='ATLAS naming convention retained; actual subgroup and Aut/Cor identifications are supplied by literal structure/action certificates, not by names or cardinality alone.'),
      dict(id='R07',source_refs=[3,5,6,19,28,29,32,39,43,47],claim='Earlier named constructions cited at individual diagrams, including Gewirtz and unital graph names, remain attributed antecedents. The fixed source supplies no fresh proof of those external identifications; this packet does not claim new acquisition of all primary articles.'),
      dict(id='R08',source_refs=[],claim='Complete TomLib L3(4) subgroup roster and transported complete local maximal-subgroup data; exact GAP group/homomorphism/transporter algorithms and full automorphism computation; exact GRAPE/nauty colored-graph completeness are explicit computational/classification premises. Small controls and positive maps do not reprove those algorithms or tables.')]

def bibliography_routes():
    return [dict(source_reference_number=n,source_pages=[19,20,21,22],retained_routes=[r['id'] for r in retained() if n in r['source_refs']],
      disposition='ATTRIBUTION_TO_FIXED_SOURCE_BIBLIOGRAPHY',new_primary_acquisition_claim=False,
      qualification='No blanket assertion that this cited work or every theorem in it was rederived. References not used in a retained route are source background attribution only.') for n in range(1,48)]

def register(rows):
    old=read(S/'corpus106_source_reading_L091_L100_L102/L100_intake.json');out=[]
    common=['exhaustion_component_v2','palette_serialization_v1']
    for r in old['items']:
        ident=r['id'];entry=dict(id=ident,source_pages=r['physical_pages'],source_claim=r['claim'],source_role=r['role'],source_page_text_hashes=r['page_text_sha256'],retained=[],qualifications=[],proofs=[])
        if ident.startswith('Diagram-'):
            label=ident[8:];need(any(x['label']==label for x in rows),'every diagram exists');entry.update(disposition='COMPLETE_CORRECTED_LITERAL_CATALOGUE_ROW',proofs=common+['source_join_component_v2','parabolic_component_v2','aut_cor_structure_component_v1','doubling_component_v1'],retained=['R07'] if 'ref' in r['detail']['construction_route'].lower() or label in ['2.3','2.7'] else [])
        elif ident=='Principal-contract':entry.update(disposition='COMPLETE_CLASSIFICATION_RELATIVE_TO_EXPLICIT_INPUTS',proofs=common+['incremental_fusion_interface_v2'],retained=['R08'])
        elif ident=='Coset-conventions':entry.update(disposition='EXPLICIT_CONVENTION_JOIN',proofs=['exhaustion_component_v2','palette_serialization_v1'],qualifications=['left/right cosets related by inversion','firmness applies to panels/nonmaximal flags','correlations preserve the partition into whole types; markers are separate'])
        elif ident in ['Lemma2.1','Lemma2.2']:entry.update(disposition='RETAINED_QUOTED_ANTECEDENT_WITH_ACQUIRED_IMPLEMENTATION',retained=['R01' if ident=='Lemma2.1' else'R02'],proofs=['exhaustion_component_v2'])
        elif ident in ['PG24-inputs','Definition2.1','Lemma2.3','Butterfly-hyperovals']:entry.update(disposition='COMPLETE_CONCRETE_MODELS_WITH_EXPLICIT_BUTTERFLY_CONVENTION',proofs=['constructions_component_v1','baer_component_v1','butterfly_component_v2'],retained=['R03'],qualifications=['displayed two cross-intersections alone do not imply the claimed unique opposite pole; all four cross-intersections are imposed in the certified recipe'])
        elif ident=='Corollary2.1':entry.update(disposition='RETAINED_GENERAL_ANTECEDENT_AND_COMPLETE_FINITE_APPLICATIONS',proofs=['doubling_component_v1'],retained=['R04'])
        elif ident=='Classification-method':entry.update(disposition='RETAINED_HISTORICAL_ATTRIBUTION_NEW_COMPLETENESS_PROOF',proofs=common,retained=['R05','R08'])
        elif ident in ['Construction-scope','Construction-5.1','Construction-5.2','Lemma4.1','Table1','Lemma4.2']:entry.update(disposition='COMPLETE_LITERAL_CONSTRUCTION_AND_FLAG_PROOF',proofs=['constructions_component_v1','source_join_component_v2'])
        elif ident=='Lemma4.3':entry.update(disposition='COMPLETE_RESIDUES_AND_INTERMEDIATE_STRUCTURES',proofs=['constructions_component_v1','parabolic_component_v2','flag_structure_component_v1'])
        elif ident=='Construction-3.3':entry.update(disposition='CORRECTED_ANCILLARY_CONSTRUCTION',proofs=['baer_component_v1'])
        elif ident.startswith('Construction-4.'):
            entry.update(disposition='COMPLETE_LITERAL_CONSTRUCTION_WITH_DECLARED_ORBIT_CHOICES',proofs=['butterfly_component_v2'])
            if ident=='Construction-4.11':entry['qualifications']=['two distinct Baer orbits, explicit relative oval/dual-oval choice; printed clauses alone do not specify this orbit correspondence']
        elif ident=='Bibliography':entry.update(disposition='COMPLETE_FIXED_SOURCE_ATTRIBUTION_REGISTER',retained=['R01','R02','R03','R04','R05','R06','R07'],qualifications=['47 source references retained; no blanket claim every cited theorem was reproved'])
        else:raise ValueError('unrouted source clause '+ident)
        entry['corrections']=[c['id'] for c in corrections() if ident in c['clauses']];out.append(entry)
    return dict(status='AUTHOR_SOURCE_DISPOSITION_OVERLAY',original_register_path='corpus106_source_reading_L091_L100_L102/L100_intake.json',original_register_unchanged=True,rows=out,retained_inputs=retained(),corrections=corrections(),questions=old['questions'],whole_source_credit=0,new_measurements=0,new_Lean=0,new_question_credit=0)

def validate(rows,reg):
    old=read(S/'corpus106_source_reading_L091_L100_L102/L100_intake.json')
    need(len(rows)==29 and len({r['catalogue_index'] for r in rows})==29,'29 distinct actual catalogue models')
    need([sum(r['rank']==k for r in rows) for k in [2,3,4,5]]==[7,7,11,4],'complete rank partition')
    need([sum(r['fusion_multiplicity'] for r in rows if r['rank']==k) for k in [2,3,4,5]]==[21,25,63,36],'all145 actual inner/type members')
    need(len(reg['rows'])==55 and [r['id'] for r in reg['rows']]==[r['id'] for r in old['items']],'all55 original clauses in unchanged order')
    for a,b in zip(reg['rows'],old['items']):need(a['source_claim']==b['claim'] and a['source_pages']==b['physical_pages'] and a['source_page_text_hashes']==b['page_text_sha256'],'exact original clause identity')
    need(reg['corrections']==corrections() and reg['retained_inputs']==retained() and reg['questions']==old['questions'],'exact corrections/antecedents/questions')
    need(all(r['proofs'] or r['retained'] for r in reg['rows']),'explicit evidence route')
    for r in rows:
        for n in r['nodes']:
            mismatch=n['printed_panel_order']!=n['actual_panel_order'];need(mismatch==(r['label'] in ['5.1','5.2'] and n['type_size']==210),'only exact two panel corrections')
    need(reg['whole_source_credit']==reg['new_measurements']==reg['new_Lean']==reg['new_question_credit']==0,'no administrative credit in author assembly')

def tex(rows):
    names={'G':'G','Sigma':r'\Sigma','Graph':'T','Unitary':'U','Gamma':r'\Gamma','V':'V','AutG':'A','C2xAutG':r'2\times A','C2xV':r'2\times V','C2xSigma':r'2\times\Sigma','C2xG':r'2\times G'}
    lines=[r'\begin{longtable}{@{}l l l r c c c@{}}',r'\toprule Label & Type sizes & Panel orders & $c$ & $2T$ & Aut & Cor\\\midrule\endhead']
    for r in rows:
        ts=','.join(str(n['type_size']) for n in r['nodes']);ps=','.join(str(n['actual_panel_order']) for n in r['nodes']);two='yes' if all(n['local_two_transitive'] for n in r['nodes'])else'no'
        lines.append(f"{r['label']}&$({ts})$&$({ps})$&{r['fusion_multiplicity']}&{two}&${names[r['aut_cor']['typed']['actual']]}$&${names[r['aut_cor']['correlations']['actual']]}$"+r'\\')
    return '\n'.join(lines+[r'\bottomrule\end{longtable}'])+'\n'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    rows=catalogue();reg=register(rows);validate(rows,reg);execution=execution_join();damages=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):damages.append(name);return
        raise ValueError('damaged assembly accepted '+name)
    reject('missing-model',lambda:validate(rows[:-1],reg))
    bad=copy.deepcopy(rows);bad[1]['catalogue_index']=bad[0]['catalogue_index'];reject('duplicate-model',lambda:validate(bad,reg))
    bad=copy.deepcopy(rows);bad[0]['fusion_multiplicity']+=1;reject('wrong-fusion-total',lambda:validate(bad,reg))
    for field in ['source_claim','source_pages','source_page_text_hashes']:
        bad=copy.deepcopy(reg);bad['rows'][0][field]='damaged';reject('wrong-original-'+field,lambda bad=bad:validate(rows,bad))
    bad=copy.deepcopy(reg);bad['rows'].pop();reject('missing-clause',lambda:validate(rows,bad))
    bad=copy.deepcopy(reg);bad['corrections'].append(dict(id='false3.5missingbond'));reject('invented-source-correction',lambda:validate(rows,bad))
    bad=copy.deepcopy(reg);bad['retained_inputs'].pop();reject('omitted-antecedent',lambda:validate(rows,bad))
    bad=copy.deepcopy(reg);bad['questions']=[];reject('changed-question-scope',lambda:validate(rows,bad))
    bad=copy.deepcopy(reg);bad['whole_source_credit']=1;reject('premature-credit',lambda:validate(rows,bad))
    bad=copy.deepcopy(rows);bad[0]['nodes'][0]['actual_panel_order']=99;reject('wrong-panel-value',lambda:validate(bad,reg))
    rs=[read(G/n/'receipt.json') for n in ['exhaustion_target01','exhaustion_target02','exhaustion_target03_anchor2','exhaustion_target05_level_resume']]
    for tag,fn in [('missing-anchor',lambda r:r[-1]['audited_returned_rows'].clear()),('no-empty-terminal',lambda r:r[-1]['audited_returned_rows'][0][1].__setitem__(-1,9)),('failed-audit',lambda r:r[-1]['audit'].__setitem__('returncode',1)),('false-completed-id',lambda r:r[-1].__setitem__('completed_anchors',[2]))]:
        bad=copy.deepcopy(rs);fn(bad);reject(tag,lambda bad=bad:execution_join(bad))
    save(a.out/'catalogue.json',rows);save(a.out/'claim_register.json',reg);save(a.out/'execution_join.json',execution);save(a.out/'bibliography_routes.json',bibliography_routes());(a.out/'catalogue.tex').write_text(tex(rows));save(a.out/'report.json',dict(status='PASS_L100_PRINCIPAL_INTERFACE_JOIN',models=29,original_clauses=55,bibliography_attributions=47,anchors=95,inner_families=145,corrections=6,retained_inputs=8,damages=damages,target_censuses=0,whole_source_credit=0));print('PASS_L100_PRINCIPAL_INTERFACE_JOIN')
if __name__=='__main__':main()
