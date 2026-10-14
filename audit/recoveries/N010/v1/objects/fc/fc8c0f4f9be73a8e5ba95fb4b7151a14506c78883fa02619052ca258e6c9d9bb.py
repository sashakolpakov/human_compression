import copy
import json
from pathlib import Path

W = Path(__file__).resolve().parent
contract = json.loads((W / 'source_contract02.json').read_text())
retained = json.loads((W.parent / 'N010_retained_inputs/register01/retained_register.json').read_text())


def tex(s):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%',
                    '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{',
                    '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(c, c) for c in s)


contexts = [
('C01', 'Definitions and chambers', 'R01', 'Adopt the definitions and retain the marked reconstruction theorems. The acquired residue proof supplies the stabilizer identities under actual polytope hypotheses.'),
('C02', 'Orientations', 'R02', 'The complete word proof identifies both reflection conventions. Index at most two for rotations does not mean index exactly two.'),
('C03', 'Dualities and maps', 'R03--R08', 'Retain the Archdeacon--Richter and Servatius sphere results, Hubard--Weiss polarity theorem, Jendrol counterexample, and attributed toroidal and genus statements. The extra fully transitive toroidal family is not chiral.'),
('C04', 'Hole and zigzag periods', 'R09', 'The full flag-walk proof gives all stated periods. It gives no classification from period data.'),
('C05', 'Amalgamation', 'R10--R16', 'Prove the regular universal theorem from a witness and reproduce the two oriented examples. Retain oriented universality, the ARP cross-polytope criterion, the negative pair, and historical extension/rank-five assertions.'),
('C06', 'Global topology', 'R17--R19', 'Retain the spherical, projective and toroidal classifications and chiral restrictions from Coxeter and ARP, with their tessellation hypotheses.'),
('C07', 'Local spherical and projective types', 'R20--R23,R52', 'Retain the universal Coxeter tessellation theorem and the reported finiteness distinction between projective ranks four and five. Acquire the exact J1 times PSL2(19) example and its corrected family census. The global17/441 aggregates remain unverified source reports.'),
('C08', 'Local toroidal types', 'R24--R29', 'Retain the precise rank/type and regular finite-family classifications in ARP. Conditional regular universality explains the rank-five/six universal restriction. Finite-list conjectures remain separate.'),
('C09', 'Other local surfaces', 'R30--R31', 'The four orientability combinations are definitions. Retain the historical catalogue report with its unverified chiral-citation scope.'),
('C10', 'Equivariant realizations', 'R32,R50', 'Prove the finite orbit-stabilizer and recursive faithfulness criteria. Infinite Euclidean Wythoff constructions remain separate retained inputs with discreteness and exact stabilizers required.'),
('C11', 'Realization cones', 'R33--R34', 'Prove the common centered Gram-cone and irreducibility theorems. Individual cone catalogues and unevaluated character identities retain their published scope.'),
('C12', 'Geometric classifications', 'R35--R38', 'Retain Grunbaum--Dress, Schulte, McMullen, and the finite planar-faced uniform classifications. Skew-faced and infinite cases are not covered by the finite planar list.'),
('C13', 'Medial graphs', 'R39--R40', 'Retain the precise rank-four type{3,q,3} results and their arc-transitivity or semisymmetry hypotheses. The reverse construction has a separate polytopality condition.'),
('C14', 'Petrie schemes', 'R41--R42', 'Retain the attributed positive geometric classes and necessary local condition. A return of a full flag does not exclude repetition of a proper face.'),
('C15', 'Specified groups', 'R43--R46,R51', 'Acquire the complete sporadic existence and regular alternating ranks, and only the specified restricted2-group results. Prove the neighborliness implication, with no classification converse.'),
('C16', 'Quotients', 'R47--R49', 'Retain Hartley quotient and semisparseness theorems with every conjugate quantifier. The general end-condition converse remains a distinct question.')]

head = r'''\small
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{.23\textwidth}>{\raggedright\arraybackslash}p{.73\textwidth}@{}}
\toprule Context and register & Proof or retained input\\\midrule\endhead
'''
body = []
for ident, title, ids, note in contexts:
    body.append(tex(ident + ': ' + title) + r'\newline ' + tex(ids)
                + ' & ' + tex(note) + r'\\[5pt]' + '\n')
(W / 'context_table.tex').write_text(head + ''.join(body) + '\\bottomrule\n\\end{longtable}\n\\normalsize\n')

