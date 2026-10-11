"""Bound image/vector presence, never infer graphical cost from operator counts."""
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ContentStream
import hashlib

def inventory(path,key):
 reader=PdfReader(path);pages=[]
 for n,page in enumerate(reader.pages,1):
  images=[];forms=[];vector_ops={};inline_images=0
  def visit(content,resources,route):
   nonlocal inline_images
   for i,(args,op) in enumerate(ContentStream(content,reader).operations):
    if op in (b'm',b'l',b'c',b'v',b'y',b're',b'h',b'S',b's',b'f',b'F',b'f*',b'B',b'B*',b'b',b'b*'):
     name=op.decode();vector_ops[name]=vector_ops.get(name,0)+1
    if op==b'INLINE IMAGE':inline_images+=1
    if op!=b'Do':continue
    name=args[0];obj=resources['/XObject'][name].get_object();subroute=route+[dict(operator_index=i,resource=str(name))]
    if obj.get('/Subtype')=='/Form':
     data=obj.get_data();forms.append(dict(route=subroute,decoded_stream_bytes=len(data),decoded_stream_sha256=hashlib.sha256(data).hexdigest()));visit(obj,obj.get('/Resources',resources),subroute)
    elif obj.get('/Subtype')=='/Image':
     data=obj.get_data();images.append(dict(route=subroute,width=int(obj['/Width']),height=int(obj['/Height']),decoded_bytes=len(data),decoded_sha256=hashlib.sha256(data).hexdigest(),image_mask=bool(obj.get('/ImageMask',False))))
  visit(page.get_contents(),page['/Resources'],[])
  pages.append(dict(page=n,vector_path_operator_counts=vector_ops,image_xobject_uses=images,form_xobject_uses=forms,inline_images=inline_images,graphic_cost=None))
 return dict(document=key,physical_pages=len(pages),pages=pages,scope='Content-stream image/form/path presence only. Type1 and Type3 glyph outlines are audited separately. Path operators include formula rules and table borders; they are not figure counts or complexity weights. Extracted labels and glyph proxies do not recover topology, layout, curvature or graphical construction.',full_graphic_cost=None)
