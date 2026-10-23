/* UNRUN synthetic controls for the ACTUAL new native implementation.
 * No named ON model, acquired maps, tape, ledger, process or state input. */
#include "../generation.c"
#include <stdio.h>

#define TEST(ok) do {if(!(ok)){fprintf(stderr,"NATIVE_SYNTHETIC_REFUSAL line%u\n",(unsigned)__LINE__);return 1;}}while(0)
static int fresh(gn_work *w){return gn_work_init(w,GN_MAX_OPERATIONS,GN_MAX_SECONDS,NULL,NULL);}
static gn_context *small(gn_work *w,int *s){
    static const uint32_t a[8]={1,0,3,2,5,4,7,6};
    static const uint32_t c1[8]={2,3,0,1,6,7,4,5};
    static const uint32_t c2[8]={4,5,6,7,0,1,2,3};
    /* Positive original factors are NOT involutions and do not commute. */
    static const uint32_t factors[16]={1,2,0,3,4,5,6,7,2,1,3,4,0,5,6,7};
    gn_input in={8,2,a,{c1,c2},factors};return gn_create(&in,w,s);
}
static gn_context *prime_fixture(gn_work *w,int *s,uint32_t maps[800]){
    uint32_t x,local,base,p,t,shift,layer;gn_input in;
    for(x=0;x<200;++x){
        layer=x/50;local=x%50;base=local<19?0:19;p=local<19?19:31;t=local-base;shift=(p+1)/2;
        maps[x]=50*layer+base+(p-t)%p;
        maps[200+x]=50*(layer^1u)+local;maps[400+x]=50*(layer^2u)+local;
        maps[600+x]=50*layer+base+(t+shift)%p;
    }
    in.degree=200;in.factor_count=1;in.a=maps;in.endpoints[0]=maps+200;in.endpoints[1]=maps+400;in.factors=maps+600;
    return gn_create(&in,w,s);
}
int main(void){
    gn_work w,shortwork;gn_context *c,*p;gn_word word={0};
    gn_cycle cy19,cy31,bad,out19,out31;gn_batch batch;
    uint32_t x,y,z,maps[800],starts[2]={0,19},kind,size,i;uint8_t rev[2]={2,1},wrong[2]={1,2},single[1]={1},zero[1]={0};
    uint8_t tags[8]={0,4,6,9,8,5,14,10},badtag[8],bits[25],orbit_tags[200],orbit_bits[25];
    unsigned tests=0;int s,r;
    memset(&word,0,sizeof(word));word.length=1;word.letters[0]=1;
    TEST(fresh(&w)==GN_OK);c=small(&w,&s);TEST(c&&s==GN_OK);
    TEST(gn_virtual_b(c,rev,2,0,&x,&w)==GN_OK&&x==5);
    TEST(gn_virtual_b(c,wrong,2,0,&y,&w)==GN_OK&&y==2&&x!=y);++tests;
    TEST(gn_rotation_word(c,1,rev,2,&word,0,&x,&w)==GN_OK&&x==3);word.letters[0]=-1;
    TEST(gn_rotation_word(c,1,rev,2,&word,0,&x,&w)==GN_OK&&x==4);word.letters[0]=2;
    TEST(gn_rotation_word(c,1,rev,2,&word,0,&x,&w)==GN_OK&&x==7);word.letters[0]=-2;
    TEST(gn_rotation_word(c,1,rev,2,&word,0,&x,&w)==GN_OK&&x==4);++tests;
    TEST(gn_check_tree(c,1,rev,2,tags,8,3,&w)==GN_OK);++tests;
    memcpy(badtag,tags,8);badtag[6]=6;TEST(gn_check_tree(c,1,rev,2,badtag,8,3,&w)==GN_BAD);++tests;
    memcpy(badtag,tags,8);badtag[0]=4;TEST(gn_check_tree(c,1,rev,2,badtag,8,3,&w)==GN_BAD);++tests;
    memcpy(badtag,tags,8);badtag[3]=11;TEST(gn_check_tree(c,1,rev,2,badtag,8,3,&w)==GN_BAD);++tests;
    TEST(gn_check_tree(c,1,rev,2,tags,8,2,&w)==GN_BAD);++tests;
    TEST(gn_propose_orbit(c,1,rev,2,orbit_tags,8,orbit_bits,1,&kind,&size,&w)==GN_OK&&kind==GN_ROW_TREE&&size==3);++tests;
    word.letters[0]=3;TEST(gn_rotation_word(c,1,rev,2,&word,0,&x,&w)==GN_BAD);word.length=65;
    TEST(gn_rotation_word(c,1,rev,2,&word,0,&x,&w)==GN_BAD);word.length=1;word.letters[0]=1;++tests;
    TEST(gn_virtual_b(c,zero,1,0,&x,&w)==GN_BAD&&gn_virtual_b(c,rev,GN_MAX_CONJUGATOR+1u,0,&x,&w)==GN_BAD);++tests;
    TEST(gn_work_init(&shortwork,3,60,NULL,NULL)==GN_OK);
    TEST(gn_virtual_b(c,rev,2,0,&x,&shortwork)==GN_STOP&&shortwork.stopped&&shortwork.used==3);++tests;
    TEST(gn_batch_init(&batch,3,GN_MAX_ARTIFACT-5)==GN_OK);
    TEST(gn_batch_commit(&batch,&w,GN_ROW_CYCLES,3)==GN_OK&&batch.status[0]==GN_ROW_CYCLES);
    TEST(gn_batch_commit(&batch,&w,GN_ROW_TREE,3)==GN_STOP&&batch.tail_cause==GN_TAIL_BYTES&&batch.next==1&&batch.status[1]==GN_ROW_UNPAID&&batch.status[2]==GN_ROW_UNPAID);
    TEST(gn_batch_commit(&batch,&w,GN_ROW_SET,1)==GN_STOP);++tests;
    TEST(gn_batch_init(&batch,2,0)==GN_OK&&gn_batch_commit(&batch,&shortwork,GN_ROW_CYCLES,3)==GN_STOP&&batch.tail_cause==GN_TAIL_POINT_OR_TIME&&batch.status[0]==GN_ROW_UNPAID&&batch.status[1]==GN_ROW_UNPAID);++tests;
    TEST(!strcmp(gn_status_text(GN_ROW_SET),"NONGENERATING_INVARIANT_SET")&&!strcmp(gn_reason_text(GN_ROW_UNPAID,GN_TAIL_BYTES),"BOUNDED_PROPOSAL_UNPAID")&&!strcmp(gn_reason_text(GN_ROW_UNPAID,GN_TAIL_POINT_OR_TIME),"POINT_BUDGET"));++tests;
    TEST(fresh(&w)==GN_OK);p=prime_fixture(&w,&s,maps);TEST(p&&s==GN_OK);
    memset(&cy19,0,sizeof(cy19));memset(&cy31,0,sizeof(cy31));cy19.word=cy31.word=word;cy19.length=19;cy31.length=31;
    for(i=0;i<19;++i)cy19.vertices[i]=i;for(i=0;i<31;++i)cy31.vertices[i]=19+i;
    TEST(gn_check_cycle(p,1,single,1,&cy19,19,&w)==GN_OK);++tests;
    TEST(gn_check_cycle(p,2,single,1,&cy31,31,&w)==GN_OK);++tests;
    bad=cy19;bad.vertices[1]=bad.vertices[0];TEST(gn_check_cycle(p,1,single,1,&bad,19,&w)==GN_BAD);++tests;
    bad=cy19;bad.vertices[0]=1;bad.vertices[1]=0;TEST(gn_check_cycle(p,1,single,1,&bad,19,&w)==GN_BAD);++tests;
    bad=cy19;bad.length=18;TEST(gn_check_cycle(p,1,single,1,&bad,19,&w)==GN_BAD);++tests;
    TEST(gn_propose_cycles(p,1,single,1,&word,1,starts,2,64,&out19,&out31,&w)==GN_OK&&out19.length==19&&out31.length==31);++tests;
    z=0;TEST(gn_propose_cycles(c,1,rev,2,&word,1,&z,1,2,&out19,&out31,&w)==GN_MISS);++tests;
    memset(bits,0,sizeof(bits));for(i=0;i<100;++i)bits[i/8]|=(uint8_t)(1u<<(i%8));
    TEST(gn_check_subset(p,1,single,1,bits,25,100,&w)==GN_OK);++tests;
    TEST(gn_check_subset(p,1,single,1,bits,25,99,&w)==GN_BAD);++tests;
    memset(bits,0,sizeof(bits));bits[0]=1;TEST(gn_check_subset(p,1,single,1,bits,25,1,&w)==GN_BAD);++tests;
    TEST(gn_propose_orbit(p,1,single,1,orbit_tags,200,orbit_bits,25,&kind,&size,&w)==GN_OK&&kind==GN_ROW_SET&&size==38);++tests;
    gn_destroy(c);gn_destroy(p);r=gn_work_finish(&w);TEST(r==GN_OK&&tests==25);
    printf("{\"schema\":\"TEST_ONLY_L026_NATIVE_GENERATION_CONTROLS_V1\",\"tests\":%u,\"all_passed\":true,\"production_fit_acquired\":false}\n",tests);
    TEST(gn_work_finish(&w)==GN_OK);return 0;
}
