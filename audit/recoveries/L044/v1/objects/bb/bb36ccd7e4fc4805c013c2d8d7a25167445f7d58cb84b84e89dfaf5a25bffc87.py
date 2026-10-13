"""Extract literal permutation tuples from a terminal census output."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def literal(raw, marker):
    if raw.count(marker) != 1:
        raise ValueError('nonunique tuple marker')
    start=raw.index('[',raw.index(marker)+len(marker));depth=0
    for end in range(start,len(raw)):
        if raw[end]=='[':depth+=1
        elif raw[end]==']':depth-=1
        if depth==0:
            result=raw[start:end+1]
            if not re.fullmatch(r'[\s\d,()\[\]]+',result):
                raise ValueError('nonliteral tuple output')
            return result
    raise ValueError('unclosed tuple output')


def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path)
    p.add_argument('output',type=Path);a=p.parse_args();raw=a.source.read_text()
    if raw.count('COMPLETE_EXHAUSTION')+raw.count('COMPLETE_ENDS_EXHAUSTION')!=1:
        raise ValueError('missing unique terminal exhaustion marker')
    ranks=list(map(int,re.findall(r'COMPLETE_TUPLES_RANK_(\d+) ',raw)))
    text='recordedMarks:=[];;\n'
    for rank in ranks:
        text+=f'recordedMarks[{rank}]:='+literal(raw,f'COMPLETE_TUPLES_RANK_{rank} ')+';;\n'
    text+='recordedRanks:='+str(ranks)+';;\n'
    a.output.write_text(text)
    a.output.with_suffix('.json').write_text(json.dumps({'source':str(a.source),
        'source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),
        'ranks':ranks},indent=2)+'\n')


if __name__=='__main__':main()
