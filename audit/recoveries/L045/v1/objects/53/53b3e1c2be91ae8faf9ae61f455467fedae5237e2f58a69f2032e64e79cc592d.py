"""Arithmetic and native-text controls for the written uniform proof.

These controls are not a finite replacement for its uniform arguments.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse
import hashlib
import json
import shutil
import subprocess
import time
from fractions import Fraction
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pin(path):
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def orthogonal_order(dimension, q, sign=1):
    if dimension % 2:
        m = (dimension - 1) // 2
        value = q ** (m * m)
        for j in range(1, m + 1):
            value *= q ** (2 * j) - 1
        return value  # projective conformal group in odd dimension
    m = dimension // 2
    value = 2 * q ** (m * (m - 1)) * (q ** m - sign)
    for j in range(1, m):
        value *= q ** (2 * j) - 1
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    out = args.out.resolve()
    need(not out.exists(), 'fresh output required')
    dependencies = json.loads((packet / 'dependencies.json').read_text())
    for entry in dependencies:
        path = Path(entry['path'])
        if not path.is_absolute():
            path = args.study / path
        need(pin(path) == {k: entry[k] for k in ('bytes', 'sha256')}, 'dependency ' + str(path))
    exports = []
    if (packet / 'manifest.json').exists():
        exports = json.loads((packet / 'manifest.json').read_text())['exports']
        for entry in exports:
            need(pin(packet / entry['path']) == {k: entry[k] for k in ('bytes', 'sha256')}, 'export ' + entry['path'])
    out.mkdir(parents=True)
    records = []
    for q in range(3, 52, 2):
        # Integer controls include prime powers and other odd integers.
        for d in range(2, 33):
            e = d * d // 4
            for sign in (1, -1):
                need(orthogonal_order(d, q, sign) < 3 * q ** (d * (d - 1) // 2), 'order bound')
            if d >= 5:
                need(2 * q ** e + 2 * q ** (e - 1) + 1 <= 3 * q ** e, 'identity adjustment')
            records.append(dict(q=q, dimension=d, kind='order-and-upper-factor'))
        need(q + 3 <= 3*q, 'dimension two')
        need(q*q + 1 <= 3*q*q, 'dimension three')
        for v in (q**4+q**3+2*q*q-q+1, q**4+q**3+q+1):
            need(v <= 3*q**4, 'dimension four')
        for m in range(3, 33):
            e = m*m//4
            need(2*(9*q**(2*e)+3*q**(m*(m-1)//2)) <= 24*q**(2*e), 'wreath bound')
            need(m*m//4+(m+1)*(m+1)//4 == m*(m+1)//2, 'odd dimension exponent')
            records.append(dict(q=q, m=m, kind='balanced-fixed-group-factor'))
        plus = Fraction(orthogonal_order(8,q,1), 2*orthogonal_order(4,q,1)**2)
        minus = Fraction(orthogonal_order(8,q,-1), orthogonal_order(4,q,1)*orthogonal_order(4,q,-1))
        need(plus == Fraction(q**8*(q*q+1)**2*(q**4+q*q+1),4), 'plus subspace identity')
        need(minus == Fraction(q**8*(q**4+1)*(q**4+q*q+1),2), 'minus subspace identity')
        need(plus.denominator == minus.denominator == 1, 'integer subspace counts')
        need(plus > Fraction(q**16,4) and minus > Fraction(q**16,2), 'strict lower margins')
        records.append(dict(q=q, kind='rank-four-subspace-counts', plus=int(plus), minus=int(minus)))
    (out/'arithmetic.json').write_text(json.dumps(records,indent=2)+'\n')
    native = out/'native'
    native.mkdir()
    shutil.copy2(packet/'odd_fixed_groups.tex', native/'odd_fixed_groups.tex')

    def run(name, command):
        begin = time.monotonic()
        with (native/(name+'.stdout')).open('wb') as so, (native/(name+'.stderr')).open('wb') as se:
            result = subprocess.run(command, cwd=native, stdout=so, stderr=se, timeout=45)
        receipt = dict(command=command, returncode=result.returncode, seconds=time.monotonic()-begin,
                       stdout=pin(native/(name+'.stdout')), stderr=pin(native/(name+'.stderr')))
        (native/(name+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
        need(result.returncode == 0 and receipt['stderr']['bytes']==0, 'clean '+name)

    for i in range(2):
        run('native'+str(i), ['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','odd_fixed_groups.tex'])
    log=(native/'odd_fixed_groups.log').read_text()
    need('Overfull' not in log and 'LaTeX Warning' not in log, 'native layout and references')
    from pypdf import PdfReader
    pdf=PdfReader(native/'odd_fixed_groups.pdf')
    text='\n'.join(page.extract_text() or '' for page in pdf.pages)
    (native/'text.txt').write_text(text)
    if (packet/'native_expected.txt').exists():
        need(text==(packet/'native_expected.txt').read_text(), 'exact native text')
    if args.render:
        run('raster', ['/opt/homebrew/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','odd_fixed_groups.pdf'])
    report=dict(status='PASS_WRITTEN_ODD_ORTHOGONAL_CONTROLS', exports=len(exports), dependencies=len(dependencies),
                arithmetic_records=len(records), native_pages=len(pdf.pages), mathematical_scope='Written uniform fixed-group bounds and rank-four subspace counts; no generation conclusion.',
                whole_original_credit=0, new_question_credit=0, measurement=None)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
