#!/usr/bin/env python3
"""Verify current documentation and its exact programme51 historical boundary."""
from pathlib import Path, PurePosixPath
from decimal import Decimal, ROUND_HALF_UP
import argparse, ast, hashlib, json, re
from pypdf import PdfReader

def need(value, message):
    if not value:
        raise ValueError('CURRENT DOCUMENTATION: ' + message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def validate_text(readme, tex, topics):
    required = ['51 accessible originals', '54 await mathematical recovery',
                'fifty-one individual', 'first twenty-six', '19',
                'audit/overview/v17/packet/reader.pdf',
                'Executable software is excluded symmetrically',
                'there is no software-inclusive factor',
                'there is no pooled factor', 'expansion', 'L022']
    # The count19 is supplied by the parsed topic table, rather than a prose numeral.
    for phrase in required:
        if phrase != '19':
            need(phrase.lower() in readme.lower(), 'current README statement: ' + phrase)
    need(len(topics) == 19 and sum(len(row['original_ids']) for row in topics) == 51,
         'nineteen topics/fifty-one originals')
    need(len({oid for row in topics for oid in row['original_ids']}) == 51,
         'each measured original appears once')
    for row in topics:
        expected = str((Decimal(row['accepted_factor']['numerator']) /
                        Decimal(row['accepted_factor']['denominator'])).quantize(
                            Decimal('.000001'), rounding=ROUND_HALF_UP))
        need(row['display'] == expected, 'accepted factor display ' + row['topic'])
        block = (f"   * - `{row['title']} <{row['guide']}>`_\n"
                 f"     - {', '.join(row['original_ids'])}\n     - {expected}\n")
        need(readme.count(block) == 1, 'exact current topic row ' + row['topic'])
    for phrase in ['106=51', '54', '55', 'v17', 'L022', 'no current software-inclusive factor',
                   'No missing cost is interpreted', 'not assert reproduction of every assertion',
                   'Successful compilation and declaration counts do not establish complete source']:
        need(phrase in ' '.join(tex.split()), 'protocol scope: ' + phrase)
    need('R_A^{\\rm required}' not in tex and 'audit/overview/v3/' not in tex and
         'current totals are 34' not in tex, 'no obsolete current protocol formulas or counts')

def verify(root, allow_proposal=False):
    root = Path(root)
    base = 'audit/documentation/v1/'
    def read(path):
        return json.loads((root/path).read_text())
    def bind(row):
        name = row['path']; path = PurePosixPath(name)
        need(not path.is_absolute() and '..' not in path.parts and str(path) == name,
             'safe document binding')
        data = (root/path).read_bytes()
        need(len(data) == row['bytes'] and digest(data) == row['sha256'], 'exact bytes ' + name)
    admission = read(base+'admission.json')
    status = admission['status']
    need(status == 'ROOT_ADOPTED_CURRENT_DOCUMENTATION' or
         (allow_proposal and status == 'PRIVATE_TEST_DOCUMENTATION_STAGE'), 'root adoption required')
    if not allow_proposal:
        for key in ['author_manifest', 'root_review']:
            row=admission.get(key)
            need(isinstance(row,dict), 'missing adoption evidence: '+key)
            bind(row)
        author=read(admission['author_manifest']['path'])
        parent=Path(admission['author_manifest']['path']).parent
        for row in author['exports']:
            bind(dict(row,path=str(parent/row['path'])))
        review=read(admission['root_review']['path'])
        need('ACCEPT' in review.get('status',''), 'root document review not accepted')
    for key in ['replacement_documents', 'historical_documents', 'supporting_files', 'accepted_programme']:
        for row in admission[key]:
            bind(row)
    boundary = read(base+'packet/boundary.json')
    need(boundary['base_commit'] == 'f0633645938bea9861d07500d86f70f7696a8e22',
         'exact committed programme51 baseline')
    need(boundary['no_new_mathematical_or_numerical_admission'] and
         boundary['public_writer'] == 'root' and boundary['whole_source_formalized'] is False,
         'documentation-only scope')
    for row in boundary['preserved_scripts']:
        bind(row)
    actual_ast = {node.name: digest(ast.dump(node, include_attributes=False).encode())
                  for node in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name != 'main'}
    need(len(boundary['old_nonmain_ASTs']) == 128 and
         all(actual_ast.get(name) == value for name, value in boundary['old_nonmain_ASTs'].items()),
         'all128 prior non-main verifier functions unchanged')
    table = read(base+'packet/topic_table.json')['topics']
    overview = read('audit/overview/v17/packet/results.json')
    for row, original in zip(table, overview['topics']):
        need(row['topic'] == original['topic'] and row['original_ids'] == original['source_ids'] and
             row['accepted_factor'] == original['written'], 'only accepted current values')
        need((root/row['guide']).is_file(), 'current topic guide')
    corpus = read('audit/corpus/latest.json')
    need((corpus['currently_measured_originals'], corpus['accessible_pending_complete_recovery'],
          corpus['editorial_originals'], corpus['archived_unavailable_originals']) == (51, 54, 1, 55),
         'current51 partition')
    need(corpus['editorial_original_ids'] == ['L022'] and corpus['editorial_factor'] is None and
         corpus['source_retrieval_in_scope'] is False, 'editorial and archived scope')
    readme = (root/'README.rst').read_text(); tex = (root/'audit/protocol.tex').read_text()
    validate_text(readme, tex, table)
    links=[]
    for target in re.findall(r'<([^<>\n]+)>`_', readme):
        need(not re.match(r'\w+://', target), 'local reproducible documentation links')
        need((root/target).exists(), 'README target: ' + target); links.append(target)
    for target in re.findall(r'\\href\{([^{}]+)\}', tex):
        target = target.replace('\\_', '_')
        need((root/'audit'/target).exists(), 'protocol target: ' + target); links.append(target)
    pages = [page.extract_text() or '' for page in PdfReader(root/'audit/protocol.pdf').pages]
    need([digest(text.encode()) for text in pages] == boundary['protocol_page_text_sha256'],
         'exact rendered protocol page texts')
    need(len(pages) == boundary['protocol_pages'], 'complete protocol')
    return dict(status='PASS_CURRENT_DOCUMENTATION' if not allow_proposal else 'PASS_PRIVATE_DOCUMENTATION_STAGE',
                measured=51, mathematical_pending=54, editorial=1, archived=55, topics=19,
                overview_comparisons_preserved=70, topic_table_rows=19, protocol_pages=len(pages),
                checked_local_links=len(links), preserved_verifier_functions=128,
                new_measurement=False, public_adoption_checked=not allow_proposal)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--allow-proposal', action='store_true')
    args=parser.parse_args()
    print(json.dumps(verify(args.repo, args.allow_proposal), indent=2))
