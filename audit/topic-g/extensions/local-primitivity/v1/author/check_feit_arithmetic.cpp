#include <gmp.h>
#include <cstdint>
#include <iostream>
int main(){static_assert(sizeof(unsigned long)>=8,"64-bit unsigned long required");uint64_t n;mpz_t m,v,z,b;mpz_inits(m,v,z,b,nullptr);mpz_set_ui(b,2);while(std::cin>>n){mpz_set_ui(m,n);mpz_mul(v,m,m);mpz_add(v,v,m);mpz_add_ui(v,v,1);mpz_powm_ui(z,b,n+1,v);std::cout<<n<<" ";mpz_out_str(stdout,10,v);std::cout<<" ";mpz_out_str(stdout,10,z);std::cout<<"\n";}mpz_clears(m,v,z,b,nullptr);}
