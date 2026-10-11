"""E-only occurrence/encoding rules, established by actual outline inspection.
Raw extraction remains available. Glyph pieces are never combined into formulas.
"""
from font_tools import need
# document, font dictionary object, encoded byte, input, output, count, kind
RULES=[
 ('L079',37,80,'P','𝒫',28,'mathematical_alphabet'),
 ('L083',26,80,'P','𝒫',19,'mathematical_alphabet'),
 ('L083',193,90,'Z','ℤ',2,'mathematical_alphabet'),
 ('L021',226,18,'\x12','(',4,'visible_delimiter'),
 ('L021',226,19,'\x13',')',4,'visible_delimiter'),
 ('L021',164,90,'Z','ℤ',6,'mathematical_alphabet'),
 ('L021',62,70,'F','ℱ',6,'mathematical_alphabet'),
 ('L021',62,77,'M','ℳ',84,'mathematical_alphabet'),
 ('L021',92,70,'F','ℱ',1,'mathematical_alphabet'),
 ('L056',16,80,'P','𝒫',1,'mathematical_alphabet'),
 ('L056',15,80,'P','𝒫',28,'mathematical_alphabet'),
 ('L056',15,55,'↦','∣',6,'mapsto_start_piece'),
 ('L043',73,80,'P','𝒫',35,'mathematical_alphabet'),
 ('L043',95,70,'F','𝔽',46,'mathematical_alphabet'),
 ('L043',73,55,'↦','∣',4,'mapsto_start_piece'),
 ('L043',172,56,'\uf8f1','⎧',1,'brace_piece'),
 ('L043',172,58,'\uf8f3','⎩',1,'brace_piece'),
 ('L043',172,60,'\uf8f2','⎨',1,'brace_piece'),
 ('L043',172,62,'\uf8f4','⎪',2,'brace_piece')]
REASONS={
 'mathematical_alphabet':'Visible calligraphic or blackboard-bold letter; roman extraction alias corrected only for this actual font dictionary and byte.',
 'visible_delimiter':'Actual embedded CMEX outline is an opening or closing parenthesis, not a control character.',
 'mapsto_start_piece':'Actual CMSY byte55 is only the leading vertical stroke with a short right stub; use the declared single vertical-piece proxy U+2223. The separately printed right-arrow is unchanged. No joining of pieces or recovery of placement/graphic cost is claimed.',
 'brace_piece':'Actual embedded CMEX outline is the named brace component; preserve each component as one Unicode piece. No assembly or layout reconstruction.'}
def aliases_from(audit):
 out=[]
 for doc,obj,byte,inp,sym,count,kind in RULES:
  hits=[r for r in audit[doc]['encoded_glyph_classes'] if r['font_dictionary_object']['idnum']==obj and r['encoded_byte']==byte]
  need(len(hits)==1,'unique dictionary-byte class '+str((doc,obj,byte)));r=hits[0]
  need(r['decoded_text']==inp and r['occurrences']==count,'exact alias input and count '+str((doc,obj,byte)))
  need(r['glyph_evidence']['kind']=='embedded_Type1_outline' and r['glyph_evidence']['visible'],'actual visible embedded glyph')
  out.append(dict(source=doc,font_identity=r['font_identity'],font_dictionary_object=r['font_dictionary_object'],font_dictionary_sha256=r['font_dictionary_sha256'],effective_encoding_sha256=r['effective_encoding_sha256'],font=r['font'],encoded_byte=byte,glyph_name=r['glyph_name'],input=inp,output=sym,occurrences=count,kind=kind,reason=REASONS[kind],font_stream_sha256=r['font_stream_sha256'],outline_sha256=r['glyph_evidence']['outline_sha256']))
 need(len(out)==19 and sum(r['occurrences'] for r in out)==279,'nineteen actual classes /279 occurrences');return out
