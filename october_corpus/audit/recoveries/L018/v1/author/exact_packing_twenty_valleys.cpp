// Bounded independent skyline exhaustion; UNKNOWN on deadline, never exclusion.
// Every shape is an unordered pair of integer dimensions; rotations share one bit.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
struct Shape{int a,b;};struct Seg{int x,y;};
int W,H,R,A;vector<Shape>S;uint64_t nodes=0;bool stopped=false;double seconds;chrono::steady_clock::time_point start;
vector<array<int,5>> placement;
struct Config{int omit,mx,px,py;};vector<Config> configs;vector<int> oddIndex;vector<int> weights;
uint64_t allconfigs;
void make_configs(){
 oddIndex.assign(S.size(),-1);
 for(int i=0;i<(int)S.size();++i)if((S[i].a&1)||(S[i].b&1)){oddIndex[i]=weights.size();weights.push_back(((S[i].a&1)?S[i].b:S[i].a)/16);}
 if(weights.size()!=9||S.size()!=22)throw runtime_error("wrong special roster");
 vector<vector<int>> signs(512);
 for(int m=0;m<512;++m){int total=0;for(int j=0;j<9;++j)if(m>>j&1)total+=weights[j];if(total&1)continue;
  int x=m;while(true){int sum=0;for(int j=0;j<9;++j)if(x>>j&1)sum+=weights[j];if(2*sum==total)signs[m].push_back(x);if(x==0)break;x=(x-1)&m;}
 }
 for(int omit=0;omit<9;++omit){int sel=511^(1<<omit);for(int mx=sel;;mx=(mx-1)&sel){
   // Quarter-turn symmetry makes at least four odd widths horizontal.
   if(__builtin_popcount((unsigned)mx)>=4)for(int px:signs[mx])for(int py:signs[sel^mx])configs.push_back({omit,mx,px,py});
   if(mx==0)break;
  }}
 if(configs.size()!=26)throw runtime_error("wrong coloring configuration count");
 allconfigs=(uint64_t(1)<<configs.size())-1;
}
uint64_t restrict_config(uint64_t mask,int j,int x,int y,int wi,int hi){
 if(j<0)return mask;uint64_t ans=0;
 while(mask){int c=__builtin_ctzll(mask);mask&=mask-1;auto k=configs[c];if(j==k.omit)continue;
  bool horizontal=(k.mx>>j)&1;if(horizontal!=(bool)(wi&1))continue;
  int parity=horizontal?((k.px>>j)&1):((k.py>>j)&1);
  if(parity!=((horizontal?x:y)&1))continue;ans|=uint64_t(1)<<c;
 }
 return ans;
}
bool side_possible(int target,int transverse,uint64_t used,bool vertical){
 if(target==0)return true;uint64_t bits[17]={1};
 for(int i=0;i<(int)S.size();++i)if(!(used>>i&1)){
  uint64_t old[17];copy(begin(bits),end(bits),old);
  for(int o=0;o<2;++o){int d=o?S[i].b:S[i].a,e=o?S[i].a:S[i].b;if(d>target||e>transverse||(o&&S[i].a==S[i].b))continue;
   int words=d/64,shift=d%64;for(int k=target/64;k>=words;--k){uint64_t v=old[k-words]<<shift;if(shift&&k>words)v|=old[k-words-1]>>(64-shift);bits[k]|=v;}
  }
 }
 return (bits[target/64]>>(target%64)&1)!=0;
}
bool search(const vector<Seg>&p,uint64_t used,int depth,int first,uint64_t cm){
 ++nodes;if((nodes&65535)==0 && chrono::duration<double>(chrono::steady_clock::now()-start).count()>seconds){stopped=true;return false;}
 if(depth==R)return p.size()==1 && p[0].y==H;
 // Every strict valley has both neighboring covered heights larger, or a
 // container wall. Its lowest uncovered cell forces a rectangle starting at
 // its left endpoint and exact height. Choose the fewest feasible choices.
 int idx=-1,best=1000000;
 for(int j=0;j<(int)p.size();++j){
  if(p[j].y==H||(j&&p[j-1].y<p[j].y)||(j+1<(int)p.size()&&p[j+1].y<p[j].y))continue;
  int gap=(j+1==(int)p.size()?W:p[j+1].x)-p[j].x,c=0;
  for(int i=0;i<(int)S.size();++i)if(!(used>>i&1))for(int o=0;o<2;++o){
   int wi=o?S[i].b:S[i].a,hi=o?S[i].a:S[i].b;
   if(o&&S[i].a==S[i].b)continue;
   if(wi<=gap&&hi<=H-p[j].y)++c;
  }
  if(!c)return false;
  if(c<best){idx=j;best=c;}
 }
 if(idx<0)return false;
 int x=p[idx].x,y=p[idx].y,edge=(idx+1==(int)p.size()?W:p[idx+1].x),gap=edge-x;
 // Uncovered left and right boundary lengths must be sums of heights
 // of distinct unused shapes. This is necessary even before their positions
 // or orientations are selected; no rotation-list reversal is used.
 if(!side_possible(H-p.front().y,W,used,true))return false;
 if(p.back().y!=p.front().y&&!side_possible(H-p.back().y,W,used,true))return false;
 // Every component separated by a full-height column has area a multiple of A.
 int comp=0;
 for(int i=0;i<(int)p.size();++i){int nx=i+1==(int)p.size()?W:p[i+1].x;if(p[i].y==H){if(comp%A)return false;comp=0;}else comp+=(nx-p[i].x)*(H-p[i].y);}if(comp%A)return false;
 // The complete exposed minimum plateau is tiled along its base by distinct
 // remaining shapes. A bitset subset sum is a necessary condition only.
 uint64_t bits[17]={1}; // W<=1000
 for(int i=0;i<(int)S.size();++i)if(!(used>>i&1)){
  uint64_t old[17];copy(begin(bits),end(bits),old);
  for(int o=0;o<2;++o){int wi=o?S[i].b:S[i].a,hi=o?S[i].a:S[i].b;if(wi>gap || hi>H-y || (o && S[i].a==S[i].b))continue;
   int words=wi/64,shift=wi%64;
   for(int k=(gap/64);k>=words;--k){uint64_t v=old[k-words]<<shift;if(shift && k>words)v|=old[k-words-1]>>(64-shift);bits[k]|=v;}
  }
 }
 if(!(bits[gap/64]>>(gap%64)&1))return false;
 for(int i=0;i<(int)S.size();++i)if(!(used>>i&1))for(int o=0;o<2;++o){
  int wi=o?S[i].b:S[i].a,hi=o?S[i].a:S[i].b;if(o && S[i].a==S[i].b)continue;
  if(wi>gap || y+hi>H)continue;
  // The color-axis choice replaces corner diagonal normalization.
  uint64_t nextcm=restrict_config(cm,oddIndex[i],x,y,wi,hi);if(!nextcm)continue;
  // Choose the least unordered corner identity at bottom left using D4.
  // Equality permits a rectangle spanning two corners.
  if(W==H && depth && ((x+wi==W&&y==0)||(x==0&&y+hi==H)||(x+wi==W&&y+hi==H)) && i<first)continue;
  vector<Seg> q;for(int j=0;j<idx;++j)q.push_back(p[j]);q.push_back({x,y+hi});if(x+wi<edge)q.push_back({x+wi,y});for(int j=idx+1;j<(int)p.size();++j)q.push_back(p[j]);
  vector<Seg> merged;for(auto z:q)if(merged.empty()||merged.back().y!=z.y)merged.push_back(z);
  placement.push_back({i,x,y,wi,hi});if(search(merged,used|(uint64_t(1)<<i),depth+1,depth?first:i,nextcm))return true;placement.pop_back();if(stopped)return false;
 }
 return false;
}
int main(int argc,char**argv){if(argc!=5)return 2;W=stoi(argv[1]);H=stoi(argv[2]);R=stoi(argv[3]);seconds=stod(argv[4]);if(W<1||W>1000||H<1||H>1000||R<2||W*H%R)return 3;A=W*H/R;if(W!=840||H!=840||R!=20)return 5;
 for(int a=1;a*a<=A;++a)if(A%a==0){int b=A/a;if((a<=W&&b<=H)||(b<=W&&a<=H))S.push_back({a,b});}if(S.size()>63)return 4;
 make_configs();start=chrono::steady_clock::now();bool found=search({{0,0}},0,0,-1,allconfigs);double elapsed=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cout<<"{\"width\":"<<W<<",\"height\":"<<H<<",\"pieces\":"<<R<<",\"shapes\":"<<S.size()<<",\"nodes\":"<<nodes<<",\"seconds\":"<<elapsed<<",\"status\":\""<<(found?"FEASIBLE":stopped?"UNKNOWN":"INFEASIBLE")<<"\",\"placement\":[";
 for(size_t j=0;j<placement.size();++j){if(j)cout<<',';auto z=placement[j];cout<<'['<<z[0]<<','<<z[1]<<','<<z[2]<<','<<z[3]<<','<<z[4]<<']';}cout<<"]}\n";
}
