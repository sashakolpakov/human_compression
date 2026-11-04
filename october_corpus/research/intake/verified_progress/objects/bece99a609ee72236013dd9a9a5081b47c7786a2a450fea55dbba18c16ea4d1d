"""Shared typed bindings, bank preflight and strict certificate functions."""
import struct
import common as C
import point_kernel as K,subset_kernel as N
PROVIDER={'prepare_triangle':K.prepare_triangle,'rotation_word':K.rotation_word}
def fit(b,refs,operation_units):
    allrefs=dict(b.refs)
    for r in refs:C.ref(r);C.need(allrefs.get(r['path'],r)==r,'one complete prospective edition');allrefs[r['path']]=r
    future=sum(r['bytes']for p,r in allrefs.items()if p not in b.raw)+sum(r['bytes']for r in allrefs.values())
    C.need(b.bytes+future<=8388608 and len(allrefs)+2<=96,'complete prospective closing IO within unchanged bank')
    return b.work.units+future+operation_units+3*81920<=10000000

def binding(raw,row,n,work):
    C.need(type(row)is dict and set(row)=={'free_index','owner','witness_row_sha256'}and type(row['free_index'])is int and 0<=row['free_index']<n and type(row['owner'])is int and 0<=row['owner']<500178,'strict actual row identity')
    record=raw[16*row['free_index']:16*row['free_index']+16];work.charge(128,'whole adopted original witness row and digest');owner,partner,mass,x,y,z=struct.unpack('<IIHHHH',record)
    C.need(owner==row['owner']and C.digest(record)==row['witness_row_sha256']and 0<=partner<500178 and mass==1024 and len({x,y,z})==3 and all(p<3510 for p in(x,y,z)),'exact original owner/partner/mass/triangle row, never owner as H word')
    return(x,y,z)

def kernel_verify(ctx,triangle,record,work):
    C.need(set(record)=={'identity','outcome','prime11','prime13','points'},'complete typed hint result')
    if record['outcome']=='GEN_HINT':
        C.need(record['points']is None,'positive has no negative payload');K.verify_pair(ctx,triangle,dict(prime11=record['prime11'],prime13=record['prime13']),work);return'GEN'
    if record['outcome']=='PROPER_HINT':
        C.need(record['prime11']is record['prime13']is None,'proper has no positive payload');N.check_subset(PROVIDER,ctx,triangle,record['points'],work);return'PROPER'
    C.need(record['outcome']=='INCONCLUSIVE'and record['points']is record['prime11']is record['prime13']is None,'miss preserves all unpaid');return'UNPAID'

