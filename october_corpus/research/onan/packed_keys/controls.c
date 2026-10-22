#include "packed_keys.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* UNRUN synthetic representation controls. No O'Nan fixture or target file. */
#define NEED(x) do { if(!(x)){fprintf(stderr,"control refusal at line %d\n",__LINE__);exit(1);} } while(0)
static unsigned passed=0;
static void pass(const char *name){++passed;printf("PASS %s\n",name);}
static int checkpoint(void *argument){return *(const int *)argument;}
static const uint32_t base[]={0,1,2};
static const uint32_t a[]={1,0,2,3};
static const uint32_t factors[]={1,2,3,0, 1,0,2,3};
static const uint8_t t[]={2};
static const uint8_t transposition_keys[6][7]={
    {1,0,0,0,8,0,0}, {2,0,2,0,0,0,0}, {3,0,2,0,8,0,0},
    {0,0,4,0,4,0,0}, {0,0,6,0,8,0,0}, {0,0,2,0,12,0,0}
};
static pck_input input(void){
    pck_input in={4,6,3,2,4,base,a,factors,UINT64_C(1000000),NULL,NULL};
    return in;
}
int main(void){
    pck_input in=input();pck_context *c,*saved,*bad,*stopped;
    pck_orbit orbits[6],trial;unsigned n=0,single=0,doubled=0,i,j;
    uint32_t id,old,count,mask=0;uint8_t key[PCK_MAX_KEY];pck_node node;
    int status,active=1;
    c=pck_create(&in,&status);NEED(c&&status==PCK_OK&&pck_key_bytes(c)==7);
    NEED(pck_owned_bytes(c)<4096);pass("fixed_small_allocation");
    NEED(pck_close(c,0,0,t,1,2,&orbits[n++])==PCK_OK);
    for(id=1;id<=pck_count(c);++id)for(j=1;j<=2;++j){
        status=pck_close(c,id,(uint8_t)j,t,1,2,&trial);
        NEED(status==PCK_OK||status==PCK_OLD);
        if(status==PCK_OK){NEED(n<6);orbits[n++]=trial;}
    }
    NEED(pck_count(c)==6&&n==4);pass("complete_S4_transposition_class");
    for(i=0;i<n;++i){
        if(orbits[i].weight==1)++single;
        else if(orbits[i].weight==2)++doubled;
        else NEED(0);
    }
    NEED(single==2&&doubled==2);pass("literal_endpoint_orbit_weights");
    for(id=1;id<=6;++id){
        NEED(pck_get_node(c,id,&node)==PCK_OK);
        for(j=0;j<6;++j)if(memcmp(node.key,transposition_keys[j],7)==0)break;
        NEED(j<6&&!(mask&(1u<<j)));mask|=1u<<j;
    }
    NEED(mask==63);pass("all_full_literal_keys_including_shared_first_image");
    for(i=0;i<n;++i)NEED(pck_check_orbit(c,t,1,2,&orbits[i])==PCK_OK);
    pass("every_complete_edge_and_reachability_check");
    saved=pck_create(&in,&status);NEED(saved&&status==PCK_OK);
    for(id=1;id<=6;++id){
        NEED(pck_get_node(c,id,&node)==PCK_OK);
        NEED(pck_check_append(saved,node.parent,node.factor,node.key,&old)==PCK_OK&&old==id);
    }
    for(i=0;i<n;++i)NEED(pck_check_orbit(saved,t,1,2,&orbits[i])==PCK_OK);
    pass("saved_supplied_nodes_and_edges_without_proposal");
    NEED(pck_get_node(c,6,&node)==PCK_OK);
    NEED(pck_check_append(saved,node.parent,node.factor,node.key,&old)==PCK_OLD&&pck_count(saved)==6);
    pass("saved_duplicate_last_node_is_refused");
    NEED(pck_check_append(saved,node.parent,0,node.key,&old)==PCK_BAD);
    pass("saved_invalid_parent_factor_pair_is_refused");
    NEED(pck_check_append(saved,0,0,transposition_keys[0],&old)==PCK_BAD);
    pass("second_root_is_refused");
    bad=pck_create(&in,&status);NEED(bad&&status==PCK_OK);
    memcpy(key,transposition_keys[0],7);key[6]|=128;
    NEED(pck_check_append(bad,0,0,key,&old)==PCK_BAD&&pck_count(bad)==0);
    pck_destroy(bad);pass("saved_key_padding_corruption_is_refused");
    for(i=0;i<n&&orbits[i].weight!=2;++i){}
    NEED(i<n);trial=orbits[i];trial.edges[0]=trial.first;
    NEED(pck_check_orbit(saved,t,1,2,&trial)==PCK_BAD);
    pass("in_range_wrong_edge_is_refused");
    trial=orbits[i];trial.ids[0]=trial.first+1;
    NEED(pck_check_orbit(saved,t,1,2,&trial)==PCK_BAD);
    pass("orbit_node_order_corruption_is_refused");
    {
        const uint32_t three[]={1,2,3,0, 1,0,2,3, 2,3,0,1};
        in=input();in.factor_count=3;in.factors=three;
        bad=pck_create(&in,&status);NEED(bad&&status==PCK_OK);
        NEED(pck_key(bad,0,0,key)==PCK_OK);
        NEED(pck_check_append(bad,0,0,key,&old)==PCK_OK&&old==1);
        NEED(pck_key(bad,1,3,key)==PCK_OK);
        NEED(pck_check_append(bad,1,3,key,&old)==PCK_OK&&old==2);
        memset(&trial,0,sizeof(trial));trial.first=1;trial.weight=2;
        trial.ids[0]=1;trial.ids[1]=2;trial.edges[0]=1;trial.edges[1]=2;
        NEED(pck_check_orbit(bad,t,1,2,&trial)==PCK_BAD);
        pck_destroy(bad);pass("closed_disconnected_union_is_refused");
    }
    {
        uint32_t malformed[]={0,0,2,3, 1,0,2,3};
        in=input();in.factors=malformed;bad=pck_create(&in,&status);
        NEED(!bad&&status==PCK_BAD);pass("non_permutation_factor_is_refused");
    }
    {
        uint32_t identity[]={0,1,2,3};
        in=input();in.involution=identity;bad=pck_create(&in,&status);
        NEED(!bad&&status==PCK_BAD);pass("identity_involution_is_refused");
    }
    {
        uint32_t *high=malloc((size_t)PCK_MAX_DEGREE*sizeof(*high));uint32_t zero=0;
        uint8_t one=1;NEED(high);
        for(id=0;id<PCK_MAX_DEGREE;++id)high[id]=id;
        high[0]=PCK_MAX_DEGREE-1;high[PCK_MAX_DEGREE-1]=0;
        in=input();in.degree=PCK_MAX_DEGREE;in.target=1;in.base_length=1;
        in.factor_count=1;in.hash_bits=2;in.base=&zero;in.involution=high;in.factors=high;
        bad=pck_create(&in,&status);NEED(bad&&status==PCK_OK);
        NEED(pck_close(bad,0,0,&one,1,2,&trial)==PCK_OK&&trial.weight==1);
        NEED(pck_get_node(bad,1,&node)==PCK_OK&&pck_key_bytes(bad)==3);
        NEED(node.key[0]==255&&node.key[1]==255&&node.key[2]==1);
        pck_destroy(bad);free(high);pass("seventeen_bit_boundary_and_zero_padding");
    }
    in=input();in.operation_limit=1;bad=pck_create(&in,&status);
    NEED(!bad&&status==PCK_STOP);pass("finite_operation_budget_is_enforced");
    in=input();in.checkpoint=checkpoint;in.checkpoint_argument=&active;
    stopped=pck_create(&in,&status);NEED(stopped&&status==PCK_OK);
    NEED(pck_close(stopped,0,0,t,1,2,&trial)==PCK_OK&&pck_count(stopped)==1);
    NEED(pck_get_node(stopped,1,&node)==PCK_OK);memcpy(key,node.key,7);
    while(pck_operations(stopped)<4084)NEED(pck_find(stopped,key,&old)==PCK_OK&&old==1);
    active=0;count=pck_count(stopped);
    NEED(pck_close(stopped,1,1,t,1,2,&trial)==PCK_STOP);
    NEED(pck_count(stopped)==count&&trial.weight==0&&trial.first==0);
    NEED(pck_find(stopped,key,&old)==PCK_OK&&old==1);
    pck_destroy(stopped);pass("interrupted_new_orbit_rolls_back_without_breaking_old_lookup");
    pck_destroy(saved);pck_destroy(c);
    NEED(passed==18);printf("COMPLETE_PACKED_KEYS_CONTROLS %u\n",passed);return 0;
}
