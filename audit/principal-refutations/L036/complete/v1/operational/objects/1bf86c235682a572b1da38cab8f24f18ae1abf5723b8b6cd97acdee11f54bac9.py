"""Supported cooperative peak-RSS guard; no hard kernel-limit claim."""
import resource
import sys
LIMIT_BYTES=1024*2**20
COUNT=0
def peak_bytes():
    value=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform=='darwin' else value*1024)
def check_memory(force=False):
    global COUNT
    COUNT+=1
    if force or COUNT%1024==0:
        value=peak_bytes()
        if value>LIMIT_BYTES:
            raise MemoryError('sampled peak RSS exceeds '+str(LIMIT_BYTES)+' bytes: '+str(value))
        return value
    return None
