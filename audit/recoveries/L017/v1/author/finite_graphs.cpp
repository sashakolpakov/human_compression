// Exact finite-field/coset construction for the L017 current recovery.
// Every check remains active in optimized builds.
#include <algorithm>
#include <array>
#include <stdexcept>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>
using M=std::array<int,4>; using U=std::uint64_t;
void require(bool condition){if(!condition)throw std::runtime_error("finite construction invariant failed");}
struct Field {
 int p,e,Q;std::vector<int> polynomial,add,mul,neg,inv,powers,logs;
 Field(int pp,std::vector<int> poly):p(pp),e(int(poly.size())-1),polynomial(poly){
  Q=1;for(int i=0;i<e;i++)Q*=p;
  add.resize(Q*Q);mul.resize(Q*Q);neg.resize(Q);inv.resize(Q);logs.assign(Q,-1);
  std::vector<std::vector<int>> digits(Q,std::vector<int>(e));
  for(int a=0;a<Q;a++){int n=a;for(int i=0;i<e;i++){digits[a][i]=n%p;n/=p;}}
  for(int a=0;a<Q;a++)for(int b=0;b<Q;b++){
   int value=0,place=1;for(int i=0;i<e;i++){value+=((digits[a][i]+digits[b][i])%p)*place;place*=p;}add[a*Q+b]=value;
   std::vector<int> c(2*e-1,0);for(int i=0;i<e;i++)for(int j=0;j<e;j++)c[i+j]=(c[i+j]+digits[a][i]*digits[b][j])%p;
   for(int k=2*e-2;k>=e;k--)for(int j=0;j<e;j++)c[k-e+j]=(c[k-e+j]-c[k]*polynomial[j]%p+p)%p;
   value=0;place=1;for(int i=0;i<e;i++){value+=c[i]*place;place*=p;}mul[a*Q+b]=value;
  }
  for(int a=0;a<Q;a++)for(int b=0;b<Q;b++)if(A(a,b)==0)neg[a]=b;
  int z=1;for(int n=0;n<Q-1;n++){require(logs[z]<0);logs[z]=n;powers.push_back(z);z=P(z,p);}require(z==1);
  for(int a=1;a<Q;a++)inv[a]=powers[(Q-1-logs[a])%(Q-1)];
 }
 int A(int a,int b)const{return add[a*Q+b];}int P(int a,int b)const{return mul[a*Q+b];}
 int pow(int a,int n)const{if(!a)return n?0:1;return powers[(std::int64_t(logs[a])*n)%(Q-1)];}
 M I()const{return {1,0,0,1};}
 M mm(M a,M b)const{return {A(P(a[0],b[0]),P(a[1],b[2])),A(P(a[0],b[1]),P(a[1],b[3])),A(P(a[2],b[0]),P(a[3],b[2])),A(P(a[2],b[1]),P(a[3],b[3]))};}
 M mi(M a)const{int d=A(P(a[0],a[3]),neg[P(a[1],a[2])]);require(d);int v=inv[d];return {P(v,a[3]),P(v,neg[a[1]]),P(v,neg[a[2]]),P(v,a[0])};}
 M minus(M a)const{for(auto&v:a)v=neg[v];return a;}
 M sig(M a,int q)const{for(auto&v:a)v=pow(v,q);return a;}
 U code(M a)const{U n=0;for(auto v:a)n=n*Q+v;return n;}
 M decode(U n)const{M a;for(int i=3;i>=0;i--){a[i]=n%Q;n/=Q;}return a;}
 int order(M a)const{M b=I();for(int n=1;n<=2*(Q+1);n++){b=mm(b,a);if(b==I())return n;}return -1;}
};
void matrix(std::ostream&o,M a){o<<"[["<<a[0]<<","<<a[1]<<"],["<<a[2]<<","<<a[3]<<"]]";}
void pairs(std::ostream&o,const std::set<std::pair<int,int>>& es){o<<"[";bool first=true;for(auto [i,j]:es){if(!first)o<<",";first=false;o<<"["<<i<<","<<j<<"]";}o<<"]";}
void run(int q,int p,std::vector<int> poly,std::array<int,4> seedlogs){
 Field f(p,poly);int Q=f.Q;require(Q==q*q*q);M J={0,1,f.neg[1],0};
 std::vector<int> base;for(int x=0;x<Q;x++)if(f.pow(x,q)==x)base.push_back(x);require(int(base.size())==q);
 std::vector<M> PGL,H,C;std::map<U,M> sols;
 for(int a:base)if(a)for(int b:base)PGL.push_back({a,b,0,1});
 for(int a:base)for(int b:base)for(int d:base)if(f.P(a,d)!=b)PGL.push_back({a,b,1,d});
 for(M g:PGL){M j=f.mm(f.mi(g),f.mm(J,g));if(j==J||j==f.minus(J))C.push_back(g);}
 for(int a:base)if(a)for(int b:base)for(int c:base)H.push_back({a,b,c,f.P(f.A(1,f.P(b,c)),f.inv[a])});
 for(int b:base)if(b)for(int d:base)H.push_back({0,b,f.neg[f.inv[b]],d});
 if(p==2){
  for(int t=1;t<Q;t++)if(f.A(t,f.A(f.pow(t,q),f.pow(t,q*q)))==0){
   M R={1,t,0,1};sols[f.code(R)]=R;
   for(int x:base){M g={x,1,1,0};M r=f.mm(g,f.mm(R,f.mi(g)));sols[f.code(r)]=r;}
  }
 }else{
  M seed;for(int i=0;i<4;i++)seed[i]=seedlogs[i]<0?0:f.powers[seedlogs[i]];
  for(M g:PGL){M r=f.mm(f.mi(g),f.mm(seed,g));sols[f.code(r)]=r;}
 }
 std::set<U> unseen;for(auto [key,r]:sols)unseen.insert(key);std::vector<M> reps;
 while(!unseen.empty()){
  M r=sols.at(*unseen.begin());reps.push_back(r);std::vector<M> todo={r};std::set<U> orbit={f.code(r)};
  for(std::size_t n=0;n<todo.size();n++){
   M s=f.sig(todo[n],p);if(orbit.insert(f.code(s)).second)todo.push_back(s);
   for(M g:C){s=f.mm(f.mi(g),f.mm(todo[n],g));if(orbit.insert(f.code(s)).second)todo.push_back(s);}
  }
  for(U key:orbit){require(sols.count(key));unseen.erase(key);}
 }
 require(sols.size()==std::size_t(p==2?(q+1)*(q*q-1):q*(q*q-1)));
 for(auto [key,r]:sols){
  require(f.mm(r,r)==f.minus(f.I()));require(f.sig(r,q*q)==f.mm(r,f.sig(r,q)));
 }
 std::ofstream orbitout("orbits_q"+std::to_string(q)+".json");
 orbitout<<"{\"q\":"<<q<<",\"solutions\":"<<sols.size()<<",\"centralizer_order\":"<<C.size()<<",\"representatives\":[";
 for(std::size_t i=0;i<reps.size();i++){if(i)orbitout<<",";matrix(orbitout,reps[i]);}orbitout<<"]}\n";
 std::cout<<"q="<<q<<" solutions="<<sols.size()<<" centralizer="<<C.size()<<" representatives="<<reps.size()<<std::endl;
 for(std::size_t ri=0;ri<reps.size();ri++){
  if((q==4 && ri!=0) || (q==5 && ri!=3 && ri!=4) || (q==9 && ri!=0))continue;
  M R=reps[ri],S=f.sig(R,q);require(f.mm(R,R)==f.minus(f.I()));require(f.sig(R,q*q)==f.mm(R,S));
  M rot=f.mm(R,J);int o=f.order(rot);require(o>0);
  int m=o;M rr=f.I();for(int n=1;n<=o;n++){rr=f.mm(rr,rot);if(rr==f.I()||rr==f.minus(f.I())){m=n;break;}}
  if(m<=2){std::cout<<"skip degenerate "<<ri<<" m="<<m<<std::endl;continue;}
  std::map<U,M> hmap,vmap;rr=f.I();
  for(int n=0;n<o;n++){
   hmap[f.code(rr)]=rr;hmap[f.code(f.minus(rr))]=f.minus(rr);
   M r=f.mm(R,rr);hmap[f.code(r)]=r;hmap[f.code(f.minus(r))]=f.minus(r);
   rr=f.mm(rr,rot);
  }
  for(M v:{f.I(),R,S,f.mm(R,S)}){vmap[f.code(v)]=v;vmap[f.code(f.minus(v))]=f.minus(v);}
  std::vector<M> verts;std::unordered_map<U,int> dict;dict.reserve(2*H.size()*hmap.size());
  for(M h:H)for(M g:{h,f.mm(S,h)})if(!dict.count(f.code(g))){
   int index=verts.size();verts.push_back(g);for(auto [_,a]:hmap){U key=f.code(f.mm(a,g));auto [it,ok]=dict.emplace(key,index);require(ok||it->second==index);}
  }
  std::set<std::pair<int,int>> edges,fixed;std::set<U> edgekeys,fixedkeys;
  for(int i=0;i<int(verts.size());i++){
   rr=f.I();for(int n=0;n<m;n++){
    M g=f.mm(rr,verts[i]);rr=f.mm(rr,rot);auto it=dict.find(f.code(f.mm(S,g)));if(it==dict.end())continue;
    int j=it->second;require(i!=j);
    auto pair=std::minmax(i,j);U key=~U(0);for(auto [_,v]:vmap)key=std::min(key,f.code(f.mm(v,g)));
    if(vmap.count(f.code(f.mm(f.sig(g,q),f.mi(g))))){fixed.insert(pair);fixedkeys.insert(key);}else{edges.insert(pair);edgekeys.insert(key);}
   }
  }
  require(edges.size()==edgekeys.size());require(fixed.size()==fixedkeys.size());
  std::map<int,int> deg;for(int i=0;i<int(verts.size());i++){int d=0;for(auto [a,b]:edges)if(a==i||b==i)d++;deg[d]++;}
  std::cout<<"rep="<<ri<<" m="<<m<<" vertices="<<verts.size()<<" edges="<<edges.size()<<" fixed="<<fixed.size()<<" deg=";for(auto [a,b]:deg)std::cout<<a<<":"<<b<<" ";std::cout<<std::endl;
  std::ofstream out("graph_q"+std::to_string(q)+"_r"+std::to_string(ri)+".json");
  out<<"{\"q\":"<<q<<",\"p\":"<<p<<",\"polynomial\":[";for(std::size_t i=0;i<poly.size();i++){if(i)out<<",";out<<poly[i];}
  out<<"],\"representative\":"<<ri<<",\"m\":"<<m<<",\"matrix_order\":"<<o<<",\"R\":";matrix(out,R);out<<",\"R_log\":[";
  for(int i=0;i<4;i++){if(i)out<<",";out<<f.logs[R[i]];}out<<"],\"absolute\":"<<verts.size()<<",\"edges\":";pairs(out,edges);out<<",\"fixed\":";pairs(out,fixed);out<<"}\n";
 }
}
int main(){
 run(2,2,{1,1,0,1},{});run(4,2,{1,1,0,1,1,0,1},{});
 run(5,5,{3,3,0,1},{1,16,117,63});run(7,7,{4,0,6,1},{57,38,190,228});
 run(9,3,{2,2,1,0,2,0,1},{28,224,0,392});
}
