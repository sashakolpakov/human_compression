"""Prospective, sampled resource supervision; never changes acquired owners.

No kernel memory quota or process containment is claimed. On Darwin, descendant
discovery uses targeted libproc calls rather than a global process enumeration.
An observed task that escapes a process group remains owned by its birth pin.
"""
import argparse
import collections
import ctypes
import datetime
import errno
import fcntl
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
import psutil

GIB = 2**30
ADMIT_DISK, ADMIT_RAM = 10 * GIB, 6 * GIB
DISK_FLOOR, RAM_FLOOR = 8 * GIB, 3 * GIB
LOG_CAP, RECORD_CAP, PID_CAP = 256 * 2**10, 128 * 2**10, 128
POLL_SECONDS, GRACE_SECONDS = .5, 3.0


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def remember(errors, messages):
    errors.extend(list(messages)[:max(0, 16 - len(errors))])


def write_record(path, value):
    raw = (json.dumps(value, indent=2) + '\n').encode()
    require(len(raw) <= RECORD_CAP, 'metadata record cap')
    stage = path.with_suffix(path.suffix + '.staged')
    with stage.open('xb') as stream:
        stream.write(raw)
    os.replace(stage, path)


class Family:
    """Retain owned identities, including descendants whose parents have exited."""
    def __init__(self, child):
        self.known = {}
        self.lib = None
        if sys.platform == 'darwin':
            self.lib = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
            self.lib.proc_listchildpids.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
            self.lib.proc_listchildpids.restype = ctypes.c_int
        self.add(child.pid, os.getpid())
        require(self.known[child.pid]['group'] == child.pid, 'new child session group')

    def children(self, pid):
        if self.lib is None:
            return [p.pid for p in psutil.Process(pid).children(recursive=False)]
        buffer = (ctypes.c_int * (PID_CAP + 1))()
        ctypes.set_errno(0)
        count = self.lib.proc_listchildpids(pid, buffer, ctypes.sizeof(buffer))
        if count < 0 or (count == 0 and ctypes.get_errno()):
            raise OSError(ctypes.get_errno(), 'targeted child observation failed')
        require(count < len(buffer), 'child observation capacity')
        return [int(buffer[i]) for i in range(count) if buffer[i] > 0]

    def same(self, row):
        try:
            process = psutil.Process(row['pid'])
            if process.create_time() != row['birth']:
                return None
            return process
        except psutil.NoSuchProcess:
            return None

    def add(self, pid, parent):
        if pid in self.known:
            process = psutil.Process(pid)
            require(process.create_time() == self.known[pid]['birth'],
                    'observed owned PID reused')
            return
        require(len(self.known) < PID_CAP, 'owned process count cap')
        process = psutil.Process(pid)
        require(process.ppid() == parent, 'descendant ancestry changed during observation')
        self.known[pid] = dict(pid=pid, birth=process.create_time(),
                               initial_parent=parent, group=os.getpgid(pid),
                               session=os.getsid(pid), peak_rss=0)

    def sample(self):
        # Scan every retained living ancestor, so reparenting does not discard
        # already discovered children. Processes born and lost between samples
        # are not proved absent: this is sampling, not process containment.
        pending = list(self.known)
        visited = set()
        while pending:
            pid = pending.pop()
            if pid in visited:
                continue
            visited.add(pid)
            try:
                process = self.same(self.known[pid])
                if process is None or process.status() == psutil.STATUS_ZOMBIE:
                    continue
                children = self.children(pid)
            except psutil.NoSuchProcess:
                continue
            except ProcessLookupError as exc:
                if exc.errno != errno.ESRCH:
                    raise
                continue
            for child in children:
                try:
                    self.add(child, pid)
                    pending.append(child)
                except psutil.NoSuchProcess:
                    continue
                except ProcessLookupError as exc:
                    if exc.errno != errno.ESRCH:
                        raise
                    continue
        total, live = 0, []
        for row in self.known.values():
            try:
                process = self.same(row)
                if process is None or process.status() == psutil.STATUS_ZOMBIE:
                    continue
                rss = process.memory_info().rss
            except psutil.NoSuchProcess:
                continue
            except ProcessLookupError as exc:
                if exc.errno != errno.ESRCH:
                    raise
                continue
            row['peak_rss'] = max(row['peak_rss'], rss)
            total += rss
            live.append(row['pid'])
        supervisor_rss = psutil.Process().memory_info().rss
        return dict(task_rss=total, supervisor_rss=supervisor_rss,
                    total_rss=total + supervisor_rss, live_pids=live)

    def signal_known(self, sig):
        # Never signal by a name or a stale PID. Detached sessions discovered
        # through owned ancestry are included; birth mismatch means no signal.
        errors = []
        signalled_groups = set()
        for row in reversed(list(self.known.values())):
            try:
                process = self.same(row)
                if process is None or process.status() == psutil.STATUS_ZOMBIE:
                    continue
                require(process.create_time() == row['birth'], 'fresh signal identity')
                group = os.getpgid(row['pid'])
                session = os.getsid(row['pid'])
                # A live birth-pinned descendant belongs to a session descending
                # from the wrapped child's fresh session. It can create a new
                # session, but cannot join an unrelated session. Such a member
                # proves group ownership even after its group leader exits.
                require(group != os.getpgrp() and session != os.getsid(0),
                        'never signal supervisor session or group')
                require(process.create_time() == row['birth'], 'fresh group witness identity')
                if group not in signalled_groups:
                    os.killpg(group, sig)
                    signalled_groups.add(group)
                process.send_signal(sig)
            except (psutil.NoSuchProcess, ProcessLookupError):
                continue
            except Exception as exc:
                remember(errors, [type(exc).__name__ + ': ' + str(exc)[:512]])
        return errors

    def cleanup(self, child):
        errors = []
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                self.sample()
                remember(errors, self.signal_known(sig))
            except Exception as exc:
                remember(errors, [type(exc).__name__ + ': ' + str(exc)[:512]])
                # Observation failure must not prevent signalling identities
                # that were already proved ours.
                try:
                    remember(errors, self.signal_known(sig))
                except Exception as inner:
                    remember(errors, [type(inner).__name__ + ': ' + str(inner)[:512]])
            deadline = time.monotonic() + GRACE_SECONDS
            while time.monotonic() < deadline:
                alive = False
                for row in self.known.values():
                    try:
                        process = self.same(row)
                        alive |= process is not None and process.status() != psutil.STATUS_ZOMBIE
                    except psutil.NoSuchProcess:
                        continue
                    except Exception as exc:
                        remember(errors, [type(exc).__name__ + ': ' + str(exc)[:512]])
                        alive = True
                if child.poll() is not None and not alive:
                    break
                time.sleep(.05)
        try:
            child.wait(timeout=1)
        except subprocess.TimeoutExpired:
            remember(errors, ['wrapped owner was not reaped'])
        remaining = []
        for row in self.known.values():
            try:
                process = self.same(row)
                if process is not None and process.status() != psutil.STATUS_ZOMBIE:
                    remaining.append(dict(pid=row['pid'], birth=row['birth']))
            except psutil.NoSuchProcess:
                continue
            except Exception as exc:
                remember(errors, [type(exc).__name__ + ': ' + str(exc)[:512]])
        return dict(remaining=remaining, errors=errors[:16],
                    qualification='Known birth-pinned processes only; unseen detached descendants are not excluded.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--volume', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--rss-cap-mib', type=int, required=True)
    parser.add_argument('--timeout', type=float, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    require(command and Path(command[0]).is_absolute(), 'absolute executable required')
    require(len(command) <= 128 and sum(len(x.encode()) for x in command) <= 16384,
            'bounded command metadata')
    if Path(command[0]).name.startswith('python'):
        interpreter_options = []
        for value in command[1:]:
            if not value.startswith('-') or value in ('-c', '-m', '--'):
                break
            interpreter_options.append(value)
        require('-B' in interpreter_options, 'Python commands must explicitly use -B')
    require(1 <= args.rss_cap_mib <= 6144 and 0 < args.timeout <= 1800,
            'explicit RSS cap up to 6 GiB and wall cap up to 1800 seconds')
    require(args.output.is_absolute() and not args.output.exists(), 'fresh absolute output')
    require(args.volume.is_absolute() and args.volume.is_dir(), 'existing volume path')
    cap = args.rss_cap_mib * 2**20
    lock_path = Path(__file__).resolve().parent / 'active.lock'
    lock = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_CLOEXEC, 0o600)
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(lock)
        print('NOT_LAUNCHED: another supervised task holds the project lock', flush=True)
        return 75
    try:
        admission = dict(free_disk=shutil.disk_usage(args.volume).free,
                         available_ram=psutil.virtual_memory().available)
        required_ram = max(ADMIT_RAM, cap + RAM_FLOOR)
        require(admission['free_disk'] >= ADMIT_DISK and admission['available_ram'] >= required_ram,
                '10 GiB disk / max(6 GiB, RSS cap + 3 GiB) RAM admission')
        args.output.mkdir(mode=0o700)
        temporary = args.output / 'tmp'
        temporary.mkdir(mode=0o700)
        limits = dict(admit_disk=ADMIT_DISK, admit_ram=required_ram,
                      disk_floor=DISK_FLOOR, ram_floor=RAM_FLOOR,
                      total_rss=cap, wall_seconds=args.timeout, sample_seconds=POLL_SECONDS,
                      log_bytes_each=LOG_CAP, metadata_bytes_each=RECORD_CAP, owned_pids=PID_CAP)
        begin = time.monotonic()
        child = family = None
        stop = 'INCOMPLETE'
        error = None
        samples = collections.deque(maxlen=16)
        peaks = dict(total_rss=0, min_free_disk=admission['free_disk'],
                     min_available_ram=admission['available_ram'], samples=0)
        written = dict(stdout=0, stderr=0)
        logs = {name: (args.output / (name + '.log')).open('xb') for name in written}
        selector = selectors.DefaultSelector()
        interrupted = []
        previous = {}
        def interrupt(sig, frame):
            if not interrupted:
                interrupted.append(sig)
        for sig in (signal.SIGINT, signal.SIGTERM):
            previous[sig] = signal.signal(sig, interrupt)
        try:
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1',
                               TMPDIR=str(temporary), TMP=str(temporary), TEMP=str(temporary))
            child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     start_new_session=True, env=environment, close_fds=True)
            family = Family(child)
            write_record(args.output / 'started.json', dict(utc=utc(), command=command,
                         identities=list(family.known.values()), limits=limits, admission=admission))
            for name in logs:
                pipe = getattr(child, name)
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, name)
            next_sample = 0
            while True:
                elapsed = time.monotonic() - begin
                if interrupted:
                    stop = 'INTERRUPTED'
                    break
                if elapsed >= args.timeout:
                    stop = 'WALL_CAP'
                    break
                if elapsed >= next_sample:
                    observed = family.sample()
                    free = shutil.disk_usage(args.volume).free
                    available = psutil.virtual_memory().available
                    samples.append(dict(seconds=round(elapsed, 3), total_rss=observed['total_rss'],
                                        free_disk=free, available_ram=available,
                                        live_processes=len(observed['live_pids'])))
                    peaks['samples'] += 1
                    peaks['total_rss'] = max(peaks['total_rss'], observed['total_rss'])
                    peaks['min_free_disk'] = min(peaks['min_free_disk'], free)
                    peaks['min_available_ram'] = min(peaks['min_available_ram'], available)
                    if free < DISK_FLOOR or available < RAM_FLOOR or observed['total_rss'] > cap:
                        stop = ('DISK_FLOOR' if free < DISK_FLOOR else
                                'HOST_RAM_FLOOR' if available < RAM_FLOOR else 'TREE_RSS_CAP')
                        break
                    next_sample = elapsed + POLL_SECONDS
                for key, event in selector.select(timeout=.05):
                    raw = os.read(key.fileobj.fileno(), 65536)
                    if not raw:
                        selector.unregister(key.fileobj)
                        continue
                    name = key.data
                    room = LOG_CAP - written[name]
                    logs[name].write(raw[:room])
                    written[name] += min(len(raw), room)
                    if len(raw) > room:
                        stop = 'LOG_CAP'
                        break
                if stop == 'LOG_CAP':
                    break
                if child.poll() is not None and not selector.get_map():
                    observed = family.sample()
                    stop = 'RETURNED' if not observed['live_pids'] else 'DESCENDANTS_REMAIN'
                    break
        except BaseException as exc:
            stop = 'OBSERVATION_OR_OWNER_FAILURE'
            error = type(exc).__name__ + ': ' + str(exc)[:1024]
        finally:
            try:
                cleanup = family.cleanup(child) if family is not None else None
            except BaseException as exc:
                cleanup = dict(errors=['cleanup failed: ' + type(exc).__name__ + ': ' + str(exc)[:512]])
            if child is not None and family is None:
                # The unreaped Popen PID cannot have been reused. Only signal
                # that direct child; unknown descendants remain an explicit gap.
                try:
                    child.terminate()
                    child.wait(timeout=GRACE_SECONDS)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait(timeout=1)
                except ProcessLookupError:
                    pass
                cleanup = dict(errors=['family initialization failed; descendant absence unproved'])
            for pipe in (getattr(child, 'stdout', None), getattr(child, 'stderr', None)):
                if pipe is not None:
                    pipe.close()
            selector.close()
            for log in logs.values():
                log.close()
            for sig, handler in previous.items():
                signal.signal(sig, handler)
            ok = (stop == 'RETURNED' and child is not None and child.returncode == 0
                  and cleanup is not None and not cleanup.get('remaining') and not cleanup.get('errors'))
            receipt = dict(status='PASS' if ok else 'INCOMPLETE', stop=stop, error=error,
                           utc=utc(), seconds=time.monotonic() - begin,
                           returncode=child.returncode if child else None, command=command,
                           limits=limits, admission=admission, peaks=peaks,
                           recent_samples=list(samples), identities=list(family.known.values()) if family else [],
                           logs=written, cleanup=cleanup,
                           qualification='Sampled limits; no kernel quota or absence proof for unseen detached descendants.')
            write_record(args.output / 'receipt.json', receipt)
            print(json.dumps(dict(status=receipt['status'], stop=stop,
                                  receipt=str(args.output / 'receipt.json'))), flush=True)
        return 0 if ok else 1
    finally:
        os.close(lock)  # Keep the stable lock file; unlinking creates a lock race.


if __name__ == '__main__':
    raise SystemExit(main())
