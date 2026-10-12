"""Check displayed reader fractions directly from the accepted count cells."""
import re
from pathlib import Path
from pypdf import PdfReader
from arithmetic import read, need, dec, VAR, FORMS, UNITS

def check(p):
    cells = read(p/'inputs/author_counts.json')['documents']
    def values(v, f, u):
        c = {k:x['variants'][v][f][u] for k,x in cells.items()}
        return [dec(c['L050']+c['F017'], c['U_LCD']+c['A_L050']+c['A_F017'], 6),
                dec(c['L050'], c['A_L050'], 6), dec(c['F017'], c['A_F017'], 6)]
    expected = values('calibrated_selected','NFC',UNITS[2])
    for u in UNITS:
        expected += values('calibrated_selected','NFC',u)
    for v in VAR:
        for f in FORMS:
            expected += values(v,f,UNITS[2])
    text = (p/'reader.tex').read_text()
    need(re.findall(r'\b\d+\.\d{6}\b',text)==expected, 'all 36 displayed reader fractions')
    pages = PdfReader(p/'reader.pdf').pages
    need(len(pages)==3,'whole three-page reader')
    visible = ''.join(x.extract_text() for x in pages)
    need(re.findall(r'\b\d+\.\d{6}\b',visible)==expected,'all 36 actual PDF fractions')
    for claim in ['This is expansion', 'unknown, not zero', 'no software-inclusive factor',
                  'complete topic-wide', 'not a required premise', 'not newly solved']:
        need(claim in ' '.join(visible.split()), 'reader qualification '+claim)
    return {'displayed_fraction_occurrences':len(expected),'actual_PDF_pages':len(pages),
            'both_TeX_and_PDF_values':True,'scope_qualifications_present':True}

if __name__=='__main__':
    import sys,json
    print(json.dumps(check(Path(sys.argv[1])),indent=2))
