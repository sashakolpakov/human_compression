#!/usr/bin/env python3
"""Verify exact fractions, complete manuscript sums and actual vector graphs."""
from copy import deepcopy
from pathlib import Path
import argparse
import json
import math
import subprocess
from pypdf import PdfReader
from calculate import R, load, need, sha, derive, outputs, key
from presentation import plots, tex
from geometry_checks import svg_rectangles, compare_geometry, pdf_rectangles, compare_pdf

POLICY = 'd3d26cbbd599e7d66134cb62bc9ad50ce17f6e4bd4400298d001f965fac76632'

def bind(row, root):
    path = Path(row['path'])
    need(not path.is_absolute() and '..' not in path.parts, 'safe packet path')
    data = (root/path).read_bytes()
    need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'exact ' + str(path))

def packet(folder):
    for row in load(folder/'manifest.json')['exports']:
        bind(row, folder)

def inputs():
    p = load(R/'protocol.json')
    need(sha((R/'protocol.json').read_bytes()) == POLICY, 'fixed pre-arithmetic policy')
    need(load(R/'protocol_freeze.json')['protocol']['sha256'] == POLICY,
         'preserved protocol freeze')
    for row in p['input_bindings']:
        bind(row, R)
        packet(R/Path(row['path']).parent)
    for row in p['prior_bindings']:
        bind(row, R)
    packet(R/'prior/root_adoption')
    numerical = load(R/'prior_acceptance_binding.json')
    bind(numerical, R)
    packet(R/'prior/numerical_root_adoption')
    accepted = load(R/'prior/numerical_root_adoption/adoption.json')
    need(accepted['bindings']['author']['sha256'] == sha((R/'prior/manifest.json').read_bytes()),
         'previous numerical acceptance binds exact prior packet')
    for row in load(R/'prior/manifest.json')['exports']:
        if row['path'] in ['results.json', 'protocol.json']:
            bind(row, R/'prior')
    accepted = load(R/'inputs/root_review/review.json')
    need(accepted['status'] == 'ROOT_ACCEPTED_COMPLETE_A10_INPUT_BOUNDARY'
         and accepted['numerical_comparison_authorized'], 'accepted complete input boundary')
    need(accepted['author']['sha256'] == sha((R/'inputs/input/manifest.json').read_bytes()),
         'acceptance applies to exact input author packet')
    for row in p['reused_helpers']:
        bind(row, R)
    if (R/'manifest.json').exists():
        packet(R)
    return (p, load(R/'inputs/input/author_counts.json'),
            load(R/'inputs/input/precount/raw_inventory.json'), load(R/'prior/results.json'))

def validate(r, p, counts, inventory, prior):
    need(r['source_ids'] == p['source_order'] and r['source_count'] == 10, 'ten originals')
    need((r['source_pages'], r['whole_common_pages'], sum(r['application_pages'].values()))
         == (152, 41, 63), 'all complete written pages')
    need(r['common_documents'] == ['U','U_HEX','U_STRUCT'], 'all common components')
    need(r['application_documents'] == p['application_documents'], 'all native app companions')
    need(len(r['whole_file_inventory']) == 203, 'all raw contents')
    need(len(r['coordinates']) == 30 and r['exact_fraction_count'] == 330, 'all coordinates')
    checked = preserved = 0
    for v in p['variants']:
        for n in p['normalizations']:
            for u in p['units']:
                k = key(v,n,u)
                row = r['coordinates'][k]
                d = {name: x['metrics'][v][n][u] for name,x in counts['documents'].items()}
                need(row['document_costs'] == d, 'all29 complete document costs')
                commons = sum(d[x] for x in p['common_documents'])
                apps = {a:sum(d[x] for x in parts) for a,parts in p['application_documents'].items()}
                sources = sum(d[x] for x in p['source_order'])
                whole = commons + sum(apps.values())
                need((row['source_sum'],row['whole_common'],row['application_sum'],row['whole_written'])
                     == (sources,commons,sum(apps.values()),whole), 'entire common and application sums')
                need(row['application_costs'] == apps, 'complete native application bundles')
                for f,aa,bb in [(row['written'],sources,whole)]+[
                    (row['conditional'][s],d[s],apps[p['applications'][s]]) for s in p['source_order']]:
                    need(f['source_cost'] == aa and f['replacement_cost'] == bb, 'complete ratio costs')
                    need(f['numerator']*bb == f['denominator']*aa
                         and math.gcd(f['numerator'],f['denominator']) == 1, 'exact reduced ratio')
                    checked += 1
                for s in p['unchanged_conditionals']:
                    need(row['conditional'][s] == prior['coordinates'][k]['conditional'][s],
                         'eight previous application fractions unchanged')
                    preserved += 1
    need((checked,preserved) == (330,240), '330 exact and240 preserved fractions')
    need(r == derive(p,counts,inventory,prior), 'all decimal, inventory, unknown and acquisition fields')
    return checked

