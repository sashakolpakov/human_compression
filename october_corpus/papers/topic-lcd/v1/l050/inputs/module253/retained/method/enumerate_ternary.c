/* Enumerate every coefficient vector of a supplied independent ternary basis.
 * A base-three counter gives each vector exactly once. A carry from2to0 adds
 * the same basis row, because2+1=0 inF3. Codewords use two disjoint bit planes.
 * The input basis must be certified independently; this program checks its
 * format, and makes no claim about its rank or its mathematical provenance.
 */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_N 1024
#define MAX_K 39
#define MAX_W ((MAX_N+63)/64)

int main(int argc, char **argv) {
    if(argc!=2){fprintf(stderr,"usage: enumerate_ternary basis.txt\n");return 2;}
    FILE *input=fopen(argv[1],"r");
    if(!input){perror("basis input");return 2;}
    unsigned n,k;
    if(fscanf(input,"%u %u",&n,&k)!=2 || n==0 || n>MAX_N || k>MAX_K){
        fprintf(stderr,"invalid dimensions\n");return 2;
    }
    const unsigned width=(n+63)/64;
    uint64_t one[MAX_K][MAX_W]={{0}},two[MAX_K][MAX_W]={{0}},zero[MAX_K][MAX_W]={{0}};
    char row[MAX_N+2];
    for(unsigned i=0;i<k;i++){
        if(fscanf(input,"%1025s",row)!=1 || strlen(row)!=n){fprintf(stderr,"invalid row\n");return 2;}
        for(unsigned j=0;j<n;j++){
            if(row[j]<'0'||row[j]>'2'){fprintf(stderr,"invalid field entry\n");return 2;}
            if(row[j]=='1')one[i][j/64]|=UINT64_C(1)<<(j%64);
            if(row[j]=='2')two[i][j/64]|=UINT64_C(1)<<(j%64);
        }
        for(unsigned w=0;w<width;w++)zero[i][w]=~(one[i][w]|two[i][w]);
    }
    if(fscanf(input,"%1025s",row)==1){fprintf(stderr,"trailing data\n");return 2;}
    fclose(input);
    uint64_t total=1;
    for(unsigned i=0;i<k;i++){
        if(total>UINT64_MAX/3){fprintf(stderr,"counter overflow\n");return 2;}
        total*=3;
    }
    unsigned digits[MAX_K]={0};
    uint64_t a[MAX_W]={0},b[MAX_W]={0},counts[MAX_N+1]={0};
    counts[0]=1;
    for(uint64_t step=1;step<total;step++){
        unsigned i=0;
        for(;;){
            for(unsigned w=0;w<width;w++){
                uint64_t c=~(a[w]|b[w]);
                uint64_t na=(c&one[i][w])|(a[w]&zero[i][w])|(b[w]&two[i][w]);
                uint64_t nb=(c&two[i][w])|(b[w]&zero[i][w])|(a[w]&one[i][w]);
                a[w]=na;b[w]=nb;
            }
            digits[i]++;
            if(digits[i]<3)break;
            digits[i]=0;i++;
            if(i>=k){fprintf(stderr,"unexpected carry\n");return 2;}
        }
        unsigned weight=0;
        for(unsigned w=0;w<width;w++)weight+=(unsigned)__builtin_popcountll(a[w]|b[w]);
        if(weight>n){fprintf(stderr,"invalid weight\n");return 2;}
        counts[weight]++;
        if((step&((UINT64_C(1)<<28)-1))==0){
            fprintf(stderr,"enumerated=%"PRIu64" total=%"PRIu64"\n",step,total);
            fflush(stderr);
        }
    }
    printf("{\"length\":%u,\"basis_rows\":%u,\"coefficient_vectors\":%"PRIu64",\"weight_counts\":[",n,k,total);
    for(unsigned i=0;i<=n;i++)printf("%s%"PRIu64,i?",":"",counts[i]);
    puts("]}");return 0;
}
