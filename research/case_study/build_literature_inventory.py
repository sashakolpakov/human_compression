"""Rebuild the auditable catalogue and finite priority corpus (no network access)."""
from pathlib import Path
from bs4 import BeautifulSoup
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources"
CATALOGUE_URL = "https://leemans.dimitri.web.ulb.be/papers.html"
AS_OF = "2026-10-09"

# Position in the archived author's HTML, not the site's reversed list numbering.
# scope describes actual reading, not the mere presence of a downloaded PDF.
SELECTED = {
    7: ("chiral_accepted.pdf", "https://amc-journal.eu/index.php/amc/article/download/3716/2232", "team_read_main_construction_and_conclusion", "Order 2p^m existence; the team checked the accepted manuscript, including its remaining even-exponent range."),
    8: ("chirality_test2026.pdf", "https://arxiv.org/pdf/2511.14562", "read_introduction_and_main_theorem", "Theorem 1.1 supplies a group-theoretic chirality test for hypertopes; do not retain this as an unresolved obstruction."),
    10: ("gluing2026.pdf", "https://arxiv.org/pdf/2504.17535", "read_introduction_and_conjecture_counterexample_sections", "Proposition 4.8 disproves the graph-list conjecture in the 2024 high-rank counting paper."),
    11: ("simplegroups2026.pdf", "https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf", "read_main_theorem_and_proof_outline", "Classifies simple groups admitting any string C-group representation; it does not determine all maximum ranks."),
    13: ("girth_diameter2025.pdf", "https://arxiv.org/pdf/2401.15539", "read_introduction_bounds_and_future_work_section", "The existence of further Moore-bound (k;5,4)-cages is an open research direction, not a numbered universal conjecture in this text."),
    16: ("faithful_maniplex2025.pdf", "https://arxiv.org/pdf/2305.01372", "read_introduction_main_theorem_and_scope", "Faithful thin non-polytopal maniplexes exist in every rank at least four; rank three is polytopal."),
    18: ("mondrian.pdf", "https://arxiv.org/pdf/2311.02385", "team_read_main_problem_and_computational_results", "Finite computations below 1001 do not settle the universal Mondrian problem; see the 2026 followup separately."),
    19: ("stability2024.pdf", "https://arxiv.org/pdf/2212.12723", "read_main_theorem_and_conjecture_sections", "Proves high-rank counting stability; later gluing paper refutes its candidate graph list."),
    20: ("rank_augmentation2024.pdf", "https://arxiv.org/pdf/2212.12563", "read_introduction_main_statement_and_conclusion", "Conditional augmentation from symmetric-group rank three to four; not a general inverse to rank reduction."),
    26: ("sporadic2022.pdf", "https://adam-journal.eu/index.php/ADAM/article/download/1405/1405", "read_introduction_and_results_section_5", "Published version resolves O'Nan enumeration: rank three 6536, rank four 16. Co2 rank three 60370; Fi22 rank three 25052."),
    27: ("psl3_chiral2022.pdf", "https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf", "read_introduction_main_statements_and_section_7", "Final version retains PSU(3,q), q>17 and the PSL(2,q) composite-exponent chiral existence cases as open."),
    31: ("orthogonal_char2_2020.pdf", "https://arxiv.org/pdf/1709.02219", "read_introduction_theorems_1_4_and_1_5", "Constructs high ranks in characteristic two; does not establish universal maximum ranks."),
    37: ("rank_reduction2019.pdf", "https://arxiv.org/pdf/1812.01055", "read_full_short_paper", "Rank-reduction theorem and Conjecture 5.1 (A11 unique finite simple rank gap)."),
    38: ("alternating2019.pdf", "https://arxiv.org/pdf/1810.12450", "read_introduction_main_theorem_and_rank_consequences", "All ranks from three through floor((n-1)/2) for An, n>=12; A11 has ranks three and six."),
    39: ("ree2018.pdf", "https://arxiv.org/pdf/1501.01125", "read_introduction_main_theorem_and_open_problem", "Small Ree string C-groups have only rank three; the unrestricted C-group rank problem is different."),
    43: ("psl2_chiral2017.pdf", "https://arxiv.org/pdf/1606.08017", "read_introduction_main_classification_and_section_6_in_detail", "Conjectures 6.1 and 6.2 are distinct primitive-square and subgroup-intersection obstructions. No later published resolution located."),
    48: ("psl4_rank2016.pdf", "https://digitalcommons.bucknell.edu/fac_journ/1204/", "primary_abstract_read_full_text_download_denied_403", "Odd q rank-four existence and even q nonexistence are confirmed by the authors' institutional abstract; full PDF download denied access."),
    120: ("survey2021.pdf", "https://arxiv.org/pdf/1910.08843", "read_all_numbered_conjectures_problems_and_surrounding_results", "Three conjectures and fifteen problems indexed in the audit; snapshot must be updated using later papers."),
    126: ("incidence_representation2025.pdf", "https://arxiv.org/pdf/2506.10464", "read_introduction_definition_and_future_work_section", "Finite-group unrestricted incidence representation existence is resolved by Diaz Ramos-Molinier-Viruel, arXiv2511.02410; stronger geometric constraints remain a research direction."),
    128: ("diagram_symmetries2026.pdf", "https://arxiv.org/pdf/2610.09711", "read_introduction_and_theorem_1_1", "Submitted October7,2026, within cutoff. Realizes every finite group as the induced diagram-symmetry group of a regular hypertope."),
}

