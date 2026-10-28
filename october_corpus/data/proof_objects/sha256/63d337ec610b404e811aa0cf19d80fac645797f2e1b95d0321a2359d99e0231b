"""UNTRUSTED bounded orbit-prefix supplier. Author /root/middle_dictionary_author.
Only supplied certificates checked independently by subset_kernel gain authority.
False cursors can omit work or propose bad sets; they cannot create paid credit.
"""

def need(ok, why):
    if not ok:
        raise ValueError(why)


def cursor(note, index, owner, digest, n, cap, seed, work):
    work.charge(128, 'whole_untrusted_subset_cursor_header')
    if note is None:
        return dict(free_index=index, owner=owner, witness_row_sha256=digest,
                    points=[seed], next_vertex=0, next_generator=0, outcome='unfinished')
    need(type(note) is dict and set(note) == {'free_index', 'owner', 'witness_row_sha256',
         'points', 'next_vertex', 'next_generator', 'outcome'}, 'exact untrusted cursor fields')
    need(type(note['free_index']) is int and type(note['owner']) is int
         and note['free_index'] == index and note['owner'] == owner and
         note['witness_row_sha256'] == digest, 'same exact original witness cursor')
    points = note['points']
    work.charge(n + 32 * len(points) if type(points) is list else n,
                'whole_untrusted_point_prefix_shape_and_slot_checks')
    need(type(points) is list and 1 <= len(points) <= cap and points[0] == seed,
         'bounded original-point prefix begins at fixed seed')
    seen = bytearray(n)
    for p in points:
        need(type(p) is int and 0 <= p < n and not seen[p], 'distinct original cursor points')
        seen[p] = 1
    head, edge, outcome = note['next_vertex'], note['next_generator'], note['outcome']
    need(type(head) is int and type(edge) is int and 0 <= head <= len(points)
         and edge in (0, 1) and outcome in ('unfinished', 'closed_hint', 'cap_miss'),
         'bounded untrusted two-edge cursor')
    need((outcome == 'closed_hint' and head == len(points) and edge == 0) or
         (outcome != 'closed_hint' and head < len(points)), 'coherent untrusted frontier status')
    return dict(note, points=list(points))


def explore(K, ctx, paths, note, work, cap):
    """Mutate only after a whole returned edge; caller preserves pre-edge cursor."""
    if note['outcome'] != 'unfinished':
        return
    work.charge(ctx['n'] + 8 * len(note['points']), 'complete_supplier_membership_slots')
    seen = bytearray(ctx['n'])
    for point in note['points']:
        seen[point] = 1
    while note['next_vertex'] < len(note['points']):
        head, edge = note['next_vertex'], note['next_generator']
        work.charge(48, 'orbit_prefix_whole_preedge_and_postedge_cursor_reserve')
        target = K['rotation_word'](ctx, paths, [edge + 1], note['points'][head], work)
        if not seen[target]:
            if len(note['points']) == cap:
                note['outcome'] = 'cap_miss'
                return
            seen[target] = 1
            note['points'].append(target)
        if edge == 0:
            note['next_generator'] = 1
        else:
            note['next_generator'] = 0
            note['next_vertex'] += 1
    note['outcome'] = 'closed_hint'
