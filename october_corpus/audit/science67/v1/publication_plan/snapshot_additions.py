"""Proposed two additive verifier functions; copy before main without old edits."""
def check_previous_science67():
    spec=importlib.util.spec_from_file_location('science67_history',ROOT/'scripts/check_science67_history.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

def check_science67():
    spec=importlib.util.spec_from_file_location('science67',ROOT/'scripts/check_science67.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.verify(ROOT)
    need(check_current_measurement_pointer()==result['counts']['measured']==53,
         'Science-only registration changed unique measurements.')
    return result