# External followups include collaborators and papers directly updating the priority topics.
FOLLOWUPS = [
    ("F001", "On the ranks of string C-group representations for symplectic and orthogonal groups", "Peter A. Brooksbank", "2021", "symplectic_ranks2020.pdf", "https://arxiv.org/pdf/1912.05512", "read_main_theorem_and_rank_spectrum_table", "PSp(4,q) has spectrum {3,4,5} except q=3, where it has none; a table of constructions should not be mistaken for a universal upper bound in higher dimension."),
    ("F002", "String C-group representations of transitive groups: a case study with degree 11", "Fernandes, Piedade, Reade", "2025", "degree11_2025.pdf", "https://arxiv.org/pdf/2302.11943", "read_introduction_and_rank_gap_statement", "Calls A11 the unique known finite simple group with a noninterval rank spectrum."),
    ("F003", "On the rank of Suzuki polytopes: an answer to Hubard and Leemans", "Pablo Spiga", "2021", "suzuki_chiral_resolution2021.pdf", "https://arxiv.org/pdf/2010.04080", "read_full_short_paper", "Resolves the conjecture that Suzuki chiral polytopes have rank three."),
    ("F004", "Abstract regular polytopes of G2(q) in even characteristic", "Malcolm Hoong Wai Chen", "2026", "g2_even2026.pdf", "https://arxiv.org/pdf/2609.25004", "read_introduction_main_results_section_4_and_computational_table", "Submitted September 21, 2026. Questions 4.1/4.2 ask for upper ranks in even/odd characteristic; all ranks 3,4,5 are constructed when q>2 is even."),
    ("F005", "Polytopality criteria for the mix of polytopes and maniplexes", "Gabe Cunningham and Isabel Hubard", "2025", "mix_criteria2025.pdf", "https://arxiv.org/pdf/2506.19334", "read_introduction_main_criteria_and_final_problems", "Three final problems concern admissible covers, preserving two-orbit class under mixing, and smallest regular covers."),
    ("F006", "Abstract Regular Polytopes of Finite Irreducible Coxeter Groups", "Malcolm Hoong Wai Chen and Peter Rowley", "2025", "coxeter_ranks2025.pdf", "https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p18/pdf/", "read_introduction_main_results_and_exceptional_group_table", "Determines rank ranges for Coxeter groups; do not transfer bounds to simple quotients without proof."),
    ("F007", "Faithfulness in maniplexes", "Gabe Cunningham, Elias Mochan, Antonio Montero, Primoz Potocnik, Micael Toledo", "2026", "faithfulness2026.pdf", "https://dirros.openscience.si/Dokument.php?id=49623&lang=eng", "read_abstract_section_7_mixing_results_and_section_8_open_problems", "Version of record, Journal of Algebraic Combinatorics 64(2), article23, September2026. Its three open problems concern two-facet faithfulness, polytopes arising as posets of unfaithful maniplexes, and reconstructing a thin flagged poset."),
    ("F008", "On solutions to the Mondrian Puzzle", "Noah Lebowitz-Lockard and Gerald Tenenbaum", "2026", "mondrian_2026.pdf", "https://tenenb.perso.math.cnrs.fr/PPP/Mondrian.pdf", "read_introduction_conjecture_1_1_and_main_theorem", "Dated August28,2026. Proves positive lower density of impossible side lengths, while explicitly retaining nonexistence of any Mondrian integer as Conjecture1.1."),
    ("F009", "On the order-diameter ratio of girth-diameter cages", "Stijn Cambie, Jan Goedgebeur, Jorik Jooken, Tibo Van den Eede", "2026", "girth_diameter_followup2026.pdf", "https://arxiv.org/pdf/2511.21144", "read_introduction_main_results_section_5_and_tables_5_6", "Version3 August19,2026; DMTCS28:4. Settles107 parameter triples, retains even-girth bipartiteness Question1. Its table does not settle (7;5,4)."),
    ("F010", "Every finite group is represented by a finite incidence geometry", "Antonio Diaz Ramos, Remi Molinier, Antonio Viruel", "2025", "incidence_representation_resolution2025.pdf", "https://arxiv.org/pdf/2511.02410", "read_introduction_theorem_A_and_proof_structure", "Version2 December16,2025. Every finite pair H normal in G is realized as (correlations,type-preserving automorphisms) of a finite incidence geometry."),
    ("F011", "Explicit constructions of Diophantine tuples over finite fields", "Seoyoung Kim, Chi Hoi Yip, Semin Yoo", "2024", "weil_bound_primary2024.pdf", "https://link.springer.com/content/pdf/10.1007/s11139-024-00888-5.pdf", "read_lemma_2_1_and_its_hypotheses", "Primary published formulation of the exact multiplicative Weil bound used in the team's candidate proof of Conjecture6.1; cites Lidl-Niederreiter Theorem5.41."),
    ("F012", "Exhaustive generation of edge-girth-regular graphs", "Jan Goedgebeur and Jorik Jooken", "2025", "egr_exhaustive2025.pdf", "https://arxiv.org/pdf/2401.08271", "full_text_searched_and_resolution_context_read", "Section4 disproves Araujo-Pardo–Leemans extremality conjecture (arXiv Conj4.6; published Conj4.4): n(3,8,8)=40<54; n(3,12,32)<=162<486. Its own Conjecture2 concerns four nonexistence parameters."),
    ("F013", "String C-groups of 2-power order project onto a common string C-group", "Dong-Dong Hou and Egon Schulte", "2026", "catalogue_F013.pdf", "https://arxiv.org/pdf/2605.20691", "full_text_searched_and_main_theorems_read", "Every finite regular d-polytope with 2-power automorphism group covers Conder's common minimal polytope. This does not classify all such polytopes."),
    ("F014", "Regular 3-polytopes of type {n,n}", "Mingchao Li and Wei-Juan Zhang", "2025", "regular_nn_resolution2025.pdf", "https://arxiv.org/pdf/2505.09505", "full_text_searched_main_theorem_and_conjecture_context_read", "Theorem1.3/Corollary3.6 resolves the Type(2) question of Hou–Feng–Leemans2025. Conjecture3.7 proposes higher-rank Coxeter quotients with specified local relations. Only preprintv1 located through cutoff."),
    ("F015", "Infinite Families of Hypertopes from Centrally Symmetric Polytopes", "Claudio Alexandre Piedade", "2023", "hypertope_infinite2023.pdf", "https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p20/pdf/", "full_text_searched_introduction_and_construction_scope_read", "Extends centrally symmetric polytopes and applies halving to construct infinite locally spherical/toroidal hypertope families. Does not state a resolution of the universal square-diagram conjectures in L003. No explicit new open problem found by full-text search."),
    ("F016", "Symmetric polytopes whose automorphism groups are 2-groups", "Gabe Cunningham, Yan-Quan Feng, Dong-Dong Hou, Egon Schulte", "2025", "symmetric_2groups2025.pdf", "https://arxiv.org/pdf/2512.15511", "full_text_searched_introduction_and_extension_theorem_scope_read", "Constructs regular and alternating semiregular polytopes with prescribed rank3 sections, and proves universal extension preserves having a2-group. Does not claim a full classification or resolve L034 Conjecture3.3."),
    ("F017", "LCD codes from adjacency matrices of graphs", "Jennifer D. Key and Bernardo G. Rodrigues", "2018", "lcd_followup2018.pdf", "https://www.math.clemson.edu/~keyj/Key/LCD_KeyRod.pdf", "full_text_searched_definitions_and_proposition_1_read", "Proposition1(2) proves graph-complement code duality implies LCD for regular graphs, a direct followup to L050. This precedes the team's elementary general matrix observation; do not advertise the regular-graph result as new."),
]

