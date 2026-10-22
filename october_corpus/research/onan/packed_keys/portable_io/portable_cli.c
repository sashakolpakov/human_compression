/* New explicit IO/closed-parent transport. Compile THIS translation unit,
 * not a separately rewritten kernel. Frozen included source is unchanged. */
#include "../packed_keys.c"
#include <stdio.h>
#include <errno.h>
#include <time.h>
#include <sys/resource.h>

#define IO_MAX_TAPE UINT64_C(402653184)
#define IO_MAX_NEW 65536u
typedef struct {uint32_t count,orbits,cursor,next;} state;
typedef struct {uint64_t left;} reader;
static clock_t begun;
static uint32_t tape_blocks;
static int bounded(unsigned seconds){
    struct rusage r;uint64_t rss;clock_t now=clock();
    if(now==(clock_t)-1||now-begun>(clock_t)(seconds*CLOCKS_PER_SEC))return 0;
    if(getrusage(RUSAGE_SELF,&r))return 0;
#if defined(__APPLE__)
    rss=(uint64_t)r.ru_maxrss;
#else
    rss=(uint64_t)r.ru_maxrss*1024u;
#endif
    return rss<=UINT64_C(402653184);
}
static int budget(void *unused){(void)unused;return bounded(20);}
static void die(const char *message){fprintf(stderr,"PACKED_IO_REFUSAL %s\n",message);exit(1);}
static void need(int yes,const char *message){if(!yes)die(message);}
static void get(void *p,size_t n,reader *r){
    if(r){need(n<=r->left,"bounded input extent");r->left-=n;}
    need(fread(p,1,n,stdin)==n,"whole exact input bytes");
}
static uint8_t r8(reader *r){uint8_t b;get(&b,1,r);return b;}
static uint16_t r16(reader *r){uint16_t n=r8(r);return n|((uint16_t)r8(r)<<8);}
static uint32_t r32(reader *r){uint32_t n=0;unsigned i;for(i=0;i<4;++i)n|=(uint32_t)r8(r)<<(8*i);return n;}
static uint64_t r64(reader *r){uint64_t n=0;unsigned i;for(i=0;i<8;++i)n|=(uint64_t)r8(r)<<(8*i);return n;}
static void put(FILE *f,const void *p,size_t n){need(fwrite(p,1,n,f)==n,"complete output write");}
static void w8(FILE *f,uint8_t n){put(f,&n,1);}
static void w16(FILE *f,uint16_t n){w8(f,(uint8_t)n);w8(f,(uint8_t)(n>>8));}
static void w32(FILE *f,uint32_t n){unsigned i;for(i=0;i<4;++i)w8(f,(uint8_t)(n>>(8*i)));}
static void marker(reader *r,const char *expected){char b[8];get(b,8,r);need(memcmp(b,expected,8)==0,"exact wire magic");}
static int same(state a,state b){return a.count==b.count&&a.orbits==b.orbits&&a.cursor==b.cursor&&a.next==b.next;}
static state rs(reader *r){state s;s.count=r32(r);s.orbits=r32(r);s.cursor=r32(r);s.next=r32(r);return s;}
static void ws(FILE *f,state s){w32(f,s.count);w32(f,s.orbits);w32(f,s.cursor);w32(f,s.next);}
static void valid_state(state s,uint32_t ng,uint32_t target){
    need(s.count<=target&&s.orbits<=s.count&&s.cursor>=1&&s.cursor<=s.count+1u&&s.next<ng,
      "bounded exact state coordinates");
    need(s.cursor!=s.count+1u||s.next==0,"exhausted queue generator coordinate");
    need(s.count!=0||(s.orbits==0&&s.cursor==1&&s.next==0),"sole empty state");
}
static void advance(state *s,uint32_t ng){if(++s->next==ng){s->next=0;++s->cursor;}}
static int at(state s,uint32_t p,uint32_t f,const uint8_t *ambient){return s.cursor==p&&ambient[s.next]==f;}
static void verify_old_transitions(pck_context *c,state *s,uint32_t stop_cursor,
                                  uint32_t stop_next,const uint8_t *ambient,uint32_t ng){
    uint8_t key[PCK_MAX_KEY];uint32_t id;
    need(s->cursor<stop_cursor||(s->cursor==stop_cursor&&s->next<=stop_next),"monotone supplied transition prefix");
    while(s->cursor!=stop_cursor||s->next!=stop_next){
        need(s->cursor<=pck_count(c),"supplied transition has actual parent");
        need(pck_key(c,s->cursor,ambient[s->next],key)==PCK_OK,"verify supplied old-transition word");
        need(pck_find(c,key,&id)==PCK_OK&&id!=0,"every skipped supplied transition already known");
        advance(s,ng);
    }
}
/* Exact closed-parent authority is an explicit external premise. This is NOT
 * a new-word verifier: it restores already-accepted keys without re-evaluating
 * every historical word, while checking the complete portable record grammar. */
