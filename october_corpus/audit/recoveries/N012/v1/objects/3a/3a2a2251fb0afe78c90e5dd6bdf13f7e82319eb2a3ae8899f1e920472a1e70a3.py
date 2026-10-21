"""Direct multiplication certificate; needs only the Python standard library."""
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError("Validation requires Python assertions; optimized Python is unsupported.")
import ast
import json
import re

HERE = Path(__file__).resolve().parent

def identity():
    return [[int(i == j) for j in range(6)] for i in range(6)]

def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(6)) % 3
             for j in range(6)] for i in range(6)]

def evaluate(word, marks):
    result = identity()
    for letter in word:
        assert letter in [-3, -2, -1, 1, 2, 3]
        result = multiply(result, marks[abs(letter)-1])
    return result

def check():
    a = identity()
    a[0][0] = a[5][5] = 2
    a[1][0] = a[4][5] = 1
    b = [[int(i+j == 5) for j in range(6)] for i in range(6)]
    c = [[int(i+j == 4 and i < 5 and j < 5)
          for j in range(6)] for i in range(6)]
    c[5][5] = 2
    marks = [a, b, c]
    assert all(multiply(m, m) == identity() for m in marks)
    assert multiply(a,b) == multiply(b,a)
    word = ast.literal_eval((HERE/'h6_3_word_letters_v2.g').read_text())
    assert len(word) == 131
    target = identity()
    target[1][0] = 1
    assert evaluate(word, marks) == target
    tex = (HERE/'finite_H.tex').read_text()
    block = re.search(r'\\begin\{center\}\\small\\ttfamily\n(.*?)\\end\{center\}', tex, re.S)
    literal = re.sub(r'\\par|\s', '', block.group(1))
    assert literal == ''.join('abc'[abs(i)-1] for i in word)
    assert evaluate(word[:-1], marks) != target
    assert evaluate([], marks) != target
    wrong_target = identity()
    wrong_target[0][1] = 1
    assert evaluate(word, marks) != wrong_target
    return {'status':'PASS', 'field':3, 'dimension':6, 'word_length':131,
            'target':'I + E21', 'tex_literal_exact':True,
            'damaged_controls':3, 'group_order_premise':False, 'Lean':False}

if __name__ == '__main__':
    print(json.dumps(check(),indent=2))
