"""Author metadata assembly; private page/outline assets are referenced, never exported."""
from pathlib import Path
import hashlib,json
import pypdf
H=Path(__file__).resolve().parent;S=H.parent
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(n,x):(H/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
d=json.loads((H/'document_map.json').read_text())['documents'];a=json.loads((H/'font_audit.json').read_text());g=json.loads((H/'glyph_aliases.json').read_text())['aliases']
paths={'L050':('/private/tmp/LCD_input_pages01/L050','fresh measurement visual reading'),'F017':('/private/tmp/F017_source_visual01','exact earlier full scientific visual reading reused'),'U_LCD':('/private/tmp/LCD_input_pages01/U_LCD','fresh measurement visual reading'),'A_F017':('/private/tmp/F017_application_final_views02','exact final author scientific visual reading reused'),'A_L050':('/private/tmp/LCD_L050_application_pages01','fresh measurement visual reading')}
views=[];graphics=[]
for r in d:
 key=r['key'];folder,kind=paths[key];pages=[]
 for i in range(1,r['pages']+1):
  q=Path(folder)/f'p-{i:02d}.png';pages.append(dict(page=i,viewed=True,private_visual=pin(q)))
 views.append(dict(document=key,pdf_sha256=r['sha256'],reading=kind,pages=pages,all_pages_viewed=True))
 pdf=pypdf.PdfReader(S/r['path']);page_records=[]
 for i,p in enumerate(pdf.pages,1):
  images=[];forms=[]
  def walk(resources,route=(),seen=frozenset()):
   for k,v in resources.get('/XObject',{}).items():
    x=v.get_object();identity=(getattr(v,'idnum',None),getattr(v,'generation',None))
    if identity in seen:continue
    if x.get('/Subtype')=='/Image':images.append(dict(route=list(route+(str(k),)),width=x.get('/Width'),height=x.get('/Height')))
    elif x.get('/Subtype')=='/Form':forms.append(list(route+(str(k),)));walk(x.get('/Resources',resources),route+(str(k),),seen|{identity})
  walk(p['/Resources']);page_records.append(dict(page=i,image_xobjects=images,form_xobjects=forms))
 graphics.append(dict(document=key,pages=page_records,visual='Displayed equations, matrices, tables and typographic layout occur; no separate unextracted raster diagram was observed. Absence of image XObjects does not measure vector/layout complexity.',graphic_cost=None,full_visible_text_claim=False))
panels=[]
for folder in ['/private/tmp/LCD_input_glyphs01','/private/tmp/LCD_input_glyphs_A01','/private/tmp/LCD_dotlessj01','/private/tmp/LCD_L050_app_glyphs01']:
 for p in json.loads((Path(folder)/'index.json').read_text()):panels.append(dict(private_visual=pin(Path(p['path'])),viewed=True,classes=p['classes']))
put('visual_review.json',dict(role='Author input audit; independent acceptance remains separate.',documents=views,outline_panels=panels,outline_classes_viewed=sum(len(p['classes'])for p in panels),plot_label_warning='The first outline contact panel has a Matplotlib label-font warning for the combining copyright-circle label. Its actual embedded glyph outline is rendered and was directly inspected; this is not a missing source glyph.',source_assets_exported=False))
put('graphics_inventory.json',dict(documents=graphics,source_graphics_and_layout_cost=None,OCR_used=False,complete_visual_text_claim=False))
screens=[]
for r in d:
 screens.append(dict(document=r['key'],pdf_sha256=r['sha256'],pages=list(range(1,r['pages']+1)),screen='Complete extracted text and all full-page visuals checked for executable/pseudocode blocks.',executable_listings=[],masks=[],retained='Mathematical algorithm and proof prose, matrix identities, tables, named software references and all footnotes/references remain.',historical_software_cost=None if r['role']=='source' else 'separate whole-file inventory'))
put('listing_screen.json',dict(policy='Symmetric manuscript boundary: executable listings excluded on both sides. No such listing occurs in these five exact PDFs, so no code masks are applied.',documents=screens,required_certificates_remain_premises=True,optional_validation_excluded_both_sides=True,software_inclusive_factor=None,final_L050_application_screen_pending=False))
put('calibration_review.json',dict(status='AUTHOR_OCCURRENCE_AND_OUTLINE_AUDIT',classes={k:len(x['encoded_glyph_classes'])for k,x in a.items()},substitution_classes=len(g),substitution_occurrences={k:sum(x['occurrences']for x in g if x['document']==k)for k in a},rules=[
 'Each repair binds the actual font dictionary, effective Encoding, encoded byte, source text event and context hash; the embedded glyph class has an outline hash.',
 'Type1 source/common/L050-application fonts were reconciled against all extracted nonspace text. The F017 application has unchanged Type0 Unicode text fonts, identified separately; only its Type1 mathematics receives outline calibration.',
 'Blackboard/script glyph aliases, explicit control-byte large delimiters, printable sum/product aliases and the private-use dotless j are repaired to the displayed glyph.',
 'The mapsto component is a tail without an arrowhead. It is represented by U+22A2 and the adjacent arrow remains a separate event. No two-event merger is made.',
 'The copyright circle component and its adjacent c remain separate source events. Overlay negation and adjacent operator remain separate.',
 'Ordinary decoded ligatures are preserved; NFC and NFKC are separate recorded sensitivities. Printed line hyphens, spaces and original mathematical errors are unchanged.',
 'No actual nonempty-outline whitespace alias remains unrepaired; generated extraction whitespace is not mistaken for a font glyph.'],raw_variant_preserved=True,source_maps_transplanted=False))
put('science_bindings.json',dict(status='BOTH_SCIENTIFIC_APPLICATIONS_ACCEPTED_INPUT_ACCEPTANCE_PENDING',bindings=[pin(S/p)for p in [
 'topic_LCD_umbrella_v2/manifest.json','topic_LCD_umbrella_root_adoption/manifest.json',
 'topic_LCD_F017_application/manifest.json','topic_LCD_F017_application/source_contract.json','topic_LCD_F017_application/scope.json','topic_LCD_F017_application/interface_inventory.json','topic_LCD_F017_root_review/manifest.json','topic_LCD_L050_application/manifest.json','topic_LCD_L050_application/source_map.json','topic_LCD_L050_application/scope.json','topic_LCD_L050_application/program_inventory.json','topic_LCD_L050_root_review/manifest.json']],F017_dispositions=104,L050_dispositions=54,F017_retained_input_classes=7,F017_partial_Lean_declarations=9,interface_inventory='Conservative context dependencies, not a minimal necessary-proof DAG.',historical_author_pending_labels='The immutable F017 author scope predates its distinct root acceptance. The separate root-review binding supplies the later accepted status.',L050_application='Complete accepted fifteen-page application, freshly extracted and viewed; exact later root acceptance supersedes historical pending wording in the immutable PDF.',whole_topic_science_accepted=True,independent_input_acceptance=False,ratios_permitted=False))
print('metadata prepared; private source/outline images not exported')
