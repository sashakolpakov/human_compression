# Root review of full marked-subgroup comparison

10 October 2026. PASS for the complete source, formal interfaces and fresh
public compilation. This supersedes the author's historical pending-review
label; previous sources and reports remain unchanged.

I read every definition and proof in ParabolicMarkedComparison.lean, and
checked its assumptions against the written comparison theorem. Proper
indexed subgroups are protected unless the index set itself is exactly the
exceptional complement. Redundant markings therefore cause no skipped case.
The proof establishes exact images of all pair intersections before assuming
IP. This gives descent; the retained transport theorem gives ascent.

The map-of-closure identity connects the theorem to actual generated markings.
The final two conclusions separately compare full marked IP and typed coset
Helly. Neither property is inferred from the other. The source marking must
generate its group. Global surjectivity is required only by the final
corollary that also proves target generation. Groups and type sets may be
infinite; no involution or distinct-marker assumption is hidden.

I freshly compiled the public source and all three transitive local imports
in a clean scratch output directory, with the pinned compiler and all nine
package revisions checked. All four passed without warnings. All seven new
printed theorem axiom audits use only propext, Classical.choice and Quot.sound.
The compiler and compiled pinned libraries remain the ordinary trust boundary.

This closes the previously written-only full marked-IP part of the abstract
comparison theorem. It does not formalize the numerical hypotheses for a
specific tensor model, the geometric identification of that model, or the
assembled forest/Frattini manuscript. It adds no paper-coverage or priority
claim. This is internal review plus a kernel run, not external peer review.
