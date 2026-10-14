#include <algorithm>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using V=std::vector<int>;
using M=std::vector<V>;
void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
struct Field {
 int q,poly;
 explicit Field(int n):q(n),poly(n==2?3:n==4?7:11){need(n==2||n==4||n==8,"field");}
 int mul(int a,int b)const{int z=0;while(b){if(b&1)z^=a;b>>=1;a<<=1;if(a&q)a^=poly;}return z;}
 int sq(int a)const{return mul(a,a);}
 int trace(int a)const{int z=0;for(int k=q;k>1;k>>=1){z^=a;a=sq(a);}need(z==0||z==1,"trace field");return z;}
};
std::uint64_t pw(std::uint64_t a,int b){std::uint64_t z=1;while(b--)z*=a;return z;}
M identity(int n){M a(n,V(n));for(int i=0;i<n;i++)a[i][i]=1;return a;}
M product(const M&a,const M&b,const Field&f){int n=a.size();M c(n,V(n));for(int i=0;i<n;i++)for(int j=0;j<n;j++)for(int k=0;k<n;k++)c[i][j]^=f.mul(a[i][k],b[k][j]);return c;}
int rank(M a,const Field&f){int n=a.size(),r=0;for(int j=0;j<n;j++){int i=r;while(i<n&&!a[i][j])i++;if(i==n)continue;std::swap(a[i],a[r]);int inv=1;while(f.mul(inv,a[r][j])!=1)inv++;for(int k=j;k<n;k++)a[r][k]=f.mul(a[r][k],inv);for(i=0;i<n;i++)if(i!=r&&a[i][j]){int z=a[i][j];for(int k=j;k<n;k++)a[i][k]^=f.mul(z,a[r][k]);}r++;}return r;}
int rank_minus_identity(M a,const Field&f){for(int i=0;i<(int)a.size();i++)a[i][i]^=1;return rank(a,f);}
int dot(const V&a,const V&b,const Field&f){int z=0;for(int i=0;i<(int)a.size();i++)z^=f.mul(a[i],b[i]);return z;}
int key(const V&a,int q){int z=0;for(int x:a)z=z*q+x;return z;}
V F(const M&d,const Field&f){V z(d.size());for(int i=0;i<(int)d.size();i++){int s=0;for(int x:d[i])s^=x;z[i]=d[i][i]^f.sq(s);}return z;}
template<class Fn>void symmetric(int m,const Field&f,Fn visit){M d(m,V(m));std::vector<std::pair<int,int>> pos;for(int i=0;i<m;i++)for(int j=i;j<m;j++)pos.emplace_back(i,j);std::function<void(int)> walk=[&](int k){if(k==(int)pos.size()){visit(d);return;}auto[i,j]=pos[k];for(int a=0;a<f.q;a++){d[i][j]=d[j][i]=a;walk(k+1);}};walk(0);}
std::vector<M> frames(int m,const Field&f){std::vector<V> vecs;V v(m);std::function<void(int)> fill=[&](int i){if(i==m){if(dot(v,v,f)==1)vecs.push_back(v);return;}for(int x=0;x<f.q;x++){v[i]=x;fill(i+1);}};fill(0);M a;std::vector<M> out;std::function<void()> walk=[&](){if((int)a.size()==m){out.push_back(a);return;}for(const auto&v:vecs){bool ok=true;for(const auto&w:a)if(dot(v,w,f)){ok=false;break;}if(ok){a.push_back(v);walk();a.pop_back();}}};walk();return out;}
std::uint64_t sp_order(int n,int q){need(n%2==0,"symplectic degree");int r=n/2;std::uint64_t z=pw(q,r*r);for(int i=1;i<=r;i++)z*=pw(q,2*i)-1;return z;}
M literal_g(const M&a,const M&d,const Field&f){int m=a.size();auto da=product(d,a,f);M g(2*m,V(2*m));for(int i=0;i<m;i++)for(int j=0;j<m;j++){g[i][j]=g[m+i][m+j]=a[i][j];g[i][m+j]=da[i][j];}return g;}
int quadratic(const V&v,const V&b,const Field&f){int m=b.size(),s=0,z=0;for(int i=0;i<m;i++){s^=v[i];z^=f.mul(v[i],v[m+i])^f.mul(b[i],f.sq(v[m+i]));}return z^f.sq(s);}
int polar(const V&a,const V&b,const Field&f){int m=a.size()/2,z=0;for(int i=0;i<m;i++)z^=f.mul(a[i],b[m+i])^f.mul(a[m+i],b[i]);return z;}
void isometry(const M&g,const V&b,const Field&f){int n=g.size();auto one=identity(n);for(int i=0;i<n;i++){V v(n);for(int k=0;k<n;k++)v[k]=g[k][i];need(quadratic(v,b,f)==quadratic(one[i],b,f),"quadratic basis");for(int j=0;j<n;j++){V w(n);for(int k=0;k<n;k++)w[k]=g[k][j];need(polar(v,w,f)==polar(one[i],one[j],f),"polar basis");}}}
int main(){try{
 std::uint64_t total=0,full=0;int rows=0;
 std::cout<<"{\"status\":\"PASS\",\"fibres\":[";
 for(auto[q,m]:std::vector<std::pair<int,int>>{{2,1},{2,2},{2,3},{2,4},{2,5},{4,1},{4,2},{4,3},{4,4},{8,1},{8,2},{8,3}}){
  Field f(q);int d=m*(m-1)/2;std::map<int,std::uint64_t> counts;std::uint64_t zero_even=0,n=0;
  symmetric(m,f,[&](const M&D){auto z=F(D,f);int sum=0;for(int x:z)sum^=x;need(f.trace(sum)==0,"image trace");counts[key(z,q)]++;if(key(z,q)==0&&rank(D,f)%2==0)zero_even++;n++;});
  need(n==pw(q,m*(m+1)/2),"all symmetric");need(counts.size()==pw(q,m)/2,"image size");for(auto[k,c]:counts)need(c==2*pw(q,d),"fibre size");need(zero_even==pw(q,d),"Dickson half");
  if(rows++)std::cout<<",";std::cout<<"{\"q\":"<<q<<",\"m\":"<<m<<",\"matrices\":"<<n<<",\"image\":"<<counts.size()<<",\"omega_kernel\":"<<zero_even<<"}";total+=n;
 }
 std::cout<<"],\"symmetric_matrices\":"<<total<<",\"frames\":[";rows=0;
 for(auto[q,m]:std::vector<std::pair<int,int>>{{2,1},{2,2},{2,3},{2,4},{2,5},{2,6},{4,2},{4,3},{4,4},{8,2},{8,3}}){Field f(q);auto as=frames(m,f);auto want=(m%2?sp_order(m-1,q):pw(q,m-1)*sp_order(m-2,q));need(as.size()==want,"frame order");for(auto&A:as)for(auto&v:A){int s=0;for(int x:v)s^=x;need(s==1,"fix s");}if(rows++)std::cout<<",";std::cout<<"{\"q\":"<<q<<",\"m\":"<<m<<",\"J_order\":"<<as.size()<<"}";}
 std::cout<<"],\"centralizers\":[";rows=0;
 for(auto[q,m]:std::vector<std::pair<int,int>>{{2,2},{2,3},{2,4},{4,2},{4,3},{8,2}}){
  Field f(q);int d=m*(m-1)/2;auto as=frames(m,f);std::map<int,std::vector<M>> buckets;symmetric(m,f,[&](const M&D){buckets[key(F(D,f),q)].push_back(D);});
  for(int arf=0;arf<2;arf++){V b(m);if(arf){int z=1;while(f.trace(z)!=1)z++;b[0]=z;}
   std::uint64_t orth=0,omega=0,nu=0;M t=identity(2*m);for(int i=0;i<m;i++)t[i][m+i]=1;M toggle=identity(2*m);toggle[0][m]=1;need(rank_minus_identity(toggle,f)==1,"toggle rank");
   for(auto&A:as){V rhs=b;for(int i=0;i<m;i++)for(int j=0;j<m;j++)rhs[i]^=f.mul(f.sq(A[i][j]),b[j]);auto&bs=buckets.at(key(rhs,q));need(bs.size()==2*pw(q,d),"lift fibre");std::uint64_t local=0;
    for(auto&D:bs){auto g=literal_g(A,D,f);need(product(g,t,f)==product(t,g,f),"commutation");isometry(g,b,f);int parity=rank_minus_identity(g,f)%2;need(rank_minus_identity(product(toggle,g,f),f)%2!=parity,"toggle parity");orth++;if(!parity){local++;omega++;if(product(g,g,f)==identity(2*m))nu++;}}
    need(local==pw(q,d),"each omega fibre");
   }
   auto exponent=m%2?(m*m-m)/2:(m*m+m-2)/2;auto image=m%2?m-1:m-2;need(image==0||image==2,"small image");auto bound=pw(q,exponent)*(image?std::uint64_t(q*q):1);need(nu<=bound,"involution bound");
   if(rows++)std::cout<<",";std::cout<<"{\"q\":"<<q<<",\"m\":"<<m<<",\"arf_parameter\":"<<arf<<",\"O_centralizer\":"<<orth<<",\"Omega_centralizer\":"<<omega<<",\"nu2\":"<<nu<<",\"bound\":"<<bound<<"}";full+=orth;
  }
 }
 std::cout<<"],\"literal_centralizer_matrices\":"<<full<<"}\n";
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
