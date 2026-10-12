#!/usr/bin/env python3
"""Assemble previously accepted L096 records; no group census or new credit."""
from pathlib import Path
import argparse, hashlib, json

PACKETS = {
    'M11': ('topic_D_L096_extended_candidate', 'mathieu_results.json', 'topic_D_L096_extended_root_review'),
    'M12': ('topic_D_L096_extended_candidate', 'mathieu_results.json', 'topic_D_L096_extended_root_review'),
    'J1': ('topic_D_L096_J1_extension', 'results.json', 'topic_D_L096_J1_root_review'),
    'J2': ('topic_D_L096_J2_extension', 'results.json', 'topic_D_L096_J2_root_adoption'),
    'M22': ('topic_D_L096_M22_extension', 'results.json', 'topic_D_L096_M22_root_adoption'),
    'M23': ('topic_D_L096_M23_extension', 'results.json', 'topic_D_L096_M23_root_adoption'),
    'HS': ('topic_D_L096_HS_extension', 'shadow_results.json', 'topic_D_L096_HS_root_review'),
    'J3': ('topic_D_L096_J3_extension', 'shadow_results.json', 'topic_D_L096_J3_root_review'),
}
GROUP_ORDER = ['M11', 'M12', 'M22', 'M23', 'J1', 'J2', 'J3', 'HS']

def read(p):
    return json.loads(p.read_text())

