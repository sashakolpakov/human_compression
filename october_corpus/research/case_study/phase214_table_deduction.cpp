// Upper-bound certificate checker.  Unlike a permutation-table check, every
// non-tree edge must be deduced from a literal relator and previously proved
// edges.  A successful COMPLETE result therefore gives an index upper bound.
// No coincidence is assumed from the supplied target table.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
int main(int argc,char**argv){
  try{
    if(argc!=2)throw runtime_error("usage: checker table.txt");
    ifstream in(argv[1]);uint32_t N,d;
    if(!(in>>N>>d)||d<3||d>5||N==0||N>1100000)throw runtime_error("bad header");
    vector<uint32_t> oracle(size_t(N)*d), known(size_t(N)*d,0);
    for(auto &v:oracle){if(!(in>>v)||v<1||v>N)throw runtime_error("bad entry");}
    string extra;if(in>>extra)throw runtime_error("extra input");
    auto at=[d](uint32_t u,uint32_t s){return size_t(u-1)*d+s;};
    uint64_t filled=0;
    auto install=[&](uint32_t u,uint32_t s,uint32_t v){
      if(oracle[at(u,s)]!=v||oracle[at(v,s)]!=u)
        throw runtime_error("deduction disagrees with oracle");
      for(auto p:{make_pair(u,v),make_pair(v,u)}){
        auto &cell=known[at(p.first,s)];
        if(cell&&cell!=p.second)throw runtime_error("inconsistent deduction");
        if(!cell){cell=p.second;++filled;}
      }
    };
    // H=<r_0,...,r_(d-2)> fixes its own right coset.
    for(uint32_t s=0;s+1<d;++s)install(1,s,1);
    // Each tree edge introduces a fresh name for the right coset Hr_u*r_s.
    vector<bool> seen(N+1,false);queue<uint32_t> todo;
    seen[1]=true;todo.push(1);uint32_t introduced=1;
    while(!todo.empty()){
      uint32_t u=todo.front();todo.pop();
      for(uint32_t s=0;s<d;++s){uint32_t v=oracle[at(u,s)];
        if(!seen[v]){seen[v]=true;todo.push(v);++introduced;install(u,s,v);}
      }
    }
    if(introduced!=N)throw runtime_error("target table disconnected");
    vector<vector<uint32_t>> rels;
    for(uint32_t i=0;i<d;++i)for(uint32_t j=i+1;j<d;++j){
      vector<uint32_t> w;uint32_t e=j==i+1?11:2;
      for(uint32_t k=0;k<e;++k){w.push_back(i);w.push_back(j);}rels.push_back(w);
    }
    for(uint32_t i=0;i+2<d;++i)for(uint32_t k=1;k<11;++k){
      vector<uint32_t>w;
      for(int twice=0;twice<2;++twice){
        for(uint32_t j=0;j<k;++j){w.push_back(i+1);w.push_back(i+2);}
        for(uint32_t j=0;j<k;++j){w.push_back(i);w.push_back(i+1);}
      }rels.push_back(w);
    }
    cerr<<"START N="<<N<<" d="<<d<<" tree_filled="<<filled<<"\n";
    uint32_t round=0;
    while(true){uint64_t before=filled;++round;
      for(uint32_t u=1;u<=N;++u)for(const auto&w:rels){
        uint32_t a=u,b=u,l=0,r=w.size();
        while(l<r&&known[at(a,w[l])]){a=known[at(a,w[l])];++l;}
        while(l<r&&known[at(b,w[r-1])]){b=known[at(b,w[r-1])];--r;}
        if(l==r){if(a!=b)throw runtime_error("unproved coincidence required");}
        else if(l+1==r)install(a,w[l],b);
      }
      cerr<<"ROUND "<<round<<" filled="<<filled<<" new="<<filled-before<<"\n";
      if(filled==uint64_t(N)*d){cout<<"COMPLETE index_upper_bound="<<N<<" rank="<<d<<" label=11\n";return 0;}
      if(filled==before){cout<<"INCOMPLETE known="<<filled<<" total="<<uint64_t(N)*d<<"\n";return 2;}
    }
  }catch(const exception&e){cerr<<"REJECT: "<<e.what()<<"\n";return 1;}
}
