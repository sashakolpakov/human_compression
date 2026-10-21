"""Independent full-document recount; no ratio or mathematical admission."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import unicodedata
from pypdf import PdfReader
import pypdf

def require(ok, message):
    if not ok:
        raise ValueError(message)

def fingerprint(data):
    return sha256(data).hexdigest()

def length_vector(text, form):
    normalized = unicodedata.normalize(form, text)
    words = normalized.split()
    collapsed = " ".join(words)
    units = 0
    in_unit = False
    for character in normalized:
        current = character.isalnum()
        if current and not in_unit:
            units += 1
        in_unit = current
    return {
        "whitespace_tokens": len(words),
        "alphanumeric_units": units,
        "characters_without_whitespace": sum(len(word) for word in words),
        "characters_with_collapsed_whitespace": len(collapsed),
        "utf8_bytes_with_collapsed_whitespace": len(collapsed.encode("utf-8")),
        "collapsed_text_sha256": fingerprint(collapsed.encode("utf-8"))}

def recount(root, key, record):
    raw_pdf = (root/record["path"]).read_bytes()
    require(fingerprint(raw_pdf)==record["pdf_sha256"], "Changed PDF: "+key)
    pages = [page.extract_text() or "" for page in PdfReader(root/record["path"]).pages]
    require(len(pages)==record["pages"], "Page count: "+key)
    offset = 0
    for number, (text, binding) in enumerate(zip(pages,record["page_bindings"]),1):
        require(binding["page"]==number and binding["start"]==offset and
                binding["end"]==offset+len(text) and
                binding["sha256"]==fingerprint(text.encode()), "Page boundary: "+key)
        offset += len(text)+1
    raw = "\n".join(pages)
    require(fingerprint(raw.encode())==record["extraction_sha256"], "Extraction: "+key)
    spans = record["included_spans"]
    require(len(spans)==1 and spans[0]["start"]==0 and spans[0]["end"]==len(raw) and
            spans[0]["sha256"]==fingerprint(raw.encode()), "Whole document: "+key)
    changes = {}
    for glyph in record["glyph_substitutions"]:
        at = glyph["offset"]
        require(at not in changes and ord(raw[at])==int(glyph["input_codepoint"][2:],16), "Glyph location: "+key)
        require(len(glyph["output"])==1, "Glyph deletion or expansion: "+key)
        changes[at] = glyph["output"]
    discarded = set()
    furniture_at = {}
    for furniture in record["excluded_furniture"]:
        a,b = furniture["start"],furniture["end"]
        part = raw[a:b]
        require(0<=a<b<=len(raw) and part==furniture["literal"] and
                fingerprint(part.encode())==furniture["sha256"], "Furniture: "+key)
        locations = set(range(a,b))
        require(not discarded.intersection(locations), "Overlapping furniture: "+key)
        discarded.update(locations)
        furniture_at[a] = "\n"
    raw_selected = "".join(furniture_at.get(i,"") if i in discarded else ch for i,ch in enumerate(raw))
    calibrated = "".join(furniture_at.get(i,"") if i in discarded else changes.get(i,ch) for i,ch in enumerate(raw))
    return {"pages":len(pages),"glyph_changes":len(changes),"metrics":{
        form:{"untrimmed":length_vector(raw,form),"raw_selected":length_vector(raw_selected,form),
              "calibrated_selected":length_vector(calibrated,form)} for form in ("NFC","NFKC")}}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-root",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    require(not args.out.exists(), "Fresh output file required")
    specdir=args.study_root/"topic_A_measurement"
    source=json.loads((specdir/"source_input_spec.json").read_text())
    replacement=json.loads((specdir/"replacement_input_spec_retractions.json").read_text())
    require(pypdf.__version__==source["pypdf_version"]==replacement["pypdf_version"], "pypdf pin")
    docs=source["sources"] | replacement["ours"]
    results={key:recount(args.study_root,key,row) for key,row in docs.items()}
    report={"status":"PASS_INDEPENDENT_DOCUMENT_RECOUNT_NO_FACTORS",
            "scope":"Complete-document extracted text; image labels and graphic structure are not included and are not assigned zero cost.",
            "input_bindings":[{"path":name,"sha256":fingerprint((specdir/name).read_bytes())} for name in ("source_input_spec.json","replacement_input_spec_retractions.json")],
            "pypdf_version":pypdf.__version__,"documents":results,"ratio":None,"new_credit":0}
    args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"status":report["status"],"documents":len(results),"pages":sum(r["pages"] for r in results.values())}))
if __name__=="__main__":
    main()