def controls(r, args):
    rejected=[]
    primary=r['primary_coordinate']
    mutations=[
        ('drop common supplement',lambda q:q['common_documents'].remove('U_HEX')),
        ('drop structural common',lambda q:q['common_documents'].remove('U_STRUCT')),
        ('omit companion',lambda q:q['application_documents']['A10'].pop()),
        ('restore historical A9',lambda q:q['coordinates'][primary]['application_costs'].update(A9=25549)),
        ('bad whole sum',lambda q:q['coordinates'][primary].update(whole_written=1)),
        ('alter exact fraction',lambda q:q['coordinates'][primary]['written'].update(numerator=1)),
        ('change old conditional',lambda q:q['coordinates'][primary]['conditional']['L012'].update(denominator=1)),
        ('wrong source pairing',lambda q:q['applications'].update(L003='A9')),
        ('code added to one side',lambda q:q['coordinates'][primary]['written'].update(replacement_cost=q['primary']['whole_written']+100)),
        ('historical code zero',lambda q:q.update(historical_source_software_cost=0)),
        ('invent software ratio',lambda q:q.update(software_inclusive_factors=1)),
        ('graphics declared free',lambda q:q['unknown_costs'].update(full_graphical_structure=0)),
        ('drop required data',lambda q:q['whole_file_group_costs']['required_data'].update(files=70)),
        ('drop whole raw file',lambda q:q['whole_file_inventory'].pop()),
        ('omit sensitivity',lambda q:q['coordinates'].pop(next(iter(q['coordinates'])))),
        ('free common at acquisition',lambda q:q['primary_acquisition'][0].update(replacement_written=0)),
        ('omit last acquisition',lambda q:q['primary_acquisition'].pop()),
        ('claim original credit',lambda q:q.update(new_source_credit=1)),
        ('claim complete formalization',lambda q:q.update(full_formalization_cost=0)),
        ('promote partial program appendix',lambda q:q.update(complete_enlarged_printed_program_representation=30)),
        ('post hoc primary selection',lambda q:q.update(primary_coordinate='raw_selected/NFKC/whitespace_tokens'))]
    for name, mutate in mutations:
        q=deepcopy(r);mutate(q)
        try:
            validate(q,*args)
        except (ValueError,KeyError):
            rejected.append(name)
        else:
            raise ValueError('accepted mutation: '+name)
    return rejected

def graphcheck(folder, expected):
    result={}
    for stem,count in [('costs',35),('cumulative',21)]:
        want=expected[stem]['expected_rectangles']
        actual=svg_rectangles((folder/(stem+'.svg')).read_text())
        compare_geometry(actual,want)
        rect,height=pdf_rectangles(folder/(stem+'.pdf'))
        compare_pdf(rect,height,want,0)
        need(len(actual)==len(rect)==count,'all actual vector bars')
        rejected=[]
        for name,fn in [('distorted width',lambda q:q[next(iter(q))].__setitem__(2,1)),
                        ('missing bar',lambda q:q.pop(next(iter(q)))),
                        ('shifted baseline',lambda q:q[next(iter(q))].__setitem__(0,0))]:
            q=deepcopy(actual);fn(q)
            try:compare_geometry(q,want)
            except ValueError:rejected.append(name)
            else:raise ValueError('accepted SVG mutation')
        q=deepcopy(rect);q[0][3]+=1
        try:compare_pdf(q,height,want,0)
        except ValueError:rejected.append('distorted PDF bar')
        else:raise ValueError('accepted PDF mutation')
        result[stem]=dict(SVG_bars=len(actual),PDF_bars=len(rect),controls=rejected)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--render',action='store_true')
    args=parser.parse_args()
    need(not args.out.exists(),'fresh output')
    args.out.mkdir(parents=True)
    inputs_tuple=inputs();r=load(R/'results.json')
    count=validate(r,*inputs_tuple)
    for name,content in outputs(derive(*inputs_tuple)).items():
        need(content==(R/name).read_text(),'exact generated artifact '+name)
        (args.out/name).write_text(content)
    reader=tex(r)
    need(reader==(R/'reader.tex').read_text(),'same reader derivation')
    (args.out/'reader.tex').write_text(reader)
    expected=plots(r,args.out)
    need(expected==load(R/'plot_data.json'),'exact plotting expectations')
    graph=graphcheck(args.out,expected)
    need(graphcheck(R,expected)==graph,'retained graph vectors agree')
    render=None
    if args.render:
        for passno in [1,2]:
            q=subprocess.run(['/opt/homebrew/bin/xelatex','-interaction=nonstopmode','-halt-on-error','reader.tex'],
                             cwd=args.out,capture_output=True,text=True,timeout=60)
            (args.out/f'render{passno}.log').write_text(q.stdout+q.stderr)
            need(q.returncode==0,'complete reader render')
        bad=[x for x in (args.out/'reader.log').read_text().splitlines()
             if any(t in x for t in ['Overfull','Underfull','Missing character','LaTeX Warning'])]
        need(not bad,'reader diagnostics: '+str(bad))
        texts=[p.extract_text() or '' for p in PdfReader(args.out/'reader.pdf').pages]
        need(len(texts)==4,'complete four-page reader')
        if (R/'reader.pdf').exists():
            need(texts==[p.extract_text() or '' for p in PdfReader(R/'reader.pdf').pages],
                 'saved reader text agrees')
        render=dict(pages=len(texts),diagnostics=bad,page_text_sha256=[sha(x.encode()) for x in texts])
    report=dict(status='PASS_AUTHOR_A10_NUMERICAL_REPLAY_PENDING_DISTINCT_REVIEW',
                protocol_sha256=POLICY,coordinates=30,exact_fractions=count,
                unchanged_conditional_fractions=240,accepted_PDF_cells=870,accepted_raw_cells=2030,
                controls=controls(r,inputs_tuple),graphs=graph,reader=render,
                software_inclusive_factors=None,scientific_or_formal_replay=False)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
