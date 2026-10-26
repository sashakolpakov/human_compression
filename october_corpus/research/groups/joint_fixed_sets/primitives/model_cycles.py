"""Typed prefix decoder for the WHOLE pinned historical model; no GAP Eval.

The exact old recipe prints G:=Group([perm1,perm2]);; before A/metadata.
The remaining already-whole-authenticated bytes stay opaque and unexecuted.
No model body was opened to assemble this Source. Any format mismatch refuses.
"""
from array import array
import re
SPACE=re.compile(r'(?:[ \t\r\n]|\\\r?\n)*')
DECIMAL=re.compile(r'[1-9][0-9]*')


def need(ok,why):
    if not ok:raise ValueError(why)


class Cursor:
    def __init__(self,raw):
        need(type(raw)is bytes and len(raw)<=16*2**20,'bounded whole model bytes')
        self.text=raw.decode('ascii');self.at=0

    def space(self):
        self.at=SPACE.match(self.text,self.at).end()

    def token(self,value):
        self.space();need(self.text.startswith(value,self.at),'literal token '+value)
        self.at+=len(value)

    def peek(self):
        self.space();return self.text[self.at:self.at+1]

    def integer(self,degree):
        self.space();m=DECIMAL.match(self.text,self.at)
        need(m is not None,'positive typed decimal cycle label')
        value=int(m.group());need(1<=value<=degree,'cycle label domain')
        self.at=m.end();return value


def permutation(cursor,degree,budget):
    need(type(degree)is int and 1<=degree<=37449,'literal model degree')
    budget.charge(degree);images=array('I',range(1,degree+1));seen=bytearray(degree+1)
    cycles=0
    while cursor.peek()=='(':
        cursor.token('(')
        if cursor.peek()==')':
            need(cycles==0,'identity is the entire permutation');cursor.token(')')
            need(cursor.peek()!='(','no redundant empty cycle');return images
        cycle=[cursor.integer(degree)]
        while cursor.peek()==',':cursor.token(',');cycle.append(cursor.integer(degree))
        cursor.token(')');need(len(cycle)>=2,'nontrivial printed cycle')
        budget.charge(len(cycle))
        for x in cycle:need(not seen[x],'disjoint cycles without repeated labels');seen[x]=1
        for x,y in zip(cycle,cycle[1:]+cycle[:1]):images[x-1]=y
        cycles+=1
    need(cycles>0,'printed permutation required');budget.charge(0);return images


def decode_model(raw,degree,budget):
    """Caller MUST verify the exact entire old model pin before/after this call."""
    c=Cursor(raw)
    for token in ['G',':=','Group','(','[']:c.token(token)
    left=permutation(c,degree,budget);c.token(',');right=permutation(c,degree,budget)
    for token in [']',')',';',';']:c.token(token)
    c.space();need(c.at<len(c.text)and c.text.startswith('A',c.at),'retained opaque A suffix exists')
    budget.charge(0)
    return [left,right],dict(schema='F004_TYPED_ORIGINAL_MODEL_PREFIX_V1',
        degree=degree,ordered_generators=2,prefix_end=c.at,whole_model_was_required=True,
        opaque_remaining_bytes_not_executed=True,Read_Eval_Group_calls=0)
