"""Validate the frozen positive maps directly, without searching for new maps."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import time

AUTHOR = '4afcee9bb0489aed5111feaa479057e0746728c8270a6363e7794980f4ca969b'

def need(value, message):
    if not value:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study-root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    author = args.study_root/'topic_D_L096_J3_extension'
    sha = lambda b: hashlib.sha256(b).hexdigest()
    need(sha((author/'manifest.json').read_bytes()) == AUTHOR, 'exact author packet')
    bound = {r['path']:r for r in json.loads((author/'manifest.json').read_text())['exports']}
    names = ['archive_data/inputs.g', 'receipts/actual_witnesses/positive_witnesses.g.stdout.log']
    for name in names:
        data = (author/name).read_bytes()
        need(len(data) == bound[name]['bytes'] and sha(data) == bound[name]['sha256'], 'frozen '+name)
    need(not args.out.exists(), 'fresh output')
    args.out.mkdir(parents=True)
    shutil.copyfile(author/names[0], args.out/'inputs.g')
    text = (author/names[1]).read_text().replace('\\\n','')
    witnesses = [json.loads(line[len('WITNESS|'):]) for line in text.splitlines()
                 if line.startswith('WITNESS|')]
    need([w['pair'] for w in witnesses] == [[14,13],[17,16]], 'two exact saved maps')
    fields = ['pair','type_indices','inner_conjugator','automorphism_generator_images','ambient_generators']
    program = 'Read("inputs.g");;\nW:=[' + ','.join(
        'rec('+','.join(k+':='+json.dumps(w[k],separators=(',',':')) for k in fields)+')'
        for w in witnesses) + '];;\n'
    program += '''
G:=Group(Concatenation(L096Inputs[1].parabolic_generators));;
if Size(G)<>50232960 then Error("ambient order");fi;
VerifySaved:=function(w)
 local gens,imgs,phi,u,P,Q;
 gens:=List(w.ambient_generators,PermList);
 imgs:=List(w.automorphism_generator_images,PermList);
 if Group(gens)<>G or not ForAll(imgs,x->x in G) then Error("ambient witness");fi;
 phi:=GroupHomomorphismByImages(G,G,gens,imgs);
 if phi=fail or not IsBijective(phi) then Error("saved images are not an automorphism");fi;
 u:=PermList(w.inner_conjugator);
 if not u in G then Error("conjugator outside ambient");fi;
 P:=List(L096Inputs[w.pair[1]].parabolic_generators,Group);
 Q:=List(L096Inputs[w.pair[2]].parabolic_generators,Group);
 if not ForAll([1..3],i->Image(phi,P[i])^u=Q[w.type_indices[i]]) then
  Error("saved family map false");
 fi;
 Print("CHECKED_SAVED_TRANSPORTER|",w.pair,"|all3subgroups\\n");
end;;
for w in W do VerifySaved(w);od;
Print("PASS_INDEPENDENT_SAVED_TRANSPORTERS\\n");QUIT;
'''
    (args.out/'validate_saved.g').write_text(program)
    start = time.monotonic()
    run = subprocess.run(['/opt/homebrew/bin/gap','-q','-b','validate_saved.g'],
                         cwd=args.out,capture_output=True,text=True,timeout=90)
    (args.out/'stdout.log').write_text(run.stdout)
    (args.out/'stderr.log').write_text(run.stderr)
    need(run.returncode == 0 and not run.stderr and 'Error,' not in run.stdout
         and 'Syntax warning' not in run.stdout, 'clean independent evaluation')
    need(run.stdout.count('CHECKED_SAVED_TRANSPORTER|') == 2
         and 'PASS_INDEPENDENT_SAVED_TRANSPORTERS' in run.stdout, 'two verified complete family maps')
    report = dict(status='PASS_INDEPENDENT_SAVED_TRANSPORTERS', seconds=time.monotonic()-start,
                  pairs=[w['pair'] for w in witnesses], author_manifest_sha256=AUTHOR,
                  ambient_order=50232960, saved_automorphisms_bijective=True,
                  all_six_subgroup_images_checked=True, new_transporter_search=False,
                  generated_program_sha256=sha(program.encode()), output_sha256=sha(run.stdout.encode()))
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
