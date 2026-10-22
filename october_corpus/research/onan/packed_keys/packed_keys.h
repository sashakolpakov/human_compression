#ifndef L026_PACKED_KEYS_H
#define L026_PACKED_KEYS_H
#include <stddef.h>
#include <stdint.h>

/* Source-only representation core. The caller must authenticate the named
 * action, faithful base, complete involution class size, and full T generators.
 * Core success is not a Root acceptance or a generation decision. */
#define PCK_MAX_DEGREE 131072u
#define PCK_MAX_CLASS 2857239u
#define PCK_MAX_BASE 20u
#define PCK_MAX_FACTORS 16u
#define PCK_MAX_ENDPOINT 256u
#define PCK_MAX_WORD 8192u
#define PCK_MAX_KEY 43u

typedef struct pck_context pck_context;
typedef int (*pck_checkpoint)(void *argument);
typedef struct {
    uint32_t degree, target, base_length, factor_count, hash_bits;
    const uint32_t *base;       /* zero-based distinct points */
    const uint32_t *involution; /* complete actual a, zero-based images */
    const uint32_t *factors;    /* factor_count complete actual permutations */
    uint64_t operation_limit;
    pck_checkpoint checkpoint;
    void *checkpoint_argument;
} pck_input;
typedef struct {
    uint32_t first, weight;
    uint32_t ids[PCK_MAX_ENDPOINT];
    /* All generator edges in row-major order; factors supplied to close(). */
    uint32_t edges[PCK_MAX_ENDPOINT * PCK_MAX_FACTORS];
} pck_orbit;
typedef struct {
    uint32_t parent;
    uint8_t factor;  /* 0 only at identity conjugator; otherwise 1..factor_count */
    uint16_t depth;
    const uint8_t *key;
} pck_node;
enum { PCK_OK=0, PCK_OLD=1, PCK_STOP=2, PCK_BAD=-1, PCK_CAP=-2 };

pck_context *pck_create(const pck_input *input, int *status);
void pck_destroy(pck_context *context);
uint32_t pck_count(const pck_context *context);
uint32_t pck_key_bytes(const pck_context *context);
uint64_t pck_operations(const pck_context *context);
size_t pck_owned_bytes(const pck_context *context);
int pck_get_node(const pck_context *context, uint32_t id, pck_node *node);
/* Compute key(a^(g_parent * factor)). parent=0,factor=0 means a itself. */
int pck_key(pck_context *context,uint32_t parent,uint8_t factor,uint8_t *key);
/* Read-only dictionary lookup: complete packed-key equality, never hash alone. */
int pck_find(pck_context *context,const uint8_t *key,uint32_t *id);
/* One whole T orbit, or exact rollback of its newly inserted tail on stop/error.
 * endpoint_factors are positive codes in the authenticated factor catalogue.
 * On PCK_OLD no state changes. An interrupted orbit earns no new class nodes. */
int pck_close(pck_context *context,uint32_t parent,uint8_t factor,
              const uint8_t *endpoint_factors,uint32_t endpoint_generators,
              uint32_t endpoint_order,pck_orbit *orbit);
/* Streamed Saved verification of supplied nodes, WITHOUT a proposal/BFS.
 * Recomputes every full key from its supplied earlier parent/factor. The
 * complete orbit edge/reachability checks are a separate caller obligation. */
int pck_check_append(pck_context *context,uint32_t parent,uint8_t factor,
                     const uint8_t *key,uint32_t *id);
/* Saved-only complete orbit check: no node insertion or orbit proposal. Every
 * supplied generator edge is recomputed, and directed reachability from first
 * is checked. The caller must partition its entire accepted node prefix into
 * these consecutive, disjoint intervals and authenticate all record bytes. */
int pck_check_orbit(pck_context *context,const uint8_t *endpoint_factors,
                    uint32_t endpoint_generators,uint32_t endpoint_order,
                    const pck_orbit *orbit);
#endif
