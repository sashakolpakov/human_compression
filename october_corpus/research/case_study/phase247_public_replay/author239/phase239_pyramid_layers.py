#!/usr/bin/env python3
"""The five-layer pyramid action and its fixed orientation quotient.

The general proof uses integer affine maps; finite flag checks below verify
that the coordinate convention agrees with the existing literal face poset.
"""
import itertools
import json
from pathlib import Path

IDENTITY = (1, 0, 0, 1)
REFLECTIONS = [(-1, 0, 0, 1), (0, 1, 1, 0), (1, 0, 0, -1)]
SHIFTS = [(1, 0), (0, 0), (0, 0)]
D_GENERATORS = [
    [3, 4, 1, 2, 5, 6, 7, 8, 9, 10],
    [1, 2, 5, 6, 3, 4, 8, 7, 10, 9],
    [1, 2, 3, 4, 7, 8, 5, 6, 10, 9],
    [2, 1, 4, 3, 6, 5, 9, 10, 7, 8],
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def multiply(a, b):
    return tuple(sum(a[2*i+k] * b[2*k+j] for k in range(2))
                 for i in range(2) for j in range(2))


def apply_matrix(a, v):
    return (a[0]*v[0] + a[1]*v[1], a[2]*v[0] + a[3]*v[1])


def matrices():
    result = [IDENTITY]
    for a in result:
        for r in REFLECTIONS:
            value = multiply(a, r)
            if value not in result:
                result.append(value)
    require(len(result) == 8, 'eight signed permutation matrices')
    return result


def layer_step(k, i):
    if k < 3-i:
        return k, i
    if k == 3-i:
        return k+1, None
    if k == 4-i:
        return k-1, None
    return k, i-1


def orientation_model():
    ds = matrices()
    labels = list(itertools.product(range(5), ds))
    index = {x: i for i, x in enumerate(labels)}
    generators = []
    for i in range(4):
        image = []
        for k, m in labels:
            target, r = layer_step(k, i)
            value = m if r is None else multiply(m, REFLECTIONS[r])
            image.append(index[target, value] + 1)
        generators.append(image)
    allowed = [index[k, m]+1 for k in [1, 2, 3] for m in ds
               if apply_matrix(m, (1, 1)) == (1, 1)]
    # The face-center translations for all D8 matrices have entries 0 or 1.
    center_shifts = []
    for m in ds:
        v = apply_matrix(m, (1, 1))
        require(all(x in [-1, 1] for x in v), 'signed row sums')
        shift = tuple((1-x)//2 for x in v)
        require(all(x in [0, 1] for x in shift), 'integer center translation')
        center_shifts.append(shift)
    return {'name': 'Pyramid_orientation_quotient', 'degree': 40,
            'generators': generators, 'matrices': ds,
            'middle_basepoints': [index[k, IDENTITY]+1 for k in [1, 2, 3]],
            'allowed_middle_images': allowed, 'center_shifts': center_shifts}


def affine_model(n):
    require(n >= 3, 'nondegenerate torus parameter')
    labels = list(itertools.product(range(5), range(n), range(n), matrices()))
    index = {x: i for i, x in enumerate(labels)}
    generators = []
    for i in range(4):
        image = []
        for k, x, y, m in labels:
            target, r = layer_step(k, i)
            if r is None:
                value = (target, x, y, m)
            else:
                u, v = apply_matrix(m, SHIFTS[r])
                value = (target, (x+u) % n, (y+v) % n,
                         multiply(m, REFLECTIONS[r]))
            image.append(index[value]+1)
        generators.append(image)
    return labels, {'name': f'Pyramid_square_torus_{n}_affine',
                    'degree': len(labels), 'generators': generators}


def literal_flag(label, n):
    k, x, y, m = label
    vertex = lambda a, b: (a % n) + n*(b % n)
    v = vertex(x, y)
    u = (m[0], m[2])
    edge = 2*vertex(x+min(0, u[0]), y+min(0, u[1])) + (u[0] == 0)
    face = vertex(x+min(0, m[0])+min(0, m[1]),
                  y+min(0, m[2])+min(0, m[3]))
    ordinary, cone = [v, edge, face, 0], [0, v, edge, face]
    j = 4-k
    return tuple(('b', ordinary[i]) if i < j else ('c', cone[i])
                 for i in range(4))


def verify_literal_bridge(n, literal_module):
    labels, affine = affine_model(n)
    flags = literal_module.build_flags(n)
    literal, flag_report = literal_module.analyze_flags(flags)
    index = {flag: i for i, flag in enumerate(flags)}
    bridge = [index[literal_flag(label, n)] for label in labels]
    require(len(set(bridge)) == len(flags), 'affine-to-face flag bijection')
    for i in range(4):
        require(all(bridge[affine['generators'][i][j]-1] ==
                    literal['generators'][i][bridge[j]]-1
                    for j in range(len(labels))), 'four adjacency intertwinings')
    orientation = orientation_model()
    small_index = {(k, m): j for j, (k, m) in
                   enumerate(itertools.product(range(5), matrices()))}
    projection = [small_index[k, m] for k, x, y, m in labels]
    for i in range(4):
        require(all(projection[affine['generators'][i][j]-1] ==
                    orientation['generators'][i][projection[j]]-1
                    for j in range(len(labels))), 'orientation flag projection')
    return {'n': n, 'flags': len(labels), 'literal_component_checks':
            flag_report['all_component_intersections'],
            'bijection_and_all_four_adjacencies': 'PASS',
            'orientation_projection': 'PASS'}


def gap_input(model):
    return ('s:=[' + ','.join('PermList('+str(a)+')' for a in model['generators']) + '];;\n'
            + 'middlePoints:=' + str(model['middle_basepoints']) + ';;\n'
            + 'allowedImages:=' + str(model['allowed_middle_images']) + ';;\n'
            + 'd:=[' + ','.join('PermList('+str(a)+')' for a in D_GENERATORS) + '];;\n')
