"""Retain printed cells with font-size annotations; never normalize a mismatch."""
from pathlib import Path
from pypdf import PdfReader
import argparse
import hashlib
import json
import re

SPEC = [
    ('M11', 6, 2, [[11, 12, 55, 66, 165]],
     ['M^{10}', 'L^{2}(11)', 'M^{9} : 2', 'S^{5}', 'M^{8} :S^{3}']),
    ('M12', 9, 5, [[12, 12, 66, 66, 144, 220, 220], [396, 495, 495, 1320]],
     ['M^{11}', 'M^{11}', 'M^{10} : 2', 'M^{10} : 2', 'L^{2}(11)',
      'M^{9} : S^{3}', 'M^{9} : S^{3}', 'S^{5} × 2', '4^{2} : D^{12}',
      'M^{8} : S^{4}', 'A^{4} × S^{3}']),
    ('M22', 10, 6, [[22, 77, 176, 176, 231], [330, 616, 672]],
     ['L^{3}(4)', '2^{4} : A^{6}', 'A^{7}', 'A^{7}', '2^{4} : S^{5}',
      '2^{3} : L^{3}(2)', 'M^{10}', 'L^{2}(11)']),
    ('M23', 10, 7, [[23, 253, 253, 506], [1288, 1771, 40320]],
     ['M^{22}', 'L^{3}(4) : 2', '2^{4} : A^{7}', 'A^{8}', 'M^{11}',
      '2^{4} : (3 × A^{5}) : 2', '23 : 11']),
    ('J1', 11, 8, [[266, 1045, 1463], [1540, 1596, 2926, 4180]],
     ['L^{2}(11)', '2^{3} : 7 : 3', 'A^{5}× 2', '19 : 6', '11 : 10',
      'D^{6}×D^{10}', '7 : 6'])]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def annotated(page):
    chunks = []
    spans = []
    def visit(text, cm, tm, font, size):
        if text:
            spans.append(dict(text=text, cm=cm, tm=tm, size=size))
            chunks.append('^{' + text.strip() + '}' if 0 < size < 8 and text.strip() else text)
    page.extract_text(visitor_text=visit)
    return ''.join(chunks), spans


def cells(body):
    strings = re.sub(r'\s*–\s*', '-', body).split()
    result = []
    for cell in strings:
        entries = []
        for term in cell.split('-'):
            match = re.fullmatch(r'(\d+)(?:\^\{(\d+)\})?', term)
            need(match is not None, 'Literal positive suborbit token: ' + term)
            value = int(match.group(1))
            multiplicity = int(match.group(2) or '1')
            need(value > 0 and multiplicity > 0, 'Positive printed entry')
            entries.append([value, multiplicity])
        need(len({n for n, _ in entries}) == len(entries), 'No repeated printed length in a cell')
        result.append(dict(printed=cell, lengths=entries))
    return result


def extract(pdf_path):
    reader = PdfReader(pdf_path)
    page_data = {page: annotated(reader.pages[page - 1]) for page in [6, 9, 10, 11]}
    tables = []
    for name, page, number, blocks, labels in SPEC:
        lines = page_data[page][0].splitlines()
        start = next(i for i, line in enumerate(lines) if line.startswith('Table ' + str(number) + ':')) + 1
        cursor = start
        matrix = [[] for _ in labels]
        literal_rows = []
        for columns in blocks:
            need(lines[cursor] == ' '.join(map(str, columns)), 'Exact printed column header')
            cursor += 1
            for i, label in enumerate(labels):
                line = lines[cursor]
                need(line.startswith(label + ' '), 'Exact printed row label')
                parsed = cells(line[len(label) + 1:])
                need(len(parsed) == len(columns), 'Exact printed cell count')
                matrix[i].extend(parsed)
                literal_rows.append(line)
                cursor += 1
        indices = sum(blocks, [])
        need(len(matrix) == len(indices) and all(len(row) == len(indices) for row in matrix), 'Square source table')
        defects = [dict(row=i + 1, column=j + 1, printed=cell['printed'],
                        printed_sum=sum(n * m for n, m in cell['lengths']), column_index=indices[j])
                   for i, row in enumerate(matrix) for j, cell in enumerate(row)
                   if sum(n * m for n, m in cell['lengths']) != indices[j]]
        tables.append(dict(name=name, physical_page=page, table_number=number,
                           font_annotation='Small fonts marked ^{...}; group labels may be subscripts. Within numeric cells they are multiplicities, checked against native pages.',
                           row_labels=labels, column_indices=indices, literal_rows=literal_rows,
                           cells=matrix, printed_sum_defects=defects))
    return dict(source_pdf_sha256=hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
                tables=tables), page_data


def main(args):
    need(args.out.is_absolute() and not args.out.exists(), 'Fresh absolute extraction output')
    result, pages = extract(args.pdf)
    args.out.mkdir()
    (args.out / 'tables.json').write_text(json.dumps(result, indent=2) + '\n')
    for page, (text, spans) in pages.items():
        (args.out / ('page%02d.txt' % page)).write_text(text)
        (args.out / ('page%02d-spans.json' % page)).write_text(json.dumps(spans, indent=2) + '\n')
    print(json.dumps(dict(status='PRINTED_L036_SUBORBIT_TABLES_RETAINED',
                         cells=sum(len(t['cells'])**2 for t in result['tables']),
                         printed_sum_defects={t['name']: t['printed_sum_defects'] for t in result['tables']})))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    main(parser.parse_args())
