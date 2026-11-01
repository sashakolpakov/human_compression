"""Retained bounded finite-permutation primitives; standard library only."""
from array import array
import time

class WorkStop(RuntimeError):pass

def need(ok,why):
    if not ok:raise ValueError(why)

class Meter:
    def __init__(self,bounded,clock=time.monotonic,cap=10000000):
        need(type(cap)is int and 0<cap<=10000000,'test may lower, never raise shared work cap')
        self.bounded,self.clock,self.start=bounded,clock,clock();self.cap=cap
        self.units,self.ledger,self.publication=0,{},None
    def charge(self,n,bucket='structure'):
        need(type(n)is int and n>=0,'strict nonnegative work')
        if n>self.cap-self.units or self.clock()-self.start>=20:raise WorkStop('shared10M/20s exhausted')
        self.units+=n;self.ledger[bucket]=self.ledger.get(bucket,0)+n;self.bounded()
    def proposal(self):
        self.charge(1,'proposal_step')
        if self.units>=6000000 or self.clock()-self.start>=14:raise WorkStop('proposal6M/14s reserve')
    def reserve_publication(self,certificate_bound):
        need(type(certificate_bound)is int and 0<certificate_bound<=2**21,'whole bounded implicit certificate')
        if self.publication is None:
            self.charge(3*certificate_bound+16384,'publication_reserved')
            self.publication=dict(bound=certificate_bound,certificate=3*certificate_bound,spent=0,scalar=16384)
        elif certificate_bound>self.publication['bound']:
            self.charge(3*(certificate_bound-self.publication['bound']),'publication_reserved_growth')
            self.publication['certificate']+=3*(certificate_bound-self.publication['bound'])
            self.publication['bound']=certificate_bound
        self.charge(0)
    def spend_certificate(self,n):
        p=self.publication
        need(p is not None and type(n)is int and n>=0 and n<=p['certificate']-p['spent'],'prepaid certificate encoding/write/hash only')
        self.charge(0);p['spent']+=n
    def final(self,n):
        need(self.publication is not None and type(n)is int and 0<=n<=self.publication['scalar'],'bounded prepaid scalar/stdout')
        self.charge(0)

def identity(n,work):
    work.charge(n,'identity_initialization');return array('H',range(n))

def compose(g,h,work):
    need(len(g)==len(h),'same whole permutation degree');n=len(g)
    work.charge(n,'product_initialization');out=array('H',[0])*n
    for x in range(n):work.charge(3,'product_read_read_write');out[x]=h[g[x]]
    return out

def inverse(g,work):
    n=len(g);work.charge(n,'inverse_initialization');out=array('H',[0])*n
    for x,y in enumerate(g):work.charge(2,'inverse_read_write');out[y]=x
    return out
