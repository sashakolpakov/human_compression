from pathlib import Path
import hashlib,json,shutil,subprocess
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');P=S/'corpus106_L071_remaining_censuses_v1';W=Path(__file__).resolve().parent/'native';W.mkdir(exist_ok=False)
reports=[]
for name in ('remaining_censuses','source_orbit_comparison'):
    D=W/name;D.mkdir();T=D/(name+'.tex');shutil.copyfile(P/T.name,T)
    for i in (1,2):
        r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',T.name],cwd=D,capture_output=True)
        (D/f'build{i}.log').write_bytes(r.stdout+r.stderr);assert r.returncode==0
    F=T.with_suffix('.pdf');pages=[p.extract_text() for p in PdfReader(F).pages];assert pages==[p.extract_text() for p in PdfReader(P/F.name).pages]
    r=subprocess.run(['/opt/homebrew/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pngalpha','-r100',f'-sOutputFile={D}/page%02d.png',str(F)],capture_output=True);assert r.returncode==0
    reports.append(dict(name=name,pages=len(pages),page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in pages],exact_frozen_pdf_text_match=True))
(W.parent/'native_report.json').write_text(json.dumps(dict(status='PASS_FRESH_NATIVE_BUILD',reports=reports),indent=2)+'\n');print(json.dumps(reports))