def asset(filename, url):
    p = SRC / filename
    valid = p.exists() and (p.suffix != ".pdf" or p.read_bytes().startswith(b"%PDF"))
    return {"filename": str(p.relative_to(ROOT)), "url": url,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest() if valid else None,
            "bytes": p.stat().st_size if valid else None}

def main():
    html = SRC / "leemans_publications.html"
    soup = BeautifulSoup(html.read_text(), "html.parser")
    entries = []
    for i, item in enumerate(soup.find_all("li"), 1):
        section = item.find_previous("h2").get_text(" ", strip=True)
        citation = item.get_text(" ", strip=True)
        em = item.find("em")
        title = em.get_text(" ", strip=True) if em else citation
        years = re.findall(r"\b(?:19|20)\d{2}\b", citation)
        entry = {"id": f"L{i:03d}", "author_catalogue_position": i,
                 "title": title, "citation": citation, "category": section,
                 "mathematical": "non-mathematical" not in section,
                 "publication_year_from_catalogue": years[0] if years else None,
                 "source_urls": [CATALOGUE_URL] + [a["href"] for a in item.find_all("a", href=True)],
                 "priority_corpus": i in SELECTED,
                 "reading_scope": "catalogue_metadata_only", "assets": [], "status_note": "Not individually audited."}
        if i in SELECTED:
            filename, url, scope, note = SELECTED[i]
            entry.update(reading_scope=scope, assets=[asset(filename, url)], status_note=note)
            if url:
                entry["source_urls"].append(url)
        entries.append(entry)
    for update_file in ("catalogue_fulltext_audit.json", "older_literature_updates.json",
                        "workspace_proof_audits.json"):
        if not (ROOT / update_file).exists():
            continue
        updates = json.loads((ROOT / update_file).read_text())
        for entry in entries:
            if entry["id"] in updates:
                update = updates[entry["id"]]
                entry.update({k: v for k, v in update.items() if k not in ("filename", "url")})
                if update.get("filename"):
                    entry["assets"] = [asset(update["filename"], update["url"])]
                    entry["source_urls"].append(update["url"])
                if update.get("abstract_filename"):
                    entry["abstract_asset"] = asset(update["abstract_filename"], update.get("primary_abstract_url", ""))
                if update.get("primary_abstract_url"):
                    entry["source_urls"].append(update["primary_abstract_url"])
                for attempt in update.get("retrieval_attempts", []):
                    if attempt.get("url"):
                        entry["source_urls"].append(attempt["url"])
    for id_, title, authors, year, filename, url, scope, note in FOLLOWUPS:
        entries.append({"id": id_, "author_catalogue_position": None, "title": title,
                        "citation": f"{authors} ({year}). {title}", "category": "Directly relevant followup",
                        "mathematical": True, "publication_year_from_catalogue": year,
                        "source_urls": [url] if url else [], "priority_corpus": True,
                        "reading_scope": scope, "assets": [asset(filename, url)], "status_note": note})
    scope_counts = {}
    for e in entries:
        e["source_urls"] = list(dict.fromkeys(e["source_urls"]))
        e["fulltext_available"] = any(a["sha256"] for a in e["assets"])
        if e["fulltext_available"]:
            e.setdefault("retrieval_status", "fulltext_retrieved")
        elif e["mathematical"]:
            e.setdefault("retrieval_status", "fulltext_unavailable_after_search" if e.get("retrieval_limit") else "not_attempted")
        scope_counts[e["reading_scope"]] = scope_counts.get(e["reading_scope"], 0) + 1
    asset_urls = {a["filename"]: a["url"] for e in entries for a in e["assets"]}
    if (SRC / "manifest.json").exists():
        for a in json.loads((SRC / "manifest.json").read_text()):
            asset_urls["sources/" + a["file"]] = a["url"]
    author_math = [e for e in entries if e["id"].startswith("L") and e["mathematical"]]
    fulltext_count = sum(e["fulltext_available"] and e["reading_scope"] != "downloaded_not_read" for e in author_math)
    abstract_count = sum(not e["fulltext_available"] and "abstract" in e["reading_scope"] for e in author_math)
    result = {"as_of": AS_OF, "scope": "Every mathematical entry in the archived author catalogue has a full-text audit or an explicit retrieval limitation. Full-text search, section reading and complete reading are distinct scopes; this is not a claim to have read every proof or every publication by every collaborator.",
              "catalogue_asset": asset("leemans_publications.html", CATALOGUE_URL),
              "counts": {"author_entries": len(soup.find_all("li")), "author_mathematical_entries": sum(e["mathematical"] for e in entries if e["id"].startswith("L")),
                         "followups": len(FOLLOWUPS), "priority_corpus": sum(e["priority_corpus"] for e in entries),
                         "priority_full_text_downloaded": sum(any(a["sha256"] for a in e["assets"]) for e in entries if e["priority_corpus"]),
                         "author_fulltexts_searched_or_read": fulltext_count,
                         "author_abstracts_only": abstract_count,
                         "author_metadata_and_access_only": len(author_math) - fulltext_count - abstract_count,
                         "author_fulltext_unavailable": sum(not e["fulltext_available"] for e in author_math),
                         "author_retrieval_attempt_not_recorded": sum(e["retrieval_status"] == "not_attempted" for e in author_math),
                         "author_mathematical_metadata_only": sum(e["id"].startswith("L") and e["mathematical"] and e["reading_scope"] == "catalogue_metadata_only" for e in entries),
                         "reading_scope": scope_counts},
              "archived_pdf_assets": [asset(p.name, asset_urls.get(str(p.relative_to(ROOT)), "")) for p in sorted(SRC.glob("*.pdf")) if p.read_bytes().startswith(b"%PDF")],
              "entries": entries}
    (ROOT / "literature_inventory.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    with (ROOT / "literature_inventory.csv").open("w", newline="") as f:
        fields = ["id", "title", "category", "publication_year_from_catalogue", "priority_corpus", "reading_scope", "fulltext_available", "retrieval_status", "source_urls", "assets", "status_note", "followup_proof_audit_2026_10_09"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for e in entries:
            writer.writerow({k: json.dumps(e.get(k), ensure_ascii=False) if isinstance(e.get(k), list) else e.get(k) for k in fields})
    print(json.dumps(result["counts"]))

if __name__ == "__main__":
    main()
