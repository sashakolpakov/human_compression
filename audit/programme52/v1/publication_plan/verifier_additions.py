# Add these two functions; do not replace any of the130 previous non-main bodies.
def check_previous_programme52():
    """Replay the preceding current programme and docs through exact saved routes."""
    from types import FunctionType
    import tempfile
    routes = load('audit/programme52/v1/history_routes.json')['routes']
    check_bindings(list(routes.values()))
    with tempfile.TemporaryDirectory(prefix='programme52-history-') as temporary:
        historical_root = Path(temporary)
        def populate(source, destination, prefix=''):
            destination.mkdir(exist_ok=True)
            for child in source.iterdir():
                relative = prefix + child.name
                target = destination / child.name
                if relative in routes:
                    target.symlink_to(ROOT / routes[relative]['path'])
                elif any(k.startswith(relative + '/') for k in routes):
                    populate(child, target, relative + '/')
                else:
                    target.symlink_to(child, target_is_directory=child.is_dir())
        populate(ROOT, historical_root)
        scope = dict(globals(), ROOT=historical_root)
        for name, value in list(globals().items()):
            if isinstance(value, FunctionType) and value.__globals__ is globals():
                scope[name] = FunctionType(value.__code__, scope, value.__name__,
                                          value.__defaults__, value.__closure__)
        previous = scope['check_programme51_documentation_history']()
        need(previous['recovered'] == 51, 'Preserved programme51 changed.')
        documents = scope['check_current_documentation']()
        need(documents['measured'] == 51 and documents['topics'] == 19,
             'Preserved current51 documentation changed.')
        return previous, documents


def check_programme52():
    spec = importlib.util.spec_from_file_location('programme52', ROOT / 'scripts/check_programme52.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    result = checker.verify(ROOT)
    need(check_current_measurement_pointer() == result['measured'] == 52,
         'Programme52 and unique original registry disagree.')
    return result
