"""Exact packed earlier-parent tree encoding; no field arithmetic or search."""
import base64
import field as f
TARGET=9241

def put(raw,parent,label):
    raw.extend((parent&255,parent>>8,label))

def encode(raw,n):
    f.need(len(raw)==3*n,'whole tree extent')
    return dict(n=n,parent_tree_b64=base64.b64encode(raw).decode('ascii'))

def parse(cert,target):
    f.need(type(target)is int and 1<=target<=TARGET,'bounded reviewed target')
    f.need(type(cert)is dict and set(cert)=={'n','parent_tree_b64'}and
           type(cert['n'])is int and cert['n']==target,'exact required reachability size')
    text=cert['parent_tree_b64']
    f.need(type(text)is str and len(text)==4*target and text.isascii(),'exact packed base64 extent')
    raw=base64.b64decode(text,validate=True)
    f.need(len(raw)==3*target and base64.b64encode(raw).decode('ascii')==text and
           raw[:3]==b'\xff\xff\xff','whole canonical tree and single root')
    return raw
