# Add these two functions without changing any existing non-main function.
def check_historical_listing_symmetry_overview():
    """Keep the v11 guard against its exact prior pointer and README."""
    from types import FunctionType
    base = 'audit/overview/v12/packet/inputs/'
    record = load('audit/overview/v12/packet/bindings.json')
    snapshots = {r['public_path']: r for r in record['public_inputs']
                 if r['public_path'] in ['audit/overview/latest.json', 'README.rst']}
    check_bindings([dict(r, path='audit/overview/v12/packet/' + r['local'])
                    for r in snapshots.values()])
    routes = {'audit/overview/latest.json': base + 'v11_pointer.json'}
    class HistoricalRoot:
        def __truediv__(self, path):
            return ROOT / (base + 'v11_README.rst' if str(path) == 'README.rst' else path)
    function = check_listing_symmetry_overview
    scope = dict(function.__globals__, ROOT=HistoricalRoot(),
                 load=lambda path: load(routes.get(str(path), path)))
    return FunctionType(function.__code__, scope, function.__name__,
                        function.__defaults__, function.__closure__)()


def check_listing_restored_overview():
    spec = importlib.util.spec_from_file_location(
        'current_listing_restoration', ROOT / 'scripts/check_listing_restored_overview.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker.verify(ROOT)
