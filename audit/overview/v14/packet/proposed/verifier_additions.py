# Append without changing any existing non-main function.
def check_unified_faithfulness_overview():
    spec = importlib.util.spec_from_file_location(
        'current_unified_faithfulness_overview', ROOT / 'scripts/check_unified_faithfulness_overview.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker.verify(ROOT)
