"""Check the supplied matrix relations and the attributed quotient bound."""
import argparse, hashlib, json, os, resource, signal, stat, sys, time
from pathlib import Path

I = bytes(int(i == j) for i in range(7) for j in range(7))
BOUND = 600415200
G2_ORDER = 376611192619200
CASE_MARKS_SHA256 = '6b03795da646d44b9c46b1a9880ec860a3e2347b915ab0eb12cbf6adeead312f'

def need(value, reason):
    if not value:
        raise ValueError(reason)

class Work:
    def __init__(self):
        self.started = time.monotonic()
        self.products = self.linear = 0
    def tick(self):
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        need(rss <= 112 * 2**20 and time.monotonic() - self.started < 90,
             '112 MiB and 90 second cooperative limits')
    def scalar(self, count):
        self.tick()
        need(type(count) is int and count >= 0 and self.linear + count <= 200000,
             'shared scalar budget')
        self.linear += count
    def multiply(self, a, b):
        self.tick()
        need(self.products < 400000, 'shared matrix product budget')
        self.products += 1
        return bytes(sum(a[7*i+k] * b[7*k+j] for k in range(7)) % 11
                     for i in range(7) for j in range(7))

def matrix(value, work):
    work.scalar(49)
    need(type(value) is list and len(value) == 7 and
         all(type(row) is list and len(row) == 7 for row in value) and
         all(type(x) is int and 0 <= x < 11 for row in value for x in row),
         'canonical seven by seven matrix over F11')
    return bytes(x for row in value for x in row)

def power(value, exponent, identity, work):
    need(type(exponent) is int and exponent >= 0, 'fixed nonnegative exponent')
    result = identity
    while exponent:
        if exponent & 1:
            result = work.multiply(result, value)
        exponent //= 2
        if exponent:
            value = work.multiply(value, value)
    return result

def word_value(g, word, work):
    need(type(word) is list and 1 <= len(word) <= 15 and
         all(type(x) is int and 0 <= x < 4 for x in word), 'bounded typed word')
    value = I
    for label in word:
        value = work.multiply(value, g[label])
    return value

def relators(g, work):
    need(type(g) in (tuple, list) and len(g) == 4, 'four matrices')
    work.scalar(196)
    need(all(type(x) is bytes and len(x) == 49 and all(v < 11 for v in x) for x in g),
         'whole canonical matrices')
    for x in g:
        need(work.multiply(x, x) == I, 'involution relation')
    for i, j in ((0, 2), (0, 3), (1, 3)):
        need(work.multiply(g[i], g[j]) == work.multiply(g[j], g[i]),
             'distant generators commute')
    for i, j, exponent in ((0, 1, 5), (1, 2, 3), (2, 3, 5)):
        need(power(work.multiply(g[i], g[j]), exponent, I, work) == I,
             'adjacent Coxeter relation')
    need(power(word_value(g, [0, 1, 2], work), 5, I, work) == I,
         'LEFT hemi relation')
    need(BOUND < G2_ORDER, 'strict order comparison')

def original_marks(value, work):
    need(type(value) is list and len(value) == 4, 'four original marks')
    g = tuple(matrix(x, work) for x in value)
    need(len(set(g)) == 4 and all(x != I for x in g),
         'distinct nonidentity original marks')
    return g

def strict(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    def bad(_):
        raise ValueError('integer JSON only')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=bad, parse_constant=bad)

def whole(path):
    work_limit = 131072
    before = path.lstat()
    need(path.is_absolute() and path.resolve(strict=True) == path and
         stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
         before.st_size <= work_limit, 'bounded regular certificate before read')
    signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink,
                           s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        raw = stream.read(before.st_size + 1)
        closed = os.fstat(stream.fileno())
    need(signature(before) == signature(opened) == signature(closed) ==
         signature(path.lstat()) and len(raw) == before.st_size,
         'same-FD whole certificate and exact EOF')
    return raw

def rows(g):
    return [list(g[7*i:7*i+7]) for i in range(7)]

def permutation(p):
    return bytes(int(p[i] == j) for i in range(7) for j in range(7))

