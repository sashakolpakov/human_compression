// Exact necessary-condition sieve for the finite remark on L102 physical p5.
// Only proper divisors discard m^2+m+1; every unsieved case uses exact GMP.
#include <gmp.h>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>
using U=uint64_t;
struct Root { U p,r; };
int main(int argc,char**argv) {
 try {
  if(argc!=2)throw std::runtime_error("usage: feit_bound upper_m");
  char*end=nullptr; U limit=std::strtoull(argv[1],&end,10);
  if(*end || limit<8 || limit>10000000000ULL)throw std::runtime_error("8 <= upper_m <= 10^10");
  const U sieve_bound=10000,chunk=1000000;
  std::vector<bool> prime(sieve_bound+1,true);prime[0]=prime[1]=false;
  for(U p=2;p*p<=sieve_bound;++p)if(prime[p])for(U j=p*p;j<=sieve_bound;j+=p)prime[j]=false;
  std::vector<Root> roots;
  // Enumerate roots directly in the m=8+24*t parameter, so no inverse theorem is needed.
  for(U p=2;p<=sieve_bound;++p)if(prime[p])
   for(U t=0;t<p;++t){U m=(8+24*t)%p;if((m*m+m+1)%p==0)roots.push_back({p,t});}
  U total=(limit-8)/24+1,composite=0,powers2=0,tested=0;std::vector<U> survivors;
  mpz_t m,v,z,base;mpz_inits(m,v,z,base,nullptr);mpz_set_ui(base,2);
  auto start=std::chrono::steady_clock::now();double next_progress=30;
  for(U low=0;low<total;low+=chunk) {
   U high=std::min(total,low+chunk);std::vector<unsigned char> discard(high-low,0);
   for(auto a:roots) {
    U first=low+(a.r+a.p-low%a.p)%a.p;
    for(U t=first;t<high;t+=a.p){U value=8+24*t;
     // m^2+m+1=p is possible only for tiny m; avoid overflow and retain it.
     bool equal=(value<=sieve_bound && value*value+value+1==a.p);
     if(!equal)discard[t-low]=1;
    }
   }
   for(U t=low;t<high;++t) {
    U value=8+24*t;
    if((value&(value-1))==0){++powers2;continue;}
    if(discard[t-low]){++composite;continue;}
    ++tested;mpz_set_ui(m,value);mpz_mul(v,m,m);mpz_add(v,v,m);mpz_add_ui(v,v,1);
    mpz_powm_ui(z,base,value+1,v);
    if(mpz_cmp_ui(z,1)==0)survivors.push_back(value);
   }
   double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
   if(elapsed>=next_progress){std::cerr<<"progress "<<high<<"/"<<total<<" exact_powers="<<tested<<" seconds="<<elapsed<<"\n";next_progress=elapsed+30;}
  }
  double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\"upper_m\":"<<limit<<",\"residue_cases\":"<<total<<",\"proper_factor_rejections\":"<<composite
   <<",\"power_of_two_exclusions\":"<<powers2<<",\"exact_modular_powers\":"<<tested<<",\"sieve_bound\":"<<sieve_bound
   <<",\"root_classes\":"<<roots.size()<<",\"seconds\":"<<elapsed<<",\"survivors\":[";
  for(size_t i=0;i<survivors.size();++i){if(i)std::cout<<",";std::cout<<survivors[i];}
  std::cout<<"],\"all_cases_accounted\":"<<((composite+powers2+tested==total)?"true":"false")<<"}\n";
  mpz_clears(m,v,z,base,nullptr);return 0;
 } catch(std::exception const&e){std::cerr<<e.what()<<"\n";return 1;}
}
