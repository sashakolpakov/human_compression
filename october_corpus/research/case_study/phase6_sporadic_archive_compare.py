#!/usr/bin/env python3
"""Compare M12 source witnesses AFTER independent exhaustion; never execute Magma."""
import argparse,ast,hashlib,json,os,re,shutil,subprocess,tempfile,time,tarfile
from pathlib import Path
from phase4_parse_j2 import perms
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parse(s):
    out=[];current=[];h=None;selected=None
    for stmt in s.split(';'):
        stmt=stmt.strip()
        if not stmt:continue
        m=re.fullmatch(r'h\s*:=\s*sub<g\|(.*)>',stmt,re.S)
        if m:h=perms(m[1],12)
        elif stmt in ['load m12','g := G']:pass
        elif re.fullmatch(r'geo\s*:=\s*\[\]',stmt):out=[]
        elif re.fullmatch(r'geosub\s*:=\s*\[\]',stmt):current=[]
        elif stmt=='Append(~geosub,h)':
            assert h is not None;current.append(h)
        elif stmt=='Append(~geo,geosub)':out.append(list(current))
        else:
            m=re.fullmatch(r'geo\s*:=\s*\[geo\[i\]\s*:\s*i in\s*(\[[\d,\s]+\])\s*\]',stmt)
            if m:selected=json.loads(m[1])
            else:raise ValueError('Unsupported statement: '+stmt[:100])
    selected=selected or list(range(1,len(out)+1))
    assert all(1<=x<=len(out) for x in selected)
    return out,selected

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True)
    ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'));a=ap.parse_args()
    if not a.gap:ap.error('Set GAP or pass --gap')
    prerequisites={n:sha(HERE/n) for n in ['phase6_sporadic_M12_representatives.g','phase4_geometry_checks.g','phase4_parse_j2.py']}
    metadata={};entries=[]
    with tarfile.open(a.archive) as t:
        for n in ['m12.rk3','m12.rk4','m12.rk5']:
            b=t.extractfile(n).read();out,selected=parse(b.decode())
            metadata[n]=dict(sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),raw=len(out),selected=selected)
            entries.append((n,out,selected))
    with tempfile.TemporaryDirectory(prefix='sporadic-archive-') as d:
        p=Path(d)/'validated_data.g'
        def gp(gens):return 'Group(['+','.join('PermList('+json.dumps(x)+')' for x in gens)+'])'
        with p.open('w') as f:
            f.write('archiveData:=[];;\n')
            for n,out,sel in entries:
                f.write('Add(archiveData,rec(name:="'+n+'",selected:='+str(sel)+',geos:=[')
                f.write(','.join('['+','.join(gp(gs) for gs in geo)+']' for geo in out));f.write(']));;\n')
        source=HERE/'phase6_sporadic_archive_compare.g';log=HERE/'phase6_sporadic_M12_archive_compare.log'
        digest=sha(source);start=time.monotonic()
        # JSON strings have valid syntax for this generated GAP filename.
        cmd='ARCHIVE_PARSED_FILE:='+json.dumps(str(p))+';Read("phase6_sporadic_archive_compare.g");QUIT;'
        with log.open('w') as f:r=subprocess.run([a.gap,'-q','-c',cmd],cwd=HERE,stdout=f,stderr=subprocess.STDOUT)
        text=log.read_text();passed=r.returncode==0 and 'ARCHIVE_COMPARISON_COMPLETE' in text and 'Error,' not in text and sha(source)==digest
    coverage=[]
    for m in re.finditer(r'SOURCE_COVERAGE file=(\S+) matched_classes=(\[[^\]]*\]) selected_classes=(\[[^\]]*\]) expected_classes=(\[[^\]]*\]) matches_complete_census=(true|false)',text):
        matched=ast.literal_eval(m[2]); selected=ast.literal_eval(m[3]); expected=ast.literal_eval(m[4])
        coverage.append(dict(member=m[1],matched_classes=matched,selected_classes=selected,expected_classes=expected,missing_classes=sorted(set(expected)-set(matched)),matches_complete_census=m[5]=='true'))
    matches=[]
    for m in re.finditer(r'SOURCE_MATCH file=(\S+) raw_id=(\d+) census_id=(\d+) selected=(true|false) twot=(true|false) rank=(\d+) parabolic_orders=(\[[^\]]*\]) truncation_from=(\[[^\]]*\])',text):
        matches.append(dict(member=m[1],raw_id=int(m[2]),census_id=int(m[3]),selected=m[4]=='true',twot=m[5]=='true',rank=int(m[6]),parabolic_orders=ast.literal_eval(m[7]),truncation_from=ast.literal_eval(m[8])))
    for n,digest0 in prerequisites.items(): assert sha(HERE/n)==digest0
    result=dict(passed=passed,prerequisites=prerequisites,coverage=coverage,matches=matches,archive_sha256=sha(a.archive),source_url='https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S1461157000001133/resource/name/S1461157000001133sup002.tar',members=metadata,executed_source_sha256=digest,parser_sha256=sha(Path(__file__)),permutation_parser_sha256=sha(HERE/'phase4_parse_j2.py'),log=log.name,log_sha256=sha(log),seconds=time.monotonic()-start,exit_code=r.returncode,scope='Post-hoc source-witness correspondence only; not an exhaustion input.')
    (HERE/'phase6_sporadic_M12_archive_compare.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=passed,members={k:[v['raw'],len(v['selected'])] for k,v in metadata.items()},seconds=result['seconds']),indent=2))
    if not passed:raise SystemExit(1)
if __name__=='__main__':main()
