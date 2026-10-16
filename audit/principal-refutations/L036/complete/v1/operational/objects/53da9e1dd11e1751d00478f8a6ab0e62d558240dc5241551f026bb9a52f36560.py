"""Disposable ordinary-memory checks; never run the M11 computation."""
import json
import memory_guard as guard
value=guard.check_memory(force=True)
assert 0<value<guard.LIMIT_BYTES
old=guard.LIMIT_BYTES;guard.LIMIT_BYTES=1
try:
    guard.check_memory(force=True)
except MemoryError as e:
    assert 'sampled peak RSS exceeds' in str(e)
else:raise ValueError('one-byte threshold was ignored')
finally:guard.LIMIT_BYTES=old
print(json.dumps({'status':'PASS_L036_SELF_MEMORY_GUARD','platform_units':'Darwin bytes, other platforms KiB converted to bytes','observed_peak_bytes':value,'one_byte_limit_rejected':True,'M11_target_executed':False}))
