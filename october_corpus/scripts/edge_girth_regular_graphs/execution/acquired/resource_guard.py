"""Operational observations of this controller's own subprocess group only."""
import ctypes, errno, os, shutil, signal, time
from pathlib import Path

GIB=1024**3
LIB=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
LIB.proc_listchildpids.argtypes=[ctypes.c_int,ctypes.c_void_p,ctypes.c_int]
LIB.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p]

def children(pid):
    buf=(ctypes.c_int*256)()
    ctypes.set_errno(0)
    count=LIB.proc_listchildpids(pid,buf,ctypes.sizeof(buf))
    if count<0:raise OSError(ctypes.get_errno(),'own child list unavailable')
    if count>=len(buf):raise RuntimeError('own process family exceeds sampling capacity')
    return [int(buf[i]) for i in range(count) if buf[i]>0]

def group_memory(leader,known):
    # Retain discovered descendants in case their immediate parent returns.
    todo=[leader];seen=set();rows=[]
    while todo:
        pid=todo.pop()
        if pid in seen:continue
        seen.add(pid)
        try:
            if os.getpgid(pid)!=leader:raise RuntimeError('owned descendant left its group')
            todo.extend(children(pid))
        except ProcessLookupError:continue
    known.update(seen)
    for pid in sorted(known):
        try:
            if os.getpgid(pid)!=leader:continue  # exited PID may have been reused
        except ProcessLookupError:continue
        buf=ctypes.create_string_buffer(4096);ctypes.set_errno(0)
        if LIB.proc_pid_rusage(pid,0,ctypes.byref(buf)):
            if ctypes.get_errno()==errno.ESRCH:continue
            raise OSError(ctypes.get_errno(),'own process memory unavailable')
        words=ctypes.cast(buf,ctypes.POINTER(ctypes.c_uint64))
        rows.append(dict(pid=pid,resident_bytes=int(words[8]),footprint_bytes=int(words[9])))
    return dict(resident_bytes=sum(r['resident_bytes'] for r in rows),processes=rows)

def logical_bytes(roots):
    total=0
    for root in roots:
        root=Path(root)
        if not root.exists():continue
        if root.is_symlink():raise RuntimeError('owned output root became a symlink')
        if root.is_file():
            total+=root.stat().st_size
            continue
        for directory,dirs,files in os.walk(root):
            for name in dirs+files:
                p=Path(directory)/name
                if p.is_symlink():raise RuntimeError('owned output contains a symlink')
            for name in files:
                try:total+=(Path(directory)/name).stat().st_size
                except FileNotFoundError:pass  # atomic status replacement
    return total

def decision(free,growth,rss,elapsed,limits):
    if free<limits['reserve_bytes']:return 'HOLD_DISK_RESERVE'
    if growth>limits['growth_cap_bytes']:return 'HOLD_OUTPUT_GROWTH_CAP'
    if rss>limits['family_rss_cap_bytes']:return 'HOLD_PROCESS_MEMORY_CAP'
    if elapsed>=limits['phase_seconds']:return 'HOLD_PHASE_WALL_CAP'
    return None

def stop_group(proc):
    try:os.killpg(proc.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    try:proc.wait(timeout=5)
    except __import__('subprocess').TimeoutExpired:
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        proc.wait(timeout=5)

def watch(proc,roots,study,limits):
    begin=time.monotonic();known=set();samples=[];status='RETURNED';error=None
    try:
        while proc.poll() is None:
            sample=dict(elapsed_seconds=time.monotonic()-begin,
                free_disk_bytes=shutil.disk_usage(study).free,
                logical_output_bytes=logical_bytes(roots),**group_memory(proc.pid,known))
            samples.append(sample)
            status=decision(sample['free_disk_bytes'],sample['logical_output_bytes'],
                            sample['resident_bytes'],sample['elapsed_seconds'],limits) or 'RETURNED'
            if status!='RETURNED':stop_group(proc);break
            time.sleep(limits['sample_seconds'])
        code=proc.wait()
    except BaseException as exc:
        stop_group(proc);code=proc.returncode;status='HOLD_RESOURCE_OBSERVATION_FAILURE'
        error=dict(type=type(exc).__name__,message=str(exc))
    return dict(terminal=status,returncode=code,seconds=time.monotonic()-begin,
                peak_sampled_family_rss_bytes=max((r['resident_bytes'] for r in samples),default=0),
                maximum_sampled_output_bytes=max((r['logical_output_bytes'] for r in samples),default=0),
                minimum_sampled_free_bytes=min((r['free_disk_bytes'] for r in samples),default=None),
                samples=samples,error=error,limits=limits,
                limitation='Sampled operational guards may overshoot between observations; no mathematical resource bound is claimed.')
