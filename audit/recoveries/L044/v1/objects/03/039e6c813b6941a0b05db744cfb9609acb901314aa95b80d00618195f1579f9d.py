import json

def check_case(a,b,eta,kind):
 names=[f'{c}{j}{e}' for c,k in [('A',a),('B',b)] for e in ['',"p"] for j in range(k)]
 def permutation(pairs):
  p={x:x for x in names}
  for u,v in pairs:p[u],p[v]=p[v],p[u]
  return p
 def mul(*gs):
  p={x:x for x in names}
  for g in gs:p={x:g[p[x]] for x in names}
  return p
 def power(g,n):return mul(*([g]*n))
 tau=permutation([(f'{c}{j}',f'{c}{j}p') for c,k in [('A',a),('B',b)] for j in range(k)])
 p=permutation([('B1','B2'),('B1p','B2p')]);c=permutation([('A0','A1'),('A0p','A1p')])
 if b==4:
  x=permutation([('B1','B2') if eta==0 else ('B1p','B2p'),('B0p','B3p')])
  s=permutation([('A0','B0')]+[(f'A{j}',f'A{j}p') for j in range(1,a)])
  w=mul(s,power(mul(tau,s,x),5),tau,x);label='four'
 else:
  x=permutation([('B1','B2'),('B0p','B1p')])
  if a==5:h=[] if eta==0 else [(f'A{j}',f'A{j}p') for j in range(1,a)];parity=1
  else:
   h=[[],[('A1','A2'),('A1p','A2p')],[('A1','A1p'),('A2','A2p')],[('A1','A2p'),('A2','A1p')],[('A1','A2')],[('A1p','A2p')]][kind];parity=int(kind<4)
  s=permutation([('A0','B0')]+h+([('B1','B2')] if parity else []))
  if parity:w=mul(power(mul(c,s,tau,s),3),tau);label='three-main'
  else:w=mul(tau,s,power(mul(tau,x,tau,s,x),3),tau,x);label='three-exception'
 if w!=p:raise ValueError((a,b,eta,kind,label))
 return [a,b,eta,kind,label]
rows=[check_case(4,4,e,0) for e in [0,1]]+[check_case(5,3,e,0) for e in [0,1]]+[check_case(3,3,0,k) for k in range(6)]
print(json.dumps({'status':'PASS','literal_word_cases':rows,'uniform_scope':'Written repeated-row cancellation separately read; finite checks are corroboration only.'},indent=2))
