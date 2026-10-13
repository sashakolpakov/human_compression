from pathlib import Path
import json,hashlib,collections,sys
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;F=W.parent/'F012_recovery_work/cubic_census02'
records=[];seen=0;nonbip=0
with (F/'graphs.txt').open('rb') as f:
    while True:
        pos=f.tell();line=f.readline()
        if not line:break
        fs=line.split();name=fs[0].decode();n,k,m=map(int,fs[1:4])
        if n>768:break
        if k!=3 or len(fs)!=4+2*m:raise ValueError(name)
        seen+=1;adj=[[] for _ in range(n)]
        for a,b in zip(fs[4::2],fs[5::2]):
            a,b=int(a),int(b)
            if not 0<=a<b<n:raise ValueError(name)
            adj[a].append(b);adj[b].append(a)
        if any(len(a)!=3 for a in adj):raise ValueError(name)
        color={0:0};q=collections.deque([0]);bip=True
        while q:
            a=q.popleft()
            for b in adj[a]:
                if b not in color:color[b]=1-color[a];q.append(b)
                elif color[b]==color[a]:bip=False
        if len(color)!=n:raise ValueError('source disconnected')
        if not bip:nonbip+=1;continue
        records.append({'id':name,'n':n,'offset':pos,'bytes':len(line),'line_sha256':hashlib.sha256(line).hexdigest()})
if seen!=40580:raise ValueError('range count')
out=W/'cubic_filter';out.mkdir(exist_ok=True)
chunks=[]
for i in range(0,len(records),200):
    name=f'chunk{i//200:03d}';chunks.append(name)
    (out/(name+'.inputs.json')).write_text(json.dumps(records[i:i+200],indent=2)+'\n')
(out/'queue.json').write_text(json.dumps(chunks,indent=2)+'\n')
(out/'scope.json').write_text(json.dumps({'source':str(F/'graphs.txt'),'source_index':str(F/'index.json'),'source_report':str(F/'parse_report.json'),'full_range_graphs':seen,'nonbipartite':nonbip,'bipartite_candidates':len(records),'chunks':len(chunks),'range':'all retained cubic vertex-transitive graphs of order<=768; arc-transitivity still to be tested'},indent=2)+'\n')
print(json.dumps({'seen':seen,'nonbipartite':nonbip,'bipartite':len(records),'chunks':len(chunks)}))
