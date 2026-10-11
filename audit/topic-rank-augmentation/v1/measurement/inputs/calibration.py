"""L020-specific visible symbol rules; no font-name-only dispatch."""
from font_tools import need

def aliases_from(audit):
 out=[]
 for r in audit['L020']['encoded_glyph_classes']:
  ident=r['font_dictionary_object']['idnum'];byte=r['encoded_byte']
  if (ident,byte)==(51,71):
   need(r['font']=='/ZSYTRN+CMSY10' and r['glyph_name']=='G' and r['decoded_text']=='G' and r['occurrences']==111,'exact calligraphic G class');symbol='𝒢';reason='Visible Computer Modern math-calligraphic capital G, rather than roman G.'
  elif (ident,byte)==(109,78):
   need(r['font']=='/GEHQPJ+MSBM10' and r['glyph_name']=='N' and r['decoded_text']=='N' and r['occurrences']==1,'exact blackboard N class');symbol='ℕ';reason='Visible blackboard-bold capital N, rather than roman N.'
  else:continue
  out.append(dict(source='L020',font_identity=r['font_identity'],font_dictionary_object=r['font_dictionary_object'],font=r['font'],encoded_byte=byte,glyph_name=r['glyph_name'],input=r['decoded_text'],output=symbol,occurrences=r['occurrences'],kind='actual_visible_mathematical_alphabet',reason=reason,font_stream_sha256=r['font_stream_sha256'],outline_sha256=r['glyph_evidence']['outline_sha256']))
 need(len(out)==2 and sum(r['occurrences'] for r in out)==112,'two classes and112 occurrences');return out
