import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,hashlib,json,subprocess,time
from pathlib import Path
from decode import decode,frame,need,WIDTH
from structural import validate,palette_map
HERE=Path(__file__).resolve().parent;G=HERE.parent;S=G.parents[1]
T=G/'palette_target01';P=G/'palette_interface_v1';GAP=Path('/opt/homebrew/bin/gap')
RECEIPT_SHA='6657bc46a57372da99bc70ddfadfa5ebce4f97d6a037c0d107929cd86020b7f1'
def pin(p):
    p=Path(p).absolute();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verify(row):
    z=pin(row['path']);need(all(z[k]==row[k]for k in ['bytes','sha256']),'unchanged input '+row['path']);return z
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def reject(fn):
    try:fn()
    except (ValueError,KeyError,TypeError,IndexError):return True
    raise AssertionError('damaged control accepted')
def prepare(out):
    need(not out.exists(),'fresh output');rp=T/'receipt.json';r=json.loads(rp.read_text())
    need(pin(rp)['sha256']==RECEIPT_SHA,'fixed native result receipt')
    need(r['status']=='COMPLETE_LITERAL_PALETTE' and r['execution']['status']=='RETURNED' and r['execution']['returncode']==0,'clean acquired native execution')
    need(not(T/'execution/stderr').read_bytes(),'empty native stderr')
    inputs=[pin(rp)]+[verify(q)for q in r['inputs']+r['outputs']]
    names=['group_elements.json','checkpoint.json','result.json']+[f'{kind}{i}.json'for i in range(1,30)for kind in ['model','groups']]
    need(set(names)=={p.name for p in T.glob('*.json')if p.name!='receipt.json'},'all scientific files explicitly listed')
    out.mkdir(parents=True);(out/'decoded').mkdir();(out/'roundtrip').mkdir();(out/'boundary').mkdir();data={};links=[]
    output_paths={q['path']:q for q in r['outputs']}
    for name in names:
        raw=T/name;need(str(raw)in output_paths,'scientific file bound by native receipt');payload,d=decode(raw.read_bytes());dest=out/'decoded'/name;dest.write_bytes(payload);data[name]=d
        links.append(dict(name=name,original=pin(raw),derived=pin(dest),continuation_count=raw.read_bytes().count(b'\n')))
    # Cases place escaped backslashes/quotes/newline escapes and digit boundaries
    # at and on each side of the 4094-payload-byte split. No JSON execution.
    boundary=[]
    for offset in range(-4,5):
        for tail in ['\\','"','\\\n','12345','\\"\\']:
            value={'text':'x'*(WIDTH-12+offset)+tail+'z'*20,'digits':[123456789,0]}
            payload=json.dumps(value,separators=(',',':'),ensure_ascii=True).encode();name=f'case{len(boundary)}.json';(out/'boundary'/name).write_bytes(payload);boundary.append((name,payload,value))
    for size in [WIDTH-1,WIDTH,WIDTH+1,2*WIDTH,2*WIDTH+1]:
        payload=b'{"x":"'+b'a'*(size-8)+b'"}';need(len(payload)==size,'exact boundary length');name=f'case{len(boundary)}.json';(out/'boundary'/name).write_bytes(payload);boundary.append((name,payload,json.loads(payload)))
    q=lambda x:json.dumps(str(x))
    code=['LoadPackage("json");;SizeScreen([100000,24]);;', 'ReadText:=function(path) local stream,value;stream:=InputTextFile(path);value:=ReadAll(stream);CloseStream(stream);return value;end;;']
    for name in names:code.append('PrintTo('+q(out/'roundtrip'/name)+',ReadText('+q(out/'decoded'/name)+'));;')
    for name,_,_ in boundary:code.append('PrintTo('+q(out/'roundtrip'/name)+',ReadText('+q(out/'boundary'/name)+'));;')
    code+=['Read('+q(G/'incremental_target02/result.g')+');;',
      'WriteUnformatted:=function(path,value) local stream;stream:=OutputTextFile(path,false);SetPrintFormattingStatus(stream,false);PrintTo(stream,GapToJsonString(value));CloseStream(stream);end;;',
      'WriteUnformatted('+q(out/'source_projection.json')+',rec(group_generators:=List(L100CompleteAutFusion.group_generators,p->ListPerm(p,21)),representatives:=List(L100CompleteAutFusion.representatives,c->rec(source:=[c.borel_id,c.source_index],parabolic_generators:=List(c.parabolics,H->List(GeneratorsOfGroup(H),p->ListPerm(p,21)))))));;',
      'Print("PASS_PRINTTO_ROUNDTRIP_AND_SOURCE_PROJECTION\\n");QUIT_GAP(0);']
    (out/'native.g').write_text('\n'.join(code)+'\n')
    for path in [GAP,HERE/'repair.py',HERE/'decode.py',HERE/'structural.py',out/'native.g',G/'incremental_target02/result.g',Path('/opt/homebrew/Cellar/gap/4.15.1/include/gap/io.h'),Path('/opt/homebrew/Cellar/gap/4.15.1/share/gap/lib/streams.gd'),Path('/opt/homebrew/Cellar/gap/4.15.1/share/gap/lib/streams.gi')]:inputs.append(pin(path))
    dump(out/'active.json',dict(status='ACTIVE_FORMAT_ROUNDTRIP_NO_GRAPH',inputs=inputs,command=[str(GAP),'-q','-b',str(out/'native.g')],cap_seconds=20))
    started=time.monotonic();p=subprocess.run([str(GAP),'-q','-b',str(out/'native.g')],capture_output=True,timeout=20);(out/'stdout').write_bytes(p.stdout);(out/'stderr').write_bytes(p.stderr)
    dump(out/'native_receipt.json',dict(returncode=p.returncode,elapsed_seconds=time.monotonic()-started,stdout=pin(out/'stdout'),stderr=pin(out/'stderr')))
    need(p.returncode==0 and not p.stderr and p.stdout.count(b'PASS_PRINTTO_ROUNDTRIP_AND_SOURCE_PROJECTION')==1,'native format/source projection clean return')
    for name in names:need((out/'roundtrip'/name).read_bytes()==(T/name).read_bytes(),'actual native byte-identical roundtrip '+name)
    boundary_results=[]
    for name,payload,value in boundary:
        raw=(out/'roundtrip'/name).read_bytes()
        if b'\\' in payload:
            reject(lambda raw=raw:decode(raw));boundary_results.append([name,'REJECTED_ESCAPED_PAYLOAD'])
        else:
            need(frame(payload)==raw,'native fixed-width framing control');got,obj=decode(raw);need(got==payload and obj==value,'unescaped boundary exact inverse');boundary_results.append([name,'EXACT_INVERSE'])
    projection=json.loads((out/'source_projection.json').read_text());scientific=validate(data,projection)
    damages=[];sample=frame(json.dumps({'x':'a'*5000}).encode())
    for label,raw in [('missing-continuation',sample.replace(b'\\\n',b'\n',1)),('short-line',sample[1:]),('double-newline',sample.replace(b'\\\n',b'\\\n\n',1)),('literal-cr',sample+b'\r'),('trailing-newline',sample+b'\n'),('nonascii',sample+b'\xff'),('duplicate-key',b'{"x":1,"x":2}'),('nonfinite',b'{"x":NaN}'),('nonobject',b'[1]'),('bad-json',b'{"x":}')]:reject(lambda raw=raw:decode(raw));damages.append(label)
    d=data['model1.json'];n=d['n'];r=d['rank'];identity=list(range(1,n+r+1))
    wrong=copy.deepcopy(d);wrong['adjacency'][0]=[];reject(lambda:palette_map(d,wrong,identity));damages.append('missing-incidences')
    wrong=copy.deepcopy(d);wrong['types'][0]=2;reject(lambda:palette_map(d,wrong,identity));damages.append('wrong-type')
    wrong=identity[:];wrong[0]=wrong[1];reject(lambda:palette_map(d,d,wrong));damages.append('nonpermutation')
    wrong=identity[:];wrong[0],wrong[n]=wrong[n],wrong[0];reject(lambda:palette_map(d,d,wrong));damages.append('object-marker-mixing')
    wrong=copy.deepcopy(projection);wrong['group_generators'][0][0]=0;reject(lambda:validate(data,wrong));damages.append('different-source-generators')
    wrong=copy.deepcopy(projection);wrong['representatives'][0]['source'][0]+=1;reject(lambda:validate(data,wrong));damages.append('different-source-row')
    for row in inputs:verify(row)
    dump(out/'links.json',links)
    report=dict(status='PASS_EXACT_PALETTE_DECODING_NO_GRAPH_RERUN',inputs=inputs,scientific_files=len(names),actual_native_roundtrips=len(names),boundary_cases=boundary_results,damages=damages,scientific=scientific,native=pin(out/'native_receipt.json'),links=pin(out/'links.json'),graph_runs=0,source_credit=0,whole_original_credit=0)
    dump(out/'report.json',report);print(json.dumps({k:v for k,v in report.items()if k!='inputs'}))
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();prepare(a.out.absolute())
if __name__=='__main__':main()