def controls(work):
    names = []
    def yes(name, value):
        need(value, name)
        names.append(name)
    def no(name, call):
        try:
            call()
        except ValueError:
            names.append(name)
        else:
            raise ValueError('expected refusal: ' + name)
    work.scalar(20000)
    x = permutation([1, 0, 2, 3, 4, 5, 6])
    y = permutation([0, 2, 1, 3, 4, 5, 6])
    z = permutation([1, 2, 3, 4, 0, 5, 6])
    g = (x, y, I, I)
    relators((I, I, I, I), work)
    yes('trivial representation satisfies the pure presentation', True)
    no('original identity rejected', lambda: original_marks([rows(I)] * 4, work))
    no('original repetition rejected', lambda: original_marks([rows(x)] * 4, work))
    xy = work.multiply(x, y)
    yes('noncommuting products', xy != work.multiply(y, x))
    yes('noncommuting order three', xy != I and power(xy, 3, I, work) == I)
    yes('wrong square', power(xy, 2, I, work) != I)
    yes('order five', z != I and power(z, 5, I, work) == I)
    yes('wrong order five square', power(z, 2, I, work) != I)
    yes('zero power', power(z, 0, I, work) == I)
    yes('word order', word_value(g, [0, 1], work) == xy)
    yes('inverse word', work.multiply(word_value(g, [0, 1, 2], work),
                                     word_value(g, [2, 1, 0], work)) == I)
    no('boolean exponent', lambda: power(x, True, I, work))
    no('negative exponent', lambda: power(x, -1, I, work))
    no('word extent', lambda: word_value(g, [0] * 16, work))
    no('boolean label', lambda: word_value(g, [True], work))
    no('outside label', lambda: word_value(g, [4], work))
    no('noninvolution', lambda: relators((z, I, I, I), work))
    no('adjacent relation', lambda: relators((x, I, I, I), work))
    no('hemi relation with all Coxeter relations satisfied', lambda: relators((x, x, x, x), work))
    no('matrix extent', lambda: relators((I[:-1], I, I, I), work))
    no('field byte', lambda: relators((bytes([11]) + I[1:], I, I, I), work))
    no('boolean field', lambda: matrix([[True] * 7 for _ in range(7)], work))
    no('duplicate JSON', lambda: strict(b'{"x":1,"x":2}'))
    no('floating JSON', lambda: strict(b'{"x":1.25}'))
    need(len(names) == len(set(names)) == 24, 'all 24 controls')
    return names

def main():
    need(sys.dont_write_bytecode and not sys.flags.optimize, 'run with -B and without -O')
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('100 seconds')))
    signal.alarm(100)
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    work = Work()
    if args.controls:
        result = dict(status='PASS', controls=controls(work), original_cases=0)
    else:
        p = Path(__file__).resolve().with_name('certificate.json')
        raw = whole(p)
        data = strict(raw)
        need(set(data) == {'schema', 'original_job', 'position', 'original_row_id', 'marks'},
             'complete certificate schema')
        need(data['schema'] == 'F004_LITERAL_535_LEFT_HEMI_MATRIX_CERTIFICATE_V1' and
             data['original_job'] == [20, 4] and type(data['position']) is int and
             data['position'] == 200 and data['original_row_id'] == 'job0020:position0200:J00277',
             'recorded original tuple')
        marks_raw = (json.dumps(data['marks'], sort_keys=True, separators=(',', ':')) + '\n').encode()
        need(hashlib.sha256(marks_raw).hexdigest() == CASE_MARKS_SHA256,
             'exact supplied original matrix tuple')
        relators(original_marks(data['marks'], work), work)
        need(whole(p) == raw, 'whole input reread')
        result = dict(status='PASS', position=200, matrix_relations_verified=True,
                      generated_group_order_at_most=BOUND,
                      cannot_generate_a_group_isomorphic_to_G2_11=True,
                      universal_presentation_bound_is_attributed_theorem_input=True)
    work.tick()
    result.update(matrix_products=work.products, linear_units=work.linear)
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
