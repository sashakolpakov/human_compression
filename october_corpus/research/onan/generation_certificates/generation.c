/* NEW Source, UNRUN. The inverse-word/a/forward-word orientation is borrowed
 * from packed_keys.c:pck_key and partition_core.c:pct2_word_key. The supplied
 * proof obligations are generation_with_orbit_trees/generation.py verbatim
 * in mathematical meaning. This is not an existing native cycle API. */
#define _POSIX_C_SOURCE 200809L
#include "generation.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <limits.h>
_Static_assert(sizeof(uint32_t)==4,"exact point width");
_Static_assert(sizeof(uint8_t)==1,"exact tag width");
struct gn_context {gn_input in;uint32_t *inverse;size_t owned;};

static int nanos(uint64_t *out){
    struct timespec t;
    if(clock_gettime(CLOCK_MONOTONIC,&t)||t.tv_sec<0||t.tv_nsec<0||t.tv_nsec>=1000000000L||
       (uint64_t)t.tv_sec>(UINT64_MAX-UINT64_C(999999999))/UINT64_C(1000000000))return GN_BAD;
    *out=(uint64_t)t.tv_sec*UINT64_C(1000000000)+(uint64_t)t.tv_nsec;return GN_OK;
}
int gn_work_init(gn_work *w,uint64_t limit,uint32_t seconds,gn_checkpoint cp,void *arg){
    if(!w||!limit||limit>GN_MAX_OPERATIONS||!seconds||seconds>GN_MAX_SECONDS)return GN_BAD;
    memset(w,0,sizeof(*w));w->limit=limit;w->seconds=seconds;w->checkpoint=cp;w->checkpoint_argument=arg;
    return nanos(&w->started_ns);
}
int gn_work_finish(gn_work *w){
    uint64_t now;
    if(!w||!w->limit||w->limit>GN_MAX_OPERATIONS||!w->seconds||w->seconds>GN_MAX_SECONDS)return GN_BAD;
    if(w->stopped)return GN_STOP;
    if(nanos(&now)!=GN_OK)return GN_BAD;
    if(now<w->started_ns||now-w->started_ns>=UINT64_C(1000000000)*w->seconds||
       (w->checkpoint&&!w->checkpoint(w->checkpoint_argument))){w->stopped=1;return GN_STOP;}
    return GN_OK;
}
static int step(gn_work *w){
    if(!w||w->stopped)return GN_STOP;
    if(w->used>=w->limit){w->stopped=1;return GN_STOP;}
    ++w->used;return (w->used&4095u)?GN_OK:gn_work_finish(w);
}
void gn_destroy(gn_context *c){if(c){free(c->inverse);free(c);}}
size_t gn_owned_bytes(const gn_context *c){return c?c->owned:0;}
gn_context *gn_create(const gn_input *in,gn_work *w,int *status){
    gn_context *c=NULL;uint8_t *seen=NULL;uint32_t j,x,y,ax,ex;int r,nontrivial=0;
    if(status)*status=GN_BAD;
    if(!in||!in->a||!in->endpoints[0]||!in->endpoints[1]||!in->factors||in->degree<2||in->degree>GN_MAX_DEGREE||
       !in->factor_count||in->factor_count>GN_MAX_FACTORS)return NULL;
    r=gn_work_finish(w);if(r!=GN_OK){if(status)*status=r;return NULL;}
    c=calloc(1,sizeof(*c));if(!c)goto memory;c->in=*in;
    c->inverse=calloc((size_t)in->factor_count*in->degree,sizeof(uint32_t));seen=calloc(in->degree,1);
    if(!c->inverse||!seen)goto memory;
    c->owned=sizeof(*c)+(size_t)in->factor_count*in->degree*sizeof(uint32_t);
    for(j=0;j<in->factor_count+3u;++j){
        const uint32_t *p=j==0?in->a:j<3?in->endpoints[j-1]:in->factors+(size_t)(j-3)*in->degree;
        memset(seen,0,in->degree);
        for(x=0;x<in->degree;++x){
            if((r=step(w))!=GN_OK)goto stopped;
            y=p[x];if(y>=in->degree||seen[y])goto bad;seen[y]=1;
            if(j>=3)c->inverse[(size_t)(j-3)*in->degree+y]=x;
        }
    }
    for(x=0;x<in->degree;++x){
        if((r=step(w))!=GN_OK)goto stopped;ax=in->a[x];
        if((r=step(w))!=GN_OK)goto stopped;if(in->a[ax]!=x)goto bad;
        if(ax!=x)nontrivial=1;
        for(j=0;j<2;++j){const uint32_t *e=in->endpoints[j];
            if((r=step(w))!=GN_OK)goto stopped;ex=e[x];
            if((r=step(w))!=GN_OK)goto stopped;if(e[ex]!=x)goto bad;
            if((r=step(w))!=GN_OK)goto stopped;y=in->a[ex];
            if((r=step(w))!=GN_OK)goto stopped;if(y!=e[ax])goto bad;
        }
    }
    if(!nontrivial||!memcmp(in->a,in->endpoints[0],4u*in->degree)||!memcmp(in->a,in->endpoints[1],4u*in->degree)||
       !memcmp(in->endpoints[0],in->endpoints[1],4u*in->degree))goto bad;
    for(j=0;j<2;++j){nontrivial=0;for(x=0;x<in->degree;++x){if((r=step(w))!=GN_OK)goto stopped;if(in->endpoints[j][x]!=x)nontrivial=1;}if(!nontrivial)goto bad;}
    free(seen);r=gn_work_finish(w);if(r!=GN_OK){if(status)*status=r;gn_destroy(c);return NULL;}
    if(status)*status=GN_OK;return c;
memory:if(status)*status=GN_MEMORY;free(seen);gn_destroy(c);return NULL;
bad:if(status)*status=GN_BAD;free(seen);gn_destroy(c);return NULL;
stopped:if(status)*status=r;free(seen);gn_destroy(c);return NULL;
}
static int word_ok(const gn_context *c,const uint8_t *v,uint32_t n){
    uint32_t k;if(!c||n>GN_MAX_CONJUGATOR||(!v&&n))return 0;
    for(k=0;k<n;++k)if(v[k]<1||v[k]>c->in.factor_count)return 0;return 1;
}
static int raw(const gn_context *c,const uint32_t *p,uint32_t x,uint32_t *y,gn_work *w){
    int r;if(!c||!p||!y||x>=c->in.degree)return GN_BAD;
    if((r=step(w))!=GN_OK)return r;*y=p[x];return *y<c->in.degree?GN_OK:GN_BAD;
}
int gn_virtual_b(const gn_context *c,const uint8_t *v,uint32_t n,uint32_t x,uint32_t *out,gn_work *w){
    uint32_t k;int r;if(!out||!word_ok(c,v,n)||x>=c->in.degree)return GN_BAD;
    if((r=gn_work_finish(w))!=GN_OK)return r;
    for(k=0;k<n;++k)if((r=raw(c,c->inverse+(size_t)(v[k]-1)*c->in.degree,x,&x,w))!=GN_OK)return r;
    if((r=raw(c,c->in.a,x,&x,w))!=GN_OK)return r;
    for(k=n;k>0;--k)if((r=raw(c,c->in.factors+(size_t)(v[k-1]-1)*c->in.degree,x,&x,w))!=GN_OK)return r;
    if((r=gn_work_finish(w))!=GN_OK)return r;*out=x;return GN_OK;
}
static int rotation_ok(const gn_word *p){
    uint32_t i;if(!p||!p->length||p->length>GN_MAX_WORD)return 0;
    for(i=0;i<p->length;++i)if(p->letters[i]!=1&&p->letters[i]!=-1&&p->letters[i]!=2&&p->letters[i]!=-2)return 0;return 1;
}
int gn_rotation_word(const gn_context *c,uint32_t ep,const uint8_t *v,uint32_t n,const gn_word *p,uint32_t x,uint32_t *out,gn_work *w){
    uint32_t i;int r;const uint32_t *e;
    if(!c||ep<1||ep>2||!out||!word_ok(c,v,n)||!rotation_ok(p)||x>=c->in.degree)return GN_BAD;e=c->in.endpoints[ep-1];
    for(i=0;i<p->length;++i){
        int k=p->letters[i];
        if(k==1||k==-2){if((r=raw(c,k==1?c->in.a:e,x,&x,w))!=GN_OK)return r;}
        if((r=gn_virtual_b(c,v,n,x,&x,w))!=GN_OK)return r;
        if(k==-1||k==2){if((r=raw(c,k==-1?c->in.a:e,x,&x,w))!=GN_OK)return r;}
    }
    if((r=gn_work_finish(w))!=GN_OK)return r;*out=x;return GN_OK;
}
int gn_check_cycle(const gn_context *c,uint32_t ep,const uint8_t *v,uint32_t n,const gn_cycle *p,uint32_t prime,gn_work *w){
    uint8_t *seen;uint32_t i,y;int r=GN_BAD;
    if(!c||!p||(prime!=19&&prime!=31)||p->length<prime||p->length>GN_MAX_CYCLE||p->length%prime||!rotation_ok(&p->word))return GN_BAD;
    seen=calloc(c->in.degree,1);if(!seen)return GN_MEMORY;
    for(i=0;i<p->length;++i){uint32_t x=p->vertices[i];if(x>=c->in.degree||seen[x])goto done;seen[x]=1;}
    for(i=0;i<p->length;++i){r=gn_rotation_word(c,ep,v,n,&p->word,p->vertices[i],&y,w);if(r!=GN_OK)goto done;
        if(y!=p->vertices[(i+1)%p->length]){r=GN_BAD;goto done;}}
    r=gn_work_finish(w);
done:free(seen);return r;
}
int gn_propose_cycles(const gn_context *c,uint32_t ep,const uint8_t *v,uint32_t n,const gn_word *words,uint32_t nw,const uint32_t *starts,uint32_t ns,uint32_t cap,gn_cycle *p19,gn_cycle *p31,gn_work *w){
    uint8_t *seen;uint32_t points[GN_MAX_CYCLE],i,j,k,x,y;int got19=0,got31=0,r=GN_BAD;
    if(!c||!words||!starts||!p19||!p31||!nw||nw>GN_MAX_PROPOSALS||!ns||ns>GN_MAX_STARTS||!cap||cap>GN_MAX_CYCLE||!word_ok(c,v,n))return GN_BAD;
    for(i=0;i<nw;++i)if(!rotation_ok(&words[i]))return GN_BAD;
    for(j=0;j<ns;++j)if(starts[j]>=c->in.degree)return GN_BAD;
    seen=calloc(c->in.degree,1);if(!seen)return GN_MEMORY;
    for(i=0;i<nw;++i)for(j=0;j<ns;++j){
        memset(seen,0,c->in.degree);x=starts[j];
        for(k=0;k<cap;++k){
            if(seen[x]){r=GN_BAD;goto done;}points[k]=x;seen[x]=1;
            r=gn_rotation_word(c,ep,v,n,&words[i],x,&y,w);if(r!=GN_OK)goto done;x=y;
            if(x==starts[j]){
                if((k+1)%19==0&&!got19){p19->word=words[i];p19->length=k+1;memcpy(p19->vertices,points,4u*(k+1));got19=1;}
                if((k+1)%31==0&&!got31){p31->word=words[i];p31->length=k+1;memcpy(p31->vertices,points,4u*(k+1));got31=1;}break;
            }
        }
        if(got19&&got31){r=gn_check_cycle(c,ep,v,n,p19,19,w);if(r==GN_OK)r=gn_check_cycle(c,ep,v,n,p31,31,w);goto done;}
    }
    r=gn_work_finish(w);if(r==GN_OK)r=GN_MISS;
done:if(r!=GN_OK){p19->length=0;p31->length=0;}free(seen);return r;
}
static int member(const uint8_t *bits,uint32_t x){return (bits[x/8]>>(x%8))&1;}
int gn_check_subset(const gn_context *c,uint32_t ep,const uint8_t *v,uint32_t n,const uint8_t *bits,size_t size,uint32_t count,gn_work *w){
    uint32_t x,y,total=0;int r;
    if(!c||ep<1||ep>2||!bits||size!=(c->in.degree+7u)/8u||!count||count>=c->in.degree||!word_ok(c,v,n))return GN_BAD;
    if(c->in.degree%8u&&(bits[size-1]>>(c->in.degree%8u)))return GN_BAD;
    for(x=0;x<c->in.degree;++x)if(member(bits,x)){
        ++total;r=raw(c,c->in.a,x,&y,w);if(r!=GN_OK)return r;if(!member(bits,y))return GN_BAD;
        r=gn_virtual_b(c,v,n,x,&y,w);if(r!=GN_OK)return r;if(!member(bits,y))return GN_BAD;
        r=raw(c,c->in.endpoints[ep-1],x,&y,w);if(r!=GN_OK)return r;if(!member(bits,y))return GN_BAD;
    }
    return total==count?gn_work_finish(w):GN_BAD;
}
int gn_check_tree(const gn_context *c,uint32_t ep,const uint8_t *v,uint32_t n,const uint8_t *tags,size_t size,uint32_t height,gn_work *w){
    uint32_t x,y,label,level,max=0;int r;
    if(!c||ep<1||ep>2||!tags||size!=c->in.degree||tags[0]||!height||height>63||!word_ok(c,v,n))return GN_BAD;
    for(x=1;x<c->in.degree;++x){label=tags[x]&3u;level=tags[x]>>2;if(label==3||!level)return GN_BAD;if(level>max)max=level;
        if(label==1)r=gn_virtual_b(c,v,n,x,&y,w);else r=raw(c,label==0?c->in.a:c->in.endpoints[ep-1],x,&y,w);
        if(r!=GN_OK)return r;if((tags[y]>>2)>=level)return GN_BAD;
    }
    return max==height?gn_work_finish(w):GN_BAD;
}
int gn_propose_orbit(const gn_context *c,uint32_t ep,const uint8_t *v,uint32_t n,uint8_t *tags,size_t tagbytes,uint8_t *bits,size_t bitbytes,uint32_t *kind,uint32_t *size_or_height,gn_work *w){
    uint32_t *queue,head=0,length=1,x,y,label,level,height=0,i;int r=GN_BAD;
    if(!c||ep<1||ep>2||!tags||tagbytes!=c->in.degree||!bits||bitbytes!=(c->in.degree+7u)/8u||!kind||!size_or_height||!word_ok(c,v,n))return GN_BAD;
    *kind=GN_ROW_UNPAID;*size_or_height=0;
    queue=calloc(c->in.degree,sizeof(uint32_t));if(!queue)return GN_MEMORY;
    memset(bits,0,bitbytes);memset(tags,0,tagbytes);bits[0]=1;
    while(head<length&&length<c->in.degree){x=queue[head++];for(label=0;label<3;++label){
        if(label==1)r=gn_virtual_b(c,v,n,x,&y,w);else r=raw(c,label==0?c->in.a:c->in.endpoints[ep-1],x,&y,w);
        if(r!=GN_OK)goto done;
        if(!member(bits,y)){level=(tags[x]>>2)+1;if(level>63){r=GN_MISS;goto done;}
            tags[y]=(uint8_t)((level<<2)|label);if(level>height)height=level;bits[y/8]|=(uint8_t)(1u<<(y%8));queue[length++]=y;
            if(length==c->in.degree)break;}
    }}
    if(length==c->in.degree){r=gn_check_tree(c,ep,v,n,tags,tagbytes,height,w);if(r==GN_OK){*kind=GN_ROW_TREE;*size_or_height=height;}goto done;}
    if(head!=length){r=GN_BAD;goto done;}
    if(length>c->in.degree/2u){for(i=0;i<bitbytes;++i)bits[i]^=255u;if(c->in.degree%8u)bits[bitbytes-1]&=(uint8_t)((1u<<(c->in.degree%8u))-1u);length=c->in.degree-length;}
    r=gn_check_subset(c,ep,v,n,bits,bitbytes,length,w);if(r==GN_OK){*kind=GN_ROW_SET;*size_or_height=length;}
done:free(queue);return r;
}
int gn_batch_init(gn_batch *b,uint32_t selected,uint64_t fixed){
    if(!b||!selected||selected>GN_MAX_ROWS||fixed>GN_MAX_ARTIFACT)return GN_BAD;memset(b,0,sizeof(*b));b->selected=selected;b->bytes=fixed;return GN_OK;
}
int gn_batch_commit(gn_batch *b,gn_work *w,uint32_t kind,uint64_t bytes){
    int r;if(!b||b->next>=b->selected||kind>GN_ROW_SET||(kind==GN_ROW_UNPAID?bytes!=0:bytes==0))return GN_BAD;
    if(b->tail_cause)return GN_STOP;r=gn_work_finish(w);if(r==GN_BAD)return r;
    if(r==GN_STOP){b->tail_cause=GN_TAIL_POINT_OR_TIME;return GN_STOP;}
    if(bytes>GN_MAX_ARTIFACT-b->bytes){b->tail_cause=GN_TAIL_BYTES;return GN_STOP;}
    b->status[b->next++]=(uint8_t)kind;b->bytes+=bytes;return GN_OK;
}
const char *gn_status_text(uint32_t kind){return kind==GN_ROW_CYCLES||kind==GN_ROW_TREE?"GENERATING":kind==GN_ROW_SET?"NONGENERATING_INVARIANT_SET":kind==GN_ROW_UNPAID?"UNPAID":NULL;}
const char *gn_reason_text(uint32_t kind,uint32_t cause){return kind==GN_ROW_CYCLES?"SUPPLIED_19_AND_31_CYCLES":kind==GN_ROW_TREE?"SUPPLIED_FULL_ABC_LEVEL_TREE":kind==GN_ROW_SET?"SUPPLIED_NONEMPTY_PROPER_ABC_CLOSED_SET":kind==GN_ROW_UNPAID?(cause==GN_TAIL_POINT_OR_TIME?"POINT_BUDGET":"BOUNDED_PROPOSAL_UNPAID"):NULL;}
