# Append this function without editing any existing non-main function.
def check_projective_covers_overview():
    spec = importlib.util.spec_from_file_location(
        'current_projective_covers_overview', ROOT / 'scripts/check_projective_covers_overview.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker.verify(ROOT)
