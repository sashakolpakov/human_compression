#!/usr/bin/env python3
"""Exact positive collection system for the proposed uniform label-eight group."""
from functools import lru_cache
from itertools import combinations_with_replacement
import argparse,hashlib,json,time
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)

class Collector:
    def __init__(self,d):
        require(type(d) is int and d>=3,'rank at least three required')
        self.d=d
        self.letters=tuple((kind,i) for kind,length in [('r',1),('x',2),('y',3),('z',4),('w',2)] for i in range(d-length+1))
        self.position={v:i for i,v in enumerate(self.letters)}
        lengths={'r':1,'x':2,'y':3,'z':4,'w':2}
        self.support=tuple(frozenset(range(i,i+lengths[kind])) for kind,i in self.letters)
        self.rules={}
        for a,(kind,i) in enumerate(self.letters):
            self.rules[a,a]=(self.position['w',i],) if kind=='x' else ()
            for b,(kind2,j) in enumerate(self.letters[:a]):
                tail=[]
                if kind==kind2=='r' and i==j+1:tail=[('x',j),('w',j)]
                elif kind=='x' and kind2=='r':
                    if j==i or j==i+1:tail=[('w',i)]
                    elif j==i+2:tail=[('y',i)]
                    elif j==i-1:tail=[('y',j),('w',j),('w',i)]
                elif kind==kind2=='x':
                    if i==j+1:tail=[('w',j),('w',i)]
                    elif i==j+2:tail=[('z',j)]
                elif kind=='y' and kind2=='r':
                    if j==i-1:tail=[('z',j)]
                    elif j==i+1:tail=[('w',i),('w',i+1)]
                    elif j==i+3:tail=[('z',i)]
                self.rules[a,b]=(b,a)+tuple(self.position[v] for v in tail)
        self.normalize=lru_cache(maxsize=None)(self._normalize)
        self.steps=0
    def _normalize(self,word):
        word=tuple(word)
        while True:
            for k in range(len(word)-1):
                if word[k]>=word[k+1]:
                    word=word[:k]+self.rules[word[k],word[k+1]]+word[k+2:]
                    self.steps+=1
                    break
            else:return word
    def product(self,*words):return self.normalize(sum((tuple(w) for w in words),()))
    def power(self,word,n):return self.normalize(tuple(word)*n)
    def symbol(self,kind,i):return (self.position[kind,i],)
    def inverse(self,word):
        out=()
        for a in reversed(word):out+=self.rules[a,a]+(a,)
        return self.normalize(out)
    def commutator(self,a,b):return self.product(self.inverse(a),self.inverse(b),a,b)
    def verify_rules(self):
        for (a,b),rhs in self.rules.items():
            if a==b:
                require(all(c>a for c in rhs),'Power rule is not triangular')
            else:
                require(rhs[:2]==(b,a) and all(c>a for c in rhs[2:]),'Swap rule is not triangular')
            union=self.support[a]|self.support[b]
            require(all(self.support[c]<=union for c in rhs),'Rule creates unsupported coordinates')
            if a!=b and rhs[2:]:
                require(max(union)-min(union)+1==len(union),'Nontrivial correction crosses a support gap')
            def parity(word):
                value=0
                for c in word:
                    kind,index=self.letters[c]
                    if kind=='r':value^=1<<index
                return value
            require(parity((a,b))==parity(rhs),'Rule changes distinguished parity coordinates')
        return len(self.rules)
    def critical_pairs(self):
        count=0;digest=hashlib.sha256()
        for c,b,a in combinations_with_replacement(range(len(self.letters)),3):
            left=self.normalize(self.rules[a,b]+(c,))
            right=self.normalize((a,)+self.rules[b,c])
            require(left==right,'Critical pair failed: '+str((self.letters[a],self.letters[b],self.letters[c],left,right)))
            digest.update(json.dumps([a,b,c,left],separators=(',',':')).encode()+b'\n');count+=1
        require(count==len(self.letters)*(len(self.letters)+1)*(len(self.letters)+2)//6,'Incomplete critical-pair traversal')
        return count,digest.hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();require(not args.report.exists() and not args.report.is_symlink(),'Fresh report required')
    start=time.monotonic();C=Collector(14);rules=C.verify_rules();count,digest=C.critical_pairs()
    local=Collector(3);r=[local.symbol('r',i) for i in range(3)]
    A=r[0]+r[1];B=r[1]+r[2]
    basis_definitions=0
    for i in range(13):
        require(C.commutator(C.symbol('r',i),C.symbol('r',i+1))==C.symbol('x',i),'Uniform edge definition failed')
        require(C.power(C.symbol('x',i),2)==C.symbol('w',i),'Uniform square definition failed')
        basis_definitions+=2
    for i in range(12):
        require(C.commutator(C.symbol('x',i),C.symbol('r',i+2))==C.symbol('y',i),'Uniform triple definition failed')
        basis_definitions+=1
    for i in range(11):
        require(C.commutator(C.symbol('y',i),C.symbol('r',i+3))==C.symbol('z',i),'Uniform quadruple definition failed')
        basis_definitions+=1
    relators=[]
    for k in range(8):
        word=B*k+A*k;value=local.power(word,2);require(value==(),'Source power relation failed');relators.append({'k':k,'inner_normal_form':[local.letters[a] for a in local.normalize(word)],'squared_normal_form':value})
    for i in range(2):
        x=local.symbol('x',i);w=local.symbol('w',i)
        require(local.commutator(r[i],r[i+1])==x,'Actual edge commutator differs')
        require(local.power(x,2)==w and local.power(x,4)==(),'Exact order-four edge coordinate failed')
        require(local.power(r[i]+r[i+1],4)==w and local.power(r[i]+r[i+1],8)==(),'Exact adjacent order eight failed')
    y=local.symbol('y',0);require(local.commutator(local.symbol('x',0),r[2])==y,'Triple commutator differs')
    fourth=local.commutator(y,r[1]);require(fourth==local.symbol('w',0)+local.symbol('w',1),'Class-four witness differs')
    result={'status':'PASS','rank_for_complete_critical_pair_check':14,'basis_letters':len(C.letters),'collection_rules':rules,'overlapping_critical_pairs':count,'critical_normal_forms_sha256':digest,'all_rules_triangular':True,'all_rules_preserve_union_of_supports':True,'all_nontrivial_commutation_corrections_have_connected_input_union':True,'distinguished_parity_coordinates_preserved':True,'basis_definitions_checked':basis_definitions,'rank_three_source_relators':relators,'source_word_normal_forms_sha256':hashlib.sha256(json.dumps(relators,separators=(',',':')).encode()).hexdigest(),'class_four_nonzero_normal_form':[local.letters[a] for a in fourth],'seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'uniform_inference_requires_written_termination_locality_confluence_proof':True}
    with args.report.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
