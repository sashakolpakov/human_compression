#ifndef L026_NATIVE_GENERATION_H
#define L026_NATIVE_GENERATION_H
#include <stdint.h>
#include <stddef.h>

/* NEW, UNRUN native implementation of the existing explicit proof checks.
 * The wrapper must authenticate the SAME original maps, selected full keys,
 * reverse-DAG words, endpoint weights and still-unpaid FREE row authority.
 * This kernel discovers no class, subgroup or row owner and pays no ledger. */
#define GN_MAX_DEGREE 122760u
#define GN_MAX_FACTORS 6u
#define GN_MAX_CONJUGATOR 8192u
#define GN_MAX_WORD 64u
#define GN_MAX_CYCLE 4096u
#define GN_MAX_PROPOSALS 128u
#define GN_MAX_STARTS 4u
#define GN_MAX_ROWS 128u
#define GN_MAX_OPERATIONS UINT64_C(200000000)
#define GN_MAX_SECONDS 60u
#define GN_MAX_ARTIFACT UINT64_C(16777216)
enum { GN_OK=0, GN_MISS=1, GN_STOP=2, GN_BAD=-1, GN_MEMORY=-2 };
enum { GN_ROW_UNPAID=0, GN_ROW_CYCLES=1, GN_ROW_TREE=2, GN_ROW_SET=3 };
enum { GN_TAIL_NONE=0, GN_TAIL_POINT_OR_TIME=1, GN_TAIL_BYTES=2 };
typedef int (*gn_checkpoint)(void *argument);
typedef struct {
    uint64_t used,limit,started_ns;
    uint32_t seconds;
    int stopped;
    gn_checkpoint checkpoint;
    void *checkpoint_argument;
} gn_work;
typedef struct {
    uint32_t degree,factor_count;
    const uint32_t *a,*endpoints[2],*factors;
} gn_input;
typedef struct gn_context gn_context;
typedef struct {uint8_t length;int8_t letters[GN_MAX_WORD];} gn_word;
typedef struct {gn_word word;uint32_t length,vertices[GN_MAX_CYCLE];} gn_cycle;
typedef struct {
    uint32_t selected,next,tail_cause;
    uint64_t bytes;
    uint8_t status[GN_MAX_ROWS];
} gn_batch;

int gn_work_init(gn_work *,uint64_t,uint32_t,gn_checkpoint,void *);
int gn_work_finish(gn_work *);
gn_context *gn_create(const gn_input *,gn_work *,int *);
void gn_destroy(gn_context *);
size_t gn_owned_bytes(const gn_context *);
int gn_virtual_b(const gn_context *,const uint8_t *,uint32_t,uint32_t,uint32_t *,gn_work *);
int gn_rotation_word(const gn_context *,uint32_t,const uint8_t *,uint32_t,const gn_word *,uint32_t,uint32_t *,gn_work *);
int gn_check_cycle(const gn_context *,uint32_t,const uint8_t *,uint32_t,const gn_cycle *,uint32_t,gn_work *);
int gn_propose_cycles(const gn_context *,uint32_t,const uint8_t *,uint32_t,const gn_word *,uint32_t,const uint32_t *,uint32_t,uint32_t,gn_cycle *,gn_cycle *,gn_work *);
int gn_check_subset(const gn_context *,uint32_t,const uint8_t *,uint32_t,const uint8_t *,size_t,uint32_t,gn_work *);
int gn_check_tree(const gn_context *,uint32_t,const uint8_t *,uint32_t,const uint8_t *,size_t,uint32_t,gn_work *);
/* Caller supplies degree bytes tags and ceil(degree/8) bytes bits. Only a
 * complete checked tree or proper closed set yields GN_OK and a row kind. */
int gn_propose_orbit(const gn_context *,uint32_t,const uint8_t *,uint32_t,uint8_t *,size_t,uint8_t *,size_t,uint32_t *,uint32_t *,gn_work *);
/* fixed_bytes MUST reserve the entire selection/scalar/envelope, including
 * every UNPAID tail row. proof_bytes is the actual prospective output extent.
 * Future wrapper must additionally measure the final whole artifact bundle. */
int gn_batch_init(gn_batch *,uint32_t,uint64_t);
int gn_batch_commit(gn_batch *,gn_work *,uint32_t,uint64_t);
const char *gn_status_text(uint32_t);
const char *gn_reason_text(uint32_t,uint32_t);
#endif
