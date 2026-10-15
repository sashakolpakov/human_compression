import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;G=W.parent;S=G.parents[1];P=G/'butterfly_component_v1'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def row(p,base=None):
    b=p.read_bytes();return dict(path=str(p.relative_to(base))if base else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
    need(not P.exists(),'immutable destination');P.mkdir()
    for n in ['objects.py','objects_v2.py','recipes.py','ovals.py','replay.py','controls.py','check.py','ambiguity.py','constructions.tex','README.rst','freeze.py']:shutil.copyfile(W/n,P/n)
    shutil.copyfile(W/'native03/constructions.pdf',P/'constructions.pdf');shutil.copytree(W/'native03',P/'native_author');shutil.copytree(W/'source',P/'native_source');H=P/'history';H.mkdir();E=P/'expected';E.mkdir()
    for n in ['objects01','objects02','recipes01','ovals01','replay01','controls01','native01','native02']:shutil.copytree(W/n,H/n)
    for n in ['run_bound.py','run_bound_v2.py','run_recipes.py','run_ovals.py','completion_diagnosis01.json']:shutil.copyfile(W/n,H/n)
    aliases=[]
    for name,path in [('objects.json','objects02/result/objects.json'),('recipes.json','recipes01/result/report.json'),('ovals.json','ovals01/result/report.json'),('ambiguity.json','ambiguity01.json')]:
        src=W/path;shutil.copyfile(src,E/name);r=row(src);aliases.append(dict(original=str(src),copy='expected/'+name,bytes=r['bytes'],sha256=r['sha256']))
    # Preserve the discovery scripts' literal standalone input locator too.
    (P/'objects02/result').mkdir(parents=True);shutil.copyfile(E/'objects.json',P/'objects02/result/objects.json')
    roots={
      'constructions_component_v1':'589fad8fd4a1a46239df431184087a52793fbb838d0cf5f73688f8e5ca2e61a2',
      'constructions_review_v1':'e9ea584912ba045d60ee6d1013e349bea623497e7f809a621837888f8196b680',
      'constructions_root_adoption':'d0212cb32c1c021dfc382aa903ed7db5ea3cae131fa1f0dfeadfa82b87015e86',
      'palette_serialization_v1':'5399e45468b83a49e0d2750a2087cb8e6006919b08548d0434b5195ed550eff3',
      'palette_serialization_review_v1':'6a09697960e322a8d10bcabc9354504f8e0b1e6c17a9ed485ab36c25aa6ab96a',
      'source_join_component_v2':'2e69c5d047fa7d15fb8d101090a78c18a69f3100db2aeb111abc107878639ffb',
      'source_join_review_v2':'1cbc91ca8ba73e421cf2e6412b20654a5057f7545ffc232d29566d169f41fd00',
      'baer_component_v1':'a8569d8dfad9403a8a7fc41271aee37c8aa8491de878e8bae852d3e9f50bd07d',
      'baer_review_v1':'2d9ee5f051d2ab8a07573c2ebd5d4d56d7816bfbe6fdcfa5de70de0de9acfd5e',
      'doubling_component_v1':'1930bd893bc514511b02ea1736e7c292e26b127d3a64475cbe0ac91dd366ffa1',
      'doubling_review_v1':'2c74cab966cfed8a74366f57e8ca7004ddadf5f6f347b97ec1efd4e20d318774'}
    deps={};rootrows=[]
    def add(p,expected=None):
        p=p.absolute();r=row(p)
        if expected:need((r['bytes'],r['sha256'])==(expected['bytes'],expected['sha256']),'acquired binding '+str(p))
        if str(p)in deps:need(deps[str(p)]==r,'binding conflict')
        deps[str(p)]=r
    for name,h in roots.items():
        R=G/name;M=R/'manifest.json';need(row(M)['sha256']==h,'exact root');add(M);rootrows.append(row(M,S))
        for r in read(M)['exports']:add(R/r['path'],r)
        for r in read(R/'dependencies.json'):
            p=Path(r['path']);add(p if p.is_absolute() else S/p,r)
    for n in ['objects01','objects02','recipes01','ovals01']:
        r=read(W/n/'receipt.json')
        for q in r['inputs']:add(Path(q['path']),q)
        for k in ['stdout','stderr','result']:
            if k in r:add(Path(r[k]['path']),r[k])
    for r in read(W/'ambiguity01.json')['inputs']:add(Path(r['path']),r)
    for p in W.rglob('*'):
        if p.is_file()and '__pycache__'not in p.parts:add(p)
    F=S/'reboot_20261013/L100_recipe_source_read_f003';Q=P/'preliminary_source_read';Q.mkdir()
    for n,h in [('report.json','89a4004c3202b8d925cbe721bc80a46348a0393e8ed7a8476587e942229b7b94'),('condition1_typography.json','185847500eddcbf29205dd583ed727db7c7ead11dfed58257916fcc478452305')]:
        need(row(F/n)['sha256']==h,'exact preliminary source report');add(F/n);shutil.copyfile(F/n,Q/n)
    for p in [S/'corpus106_source_reading_L091_L100_L102/L100_intake.json',Path(sys.executable),Path('/opt/homebrew/bin/pdflatex'),Path('/opt/homebrew/bin/gs')]:add(p)
    import pypdf
    for p in Path(pypdf.__file__).parent.rglob('*.py'):add(p)
    save(P/'acquired_roots.json',rootrows);save(P/'input_aliases.json',aliases)
    replay=read(W/'replay01/report.json');maps=read(E/'recipes.json')['maps']+read(E/'ovals.json')['maps'];routes=[]
    for r in replay['local_action_routes']:
        m=next(m for m in maps if m['source_label']==r['label']);flags=[None]*4
        for t,u in enumerate(m['target_to_derived_types']):flags[u-1]=r['acquired_panel_two_transitive'][t]
        routes.append(r|dict(source_type_order_panel_two_transitive=flags))
    save(P/'source_routes.json',dict(source='corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf',source_sha256='13f207232f40ca0e00674b9e9de02a91e98226b325ddd428320c661e6131ff84',source_edition='Halle22-page preprint; journal uncollated',physical_pages=[4,5,16,17,18,19],butterfly_definition='Explicit all-four-cross-singleton convention; two displayed conditions alone are insufficient.',displayed_rule_qualification='Two fixed same-orbit completions of one positive pole satisfy both displayed conditions. No assertion about stronger conventional meaning in uninspected cited literature; no principal refutation.',lemma_2_3='Three actual transitive1260-object classes with explicit D8 times C2 stabilizer normal forms, under the explicit convention.',recipes=routes,butterfly_maps=18,oval_maps=6,oval_choice='For ordered distinct Baer classes i,j use H_e(i) for ovals and coordinate duals of H_e(d(j)) for dual ovals; no arbitrary-class assertion.',source_only_assistance='f003 native typography read; no new proof or code contribution.',remaining=['Structural names of all remaining parabolics/Borels/kernels and full Aut/Cor groups','Whole source synthesis'],full_source_credit=0,principal_classification_refuted=False))
    save(P/'roles.json',dict(author='publication_recovery',source_attribution='Gottschalk--Leemans definitions and recipes, with exact native qualifications; prior projective and finite classification inputs explicitly acquired.',root_input='Scope, source-collation and narrow-claim requests; accepted prior component reviews; no new construction or map-code contribution.',f003_input='Read-only native typography assistance, preserved separately.',distinct_review='pending',priority_claim=False))
    save(P/'development.json',dict(objects01='Preserved failed uniqueness assertion from literal two-cross conditions; no source conclusion inferred from failure alone.',objects02='Explicit stronger all-cross condition,1.06s complete finite object construction, no ambient census.',recipes='18 actual positive maps,16.01s under60s bound.',ovals='6 actual positive maps,4.84s under60s bound.',native='Initial4-page edition had2 overfull lines; native02 corrected line breaks; native03 only adds missing spaces in prose. All final4pages directly viewed, clean two-pass log.',preliminary='Source typography assistance by f003 separately retained, not mathematical acceptance.',all_owned_handles_terminal=True))
    final=[]
    for p,r in sorted(deps.items()):
        p=Path(p);final.append({**r,'path':str(p.relative_to(S))if p.is_relative_to(S)else str(p),'namespace':'study'if p.is_relative_to(S)else'runtime'})
    save(P/'dependencies.json',final)
    exports=[row(p,P)for p in sorted(P.rglob('*'))if p.is_file()];save(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_BUTTERFLY_OVAL_COMPONENT_V1',exports=exports,dependencies=len(final)))
    print(json.dumps(dict(packet=str(P),manifest=row(P/'manifest.json'),exports=len(exports),dependencies=len(final)),indent=2))
if __name__=='__main__':main()
