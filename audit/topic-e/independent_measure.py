"""Independently recount the full documents by recognizing page furniture.

Uses no author extraction spans or metric function. Requires pypdf 6.13.0.
Primary PDFs are supplied privately and are never copied to the report.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata
from pypdf import PdfReader
import pypdf

HERE = Path(__file__).resolve().parent


def need(ok, text):
    if not ok:
        raise ValueError(text)


def measurements(text, form):
    text = unicodedata.normalize(form, text)
    tokens = text.split()
    collapsed = ' '.join(tokens)
    return {'whitespace_tokens':len(tokens),
            'alphanumeric_units':len(re.findall(r'[^\W_]+',text)),
            'characters_without_whitespace':len(''.join(tokens)),
            'characters_with_collapsed_whitespace':len(collapsed),
            'utf8_bytes_with_collapsed_whitespace':len(collapsed.encode()),
            'collapsed_text_sha256':sha256(collapsed.encode()).hexdigest()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sources-root',type=Path,required=True)
    ap.add_argument('--artifacts-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args = ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'Use a fresh output.')
    protocol = json.loads((HERE/'protocol.json').read_text())
    author = json.loads((HERE/'author_measurement.json').read_text())
    need(pypdf.__version__=='6.13.0','Pinned extraction version required.')
    costs, removals, pages_record = {}, {}, {}
    for key, binding in (protocol['sources']|protocol['ours']).items():
        root = args.sources_root if key in protocol['sources'] else args.artifacts_root
        path = root/binding['path']
        need(sha256(path.read_bytes()).hexdigest()==binding['pdf_sha256'],'Changed PDF: '+key)
        pages = PdfReader(path).pages
        need(len(pages)==binding['pages'],'Page count: '+key)
        clean, discarded = [], []
        for i, page in enumerate(pages,1):
            text = page.extract_text() or ''
            if key=='L079':
                if i==1:
                    clean.append(text)
                    continue
                first, newline, remainder = text.partition('\n')
                need(bool(newline),'Missing header line.')
                marker = 'Ars Mathematica Contemporanea x (xxxx) 1–x'
                need(first in (f'{i} {marker}',f'{marker} {i}'),'Unexpected repeated header.')
                discarded.append({'page':i,'kind':'repeated journal/page header'})
                clean.append(remainder)
            else:
                body, newline, footer = text.rpartition('\n')
                need(bool(newline) and footer==str(i),'Unexpected isolated footer: '+key)
                discarded.append({'page':i,'kind':'page number'})
                clean.append(body)
        text = '\n'.join(clean)
        costs[key] = {form:measurements(text,form) for form in ('NFC','NFKC')}
        need(costs[key]==author['costs'][key],'Independent costs differ: '+key)
        removals[key] = discarded; pages_record[key] = len(pages)
    comparisons = {}
    for form in ('NFC','NFKC'):
        comparisons[form] = {}
        for metric in protocol['metrics']:
            value = {k:v[form][metric] for k,v in costs.items()}
            numerator = value['L083']+value['L079']
            denominator = value['U_E']+value['A1']+value['A2']
            with_code = denominator+value['Code']
            saved = author['comparisons'][form][metric]
            need(numerator==saved['full_source_manuscripts'] and
                 denominator==saved['replacement_complete_manuscripts'] and
                 with_code==saved['replacement_complete_manuscripts_and_required_code'],
                 'Comparison inputs differ.')
            comparisons[form][metric] = {'numerator':numerator,'written_denominator':denominator,
                'written_and_required_code_denominator':with_code,
                'written_factor':numerator/denominator,'known_artifact_factor':numerator/with_code}
    report = {'status':'PASS','scope':'Independent full-document arithmetic and furniture recognition; relies on the existing principal-result proof admissions.',
        'pypdf':pypdf.__version__,'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'protocol_sha256':sha256((HERE/'protocol.json').read_bytes()).hexdigest(),
        'author_measurement_sha256':sha256((HERE/'author_measurement.json').read_bytes()).hexdigest(),
        'costs':costs,'page_counts':pages_record,'removed_furniture':removals,
        'comparisons':comparisons,'exact_all_artifact_factor':None,
        'historical_program_cost':None,'external_library_unconditional_cost':None,
        'new_mathematical_credit':0}
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(comparisons['NFC'][protocol['primary']['metric']],indent=2))


if __name__=='__main__':
    main()
