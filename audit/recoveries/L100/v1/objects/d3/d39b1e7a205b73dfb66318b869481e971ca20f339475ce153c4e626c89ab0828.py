"""Strict inverse of the observed GAP long-string PrintTo framing, not GAP eval."""
import sys
if not __debug__: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import json

WIDTH=4094
def need(ok,why):
    if not ok: raise ValueError(why)
def pairs(rows):
    d={}
    for k,v in rows:
        need(k not in d,'duplicate JSON key'); d[k]=v
    return d
def constant(value): raise ValueError('nonfinite JSON constant '+value)
def frame(payload):
    need(payload.isascii() and b'\n' not in payload and b'\r' not in payload,'one ASCII payload line')
    return b'\\\n'.join(payload[i:i+WIDTH] for i in range(0,len(payload),WIDTH))
def decode(raw):
    need(raw and raw.isascii() and b'\r' not in raw,'nonempty ASCII framed bytes')
    lines=raw.split(b'\n')
    need(lines[-1] and len(lines[-1])<=WIDTH,'final nonempty unbroken segment')
    for line in lines[:-1]:
        need(len(line)==WIDTH+1 and line[-1:]==b'\\','exact fixed-width continuation')
    payload=b''.join(line[:-1] for line in lines[:-1])+lines[-1]
    need(frame(payload)==raw,'exact bytewise framing inverse')
    # The actual 61 files contain no escaped JSON characters. GAP may move a
    # continuation before a backslash, so do not generalize this fixed framing.
    need(b'\\' not in payload,'narrow unescaped scientific JSON payload')
    value=json.loads(payload,object_pairs_hook=pairs,parse_constant=constant)
    need(isinstance(value,dict),'scientific JSON object')
    return payload,value