questions = copy.deepcopy(contract['numbered_problems'])
for row in questions:
    row['synthesis_status'] = ('Already negative in the source.' if row['number'] == 8
                               else 'Affirmative existence by the acquired 2016 theorem.' if row['number'] == 31
                               else 'Regular ranks acquired; chiral rank-three existence only; other parts unsettled here.' if row['number'] == 32
                               else 'Restricted acquired results only; general question unsettled here.' if row['number'] == 30
                               else 'Unsettled here.')
head = r'''\small
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{.05\textwidth}>{\raggedright\arraybackslash}p{.40\textwidth}>{\raggedright\arraybackslash}p{.49\textwidth}@{}}
\toprule No. & Question in the fixed edition & Disposition and qualification\\\midrule\endhead
'''
body = []
for row in questions:
    body.append(str(row['number']) + ' & ' + tex(row['paraphrase']) + ' & '
                + tex(row['synthesis_status'] + ' ' + row['qualification'])
                + r'\\[5pt]' + '\n')
(W / 'question_table.tex').write_text(head + ''.join(body) + '\\bottomrule\n\\end{longtable}\n\\normalsize\n')

secondary = copy.deepcopy(contract['embedded_questions_and_conjectures'])
head = r'''\paragraph{Secondary records.}
\small
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{.25\textwidth}>{\raggedright\arraybackslash}p{.71\textwidth}@{}}
\toprule Record & Exact scope of the additional record\\\midrule\endhead
'''
body = []
for row in secondary:
    label = row['id'].replace('P05-', 'Problem 5: ').replace('P14-', 'Problem 14: ').replace('P16-', 'Problem 16: ').replace('P18-', 'Problem 18: ').replace('P19-', 'Problem 19: ').replace('P28-', 'Problem 28: ').replace('P31-', 'Problem 31: ').replace('U-', '')
    row['synthesis_status'] = ('Only the exact positive families of the acquired simple-group theorem are supplied; the excluded families and regular-map question are not decided.' if row['id'] == 'P31-finite-simple' else 'No new solution supplied.')
    body.append(tex(label.replace('-', ' ')) + ' & ' + tex(row['scope'] + ' ' + row['synthesis_status']) + r'\\[5pt]' + '\n')
(W / 'secondary_table.tex').write_text(head + ''.join(body) + '\\bottomrule\n\\end{longtable}\n\\normalsize\n')

for row in retained['rows']:
    row['source_register_disposition'] = row['disposition']
    if row['id'] == 'R13':
        row['disposition'] = 'COMPLETE_DISTINCTLY_REVIEWED_FINITE_COMPONENT'
        row['acceptance_overlay'] = 'corpus106_N010_oriented_examples_root_review'
    elif row['id'] == 'R46':
        row['disposition'] = 'NEW_WRITTEN_PROOF_OF_ESTABLISHED_NECESSARY_CONDITION'
        row['acceptance_overlay'] = 'principal.tex Proposition5; whole assembly still awaits distinct review'

retained['rows'].append(dict(
    id='R52', context='C07', physical_pages=[10], tex_line=337,
    source_anchor='In rank $4$ (but not in rank $5$)',
    claim='Every locally projective regular polytope of rank four is finite; the corresponding assertion fails in rank five.',
    source_citation_keys=['halp', 'arp'],
    qualification='Retained as a historical classification input reported by the fixed survey. The full primary classification and its correspondence between editions have not been independently inspected. Neither the new common proofs nor the acquired single-family census proves this general rank distinction.',
    disposition='SOURCE_ATTRIBUTED_CLASSIFICATION_NOT_INDEPENDENTLY_VERIFIED',
    independently_inspected_primary_classification=False,
    exact_acquired_join=[], new_question_credit=0,
    revision_reason='Explicit source clause added after distinct review; the frozen 51-row retained register is preserved unchanged.'))

register = dict(original='N010', source_contract='source_contract02.json',
                contexts=[dict(id=a, title=b, rows=c, disposition=d) for a,b,c,d in contexts],
                established_clauses=retained['rows'], questions=questions,
                secondary_records=secondary, source_bibliography=contract['source_bibliography'],
                source_qualifications=contract['review_qualifications'],
                source_only_aggregates=[17,441], corrected_family_count=137,
                corrected_global_total=None, source_questions_asserted_currently_open=False,
                all_classifications_reproved=False, new_question_credit=0,
                new_Lean_declarations=0, new_measurements=0, whole_original_credit=0,
                compression_factor=None)
(W / 'claim_register.json').write_text(json.dumps(register, indent=2) + '\n')
print(json.dumps(dict(contexts=len(contexts), clauses=len(retained['rows']), questions=len(questions), secondary=len(secondary))))
