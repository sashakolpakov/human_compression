"""Literal original subprocess schedules for matching atlas38--45; no execution."""


def schedule(component):
    if component not in tuple(map(str, range(38, 46))):
        raise ValueError('Only eight declared matching components')
    rows = []
    prefix = 'run_' if component == '45' else ''

    def closed(name, command, seconds, role='native'):
        rows.append(dict(command=command, timeout=seconds, role=role,
                         capture='files', directory='{O}/'+prefix+name,
                         environment='closed', returncode='zero'))

    def direct(command, seconds, role='negative', environment='plain'):
        rows.append(dict(command=command, timeout=seconds, role=role,
                         capture='bytes', environment=environment,
                         returncode='nonzero'))

    def compile_one(name, san=False):
        target = name+('_san' if san else '')
        flags = ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if san else [
            '-O2' if component == '45' else '-O3']
        warning = ['-Wall', '-Wextra', '-pedantic'] if component in ('38', '39') else []
        closed('compile_'+target, ['{CXX}', '-std=c++17', *flags, '-DWORDSIZE=64',
            *warning, '-I{INCLUDE}', '{P}/'+name+'.cpp', '-L{LIBRARY}', '-lnauty',
            '-o', '{O}/'+target], 90, 'compiler')

    def py(name, script, args, cap):
        closed(name, ['{PY}', '{P}/'+script, *args], cap, 'python')

    def inventory(lam, directory, name):
        py(name, 'prepare_patterns.py', ['--study', '{S}', '--lambda', str(lam),
            '--out', '{O}/'+directory], 30)

    def guards(names):
        for name in names:
            for mode in ('argument', 'environment'):
                direct(['{PY}', *(['-O'] if mode == 'argument' else []), '{P}/'+name,
                    '--study', '{S}', '--out', '{O}/'+name+'_'+mode+'_forbidden'],
                    10, 'optimization', 'optimized' if mode == 'environment' else 'plain')

    if component in ('38', '39'):
        last = 'compare_control' if component == '38' else 'completion_controls'
        for name in ('root_cover', 'extension_cover', 'controls', last):
            compile_one(name)
        lams = (20, 19) if component == '38' else (18,)
        lam = lams[-1]
        for value in lams:
            inventory(value, 'input'+str(value), 'prepare'+str(value))
            closed('root'+str(value), ['{O}/root_cover', '{O}/input'+str(value)+'/patterns.txt',
                '{O}/roots'+str(value)+'.txt', '{O}/root'+str(value)+'.json', '600'], 630)
        if component == '38':
            closed('old_root_control', ['{O}/compare_control',
                '{S}/corpus106_F012_quartic_twenty_hexagons_v1/inputs/root_representatives.txt',
                '{O}/roots20.txt'], 90)
        roots, joined = '{O}/roots'+str(lam)+'.txt', '{O}/joined'+str(lam)+'.txt'
        closed('extensions', ['{O}/extension_cover', roots, joined,
            *(['{O}/finals18.txt'] if component == '39' else []),
            '{O}/extension'+str(lam)+'.json', '600'], 630)
        closed('literal_controls', ['{O}/controls', roots, '{O}/actual_controls.json'], 90)
        py('independent_controls', 'independent_controls.py', ['--actual',
            '{O}/actual_controls.json', '--out', '{O}/independent_report.json'], 90)
        if component == '39':
            closed('completion_controls_run', ['{O}/completion_controls', joined,
                '{O}/finals18.txt', '{P}/source_witness.txt', '{O}/completion_actual.json'], 60)
            py('independent_completion', 'independent_completion.py', ['--actual',
                '{O}/completion_actual.json', '--out', '{O}/independent_completion.json'], 60)
        for name in ('wrong_count', 'bad_direction', 'empty_forest_edge', 'duplicate_block', 'truncated_block'):
            direct(['{O}/root_cover', '{O}/'+name+'.txt', '{O}/'+name+'_target',
                '{O}/'+name+'_report', '5'], 10)
        direct(['{O}/root_cover', '{O}/input'+str(lam)+'/patterns.txt',
            '{O}/timeout_target', '{O}/timeout_report', '0'], 10)
        guards(['check.py', 'prepare_patterns.py', 'independent_controls.py',
            *(['independent_completion.py'] if component == '39' else []), 'build_native.py', 'run_closed.py'])

    elif component in ('40', '41'):
        lam = '15' if component == '40' else '13'
        coupled = 'coupled_cover' if component == '40' else 'coupled_cover_sorted'
        first = 'profile_controls' if component == '40' else 'size_controls'
        for name in ['root_cover', coupled, first, 'coupled_controls',
                     *(['left_order_controls'] if component == '41' else [])]:
            compile_one(name)
        inventory(lam, 'input'+lam, 'prepare')
        pattern, roots = '{O}/input'+lam+'/patterns.txt', '{O}/roots'+lam+'.txt'
        closed('roots', ['{O}/root_cover', pattern, roots, '{O}/root'+lam+'.json', '120'], 150)
        closed('coupled', ['{O}/'+coupled, roots, '{O}/positives'+lam+'.txt',
            '{O}/coupled'+lam+'.json', '300'], 330)
        for name in (first, 'coupled_controls'):
            args = [] if name == first else [roots, '{P}/positive_control_graph.txt']
            closed(name+'_run', ['{O}/'+name, *args], 60)
            compile_one(name, True)
            closed(name+'_san_run', ['{O}/'+name+'_san', *args], 90)
        if component == '41':
            closed('left_order_controls_run', ['{O}/left_order_controls', roots], 60)
        independent = 'profiles' if component == '40' else 'sizes'
        py('independent_'+independent, 'independent_'+independent+'.py', ['--actual',
            '{O}/'+first+'_run/stdout', '--out', '{O}/independent_'+independent+'.json'], 90)
        py('independent_coupled', 'independent_coupled.py', ['--graph', '{P}/positive_control_graph.txt',
            '--actual', '{O}/coupled_controls_run/stdout', '--out', '{O}/independent_coupled.json'], 60)
        for name in ('wrong_count', 'truncated_block', 'bad_direction', 'duplicate_block'):
            direct(['{O}/root_cover', '{O}/'+name+'.txt', '{O}/'+name+'_target', '{O}/'+name+'_report', '5'], 10)
        for name, binary, inp in [('root', 'root_cover', pattern), ('coupled', coupled, roots)]:
            direct(['{O}/'+binary, inp, '{O}/'+name+'_timeout_target', '{O}/'+name+'_timeout_report', '0'], 10)
        guards(['check.py', 'prepare_patterns.py', 'independent_'+independent+'.py',
            'independent_coupled.py', 'build_native.py', 'run_closed.py'])

    elif component in ('42', '43'):
        lam = '14' if component == '42' else '12'
        coupled = 'coupled_cover_equal' if component == '42' else 'coupled_cover_cached'
        boundary = 'boundary_equal_controls_v2' if component == '42' else 'boundary_controls_cached'
        control = 'coupled_controls' if component == '42' else 'coupled_controls_cached'
        independent = 'check_boundary_equal_independent.py' if component == '42' else 'check_boundary_independent.py'
        for name in ('root_cover', coupled, boundary, 'size_controls', control):
            compile_one(name)
        inventory(lam, 'input'+lam, 'prepare')
        pattern, roots = '{O}/input'+lam+'/patterns.txt', '{O}/roots'+lam+'.txt'
        closed('roots', ['{O}/root_cover', pattern, roots, '{O}/root'+lam+'.json', '180'], 210)
        closed('completion', ['{O}/'+coupled, roots, '{O}/positives'+lam+'.txt', '{O}/completion'+lam+'.json', '600'], 630)
        for name, args in [(boundary, [roots]), ('size_controls', []), (control, [roots, '{P}/positive_control_graph.txt'])]:
            closed(name+'_run', ['{O}/'+name, *args], 60)
            compile_one(name, True)
            closed(name+'_san_run', ['{O}/'+name+'_san', *args], 120)
        py('independent_boundary', independent, ['{O}/'+boundary+'_run/stdout'], 60)
        py('independent_sizes', 'independent_sizes.py', ['--actual', '{O}/size_controls_run/stdout',
            '--out', '{O}/independent_sizes.json'], 60)
        py('independent_coupled', 'independent_coupled.py', ['--graph', '{P}/positive_control_graph.txt',
            '--actual', '{O}/'+control+'_run/stdout', '--out', '{O}/independent_coupled.json'], 60)
        for name in ('wrong_count', 'truncated_block', 'bad_direction', 'duplicate_block'):
            direct(['{O}/root_cover', '{O}/'+name+'.txt', '{O}/'+name+'_target', '{O}/'+name+'_report', '5'], 10)
        for name, binary, inp in [('root', 'root_cover', pattern), ('completion', coupled, roots)]:
            direct(['{O}/'+binary, inp, '{O}/'+name+'_timeout_target', '{O}/'+name+'_timeout_report', '0'], 10)
        guards(['check.py', 'prepare_patterns.py', independent, 'independent_sizes.py',
            'independent_coupled.py', 'build_native.py', 'run_closed.py'])

    elif component == '44':
        for name in ('root_cover', 'check_joint_completions', 'positive_control', 'joint_control', 'structural_control'):
            compile_one(name)
        inventory('10', 'inventory', 'prepare')
        pattern, roots = '{O}/inventory/patterns.txt', '{O}/roots10.txt'
        closed('roots', ['{O}/root_cover', pattern, roots, '{O}/root10.json', '180'], 210)
        closed('completion', ['{O}/check_joint_completions', roots, '{O}/completion10.json', '{O}/positives10.txt', '600'], 630)
        for name in ('positive_control', 'joint_control', 'structural_control'):
            args = ['{P}/positive_control_graph.txt']+([] if name == 'structural_control' else ['60'])
            closed(name+'_run', ['{O}/'+name, *args], 90)
            compile_one(name, True)
            closed(name+'_san_run', ['{O}/'+name+'_san', *args], 120)
        py('independent_structure', 'structural_control_qualified.py', ['{O}/structural_control_run/stdout', '{O}/structure.json'], 60)
        for name in ('wrong_count', 'truncated', 'bad_direction', 'duplicate_block'):
            direct(['{O}/root_cover', '{O}/'+name+'.txt', '{O}/'+name+'_target', '{O}/'+name+'_report', '5'], 10)
        for name, binary, inp in [('root', 'root_cover', pattern), ('completion', 'check_joint_completions', roots)]:
            direct(['{O}/'+binary, inp, '{O}/'+name+'_timeout_target', '{O}/'+name+'_timeout_report', '0'], 10)
        guards(['check.py', 'prepare_patterns.py', 'structural_control.py', 'structural_control_qualified.py', 'build_native.py', 'run_closed.py'])

    else:
        for name in ('root_cover', 'exterior_cover', 'complete', 'cycle_controls', 'normalization_controls', 'positive_controls'):
            compile_one(name)
        py('inventory', 'inventory.py', ['--study', '{S}', '--out', '{O}/inventory.json'], 30)
        pattern, roots, ext = '{O}/patterns.txt', '{O}/roots.txt', '{O}/exteriors.txt'
        closed('roots', ['{O}/root_cover', pattern, roots, '{O}/root.json', '60'], 90)
        closed('exteriors', ['{O}/exterior_cover', ext, '{O}/exteriors.json', '60'], 90)
        closed('boundary', ['{O}/complete', roots, ext, '{O}/classes.txt', '{O}/boundary.json', '600'], 630)
        py('result', 'verify_result.py', ['--result', '{O}/classes.txt', '--source', '{P}/source_positive.txt', '--out', '{O}/result.json'], 30)
        for name, args in [('cycle_controls', ['{P}/source_positive.txt']), ('normalization_controls', [ext]),
                           ('positive_controls', ['{P}/source_positive.txt', roots, ext])]:
            closed(name, ['{O}/'+name, *args], 60)
            compile_one(name, True)
            closed(name+'_san', ['{O}/'+name+'_san', *args], 90)
        py('normalization_oracle', 'normalization_oracle.py', ['{O}/run_normalization_controls/stdout', ext], 30)
        for name in ('count', 'truncated', 'direction', 'duplicate'):
            direct(['{O}/root_cover', '{O}/'+name+'.txt', '{O}/'+name+'_roots', '{O}/'+name+'_report', '10'], 15)
        for name, command in [('roots', ['{O}/root_cover', pattern]), ('exteriors', ['{O}/exterior_cover']),
                              ('boundary', ['{O}/complete', roots, ext])]:
            direct([*command, '{O}/'+name+'_timeout_output', '{O}/'+name+'_timeout_report', '0'], 10)
        guards(['check.py', 'inventory.py', 'normalization_oracle.py', 'verify_result.py', 'build_native.py', 'run_closed.py'])
    return rows
