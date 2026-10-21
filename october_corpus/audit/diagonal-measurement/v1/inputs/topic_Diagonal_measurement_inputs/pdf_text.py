"""Keep literal PDF extraction, recording generated newline metadata separately.

pypdf's crlf_space_check explicitly appends one synthetic newline to a
visitor callback. A CMEX left angle bracket can itself decode as newline;
the synthetic character must not be mistaken for that visible glyph.
Nothing in the returned extracted text is deleted or rewritten here.
"""
import inspect,hashlib
from contextlib import contextmanager
import pypdf
import pypdf._text_extraction._text_extractor as backend
from font_tools import need
BANNER='arXiv:2608.23223v1  [math.CO]  24 Aug 2026'

@contextmanager
def generated_newline_context(state):
 original=backend.crlf_space_check;signature=inspect.signature(original)
 state['pypdf_crlf_source_sha256']=hashlib.sha256(inspect.getsource(original).encode()).hexdigest()
 def wrapped(*args,**kwargs):
  bound=signature.bind(*args,**kwargs);visitor=bound.arguments['visitor_text']
  if visitor:
   def marked(text,*rest):
    need(text.endswith('\n'),'pinned crlf helper appends one newline');previous=state.get('generated_final_newline',False);state['generated_final_newline']=True
    try:return visitor(text,*rest)
    finally:state['generated_final_newline']=previous
   bound.arguments['visitor_text']=marked
  return original(*bound.args,**bound.kwargs)
 backend.crlf_space_check=wrapped
 try:yield
 finally:backend.crlf_space_check=original

def extract(pdf,source=False):
 texts=[];fonts=[];pages=[];at=0;generated=[];duplicates=[];state={}
 with generated_newline_context(state):
  for n,page in enumerate(pypdf.PdfReader(pdf).pages,1):
   chunks=[];local=[];position=0
   def visitor(t,cm,tm,f,size):
    nonlocal position
    if source and n==1 and f is None and t==BANNER and chunks and chunks[-1]==t:
     duplicates.append(dict(page=1,text=t,role='Repeated Form visitor callback; returned extraction and actual text stream each contain the banner once.'));return
    chunks.append(t);local.extend([str(f.get('/BaseFont',f.get('/Name',''))) if f else '']*len(t))
    if state.get('generated_final_newline') and t:generated.append(at+position+len(t)-1)
    position+=len(t)
   t=page.extract_text(visitor_text=visitor) or '';need(t==''.join(chunks) and len(t)==len(local),'literal extraction/visitor metadata alignment')
   pages.append(dict(page=n,start=at,end=at+len(t),sha256=hashlib.sha256(t.encode()).hexdigest(),empty_extraction=not t));at+=len(t)+1;texts.append(t);fonts.extend(local);fonts.append('')
 raw='\n'.join(texts);fonts=fonts[:-1]
 need(all(raw[i]=='\n' for i in generated),'only actual appended newline metadata')
 need(len(duplicates)==int(source),'exact one known Form wrapper duplicate for source only')
 return raw,fonts,pages,dict(generated_newline_offsets=generated,duplicate_callbacks=duplicates,pypdf_crlf_source_sha256=state['pypdf_crlf_source_sha256'],returned_extraction_changed=False)
