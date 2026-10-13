from pathlib import Path
import hashlib,json,re,math,ast
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L071_alternating_distinct';P=S/'corpus106_F002_recovery_v1';rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def literal(s,k):
 assert s.count(k)==1,(k,s.count(k));start=s.index('[',s.index(k)+len(k)); depth=0
 for end in range(start,len(s)):
  if s[end]=='[':depth+=1
  elif s[end]==']':
   depth-=1
   if depth==0:return s[start:end+1]
 raise ValueError('unclosed literal')
source=(S/'sources/catalogue_L071.txt').read_text();sec=source.split('--- PDF PAGE 9 ---')[1].split('Remark 6.1.')[0];expected={n:{} for n in range(11,15)}
for n,r,c in re.findall(r'A(11|12|13|14)\s+(\d+)\s+(\d+)',sec):expected[int(n)][int(r)]=int(c)
assert sum(len(x) for x in expected.values())==13
for n,dirname in [(11,'L071_A11_restored01'),(12,'L071_A12_restored01'),(13,'L071_A13_restart01'),(14,'L071_A14_full_rank01')]:
 D=S/'reboot_20261013'/dirname;V=S/'reboot_20261013'/f'L071_A{n}_full_IP01';r=json.loads((D/'report.json').read_text());v=json.loads((V/'report.json').read_text());order=math.factorial(n)//2;limit=order.bit_length()-1
 assert r['degree']==n and r['rank_limit']==limit
 for report,base in [(r,P),(v,S)]:
  assert report['status']=='EXITED' and report['returncode']==0 and report['complete_marker'] and report['unchanged']
  for p in report['pins']:assert sha(base/p['path'])==p['sha256'],p
 assert (D/'stderr.log').read_bytes()==b'' and (V/'stderr.log').read_bytes()==b''
 raw=(D/'stdout.log').read_text();vs=(V/'stdout.log').read_text();assert raw.count('COMPLETE_EXHAUSTION')==vs.count('COMPLETE_VALIDATION')==1
 assert list(map(int,re.findall(r'COMPLETE_MARKS_RANK_(\d+) ',raw)))==list(range(3,limit+1))
 header=re.search(r'DEGREE (\d+) RANK_LIMIT (\d+) GROUP_ORDER (\d+)',raw);assert tuple(map(int,header.groups()))==(n,limit,order)
 involcount=int(re.search(r'^INVOLUTIONS (\d+)$',raw,re.M)[1]);assert involcount==sum(math.factorial(n)//(2**k*math.factorial(k)*math.factorial(n-2*k)) for k in range(2,n//2+1,2))
 lines=['recordedInvolutions:='+literal(raw,'INVOLUTIONS_LITERAL')+';;','recordedMarks:=[];;'];ranktuples={}
 for rank in range(3,limit+1):
  text=literal(raw,f'COMPLETE_MARKS_RANK_{rank} ');lines.append(f'recordedMarks[{rank}]:='+text+';;');marks=ast.literal_eval(text);assert all(len(t)==rank and len(set(t))==rank and all(1<=x<=involcount for x in t) for t in marks)
  ranktuples[rank]={tuple(t) for t in marks};assert len(ranktuples[rank])==len(marks)
 assert '\n'.join(lines)+'\n'==(V/'records.g').read_text()
 printed={rank:{} for rank in range(3,limit+1)}
 for ids,o,typ,dual in re.findall(r'\bMARK\s+(\[[^\]]*\])\s+ORDER\s+(\d+)\s+TYPE\s+(\[[^\]]*\])\s+SELF_DUAL_PERMUTATION\s+(true|false)',raw):
  t=tuple(ast.literal_eval(ids));rank=len(t);ty=ast.literal_eval(typ);assert len(ty)==rank-1 and t not in printed[rank];printed[rank][t]=(int(o),ty,dual=='true')
 for rank in ranktuples:assert ranktuples[rank]==set(printed[rank])
 byrank={rank:sum(o==order for o,ty,d in printed[rank].values()) for rank in printed}
 assert {k:v for k,v in byrank.items() if v}==expected[n],(n,byrank,expected[n])
 validated={int(k):int(c) for k,c in re.findall(r'VALIDATED_RANK (\d+) ALTERNATING (\d+)',vs)};assert validated==byrank
 final=re.search(r'ALL_RECORDS_FULL_SUBSET_IP_PASS DEGREE (\d+) TOTAL (\d+) ALTERNATING (\d+)',vs);assert tuple(map(int,final.groups()))==(n,sum(map(len,ranktuples.values())),sum(byrank.values()))
 rows.append({'degree':n,'rank_limit':limit,'involutions':involcount,'all_transitive_records':sum(map(len,ranktuples.values())),'alternating_records':sum(byrank.values()),'all_source_cells_and_unlisted_zeros_agree':True,'source_table':expected[n],'records_reconstructed_byte_exact':True,'census_report_sha256':sha(D/'report.json'),'validation_report_sha256':sha(V/'report.json'),'raw_sha256':sha(D/'stdout.log'),'all_pins_current':True,'stderr_empty':True})
report={'status':'PASS_INDEPENDENT_RECEIPT_AND_LITERAL_ASSEMBLY_REVIEW','rows':rows,'source_table_cells':sum(map(len,expected.values())),'full_censuses_not_repeated':True,'full_subset_IP_executions_retained_not_repeated':True,'whole_original_credit':0};(W/'receipt_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
