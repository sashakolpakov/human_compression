/* Enumerate all systematic messages of weight at most the specified bound.
 * This is a restricted enumeration, not a complete weight distribution.
 * The caller must certify rank, information columns and a transitive action.
 * Input: n k p bound, followed by k rows of n digits over F_p, p=2 or3.
 */
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_N 1024
#define MAX_K 1024
#define MAX_DEPTH 16
#define MAX_W ((MAX_N+63)/64)
static unsigned n,k,p,bound,width,best;
static uint64_t rows1[MAX_K][MAX_W],rows2[MAX_K][MAX_W];
static uint64_t a[MAX_DEPTH+1][MAX_W],b[MAX_DEPTH+1][MAX_W];
static uint64_t counts[MAX_N+1],visited,best1[MAX_W],best2[MAX_W];

static void visit(unsigned start,unsigned depth) {
    if(depth==bound)return;
    for(unsigned i=start;i<k;i++)for(unsigned c=1;c<p;c++){
        unsigned wt=0;
        for(unsigned w=0;w<width;w++){
            if(p==2){a[depth+1][w]=a[depth][w]^rows1[i][w];b[depth+1][w]=0;}
            else{
                uint64_t x=c==1?rows1[i][w]:rows2[i][w];
                uint64_t y=c==1?rows2[i][w]:rows1[i][w];
                uint64_t z=~(x|y),az=~(a[depth][w]|b[depth][w]);
                a[depth+1][w]=(az&x)|(a[depth][w]&z)|(b[depth][w]&y);
                b[depth+1][w]=(az&y)|(b[depth][w]&z)|(a[depth][w]&x);
            }
            wt+=(unsigned)__builtin_popcountll(a[depth+1][w]|b[depth+1][w]);
        }
        if(wt>n||visited==UINT64_MAX||counts[wt]==UINT64_MAX){fprintf(stderr,"counter or weight overflow\n");exit(2);}
        counts[wt]++;visited++;
        if(wt<best){best=wt;memcpy(best1,a[depth+1],sizeof(best1));memcpy(best2,b[depth+1],sizeof(best2));}
        visit(i+1,depth+1);
    }
}

int main(int argc,char **argv){
    if(argc!=2){fprintf(stderr,"usage: enumerate_sparse_messages basis.txt\n");return 2;}
    FILE *f=fopen(argv[1],"r");if(!f){perror("basis");return 2;}
    if(fscanf(f,"%u %u %u %u",&n,&k,&p,&bound)!=4||n==0||n>MAX_N||k>n||k>MAX_K||(p!=2&&p!=3)||bound>k||bound>MAX_DEPTH){fprintf(stderr,"invalid dimensions or bound\n");return 2;}
    width=(n+63)/64;char line[MAX_N+2];
    for(unsigned i=0;i<k;i++){
        if(fscanf(f,"%1025s",line)!=1||strlen(line)!=n){fprintf(stderr,"invalid row\n");return 2;}
        for(unsigned j=0;j<n;j++){
            if(line[j]<'0'||(unsigned)(line[j]-'0')>=p){fprintf(stderr,"invalid entry\n");return 2;}
            if(line[j]=='1')rows1[i][j/64]|=UINT64_C(1)<<(j%64);
            if(line[j]=='2')rows2[i][j/64]|=UINT64_C(1)<<(j%64);
        }
    }
    if(fscanf(f,"%1025s",line)==1){fprintf(stderr,"trailing data\n");return 2;}
    fclose(f);counts[0]=1;visited=1;best=n+1;visit(0,0);
    printf("{\"length\":%u,\"dimension_input\":%u,\"prime\":%u,\"message_weight_bound\":%u,\"messages\":%"PRIu64",\"minimum_codeword_weight_over_nonzero_messages\":",n,k,p,bound,visited);
    if(best==n+1)printf("null");else printf("%u",best);
    printf(",\"minimum_witness\":\"");
    if(best<=n)for(unsigned j=0;j<n;j++)putchar('0'+((best1[j/64]>>(j%64))&1)+2*((best2[j/64]>>(j%64))&1));
    printf("\",\"restricted_weight_counts\":[");
    for(unsigned j=0;j<=n;j++)printf("%s%"PRIu64,j?",":"",counts[j]);
    puts("]}");return 0;
}