static void restore_closed_node(pck_context *c,uint32_t parent,uint8_t factor,
                                uint16_t depth,const uint8_t *key,uint32_t want){
    uint32_t id,slot,j,x,b,bit;int status;
    need(want==pck_count(c)+1u&&parent<want,"closed parent exact next/earlier node");
    need(want==1?(parent==0&&factor==0&&depth==0):
      (parent>=1&&factor>=1&&factor<=c->in.factor_count&&depth==(uint32_t)c->depths[parent]+1u&&depth<=PCK_MAX_WORD),
      "closed parent exact word fields");
    for(j=0;j<c->in.base_length;++j){
        x=0;for(b=0;b<17;++b){bit=17*j+b;if(key[bit/8]&(1u<<(bit%8)))x|=1u<<b;}
        need(x<c->in.degree,"closed parent packed point domain");
    }
    for(bit=17*c->in.base_length;bit<8*c->stride;++bit)need(!(key[bit/8]&(1u<<(bit%8))),"closed parent zero padding");
    status=append(c,parent,factor,key,&id,&slot);
    need(status==PCK_OK&&id==want&&pck_count(c)==want,"closed parent full-key uniqueness");
}
static void read_orbit(pck_context *c,reader *r,int verify,state *s,
                       const uint8_t *tg,uint32_t nt,uint32_t order,
                       const uint8_t *ambient,uint32_t ng){
    pck_orbit o;uint32_t i,j,parent,id;uint8_t factor,key[PCK_MAX_KEY],reserved;uint16_t depth;
    memset(&o,0,sizeof(o));o.first=r32(r);o.weight=r16(r);
    need(r8(r)==nt,"exact endpoint generator count");reserved=r8(r);need(!reserved,"zero orbit reserved byte");
    need(o.first==pck_count(c)+1&&o.weight>=1&&o.weight<=order&&order%o.weight==0,"consecutive bounded orbit");
    for(i=0;i<o.weight;++i){
        parent=r32(r);factor=r8(r);depth=r16(r);get(key,c->stride,r);id=o.first+i;
        if(verify&&i==0){
            if(s->count==0)need(parent==0&&factor==0,"first supplied identity seed");
            else{
                uint32_t which=0;while(which<ng&&ambient[which]!=factor)++which;
                need(which<ng,"supplied seed is an actual ambient transition");
                verify_old_transitions(c,s,parent,which,ambient,ng);
                need(at(*s,parent,factor,ambient),"exact supplied seed cursor");
            }
        }
        if(verify){
            need(pck_check_append(c,parent,factor,key,&j)==PCK_OK&&j==id,"every new supplied word/key and distinctness");
            need(c->depths[id]==depth,"exact supplied depth");
        }else restore_closed_node(c,parent,factor,depth,key,id);
        o.ids[i]=id;
    }
    for(i=0;i<o.weight;++i)for(j=0;j<nt;++j){
        id=r32(r);need(id>=o.first&&id-o.first<o.weight,"whole internal edge target");o.edges[(size_t)i*nt+j]=id;
    }
    if(verify){
        need(pck_check_orbit(c,tg,nt,order,&o)==PCK_OK,"all supplied new edges and reachability");
        if(s->count!=0)advance(s,ng);
    }
    s->count=pck_count(c);++s->orbits;
}
static void read_tape(pck_context *c,reader *r,int verify,state *s,const char digest[64],
                      const uint8_t *tg,uint32_t nt,uint32_t order,const uint8_t *ambient,uint32_t ng,
                      uint32_t maxnodes,uint32_t maxorbits){
    char got[64];state start,end;uint32_t nodes,orbits,stop,i,before;
    while(r->left){
        need(tape_blocks<65536,"finite accepted tape block count");++tape_blocks;
        marker(r,"PCKBLK01");get(got,64,r);need(memcmp(got,digest,64)==0,"same exact input digest in every block");
        start=rs(r);end=rs(r);nodes=r32(r);orbits=r32(r);stop=r32(r);
        need(same(start,*s)&&nodes>=1&&nodes<=IO_MAX_NEW&&orbits>=1&&orbits<=nodes&&
          end.count-start.count==nodes&&end.orbits-start.orbits==orbits&&stop>=1&&stop<=4,
          "entire block header and nonempty bounded extension");
        if(verify){
            need(nodes<=maxnodes&&orbits<=maxorbits,"whole same declared producer chunk limits");
            if(stop==1)need(nodes+order>maxnodes,"literal prospective node-cap stop");
            if(stop==2)need(orbits==maxorbits,"literal orbit-cap stop");
        }
        valid_state(end,ng,c->in.target);before=pck_count(c);
        for(i=0;i<orbits;++i)read_orbit(c,r,verify,s,tg,nt,order,ambient,ng);
        need(pck_count(c)-before==nodes,"all declared new nodes exactly consumed");
        if(verify)verify_old_transitions(c,s,end.cursor,end.next,ambient,ng);
        s->cursor=end.cursor;s->next=end.next;
        need(same(*s,end),"whole resulting block coordinates");
        marker(r,"PCKEND01");need(r32(r)==end.count&&r32(r)==end.orbits,"whole block footer");
        need((stop==4)==(end.count==c->in.target),"complete means exact full class mass");
        need(budget(NULL),"bounded parent/new-tape IO CPU and RSS");
    }
}
static void write_orbit(FILE *f,pck_context *c,const pck_orbit *o,uint32_t nt){
    uint32_t i,j; pck_node n;
    w32(f,o->first);w16(f,(uint16_t)o->weight);w8(f,(uint8_t)nt);w8(f,0);
    for(i=0;i<o->weight;++i){
        need(pck_get_node(c,o->first+i,&n)==PCK_OK,"exact committed output node");
        w32(f,n.parent);w8(f,n.factor);w16(f,n.depth);put(f,n.key,pck_key_bytes(c));
    }
    for(i=0;i<o->weight;++i)for(j=0;j<nt;++j)w32(f,o->edges[(size_t)i*nt+j]);
}
static uint32_t number(const char *p,uint32_t upper){
    char *end;unsigned long n;errno=0;need(p&&*p&&*p!='-'&&*p!='+',"unsigned decimal argument");
    n=strtoul(p,&end,10);need(!errno&&!*end&&n>=1&&n<=upper,"bounded decimal argument");return (uint32_t)n;
}
int main(int argc,char **argv){
    reader r;uint64_t input_size,parent_size,suffix_size,product=1,grouporder,centralizer;char digest[64];
    pck_input in;uint32_t *storage,*base,*indices,*a,*other,*factors;
    uint32_t i,j,x,nt,ng,order,maxnodes,maxorbits,stop=0,parentblocks;uint8_t tg[16],ambient[16];
    pck_context *c;state s={0,0,1,0},start; pck_orbit orbit;int status,check,synthetic,moved_other=0;FILE *out=NULL;long endpos;
    begun=clock();need(begun!=(clock_t)-1,"process CPU clock");
    need(argc==6&&(!strcmp(argv[1],"produce")||!strcmp(argv[1],"check")||
      !strcmp(argv[1],"control-produce")||!strcmp(argv[1],"control-check")),"mode digest output maxnodes maxorbits");
    synthetic=!strncmp(argv[1],"control-",8);check=!strcmp(argv[1],"check")||!strcmp(argv[1],"control-check");
    need(strlen(argv[2])==64,"input digest length");
    for(i=0;i<64;++i)need((argv[2][i]>='0'&&argv[2][i]<='9')||(argv[2][i]>='a'&&argv[2][i]<='f'),"lowercase input digest");
    memcpy(digest,argv[2],64);maxnodes=number(argv[4],IO_MAX_NEW);maxorbits=number(argv[5],IO_MAX_NEW);
    marker(NULL,"PCKFEED1");input_size=r64(NULL);need(input_size<=16777216,"bounded full exported input");r.left=input_size;
    marker(&r,"PCKIN001");memset(&in,0,sizeof(in));
    in.degree=r32(&r);in.target=r32(&r);in.base_length=r32(&r);in.factor_count=r32(&r);in.hash_bits=r32(&r);
    order=r32(&r);nt=r32(&r);ng=r32(&r);
    grouporder=r64(&r);centralizer=r64(&r);
    need(grouporder>=2&&centralizer>=1&&grouporder%centralizer==0&&grouporder/centralizer==in.target,"exact class denominator");
    need(in.degree>=2&&in.degree<=131072&&in.target>=1&&in.target<=2857239&&in.base_length>=1&&in.base_length<=20&&
      in.factor_count>=3&&in.factor_count<=16&&in.hash_bits>=2&&in.hash_bits<=23&&order>=1&&order<=256&&nt>=1&&nt<=8&&ng==2&&
      in.factor_count==ng+nt&&maxnodes>=order,"exact production dimensions and prospective chunk room");
    if(synthetic)need(in.degree==4&&in.target==6&&grouporder==24&&centralizer==4&&order==2,"literal S4 synthetic-only domain");
    else need(in.degree==122760&&in.target==2857239&&in.hash_bits==23&&grouporder==UINT64_C(460815505920)&&centralizer==161280&&
      (order==144||order==256),"actual named production action/order/class");
    storage=calloc((size_t)(2+in.factor_count)*in.degree+2*in.base_length,sizeof(uint32_t));need(storage!=NULL,"bounded actual input storage");
    base=storage;indices=base+in.base_length;a=indices+in.base_length;other=a+in.degree;factors=other+in.degree;
    for(i=0;i<in.base_length;++i)base[i]=r32(&r);
    for(i=0;i<in.base_length;++i){indices[i]=r32(&r);need(indices[i]>=2&&indices[i]<=in.degree&&product<=UINT64_MAX/indices[i],"strict finite chain index");product*=indices[i];}
    need(product==grouporder,"complete strict base index product");
    for(i=0;i<ng;++i){ambient[i]=r8(&r);need(ambient[i]==i+1,"original ordered ambient factor codes");}
    for(i=0;i<nt;++i){tg[i]=r8(&r);need(tg[i]==ng+i+1,"original ordered endpoint factor codes");}
    for(i=0;i<(2+in.factor_count)*in.degree;++i){a[i]=r32(&r);need(a[i]<in.degree,"whole exported point label");}
    need(r.left==0,"exact exported input EOF");
    for(i=0;i<in.degree;++i){need(other[other[i]]==i&&a[other[i]]==other[a[i]],"actual c involution and endpoint commutation");if(other[i]!=i)moved_other=1;}
    need(moved_other,"nonidentity c");
    for(j=0;j<nt;++j)for(i=0;i<in.degree;++i){x=factors[(size_t)(tg[j]-1)*in.degree+i];
        need(factors[(size_t)(tg[j]-1)*in.degree+a[i]]==a[x]&&factors[(size_t)(tg[j]-1)*in.degree+other[i]]==other[x],"every endpoint factor fixes a,c");}
    need(memcmp(a,other,(size_t)in.degree*4)!=0,"distinct endpoint involutions");
    in.base=base;in.involution=a;in.factors=factors;in.operation_limit=UINT64_C(1000000000000);in.checkpoint=budget;
    c=pck_create(&in,&status);need(c&&status==PCK_OK,"create exact fixed-memory core");
    parent_size=r64(NULL);need(parent_size<=IO_MAX_TAPE,"bounded whole borrowed parent tape");r.left=parent_size;
    read_tape(c,&r,0,&s,digest,tg,nt,order,ambient,ng,maxnodes,maxorbits);start=s;parentblocks=tape_blocks;
    if(check){
        suffix_size=r64(NULL);need(suffix_size>=1&&suffix_size<=16777216,"bounded exact new supplied suffix");r.left=suffix_size;
        read_tape(c,&r,1,&s,digest,tg,nt,order,ambient,ng,maxnodes,maxorbits);
        need(tape_blocks==parentblocks+1&&s.count>start.count,"one exact nonempty supplied new closed block");
    }else{
        need(tape_blocks<65536,"space for one new atomic tape block");
        out=fopen(argv[3],"wbx");need(out!=NULL,"fresh exclusive suffix file");
        put(out,"PCKBLK01",8);put(out,digest,64);ws(out,start);ws(out,start);w32(out,0);w32(out,0);w32(out,0);
        while(s.count<in.target){
            if(!budget(NULL)){stop=3;break;}
            if(s.count-start.count+order>maxnodes){stop=1;break;}
            if(s.orbits-start.orbits>=maxorbits){stop=2;break;}
            need(s.cursor<=s.count||(s.count==0&&s.cursor==1),"complete seed frontier not prematurely exhausted");
            if(s.count==0)status=pck_close(c,0,0,tg,nt,order,&orbit);
            else status=pck_close(c,s.cursor,ambient[s.next],tg,nt,order,&orbit);
            if(status==PCK_STOP){stop=3;break;}
            need(status==PCK_OK||status==PCK_OLD,"complete new orbit or existing seed");
            if(status==PCK_OK){write_orbit(out,c,&orbit,nt);if(s.count!=0)advance(&s,ng);s.count=pck_count(c);++s.orbits;}
            else advance(&s,ng);
        }
        if(s.count==in.target)stop=4;
        need(s.count>start.count&&stop>=1,"no empty/half-orbit checkpoint claim");
        put(out,"PCKEND01",8);w32(out,s.count);w32(out,s.orbits);endpos=ftell(out);
        need(endpos>0&&endpos<=16777216&&fseek(out,88,SEEK_SET)==0,"bounded whole suffix and exact header position");
        ws(out,s);w32(out,s.count-start.count);w32(out,s.orbits-start.orbits);w32(out,stop);
        need(fflush(out)==0&&fclose(out)==0,"whole suffix close");
        ++tape_blocks;
    }
    need(fgetc(stdin)==EOF&&!ferror(stdin),"entire authenticated feed consumed");
    valid_state(s,ng,in.target);need(bounded(100),"final total100s/RSS384MiB core budget");
    printf("{\"blocks\":%u,\"complete\":%s,\"count\":%u,\"cursor\":%u,\"new_count\":%u,\"new_orbits\":%u,\"next\":%u,\"orbits\":%u,\"parent_count\":%u,\"parent_orbits\":%u,\"proposal_search\":%s,\"synthetic_only\":%s}\n",
      tape_blocks,s.count==in.target?"true":"false",s.count,s.cursor,s.count-start.count,s.orbits-start.orbits,s.next,s.orbits,start.count,start.orbits,check?"false":"true",synthetic?"true":"false");
    need(fflush(stdout)==0,"whole scalar result");pck_destroy(c);free(storage);return 0;
}
