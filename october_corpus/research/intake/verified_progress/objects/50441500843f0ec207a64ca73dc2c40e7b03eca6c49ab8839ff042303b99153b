"""Shared coded point/byte work; no authority or numerical model recognition."""
import time,resource,sys
class WorkStop(RuntimeError):pass
class Work:
    def __init__(self):self.start=time.monotonic();self.units=0
    def charge(self,n,why=''):
        if type(n)is not int or n<0:raise ValueError('nonnegative exact work debit')
        if self.units+n>10000000 or time.monotonic()-self.start>=20:raise WorkStop('10M/20s shared work')
        self.units+=n
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
        if rss>=117440512:raise WorkStop('112MiB cooperative RSS')
