#!/usr/bin/env python3
"""Bounded publication-plan checks; no primary or scientific-program execution."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json,re
H=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def inputs():
    return {k:load(H/v)for k,v in {
      'copy':'copy_plan.json','raw':'raw_roles.json','cat':'proposed/papers/catalogue.json',
      'basecat':'baseline/papers/catalogue.json','corpus':'proposed/audit/corpus/next.json',
      'basecorpus':'baseline/audit/corpus/latest.json','active':'proposed/audit/corpus/active_catalogue.json',
      'latest':'proposed/papers/latest_catalogue.json','baselatest':'baseline/papers/latest_catalogue.json',
      'rows':'catalogue_additions.json','overview':'overview17_plan.json','pointer':'topic_pointer_proposal.json'}.items()}
def validate(q):
    c,b=q['cat'],q['basecat'];rows=q['rows']['entries'];need(len(rows)==10,'ten current science rows')
    need(c['papers']==b['papers'],'preserve all original canonical rows')
    need(c['new_editions'][:len(b['new_editions'])]==b['new_editions'],'preserve historical editions')
    need(c['new_editions'][len(b['new_editions']):]==rows,'exact additive registration')
    need(len({r['id']for r in c['papers']+c['new_editions']})==len(c['papers']+c['new_editions']),'unique IDs')
    need(c['current_topic_editions']['A']==[r['id']for r in rows],'current A science routes')
    need({k:v for k,v in c['current_topic_editions'].items()if k!='A'}=={k:v for k,v in b['current_topic_editions'].items()if k!='A'},'no other current topic changes')
    need(all(r['compiler']=='xelatex'for r in rows[:-1])and rows[-1]['compiler']=='pdflatex','exact engines')
    need(sum(r['physical_pages']for r in rows)==79 and rows[0]['physical_pages']==23,'full U and all apps')
    x=q['corpus'];old=q['basecorpus'];a=set(x['active_original_ids']);m=set(x['measured_original_ids']);p=set(x['accessible_pending_original_ids']);e=set(x['editorial_original_ids'])
    need((len(a),len(m),len(p),len(e))==(106,51,54,1),'programme cardinalities')
    need(a==set(old['active_original_ids'])and a==m|p|e and not(m&p or m&e or p&e),'all active IDs partitioned')
    need(e=={'L022'}and m-set(old['measured_original_ids'])=={'L121'},'only L121 measured; editorial separate')
    need(x['admitted_original_ids']==x['measured_original_ids']and x['editorial_factor']is None,'no editorial factor')
    need(x['archived_original_ids']==old['archived_original_ids']and len(x['archived_original_ids'])==55,'archives unchanged')
    need(x['pending_source_retrieval']==0 and not x['source_retrieval_in_scope'],'no retrieval')
    active=q['active'];original=load(H/'baseline'/old['active_catalogue']['path'])
    need(len(active['entries'])==106,'all catalogue rows')
    for new,prior in zip(active['entries'],original['entries']):
        need(new['original_id']==prior['original_id']and new['source_access']==prior['source_access'],'source provenance unchanged')
        if new['original_id']not in['L121','L022']:need(new==prior,'other source rows unchanged')
        if new['original_id']=='L022':need(new['active']and new['current_principal_recovery']['factor']is None and not new['current_principal_recovery']['count_as_measured_mathematical_recovery'],'editorial remains active')
    new=q['latest'];oldl=q['baselatest'];need(new['entries'][-1]==rows[-1],'new application entry')
    current={r['id']for r in rows[:-1]}
    for a,b in zip(new['entries'][:-1],oldl['entries']):
        expected=deepcopy(b)
        if b.get('id')in current:expected['measurement_admission']='audit/topic-a/v4/admission.json'
        need(a==expected,'other catalogue entries/measurements unchanged')
    need(len(new['entries'])==len(oldl['entries'])+1,'one application only')
    o=q['overview'];need((o['topics'],o['active_originals'],o['measured_originals'],o['editorial_originals'])==(19,106,51,1),'no topic growth/editorial credit')
    need(o['no_pooled_factor']and o['source_software_unknown'],'symmetric limits')
    raw=q['raw'];need((raw['required_programs'],raw['required_data'],raw['operational'],raw['partial_formal_files'])==(8,1,4,2),'new whole file roles')
    need(len(raw['new_L121_files'])==15 and raw['entire_topic_required_files']==20 and raw['entire_topic_files']==45,'complete raw closure')
    need(raw['complete_enlarged_printed_cost']is None and raw['source_software_cost']is None,'unknown software costs')
    ptr=q['pointer'];need(ptr['common']=='papers/topic-a/v3/umbrella.pdf'and len(ptr['applications'])==9,'old common reused in full')
    need(ptr['software_inclusive_factor']is None and ptr['complete_enlarged_printed_program_factor']is None,'no asymmetric or incomplete code factor')
    routes=q['copy']['files'];need(len({r['public_path']for r in routes})==len(routes),'unique targets')
    for r in routes:
        path=Path(r['public_path']);need(not path.is_absolute()and'..'not in path.parts,'safe public route')
        need(not str(path).startswith('papers/topic-a/v3/'),'no duplicate/mutated common edition')
        need(not str(path).startswith(('sources/','private_source/')),'no original redistribution')
    return True
def controls(q):
    rejected=[]
    tests=[('editorial measured',lambda q:q['corpus']['measured_original_ids'].append('L022')),
      ('drop accessible editorial',lambda q:q['corpus']['active_original_ids'].remove('L022')),
      ('editorial zero factor',lambda q:q['corpus'].update(editorial_factor=0)),
      ('free common',lambda q:q['rows']['entries'][0].update(physical_pages=0)),
      ('wrong L121 compiler',lambda q:q['rows']['entries'][-1].update(compiler='xelatex')),
      ('delete historical row',lambda q:q['cat']['papers'].pop()),
      ('wrong existing topic pointer',lambda q:q['cat']['current_topic_editions'].update(E=[])),
      ('drop mandatory data',lambda q:q['raw'].update(required_data=0)),
      ('turn runner into premise',lambda q:q['raw'].update(required_programs=9)),
      ('complete old appendices',lambda q:q['raw'].update(complete_enlarged_printed_cost=30)),
      ('invent software factor',lambda q:q['pointer'].update(software_inclusive_factor=1)),
      ('new singleton topic',lambda q:q['overview'].update(topics=20)),
      ('copy original PDF',lambda q:q['copy']['files'][0].update(public_path='sources/older_L121.pdf'))]
    for name,fn in tests:
        x=deepcopy(q);fn(x)
        try:validate(x)
        except(ValueError,KeyError):rejected.append(name)
        else:raise ValueError('accepted control '+name)
    return rejected
def wrappers(repo):
    routes=load(H/'copy_plan.json')['files'];mapped={r['public_path']:r for r in routes}
    generated=load(H/'wrapper_routes.json')['files'];expected={r['public_path']:r for r in generated}
    def exact(row):
        path=row['path']
        if path in expected:
            b=(H/expected[path]['proposal_path']).read_bytes()
        elif path in mapped:
            x=mapped[path];need(x['bytes']==row['bytes']and x['sha256']==row['sha256'],'mapped binding '+path);return
        else:b=(repo/path).read_bytes()
        need(len(b)==row['bytes']and sha(b)==row['sha256'],'generated binding '+path)
    for r in generated:exact(dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
    a=load(H/'wrappers/audit/topic-a/v4/admission.json')
    for key in ['prior_eight_original_admission','new_scientific_admission','numerical_author','numerical_distinct_review',
                'numerical_root_adoption','measurement','reader','input_author','input_distinct_review','input_root_adoption']:
        exact(a[key])
    for r in a['frozen_payloads']:exact(r)
    need((a['source_sum'],a['whole_common'],a['application_sum'],a['whole_written'])==(273937,66140,136125,202265),'accepted whole values')
    need(a['exact_fractions']==300 and a['old_conditionals_preserved']==240 and a['software_inclusive_factor']is None,'complete numerical boundary')
    c=load(H/'wrappers/audit/corpus/latest.json');exact(c['snapshot']);exact(c['active_catalogue']);exact(c['previous_snapshot'])
    need(c['editorial_original_ids']==['L022'] and c['currently_measured_originals']==51 and c['accessible_pending_complete_recovery']==54,'final proposed corpus')
    p=load(H/'wrappers/papers/topic-a/latest.json');exact(p['admission']);exact(p['measurement']);exact(p['reader'])
    need(len(p['applications'])==9 and p['common']=='papers/topic-a/v3/umbrella.pdf','current pointer keeps whole common')
    links=[];pending=[]
    import posixpath
    texts=[('papers/topic-a/v4/PUBLICATION.rst',(H/'wrappers/papers/topic-a/v4/PUBLICATION.rst').read_text()),
           ('papers/topic-a/extensions/locally-toroidal/v1/PUBLICATION.rst',(H/'wrappers/papers/topic-a/extensions/locally-toroidal/v1/PUBLICATION.rst').read_text())]
    texts += [('README.rst',e['after'])for e in load(H/'documentation_delta.json')['readme_replacements']]
    for where,text in texts:
        for target in re.findall(r'`[^`]*<([^<>]+)>`_',text,re.S):
            if '://'in target:continue
            target=target.split('#')[0];path=posixpath.normpath(posixpath.join(posixpath.dirname(where),target))
            if path.startswith('audit/overview/v17/'):
                need(path in {'audit/overview/v17/packet/reader.pdf','audit/overview/v17/packet/whole_topics.svg','audit/overview/v17/packet/conditional_1.svg','audit/overview/v17/packet/conditional_2.svg','audit/overview/v17/README.rst'},'named overview gate');pending.append(path)
            else:need(path in expected or path in mapped or(repo/path).exists(),'new local link '+path);links.append(path)
    return dict(generated_files=len(generated),new_local_links=len(links),pending_overview17_links=sorted(set(pending)))
def main():
    a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args()
    need(not args.out.exists(),'fresh report directory');args.out.mkdir(parents=True)
    q=inputs();validate(q)
    for r in q['copy']['files']:
        b=(args.study_root/r['study_path']).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'exact frozen export '+r['study_path'])
    for r in load(H/'reused_science.json')['files']:
        b=(args.repo/r['path']).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'existing science unchanged')
    for r in q['rows']['entries']:
        path=(args.repo/r['tex'])if r is not q['rows']['entries'][-1]else(args.study_root/'topic_A_L121_application/application.tex')
        title=re.search(r'\\title\{([^{}]*)\}',path.read_text()).group(1)
        need(title==r['title'],'literal title '+r['id'])
    report=dict(status='PASS_PRIVATE_PUBLICATION_PLAN_AFTER_NUMERICAL_ADOPTION',
      copied_exports_and_manifests=len(q['copy']['files']),reused_science_files=len(load(H/'reused_science.json')['files']),
      scientific_build_rows=10,programme=dict(active=106,measured=51,mathematical_pending=54,editorial=1,archived=55),
      controls=controls(q),wrapper_checks=wrappers(args.repo),public_writes=False,scientific_programs_run=False)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
