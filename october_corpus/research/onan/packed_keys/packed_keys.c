#include "packed_keys.h"
#include <limits.h>
#include <stdlib.h>
#include <string.h>

_Static_assert(sizeof(uint32_t)==4,"exact four-byte node and point labels");
_Static_assert(sizeof(uint16_t)==2,"exact two-byte bounded word depth");

struct pck_context {
    pck_input in;
    uint32_t count,stride,slots,tombstones;
    uint64_t operations;
    size_t owned;
    uint8_t *keys,*labels;
    uint16_t *depths;
    uint32_t *parents,*table,*inverse;
};
_Static_assert(sizeof(struct pck_context)<=256,"bounded context header");
#define TOMBSTONE UINT32_MAX

static int tick(pck_context *c) {
    if(c->operations>=c->in.operation_limit) return PCK_STOP;
    ++c->operations;
    if((c->operations&4095u)==0u && c->in.checkpoint &&
       !c->in.checkpoint(c->in.checkpoint_argument)) return PCK_STOP;
    return PCK_OK;
}
static void *allocate(pck_context *c,size_t n,size_t width) {
    void *p;
    if(width && n>SIZE_MAX/width) return NULL;
    p=calloc(n,width);
    if(p) c->owned+=n*width;
    return p;
}
void pck_destroy(pck_context *c) {
    if(!c)return;
    free(c->keys);free(c->labels);free(c->depths);free(c->parents);
    free(c->table);free(c->inverse);free(c);
}
pck_context *pck_create(const pck_input *in,int *status) {
    pck_context *c=NULL;uint8_t *seen=NULL;uint32_t f,x,y;int nonidentity=0;
    if(status)*status=PCK_BAD;
    if(!in || !in->base || !in->involution || !in->factors ||
       in->degree<2 || in->degree>PCK_MAX_DEGREE || in->target<1 ||
       in->target>PCK_MAX_CLASS || in->base_length<1 ||
       in->base_length>PCK_MAX_BASE || in->factor_count<1 ||
       in->factor_count>PCK_MAX_FACTORS || in->hash_bits<2 ||
       in->hash_bits>23 || (UINT32_C(1)<<in->hash_bits)<=2u*in->target ||
       !in->operation_limit)return NULL;
    c=calloc(1,sizeof(*c));if(!c){if(status)*status=PCK_CAP;return NULL;}
    c->owned=sizeof(*c);c->in=*in;c->slots=UINT32_C(1)<<in->hash_bits;
    c->stride=(17u*in->base_length+7u)/8u;
    c->keys=allocate(c,(size_t)in->target+1u,c->stride);
    c->parents=allocate(c,(size_t)in->target+1u,sizeof(uint32_t));
    c->labels=allocate(c,(size_t)in->target+1u,sizeof(uint8_t));
    c->depths=allocate(c,(size_t)in->target+1u,sizeof(uint16_t));
    c->table=allocate(c,c->slots,sizeof(uint32_t));
    c->inverse=allocate(c,(size_t)in->factor_count*in->degree,sizeof(uint32_t));
    seen=calloc(in->degree,1);
    if(!c->keys||!c->parents||!c->labels||!c->depths||!c->table||!c->inverse||!seen)
        goto capacity;
    for(x=0;x<in->base_length;++x){
        if(in->base[x]>=in->degree)goto bad;
        for(y=0;y<x;++y)if(in->base[y]==in->base[x])goto bad;
    }
    for(x=0;x<in->degree;++x){
        if(tick(c)!=PCK_OK)goto stopped;
        y=in->involution[x];if(y>=in->degree||seen[y])goto bad;
        seen[y]=1;if(y!=x)nonidentity=1;
    }
    if(!nonidentity)goto bad;
    for(x=0;x<in->degree;++x)if(in->involution[in->involution[x]]!=x)goto bad;
    for(f=0;f<in->factor_count;++f){
        memset(seen,0,in->degree);
        for(x=0;x<in->degree;++x){
            if(tick(c)!=PCK_OK)goto stopped;
            y=in->factors[(size_t)f*in->degree+x];
            if(y>=in->degree||seen[y])goto bad;
            seen[y]=1;c->inverse[(size_t)f*in->degree+y]=x;
        }
    }
    free(seen);if(status)*status=PCK_OK;return c;
capacity: if(status)*status=PCK_CAP;free(seen);pck_destroy(c);return NULL;
stopped: if(status)*status=PCK_STOP;free(seen);pck_destroy(c);return NULL;
bad: if(status)*status=PCK_BAD;free(seen);pck_destroy(c);return NULL;
}
uint32_t pck_count(const pck_context *c){return c?c->count:0;}
uint32_t pck_key_bytes(const pck_context *c){return c?c->stride:0;}
uint64_t pck_operations(const pck_context *c){return c?c->operations:0;}
size_t pck_owned_bytes(const pck_context *c){return c?c->owned:0;}
int pck_get_node(const pck_context *c,uint32_t id,pck_node *node){
    if(!c||!node||id<1||id>c->count)return PCK_BAD;
    node->parent=c->parents[id];node->factor=c->labels[id];node->depth=c->depths[id];
    node->key=c->keys+(size_t)id*c->stride;return PCK_OK;
}
int pck_key(pck_context *c,uint32_t parent,uint8_t factor,uint8_t *key){
    uint8_t word[PCK_MAX_WORD];uint32_t len=0,id=parent,j,x,k,b,bit;
    if(!c||!key||parent>c->count||factor>c->in.factor_count||
       ((parent==0)!=(factor==0)))return PCK_BAD;
    if(parent && (uint32_t)c->depths[parent]+1u>PCK_MAX_WORD)return PCK_CAP;
    if(factor)word[len++]=factor;
    while(id){
        if(tick(c)!=PCK_OK)return PCK_STOP;
        if(c->labels[id]){if(len>=PCK_MAX_WORD)return PCK_CAP;word[len++]=c->labels[id];}
        if(c->parents[id]>=id)return PCK_BAD;
        id=c->parents[id];
    }
    /* word is in REVERSE multiplication order. No full conjugate is formed. */
    memset(key,0,c->stride);
    for(j=0;j<c->in.base_length;++j){
        x=c->in.base[j];
        for(k=0;k<len;++k){
            if(tick(c)!=PCK_OK)return PCK_STOP;
            x=c->inverse[(size_t)(word[k]-1u)*c->in.degree+x];
        }
        x=c->in.involution[x];
        for(k=len;k>0;--k){
            if(tick(c)!=PCK_OK)return PCK_STOP;
            x=c->in.factors[(size_t)(word[k-1u]-1u)*c->in.degree+x];
        }
        /* Zero-based images 0..131071 have EXACTLY seventeen available bits. */
        for(b=0;b<17;++b){bit=17u*j+b;if(x&(UINT32_C(1)<<b))key[bit/8u]|=(uint8_t)(1u<<(bit%8u));}
    }
    return PCK_OK;
}
static uint64_t hash_key(const uint8_t *p,uint32_t n){
    uint64_t h=UINT64_C(14695981039346656037);uint32_t i;
    for(i=0;i<n;++i){h^=p[i];h*=UINT64_C(1099511628211);}return h;
}
static int locate(pck_context *c,const uint8_t *key,uint32_t *id,uint32_t *slot){
    uint32_t at=(uint32_t)hash_key(key,c->stride)&(c->slots-1u),i,v,first=UINT32_MAX;
    for(i=0;i<c->slots;++i){
        if(tick(c)!=PCK_OK)return PCK_STOP;
        v=c->table[at];
        if(v==0){*id=0;*slot=first==UINT32_MAX?at:first;return PCK_OK;}
        if(v==TOMBSTONE){if(first==UINT32_MAX)first=at;}
        else{
            if(v>c->count)return PCK_BAD;
            if(memcmp(key,c->keys+(size_t)v*c->stride,c->stride)==0){*id=v;*slot=at;return PCK_OK;}
        }
        at=(at+1u)&(c->slots-1u);
    }
    if(first!=UINT32_MAX){*id=0;*slot=first;return PCK_OK;}return PCK_CAP;
}
int pck_find(pck_context *c,const uint8_t *key,uint32_t *id){
    uint32_t slot;if(!c||!key||!id)return PCK_BAD;return locate(c,key,id,&slot);
}
static int append(pck_context *c,uint32_t parent,uint8_t factor,const uint8_t *key,
                  uint32_t *id,uint32_t *slot){
    int status=locate(c,key,id,slot);uint32_t n;
    if(status!=PCK_OK||*id)return status;
    if(c->count>=c->in.target)return PCK_CAP;
    n=c->count+1u;
    c->parents[n]=parent;c->labels[n]=factor;
    c->depths[n]=parent?(uint16_t)(c->depths[parent]+1u):0;
    memcpy(c->keys+(size_t)n*c->stride,key,c->stride);
    if(c->table[*slot]==TOMBSTONE)--c->tombstones;
    c->table[*slot]=n;c->count=n;*id=n;return PCK_OK;
}
int pck_check_append(pck_context *c,uint32_t parent,uint8_t factor,
                     const uint8_t *key,uint32_t *id){
    uint8_t actual[PCK_MAX_KEY];uint32_t slot,before;int status;
    if(!c||!key||!id)return PCK_BAD;
    if((c->count==0)!=(parent==0&&factor==0))return PCK_BAD;
    status=pck_key(c,parent,factor,actual);if(status!=PCK_OK)return status;
    if(memcmp(actual,key,c->stride)!=0)return PCK_BAD;
    before=c->count;status=append(c,parent,factor,key,id,&slot);
    if(status==PCK_OK && c->count==before)return PCK_OLD;
    return status;
}
int pck_close(pck_context *c,uint32_t parent,uint8_t factor,
              const uint8_t *tg,uint32_t nt,uint32_t order,pck_orbit *orbit){
    uint8_t key[PCK_MAX_KEY];uint32_t before,id,slot,head,j,nadded=0,i;
    uint32_t slots[PCK_MAX_ENDPOINT];int status;
    if(!c||!tg||!orbit||nt<1||nt>PCK_MAX_FACTORS||order<1||order>PCK_MAX_ENDPOINT)return PCK_BAD;
    for(j=0;j<nt;++j)if(tg[j]<1||tg[j]>c->in.factor_count)return PCK_BAD;
    if((c->count==0)!=(parent==0&&factor==0))return PCK_BAD;
    before=c->count;memset(orbit,0,sizeof(*orbit));
    status=pck_key(c,parent,factor,key);if(status!=PCK_OK)return status;
    status=locate(c,key,&id,&slot);if(status!=PCK_OK)return status;
    if(id)return PCK_OLD;
    status=append(c,parent,factor,key,&id,&slot);if(status!=PCK_OK)return status;
    slots[nadded++]=slot;orbit->ids[0]=id;orbit->first=id;orbit->weight=1;
    for(head=0;head<orbit->weight;++head){
        for(j=0;j<nt;++j){
            status=pck_key(c,orbit->ids[head],tg[j],key);if(status!=PCK_OK)goto rollback;
            status=locate(c,key,&id,&slot);if(status!=PCK_OK)goto rollback;
            if(id && id<=before){status=PCK_BAD;goto rollback;}
            if(!id){
                if(orbit->weight>=order){status=PCK_BAD;goto rollback;}
                status=append(c,orbit->ids[head],tg[j],key,&id,&slot);if(status!=PCK_OK)goto rollback;
                slots[nadded++]=slot;orbit->ids[orbit->weight++]=id;
            }
            orbit->edges[(size_t)head*nt+j]=id;
        }
    }
    if(order%orbit->weight!=0){status=PCK_BAD;goto rollback;}
    return PCK_OK;
rollback:
    /* A known incomplete orbit is NEVER a committed partial orbit. Leaving
     * tombstones preserves every old probe chain; a restored snapshot rebuilds
     * the table from its exact accepted keys and has no tombstones. */
    for(i=0;i<nadded;++i){c->table[slots[i]]=TOMBSTONE;++c->tombstones;}
    c->count=before;memset(orbit,0,sizeof(*orbit));return status;
}
int pck_check_orbit(pck_context *c,const uint8_t *tg,uint32_t nt,
                    uint32_t order,const pck_orbit *orbit){
    uint8_t key[PCK_MAX_KEY],reached[PCK_MAX_ENDPOINT]={0};
    uint32_t queue[PCK_MAX_ENDPOINT],head=0,tail=0,i,j,id,to;int status;
    if(!c||!tg||!orbit||nt<1||nt>PCK_MAX_FACTORS||order<1||
       order>PCK_MAX_ENDPOINT||orbit->weight<1||orbit->weight>order||
       order%orbit->weight||orbit->first<1||orbit->first>c->count||
       orbit->weight>c->count-orbit->first+1u)return PCK_BAD;
    for(j=0;j<nt;++j)if(tg[j]<1||tg[j]>c->in.factor_count)return PCK_BAD;
    for(i=0;i<orbit->weight;++i){
        id=orbit->first+i;if(orbit->ids[i]!=id)return PCK_BAD;
        for(j=0;j<nt;++j){
            to=orbit->edges[(size_t)i*nt+j];
            if(to<orbit->first||to-orbit->first>=orbit->weight)return PCK_BAD;
            status=pck_key(c,id,tg[j],key);if(status!=PCK_OK)return status;
            if(memcmp(key,c->keys+(size_t)to*c->stride,c->stride)!=0)return PCK_BAD;
        }
    }
    reached[0]=1;queue[tail++]=0;
    while(head<tail){
        i=queue[head++];
        for(j=0;j<nt;++j){
            to=orbit->edges[(size_t)i*nt+j]-orbit->first;
            if(!reached[to]){reached[to]=1;queue[tail++]=to;}
        }
    }
    return tail==orbit->weight?PCK_OK:PCK_BAD;
}
