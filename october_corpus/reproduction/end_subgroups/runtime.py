"""Retained fixed-dimension arithmetic budget; no IO, solver or discovery."""
import resource,sys,time
CAPS=dict(matrix_products=400000,row_images=200000,linear_units=200000)
class Limit(RuntimeError):pass
def need(ok,message):
    if not ok:raise ValueError(message)
class Budget:
    Limit=Limit
    def __init__(self):
        self.started=time.monotonic();self.calls=0;self.products=0;self.rows=0;self.linear=0
        self.read_bytes=0;self.explicit_read_bytes=0;self.import_source_reserved_bytes=0
        self.paths=set();self.reads=[];self.peak_rss=0

    def tick(self):
        self.calls+=1
        if time.monotonic()-self.started>90:raise Limit('90 second cooperative deadline; outer role remains 100/150 seconds')
        if self.calls%256==1:
            rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if sys.platform!='darwin':rss*=1024
            self.peak_rss=max(self.peak_rss,rss)
            if rss>117440512:raise Limit('112 MiB cooperative RSS; outer role remains 128 MiB')

    def scalar(self,n):
        self.tick();need(type(n)is int and n>=0,'nonnegative linear debit')
        if self.linear+n>CAPS['linear_units']:raise Limit('shared 200000 linear-unit bank')
        self.linear+=n

    def multiply(self,a,b):
        self.tick()
        if self.products>=CAPS['matrix_products']:raise Limit('400000 complete matrix products')
        self.products+=1
        return bytes(sum(a[7*i+k]*b[7*k+j]for k in range(7))%11 for i in range(7)for j in range(7))

    def image(self,v,a):
        self.tick()
        if self.rows>=CAPS['row_images']:raise Limit('200000 complete row images')
        self.rows+=1
        return bytes(sum(v[k]*a[7*k+j]for k in range(7))%11 for j in range(7))

