"""Topic D visible glyph identities, independently read from its fonts/pages.

Every application is additionally bound to an exact occurrence in the input
specifications. Whitespace is never replaced: direct PDF text-operator inspection
confirms that all whitespace in these three source extractions is layout.
"""
BRACE_PIECES = {'\uf8f1':'⎧', '\uf8f2':'⎨', '\uf8f3':'⎩', '\uf8f4':'⎪'}

def glyph_alias(key, c, font):
    if key == 'L066' and font == '/DTIRST+LMMathExtension10-Regular':
        return BRACE_PIECES.get(c)
    if key == 'L074':
        if font == '/SNRLEG+CMEX10':
            return BRACE_PIECES.get(c)
        if font == '/KOMCTG+CMSY10':
            return {'B':'ℬ', 'D':'𝒟', 'K':'𝒦', 'P':'𝒫'}.get(c)
    if key == 'L104':
        if font == '/CPBKAJ+CMSY10':
            return {'L':'ℒ'}.get(c)
        if font == '/CPBKGG+LCIRCLE10':
            return {'✐':'○'}.get(c)
        if font == '/CPBMDA+LINE10':
            return {'\x00':'╱', '❅':'╲'}.get(c)
    return None
