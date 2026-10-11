"""Observed CMEX matrix-bracket components; no diagram reconstruction."""
PARTS={'bracketlefttp':'⎡','bracketleftex':'⎢','bracketleftbt':'⎣','bracketrighttp':'⎤','bracketrightex':'⎥','bracketrightbt':'⎦'}
def output(row):
    return PARTS.get(row['glyph_name']) if 'CMEX' in row['font'] else None
