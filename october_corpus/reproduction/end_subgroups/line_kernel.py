"""One supplied RIGHT37 word, fixed vector and moved line. No search/RREF."""
import runtime as rt
import field
import arithmetic
import prime_kernel

OLD_PRIME_SOURCE='330de22a2623a8c9ed29fc9e6b432179d8355a17a1b2c8e480961a5d7b529b15'
SUBJECT=('original_job','position','original_row_id','marks_sha256','model_sha256')

def same_subject(saved,joins):
    rt.need(all(saved[k]==joins[k]for k in SUBJECT),'same exact original tuple/model/row, not old eligibility')

def candidate(saved,joins):
    rt.need(saved['schema']=='F004_JOB20_RIGHT_TWO_PRIME_SUPPLIER_PROOF_V1'
        and saved['source_pins']['manifest_sha256']==OLD_PRIME_SOURCE,'known historical untrusted RIGHT-prime Source')
    same_subject(saved['original_joins'],joins)
    fact=saved['record']['prime37'];rt.need(fact is not None,'one actual supplied positive37 candidate')
    return fact

def prime37(fact,g,b):
    b.scalar(512) # Whole original-word/type/adapter copy support in the same bank.
    value=prime_kernel.checked_prime(fact,37,arithmetic.internal(g),1,
        arithmetic.I7,arithmetic,arithmetic.Adapter(b))
    return bytes(x for row in value for x in row)

def fixed(raw,Y,b):
    vector=bytes(field.vector(raw,7,b));b.scalar(7)
    rt.need(any(vector),'nonzero actual fixed vector')
    rt.need(b.image(vector,Y)==vector,'fresh whole vY=v')
    return vector

def moved(v,w,b):
    for i in range(7):
        for j in range(i+1,7):
            b.scalar(4)
            if (v[i]*w[j]-v[j]*w[i])%11:return True
    return False

def check(g,cert,b):
    rt.need(type(cert)is dict and set(cert)=={'prime37','vector','moving_label'},'exact supplied37-line certificate')
    label=cert['moving_label'];rt.need(type(label)is int and label in(1,2,3),'one original RIGHT generator label')
    Y=prime37(cert['prime37'],g,b);v=fixed(cert['vector'],Y,b)
    rt.need(moved(v,b.image(v,g[label]),b),'fresh nonzero2by2 minor moves the unique rational line')
    return dict(prime37_exact_order_verified=True,word_side=1,RIGHT_labels=[1,2,3],
        nonzero_fixed_vector_verified=True,moving_RIGHT_label=label,moved_line_minor_verified=True,
        unique_rational_line_is_the_order37_F11_dimension7_lemma=True,
        all_proper37_containers_preserve_that_line_is_borrowed=True,
        RIGHT_full_conditional_on_explicit_original_model_and_cover_imports=True,
        omitted_nonidentity_singleton_label=0,disjoint_other_labels=[1,2,3],
        disjoint_singleton_IP_failure_conditional_on_original_imports=True,
        full_quartet_generation_by_full_RIGHT_conditional_on_imports=True,
        consecutive_intersection_excess_claimed=False,irreducibility_or_norm_assumption_used=False,
        candidate_and_failed_trial_search_replayed=False,Root_case_or_class_credit=0)