def binding(root, p):
    b = p.read_bytes()
    return {'path': str(p.relative_to(root)), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def require(value, message):
    if not value:
        raise ValueError(message)

def certify_quantifiers(row):
    n = row['rank']
    residues = row['residues']
    require(len(residues) == 2**n - 1, 'all nonempty-rank base residues required')
    keys = [tuple(r['fixed_types']) for r in residues]
    require(len(set(keys)) == len(keys), 'duplicate residue')
    by_rank = []
    for k in range(2, n+1):
        selected = [r for r in residues if r['residue_rank'] == k]
        require(len(selected) == __import__('math').comb(n, k), 'missing residue rank')
        for r in selected:
            require(len(r['type_results']) == k and all(type(v) is bool for v in r['type_results']), 'type boundary')
            require(r['IP'] == all(r['type_results']) and r['WIP'] == any(r['type_results']), 'residue quantifier')
        x = {'rank': k, 'IPk': all(r['IP'] for r in selected), 'WIPk': all(r['WIP'] for r in selected)}
        old = next(b for b in row['by_rank'] if b['rank'] == k)
        require(all(old[t] == x[t] for t in x), 'rank quantifier')
        by_rank.append(x)
    require(row['IP'] == all(x['IPk'] for x in by_rank), 'full IP quantifier')
    require(row['WIP'] == all(x['WIPk'] for x in by_rank), 'full WIP quantifier')
    return by_rank

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--study-root', type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    a=ap.parse_args(); root=a.study_root.resolve(); a.out.mkdir(parents=True, exist_ok=True)
    bindings=[]; groups={}; rejected=[]
    for group,(packet, result, acceptance) in PACKETS.items():
        for rel in [f'{packet}/manifest.json', f'{packet}/{result}', f'{acceptance}/manifest.json']:
            b=binding(root,root/rel)
            if b not in bindings: bindings.append(b)
        rows=read(root/packet/result)['rows']
        if group in ['M11','M12']:
            rows=[r for r in rows if r['member'].startswith(group.lower()+'.')]
        selected=[]
        for row in rows:
            by_rank=certify_quantifiers(row)
            if not all(row['filters'].values()):
                rejected.append({'group':group,'member':row['member'],'active':row['active_row'],
                    'construction':row['construction_row'],'failed':[k for k,v in row['filters'].items() if not v]})
                continue
            require(row['filters'].get('RWPRI',row.get('retained_RWPRI',False)), 'missing RWPRI proof or exact transfer')
            selected.append({'group':group,'member':row['member'],'active':row['active_row'],
                'construction':row['construction_row'],'rank':row['rank'],'order':row['order'],
                'borel_order':row['borel_order'],'parabolic_orders':row['parabolic_orders'],
                'IP':row['IP'],'WIP':row['WIP'],'by_rank':by_rank,
                'base_residues_including_panels':len(row['residues']),
                'rank_at_least_two_residues':sum(r['residue_rank']>=2 for r in row['residues']),
                'direction_decisions':sum(len(r['type_results']) for r in row['residues'] if r['residue_rank']>=2),
                'historical_label':None,'evidence':f'{packet}/{result}',
                'whole_family_classification': 'previous census and exact family transfer' if group in ['J1','J2','M22','M23'] else
                    ('exact supplied-roster Aut/type quotient; global classification retained' if group in ['HS','J3'] else 'accepted Mathieu roster and previous census comparison')})
        groups[group]=selected
    sourcepath=root/'topic_D_L096_table_contract/source_tables.json'
    bindings.append(binding(root,sourcepath)); source=read(sourcepath)
    comparisons=[]; obligations=[]
    for sr in source['rows']:
        group,n,k=sr['group'],sr['rank'],sr['property_rank']; rows=[r for r in groups[group] if r['rank']==n]
        pred=[(r['IP'],r['WIP']) if k=='full' else next((v['IPk'],v['WIPk']) for v in r['by_rank'] if v['rank']==k) for r in rows]
        computed={'IP':sum(i for i,w in pred),'WIP_only':sum(w and not i for i,w in pred),'not_WIP':sum(not w for i,w in pred)}
        c={**sr,'computed_total':len(rows),'computed_counts':computed,'count_agrees':computed==sr['source_counts'] and len(rows)==sr['source_total'],
           'historical_label_correspondence':'UNRESOLVED_SEPARATE_OBLIGATION'}
        comparisons.append(c)
        for field,claim in [('source_positive_labels','IP'),('source_weak_only_labels','WIP_ONLY')]:
            for label in sr[field]:
                obligations.append({'group':group,'rank':n,'label':label,'property_rank':k,'claim':claim,
                    'source_page':sr['label_page'],'source_table':sr['label_table'],'source_reference':sr['source_reference'],
                    'current_family':None,'status':'NO_VERIFIED_HISTORICAL_CORRESPONDENCE'})
    require(len(comparisons)==57, 'all 57 source rows required')
    require(sum(c['count_agrees'] for c in comparisons)==53, 'unexpected source-count delta')
    require(sum(map(len,groups.values()))==278, 'unexpected actual roster total')
    population={g:len(groups[g]) for g in GROUP_ORDER}
    report={'status':'FROZEN_COUNT_COMPARISON_WITH_EXPLICIT_LABEL_OBLIGATIONS',
      'scope':'Previously accepted literal rosters and exact prior-census representatives; not a new classification.',
      'population_by_group':population,'actual_roster_total':sum(population.values()),'printed_population_total':277,
      'count_rows':57,'agreeing_count_rows':53,'differences':[c for c in comparisons if not c['count_agrees']],
      'comparisons':comparisons,'rejected_literal_mathieu_entries':rejected,
      'classes':[r for g in GROUP_ORDER for r in groups[g]],
      'historical_label_claim_occurrences':len(obligations),'historical_labels_resolved':0,
      'full_source_credit':False,'new_originals':0,'new_questions':0,'measurement_factor':None,'bindings':bindings}
    (a.out/'combined_results.json').write_text(json.dumps(report,indent=2)+'\n')
    (a.out/'historical_label_claims.json').write_text(json.dumps({'status':'UNRESOLVED_CORRESPONDENCES','claims':obligations},indent=2)+'\n')
    header=r'\toprule Group&Rank&$N$&$k=3$&$k=4$&$k=5$&$k=6$&Full\\'
    table=[r'\begin{longtable}{llrrrrrr}',r'\caption{Exact current sporadic roster counts.}\label{counts}\\',header,r'\midrule\endfirsthead',header,r'\midrule\endhead']
    for g in GROUP_ORDER:
        for n in sorted({r['rank'] for r in groups[g]}):
            cells=[]
            for k in [3,4,5,6,'full']:
                if k!='full' and k>n:cells.append('--');continue
                sr=next((c for c in comparisons if c['group']==g and c['rank']==n and c['property_rank']==k),None)
                if sr is not None:d=sr['computed_counts']
                else:
                    rr=[r for r in groups[g] if r['rank']==n]
                    ps=[next((v['IPk'],v['WIPk']) for v in r['by_rank'] if v['rank']==k) for r in rr]
                    d={'IP':sum(i for i,w in ps),'WIP_only':sum(w and not i for i,w in ps),'not_WIP':sum(not w for i,w in ps)}
                cells.append('/'.join(str(d[x]) for x in ['IP','WIP_only','not_WIP']))
            table.append(f'{g}&{n}&{sum(r["rank"]==n for r in groups[g])}&'+ '&'.join(cells)+r'\\')
    table.extend([r'\bottomrule',r'\end{longtable}'])
    (a.out/'combined_table.tex').write_text('\n'.join(table)+'\n')
    print(json.dumps({k:report[k] for k in ['actual_roster_total','count_rows','agreeing_count_rows','historical_label_claim_occurrences']}))

if __name__=='__main__':main()
