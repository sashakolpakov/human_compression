"""Proposed NEW functions only; append after root inspection, preserving 133 ASTs.

Expected existing verifier globals: Path, ROOT, load, check_bindings, need,
importlib. Main wiring is described in README; no old function is replaced.
"""

def check_previous_programme53():
    """Run unchanged current52 checks against exact saved current52 routes."""
    from types import FunctionType
    import tempfile
    routes=load('audit/programme53/v1/history_routes.json')['routes']
    check_bindings(list(routes.values()))
    with tempfile.TemporaryDirectory(prefix='programme53-history-') as temporary:
        historical_root=Path(temporary)
        def populate(source,destination,prefix=''):
            destination.mkdir(exist_ok=True)
            for child in source.iterdir():
                relative=prefix+child.name;target=destination/child.name
                if relative in routes:target.symlink_to(ROOT/routes[relative]['path'])
                elif any(k.startswith(relative+'/') for k in routes):
                    populate(child,target,relative+'/')
                else:target.symlink_to(child,target_is_directory=child.is_dir())
        populate(ROOT,historical_root)
        scope=dict(globals(),ROOT=historical_root)
        for name,value in list(globals().items()):
            if isinstance(value,FunctionType)and value.__globals__ is globals():
                scope[name]=FunctionType(value.__code__,scope,value.__name__,value.__defaults__,value.__closure__)
        legacy=scope['check_previous_programme52']()
        previous=scope['check_programme52']()
        need(previous['measured']==52 and previous['mathematical_pending']==53,
             'Preserved programme52 partition changed.')
        return legacy,previous


def check_programme53():
    spec=importlib.util.spec_from_file_location('programme53',ROOT/'scripts/check_programme53.py')
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    result=checker.verify(ROOT)
    need(check_current_measurement_pointer()==result['measured']==53,
         'Programme53 and unique original registry disagree.')
    return result
