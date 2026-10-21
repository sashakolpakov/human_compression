"""Six observed script/fraktur classes; actual occurrence dictionaries stay bound."""
SCRIPT={'D':'𝒟','E':'ℰ','H':'ℋ','O':'𝒪'}
FRAKTUR={'M':'𝔐','X':'𝔛'}
def output(row):
 if 'CMSY' in row['font']:return SCRIPT.get(row['glyph_name'])
 if 'EUFM' in row['font']:return FRAKTUR.get(row['glyph_name'])
 return None
