"""Mappings follow direct inspection of the actual 84 embedded outline classes.

The tail of mapsto is a separate glyph, so it is represented by U+22A2 without
merging or deleting the adjacent arrow/minus components. Raw text is untouched.
The printed code's literal hook extraction is retained, with its visual limit.
"""
RULES={
 '/UEQSDS+CMMI8':{'epsilon1':'ϵ'},
 '/VCYDRP+CMSY10':{'minus':'−','periodcentered':'·','multiply':'×','lessequal':'≤','greaterequal':'≥','similar':'∼','arrowright':'→','element':'∈','negationslash':'̸','mapsto':'⊢','intersection':'∩','floorleft':'⌊','floorright':'⌋','ceilingleft':'⌈','ceilingright':'⌉','braceleft':'{','braceright':'}','angbracketleft':'⟨','angbracketright':'⟩','bar':'|','wreathproduct':'≀'},
 '/MNRBOE+MSBM10':{'F':'𝔽'},
}
def output(r):
 v=RULES.get(r['font'],{}).get(r['glyph_name'])
 return v if v is not None and v!=r['decoded_text']else None
