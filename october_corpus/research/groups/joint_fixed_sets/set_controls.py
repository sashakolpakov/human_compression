"""STATIC synthetic controls for the set certificate; no original-group fixture.

The generic caller supplies the one shared Budget, unchanged decoder/profile
namespaces and the new kernel namespace. No test or represented code has run.
"""


def run(kernel, profile, decoder, budget):
    reports = []

    def passed(name, value=True):
        if value is not True:
            raise ValueError('control failed: ' + name)
        reports.append(dict(name=name, passed=True, TEST_ONLY=True))

    def refuses(name, operation):
        try:
            operation()
        except ValueError:
            passed(name)
        else:
            raise ValueError('control did not refuse: ' + name)

    # Root supplied this independent degree-six fixture:
    # A=(3 5), E=(3 5)(4 6), B=(3 4)(5 6). AB has order four.
    # These are TEST_ONLY synthetic labels, not original-group elements.
    a = [1, 2, 5, 4, 3, 6]
    b = [1, 2, 4, 3, 6, 5]
    e = [1, 2, 5, 6, 3, 4]
    base = kernel['scan'](a, e, b, 6, profile, budget)
    passed('noncommuting_AB_prefix_is_allowed',
           a[b[2] - 1] != b[a[2] - 1] and base['AE_points'] == base['AB_points'] == [1, 2])
    lookups = [dict(original_generator_index=1, point=1, image=3),
               dict(original_generator_index=2, point=2, image=4)]
    proposed = kernel['proposed'](base, lookups, lookups[0], budget)
    passed('whole_equal_fixed_sets_with_escape',
           proposed['status'] == 'EQUAL_JOINT_FIXED_SETS_WITH_ORIGINAL_ESCAPE')
    supplied = dict(proposed, escape=dict(lookups[1]))
    passed('ANY_nonfirst_attested_escape',
           kernel['verified'](supplied, base, lookups, budget) == supplied)
    no_escape = kernel['proposed'](base, [dict(original_generator_index=1, point=1, image=2)],
                                  dict(original_generator_index=1, point=1, image=2), budget)
    passed('equal_sets_without_escape_remain_unpaid',
           no_escape['status'] == 'VALID_PREFIX_WITHOUT_APPLICATION'
           and kernel['verified'](no_escape, base, lookups, budget) == no_escape)
    for name, witness in [
        ('unattested_original_lookup', dict(original_generator_index=3, point=1, image=3)),
        ('zero_based_point_label', dict(original_generator_index=1, point=0, image=1)),
        ('Boolean_generator_label', dict(original_generator_index=True, point=1, image=3))]:
        refuses(name, lambda witness=witness:
                kernel['verified'](dict(proposed, escape=witness), base, lookups, budget))
    for name, witness in [
        ('escape_point_not_in_S', dict(original_generator_index=1, point=3, image=4)),
        ('escape_image_stays_in_S', dict(original_generator_index=1, point=1, image=2))]:
        refuses(name, lambda witness=witness:
                kernel['verified'](dict(proposed, escape=witness), base, lookups + [witness], budget))
    forged = dict(proposed, AE_points=[1, 2, 3], AE_count=3)
    refuses('forged_complete_AE_set', lambda: kernel['verified'](forged, base, lookups, budget))
    forged_hash = dict(proposed, vector_hashes=['0' * 64] + proposed['vector_hashes'][1:])
    refuses('forged_original_vector_digest',
            lambda: kernel['verified'](forged_hash, base, lookups, budget))
    unequal = kernel['scan'](a, list(range(1, 7)), b, 6, profile, budget)
    unpaid = kernel['proposed'](unequal, lookups, lookups[0], budget)
    passed('unequal_fixed_sets_remain_unpaid',
           unpaid['status'] == 'VALID_PREFIX_WITHOUT_APPLICATION'
           and kernel['verified'](unpaid, unequal, lookups, budget) == unpaid)
    # Equal cardinalities alone are insufficient, even as a supplied record.
    forged_equal_count = dict(unequal, AE_points=[1], AB_points=[2],
                             AE_count=1, AB_count=1, triple_points=[], triple_count=0)
    unpaid_equal_count = kernel['proposed'](forged_equal_count, lookups, lookups[0], budget)
    passed('same_count_is_not_set_equality', unpaid_equal_count['status'] == 'VALID_PREFIX_WITHOUT_APPLICATION')
    bad = list(a)
    bad[0] = True
    refuses('Boolean_original_image', lambda: kernel['scan'](bad, e, b, 6, profile, budget))
    bad = list(a)
    bad[0] = bad[1]
    refuses('nonbijection_original_B', lambda: kernel['scan'](a, e, bad, 6, profile, budget))
    cycle = [2, 3, 1, 4, 5, 6]
    refuses('noninvolution_original_B', lambda: kernel['scan'](a, e, cycle, 6, profile, budget))
    swap = [3, 2, 1, 4, 5, 6]
    refuses('AE_commutation_required', lambda: kernel['scan'](swap, e, b, 6, profile, budget))
    refuses('BE_commutation_required', lambda: kernel['scan'](a, e, swap, 6, profile, budget))
    good = b'thirdMark:=(1,2);;\n'
    passed('whole_thirdMark_decoder', list(kernel['decode_third'](good, 3, decoder, budget)) == [2, 1, 3])
    for name, raw in [('wrong_third_assignment', b'b:=(1,2);;'),
                      ('truncated_third_wrapper', b'thirdMark:=(1,2);'),
                      ('trailing_third_source', good + b'QUIT;')]:
        refuses(name, lambda raw=raw: kernel['decode_third'](raw, 3, decoder, budget))
    budget.charge(0)
    return dict(schema='F004_BRANCH68_SET_TEST_ONLY_CONTROLS_V1',
                tests=len(reports), all_passed=True, reports=reports,
                original_group_membership_claimed=False, original_job_credit=0)
