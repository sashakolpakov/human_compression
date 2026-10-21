#!/usr/bin/env python3
"""Exercise literal C++ color filters independently of packing exhaustion."""
import argparse,json,subprocess
from pathlib import Path
from coloring_certificate import derive

def run(out):
 root=Path(__file__).resolve().parent;out.mkdir(parents=True,exist_ok=True)
 c20='''#define main saved_search_main
#include "exact_packing_twenty_valleys.cpp"
#undef main
int main(){W=840;H=840;R=20;A=W*H/R;for(int a=1;a*a<=A;++a)if(A%a==0){int b=A/a;if(b<=840)S.push_back({a,b});}make_configs();cout<<"[";bool first=true;for(auto c:configs){if(!first)cout<<",";first=false;cout<<"["<<c.omit<<","<<c.mx<<","<<c.px<<","<<c.py<<"]";}cout<<"]\\n";}
'''
 c21='''#define main saved_search_main
#include "exact_packing_odd_valleys.cpp"
#undef main
int main(){W=840;H=840;R=21;int pass=0,reject=0;for(int k=0;k<6;++k)for(int off: {0,2,64})for(int bit=0;bit<2;++bit){placement.clear();for(int j=0;j<4;++j){int x=bit^((j==1||j==2)?1:0);placement.push_back({j,x,off+64*pat[k][j],oddW[j],oddH[j]});}if(!odd_possible({{0,0}}))return 11;++pass;placement[0][1]^=1;if(odd_possible({{0,0}}))return 12;++reject;placement[0][1]^=1;placement[0][2]+=2;if(odd_possible({{0,0}}))return 13;++reject;}cout<<"["<<pass<<","<<reject<<"]\\n";}
'''
 got=[]
 for n,src in [('twenty',c20),('twenty_one',c21)]:
  f=out/(n+'.cpp');f.write_text(src);exe=out/n
  subprocess.run(['clang++','-O3','-std=c++17','-include','array','-I',str(root),str(f),'-o',str(exe)],check=True,capture_output=True,text=True)
  got.append(json.loads(subprocess.check_output([str(exe)],text=True,timeout=10)))
 expected=derive()
 if sorted(map(tuple,got[0]))!=list(map(tuple,expected['rotation26'])):raise ValueError('literal C++ color list differs')
 if got[1]!=[36,72]:raise ValueError('literal endpoint control count differs')
 report={'status':'PASS_BOUNDED_LITERAL_FILTER_VALIDATION','cpp20_configurations':26,'cpp21_positive_endpoint_configurations':36,'cpp21_rejected_mutations':72,'scope':'The entire C++ sources are included unchanged under renamed entry points; these checks do not replace the finite exhaustive searches.'}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();print(run(a.out))
