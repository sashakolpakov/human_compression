def check_programme51_documentation_history():
    """Replay the unchanged programme51 guard against its exact old documents."""
    from types import FunctionType
    import tempfile
    routes = {
        'README.rst': 'audit/documentation/v1/previous/README.rst',
        'audit/protocol.tex': 'audit/documentation/v1/previous/protocol.tex',
        'audit/protocol.pdf': 'audit/documentation/v1/previous/protocol.pdf',
    }
    admission = load('audit/documentation/v1/admission.json')
    check_bindings(admission['historical_documents'])
    need({row['path'] for row in admission['historical_documents']} == set(routes.values()),
         'Exactly three historical document bindings required.')
    with tempfile.TemporaryDirectory(prefix='programme51-doc-history-') as temporary:
        historical_root = Path(temporary)
        def populate(source, destination, prefix=''):
            destination.mkdir(exist_ok=True)
            for child in source.iterdir():
                relative = prefix + child.name
                target = destination / child.name
                if relative in routes:
                    target.symlink_to(ROOT / routes[relative])
                elif any(key.startswith(relative + '/') for key in routes):
                    populate(child, target, relative + '/')
                else:
                    target.symlink_to(child, target_is_directory=child.is_dir())
        populate(ROOT, historical_root)
        function = check_programme51
        scope = dict(function.__globals__, ROOT=historical_root)
        return FunctionType(function.__code__, scope, function.__name__,
                            function.__defaults__, function.__closure__)()


def check_current_documentation():
    spec = importlib.util.spec_from_file_location(
        'current_documentation', ROOT / 'scripts/check_current_documentation.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker.verify(ROOT)
