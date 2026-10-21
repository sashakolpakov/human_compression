#!/usr/bin/env python3
"""Count the complete available authored text; export counts and boundaries only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def binding(path, root):
    data = path.read_bytes()
    return dict(path=str(path.relative_to(root)), bytes=len(data), sha256=digest(data))


def displayed(text):
    # Tool link annotations are not characters authored by the original authors.
    pattern = r'\ue200cite\ue202[^†\ue201]*†([^†\ue201]*)(?:†[^\ue201]*)?\ue201'
    result = re.sub(pattern, lambda m: m[1], text)
    require('\ue200' not in result and '\ue201' not in result and '\ue202' not in result,
            'Uninterpreted tool annotation in authored body')
    return result


def body(record, spec):
    matches = list(re.finditer(r'(?m)^L(\d+): ?(.*)$', record))
    first, last = spec['first_body_line'], spec['last_body_line']
    selected = [m for m in matches if first <= int(m[1]) <= last]
    require([int(m[1]) for m in selected] == list(range(first, last + 1)),
            'Exactly one occurrence of every authored-body line, in order')
    require(len(selected) == spec['expected_body_lines'], 'Complete original body')
    lines = [displayed(m[2]) for m in selected]
    text = '\n'.join(lines)
    return text, [dict(line=int(m[1]), start=m.start(2), end=m.end(2),
                       sha256=digest(m[2].encode()), displayed_sha256=digest(s.encode()))
                  for m, s in zip(selected, lines)]


def measures(text, normalization):
    s = unicodedata.normalize(normalization, text)
    collapsed = ' '.join(s.split())
    return dict(whitespace_tokens=len(s.split()),
                alphanumeric_units=len(re.findall(r'[^\W_]+', s)),
                characters_without_whitespace=sum(not c.isspace() for c in s),
                characters_with_collapsed_whitespace=len(collapsed),
                utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
                collapsed_text_sha256=digest(collapsed.encode()))


def extract(study, policy):
    documents = {}
    for original, spec in policy['originals'].items():
        old = study / spec['historical_record']
        fresh = study / spec['fresh_record']
        text, spans = body(old.read_text(), spec)
        fresh_text, fresh_spans = body(fresh.read_text(), spec)
        require(text == fresh_text, original + ': fresh complete body differs')
        before_trailer_cut = text
        cuts = []
        if spec.get('non_author_trailer'):
            trailer = spec['non_author_trailer']
            require(text.count(trailer) == 1 and text.endswith(trailer),
                    'Exactly one platform trailer, at end of body')
            text = text[:-len(trailer)].rstrip()
            require(text.endswith('pcara@vub.ac.be'), 'Final author address preserved')
            cuts.append(dict(reason='nonauthor platform trailer', exact_text=trailer,
                             first_codepoint=len(text), last_codepoint=len(before_trailer_cut),
                             removed_codepoints=len(before_trailer_cut)-len(text)))
        require('Abstract' in text and 'References' in text, 'Both front matter and bibliography')
        if original == 'N001':
            require(text.startswith('Some properties of inductively minimal geometries') and
                    '[11]' in text and 'pcara@vub.ac.be' in text and
                    all('Lemma ' + str(i) in text for i in range(1, 8)),
                    'N001 entire authored body through final reference and addresses')
        else:
            require(text.startswith('J. geom. 71 (2001)') and '[10]' in text and
                    text.endswith('Received 12 October 1999; revised 25 March 2000.'),
                    'L108 entire authored body through final reference, addresses and dates')
        controls = {}
        for c in text:
            if unicodedata.category(c).startswith('C'):
                label = 'U+' + format(ord(c), '04X')
                controls[label] = controls.get(label, 0) + 1
        documents[original] = dict(
            representation='complete_literal_authored_rendering',
            primary_url=spec['primary_url'],
            original_PDF_retrieved=False,
            historical_record=binding(old, study), fresh_record=binding(fresh, study),
            historical_body_spans=spans, fresh_body_spans=fresh_spans,
            complete_body_sha256=digest(text.encode()),
            pre_trailer_cut_sha256=digest(before_trailer_cut.encode()),
            pre_trailer_cut_metrics={form: measures(before_trailer_cut, form)
                                     for form in policy['normalizations']},
            nonauthor_trailer_cuts=cuts,
            complete_body_codepoints=len(text), body_lines=len(spans),
            fresh_complete_body_identical=True, printed_pages=spec['printed_pages'],
            running_furniture_removed=False, nonprinting_characters=controls,
            metrics={form: measures(text, form) for form in policy['normalizations']},
            unmeasured_graphics_cost=None, full_original_PDF_glyph_identity_verified=False)
    return documents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'Fresh count output')
    policy = json.loads((HERE / 'policy.json').read_text())
    documents = extract(args.study_root.resolve(), policy)
    result = dict(status='AUTHOR_LITERAL_RENDERING_INPUT_COUNTS_PENDING_REVIEW',
                  policy_sha256=digest((HERE / 'policy.json').read_bytes()),
                  implementation_sha256=digest(Path(__file__).read_bytes()),
                  documents=documents, original_manuscripts=2, metric_cells=20,
                  source_PDF_claim=False, factors_admitted=False,
                  source_or_question_credit_added=False, primary_body_exported=False)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v['metrics']['NFC'] for k, v in documents.items()}))


if __name__ == '__main__':
    main()
