#!/usr/bin/env python3
"""Replay 285 accepted finite GF(11) matrix certificates using only local JSON."""
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys
import time

if sys.flags.optimize:
    raise SystemExit("Run without -O: this verifier uses assertions.")

START = time.monotonic()
PRODUCTS = {}
FIELD = 0
INVERSES = 0
READ = 0
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
MANIFEST = {"file":"cases.json","bytes":98626,"sha256":"c7d06513d72110d64f0934c6862a7bd0dea2e37575f34f64cd499bf4091d8cae"}
IP_POSITIONS = [511,741,970,1199,1449,1676,1915,2126,2353,2793,3271,3517]
NG_POSITIONS = [3,5,6,10,12,14,18,19,20,22,24,25,27,36,43,87,102,147,152,190,256,257,258,259,265,267,269,270,273,275,277,278,279,282,284,285,286,288,289,292,294,297,300,302,304,306,307,308,311,312,333,341,416,502,522,569,589,610,618,693,701,796,820,833,857,905,909,964,968,1012,1065,1081,1101,1102,1103,1105,1107,1109,1111,1113,1114,1115,1121,1123,1124,1125,1127,1128,1131,1132,1134,1136,1138,1139,1140,1141,1142,1144,1145,1146,1147,1148,1150,1153,1192,1225,1241,1376,1391,1399,1558,1567,1612,1645,1765,1768,1803,1873,1913,1938,2002,2016,2044,2079,2114,2149,2175,2274,2282,2305,2362,2416,2435,2515,2550,2582,2624,2625,2667,2713,2732,2792,2800,2818,2819,2821,2822,2824,2825,2826,2827,2828,2829,2830,2831,2832,2835,2836,2837,2838,2839,2840,2845,2846,2847,2848,2849,2851,2852,2854,2855,2881,2904,2962,2974,3170,3206,3226,3299,3330,3361,3396,3397,3399,3400,3401,3402,3403,3406,3408,3409,3410,3412,3415,3416,3417,3419,3422,3424,3427,3430,3431,3433,3434,3435,3437,3439,3440,3443,3444,3445,3449,3451,3454,3457,3459,3466,3499,3525,3550,3567,3673,3674,3676,3677,3683,3686,3688,3689,3692,3694,3699,3701,3705,3708,3709,3711,3714,3716,3717,3718,3722,3723,3724,3725,3726,3730,3732,3733,3735,3737,3739,3741,3742,3744,3746,3747,3749,3750,3753,3754,3755,3756,3757,3762,3764,3765,3766,3767,3770,3773,3775,3776]


def tick():
    if time.monotonic() - START >= 100:
        raise RuntimeError("The finite replay exceeded its 100-second limit.")


def can(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def signature(value):
    return (value.st_dev,value.st_ino,value.st_mode,value.st_nlink,
            value.st_size,value.st_mtime_ns,value.st_ctime_ns)


def document(pin):
    global READ
    tick()
    assert type(pin) is dict and set(pin)=={"file","bytes","sha256"}
    name, size, digest = pin["file"], pin["bytes"], pin["sha256"]
    assert type(name) is str and name.endswith(".json")
    assert name.isascii() and all(c in "abcdefghijklmnopqrstuvwxyz0123456789_." for c in name)
    assert "/" not in name and "\\" not in name and name.count(".")==1
    assert type(size) is int and 0 < size <= 1048576
    assert type(digest) is str and len(digest)==64 and set(digest)<=set("0123456789abcdef")
    assert DATA.resolve(strict=True)==DATA
    path = DATA / name
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size==size
    assert READ + size + 1 <= 2097152
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        raw = stream.read(size + 1)
        closed = os.fstat(stream.fileno())
    assert signature(before)==signature(opened)==signature(closed)==signature(path.lstat())
    assert len(raw)==size and hashlib.sha256(raw).hexdigest()==digest
    READ += size + 1
    def unique(items):
        out = {}
        for key, value in items:
            assert key not in out
            out[key] = value
        return out
    def finite(text):
        value = float(text)
        assert math.isfinite(value)
        return value
    return json.loads(raw, object_pairs_hook=unique, parse_float=finite,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON")))


# These eight arithmetic definitions are literal copies of the Root-owned
# independent checker identified in SOURCE_PROVENANCE.json.
def mat(v,n):
 assert type(v)in(list,tuple)and len(v)==n and all(type(r)in(list,tuple)and len(r)==n and all(type(x)is int and 0<=x<11 for x in r)for r in v)
 return tuple(tuple(r)for r in v)

def identity(n):return tuple(tuple(int(i==j)for j in range(n))for i in range(n))

def mul(a,b):
 n=len(a);assert n==len(b)and all(len(r)==n for r in a+b)
 PRODUCTS[n]=PRODUCTS.get(n,0)+1;assert sum(PRODUCTS.values())<=400000;tick()
 return tuple(tuple(sum(a[i][k]*b[k][j]for k in range(n))%11 for j in range(n))for i in range(n))

def linpow(a,k):
 assert type(k)is int and 0<=k<=37
 x=identity(len(a))
 for _ in range(k):x=mul(x,a)
 return x

def image(v,a):return tuple(sum(v[i]*a[i][j]for i in range(7))%11 for j in range(7))

def inv2(a):
 global INVERSES
 d=(a[0][0]*a[1][1]-a[0][1]*a[1][0])%11;assert d
 x=pow(d,-1,11);INVERSES+=1
 return((a[1][1]*x%11,-a[0][1]*x%11),(-a[1][0]*x%11,a[0][0]*x%11))

def from_pair(row,IR,R):
 assert len(row)==7 and all(type(x)is int and 0<=x<11 for x in row)
 if row[0]==0:P=identity(2);Q=((10,0),(0,10))
 else:
  _,x,y,z,a,b,c=row;P=((x,y),(z,-x%11));Q=((a,b),(c,-a%11))
 det=lambda a:(a[0][0]*a[1][1]-a[0][1]*a[1][0])%11
 assert det(P)==det(Q)!=0
 ip=inv2(P);rows=[]
 for k in range(8):
  E=tuple(tuple(int(2*i+j==k%4)for j in range(2))for i in range(2))
  E=mul(mul(P if k<4 else Q,E),ip);flat=tuple(x for r in E for x in r)
  rows.append(flat+(0,0,0,0)if k<4 else(0,0,0,0)+flat)
 x=mul(mul(IR,tuple(rows)),R)
 assert x[0]==(1,0,0,0,0,0,0,0)and all(x[i][0]==0 for i in range(1,8))
 return tuple(tuple(x[i][j]for j in range(1,8))for i in range(1,8))

def fixed_row(y):
 global FIELD,INVERSES
 a=[[(y[j][i]-int(i==j))%11 for j in range(7)]for i in range(7)];pivots=[];rank=0
 for j in range(7):
  p=next((p for p in range(rank,7)if a[p][j]),None)
  if p is None:continue
  a[rank],a[p]=a[p],a[rank];z=pow(a[rank][j],-1,11);INVERSES+=1
  a[rank]=[z*x%11 for x in a[rank]];FIELD+=7
  for i in range(7):
   if i!=rank and a[i][j]:
    z=a[i][j];a[i]=[(x-z*b)%11 for x,b in zip(a[i],a[rank])];FIELD+=14
  pivots.append(j);rank+=1
 assert FIELD<=200000 and rank==6
 j=next(j for j in range(7)if j not in pivots);v=[0]*7;v[j]=1
 for i,k in enumerate(pivots):v[k]=-a[i][j]%11
 v=tuple(v);assert any(v)and image(v,y)==v
 return v

def row(value):
    assert type(value) is list and len(value)==7
    assert all(type(x) is int and 0<=x<11 for x in value) and any(value)
    return tuple(value)


def moved_line(v, mark, carrier):
    assert type(carrier) is dict
    z = image(v, mark)
    i, j = carrier["coordinates"]
    assert type(i) is int and type(j) is int and 0<=i<j<7
    minor = (v[i]*z[j] - v[j]*z[i]) % 11
    assert minor != 0 and minor == carrier["minor"]
    assert tuple(carrier["image"]) == z
    return z


def check_marks(position, representative, domain, a, b, e, R, IR):
    assert type(position) is int and 1<=position<=len(domain["orbits"])
    orbit = domain["orbits"][position-1]
    assert type(representative) is int and orbit[0]==representative
    assert 1<=representative<=len(domain["catalogue"]) and representative in orbit[1]
    c = from_pair(domain["catalogue"][representative-1], IR, R)
    marks = (a,b,c,e)
    I = identity(7)
    assert len(set(marks))==4
    assert all(g!=I and mul(g,g)==I for g in marks)
    assert all(mul(marks[i],marks[j])==mul(marks[j],marks[i])
               for i in range(4) for j in range(i+2,4))
    return marks


def main():
    manifest = document(MANIFEST)
    assert manifest["schema"]=="HUMAN_COMPRESSION_Q11_MATRIX_CERTIFICATES_V2"
    assert manifest["field"]==11 and manifest["dimension"]==7
    assert manifest["original_job"]==[24,4]
    assert set(manifest["files"])=={"domain","prefix","ambient_frame","spread_proof"}
    domain = document(manifest["files"]["domain"])
    prefix = document(manifest["files"]["prefix"])
    frame = document(manifest["files"]["ambient_frame"])
    proof = document(manifest["files"]["spread_proof"])
    assert domain["schema"]=="F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1"
    assert domain["certificate_verified"] is True
    assert domain["original_job"]==prefix["original_job"]==proof["original_job"]==[24,4]
    assert domain["rank"]==prefix["rank"]==4
    assert domain["field"]==prefix["field"]==frame["field"]==11
    assert prefix["dimension"]==frame["dimension"]==7
    assert domain["convention"]==prefix["convention"]=="RIGHT_ROW"
    assert domain["selected_labels"]==prefix["selected_labels"]==[1,4,2]
    assert prefix["end_order"]==[1,4,2,3]
    assert domain["external_premises"]==prefix["external_premises"]
    assert domain["external_premises"]["original_A_equals_G"] is True
    # Original absolute references are inert provenance. No referenced path is opened.
    for original, local in [(domain["prefix_export"],manifest["files"]["prefix"]),
                            (prefix["matrix_frame_result"],manifest["files"]["ambient_frame"])]:
        assert original["bytes"]==local["bytes"] and original["sha256"]==local["sha256"]
    assert len(domain["catalogue"])==domain["catalogue_size"]==14763
    assert hashlib.sha256(can(domain["catalogue"])).hexdigest()==domain["catalogue_sha256"]
    assert len(domain["orbits"])==3779
    assert hashlib.sha256(can(domain["orbits"])).hexdigest()==manifest["original_orbit_array_sha256"]==proof["original_orbit_array_sha256"]
    assert frame["full_generator_point_checks"]==354312 and frame["six_inverse_checks"]==6
    assert frame["ordered_generators"]==len(frame["source_matrices"])==2
    R = mat(domain["standard_to_actual_row_map"],8)
    IR = mat(domain["actual_to_standard_row_map"],8)
    assert mul(R,IR)==mul(IR,R)==identity(8)
    a,e,b = (mat(g,7) for g in prefix["matrices"])
    assert len(domain["standard_ordered_prefix_matrices"])==3
    for g, standard in zip((a,e,b), domain["standard_ordered_prefix_matrices"]):
        extended = ((1,0,0,0,0,0,0,0),) + tuple((0,)+r for r in g)
        assert mul(mul(IR,mat(standard,8)),R)==extended
    ambient = tuple(mat(g,7) for g in frame["source_matrices"])
    assert len(proof["records"])==16
    proof_rows = {r["original_orbit_position"]:r for r in proof["records"]}
    assert len(proof_rows)==16
    assert [r["position"] for r in manifest["IP_cases"]]==IP_POSITIONS
    assert [r["position"] for r in manifest["nongeneration_cases"]]==NG_POSITIONS
    assert set(IP_POSITIONS).isdisjoint(NG_POSITIONS)
    assert manifest["accepted_dispositions"]["IP_failure"]==12
    assert manifest["accepted_dispositions"]["nongeneration"]==273
    assert manifest["accepted_dispositions"]["total"]==285
    lines = manifest["nongeneration_prefix_lines"]
    assert type(lines) is list and len(lines)==3
    assert [line["line_index"] for line in lines]==[0,1,2]
    for line in lines:
        v = row(line["vector"])
        signs = line["prefix_signs"]
        assert type(signs) is dict and set(signs)=={"a","b","e"}
        assert all(type(q) is int and q in (1,10) for q in signs.values())
        for name,g in (("a",a),("b",b),("e",e)):
            assert image(v,g)==tuple(signs[name]*x%11 for x in v)
        j = line["ambient_index"]
        assert type(j) is int and 0<=j<len(ambient)
        moved_line(v,ambient[j],{"coordinates":line["minor_coordinates"],
                   "minor":line["minor"],"image":line["ambient_image"]})
    I = identity(7)
    for case in manifest["IP_cases"]:
        tick()
        p, rep = case["position"],case["representative_J_index"]
        marks = check_marks(p,rep,domain,a,b,e,R,IR)
        assert hashlib.sha256(can(marks)).hexdigest()==case["marks_sha256"]
        assert case["acceptance"]=="IP_batch_0001"
        carried = proof_rows[p]
        assert carried["representative_J_index"]==rep
        assert tuple(mat(g,7) for g in carried["actual_marks"])==marks
        end = case["end"]
        assert end in ("left","right")
        allowed = (0,1,2) if end=="left" else (1,2,3)
        w = carried["end_searches"][end]["prime_witnesses"]["37"]
        word = case["word"]
        assert type(word) is list and 1<=len(word)<=63
        assert all(type(j) is int and j in allowed for j in word)
        assert all(i!=j for i,j in zip(word,word[1:]))
        assert word==w["word"] and w["end"]==end
        assert type(w["prime"]) is int and w["prime"]==case["prime"]==37
        assert type(w["cofactor"]) is int and w["cofactor"]==case["cofactor"]==3
        W = I
        for j in word:
            W = mul(W,marks[j])
        assert W==mat(w["word_matrix"],7)
        Y = linpow(W,3)
        assert Y!=I and Y==mat(w["prime_element"],7)
        assert linpow(Y,37)==mat(w["prime_power"],7)==I
        v = row(case["fixed_row"])
        # Independently find a left fixed row, then check both exact row equations.
        found = fixed_row(Y)
        assert found==v and image(found,Y)==found and image(v,Y)==v
        j = case["moved"]["generator"]
        assert type(j) is int and j in allowed
        moved_line(v,marks[j],case["moved"])
        omitted = 3 if end=="left" else 0
        assert marks[omitted]!=I
    for case in manifest["nongeneration_cases"]:
        tick()
        marks = check_marks(case["position"],case["representative_J_index"],domain,a,b,e,R,IR)
        assert hashlib.sha256(can(marks)).hexdigest()==case["marks_sha256"]
        assert case["acceptance"] in ("NG_batch_0001","NG_batch_0002")
        k = case["prefix_line_index"]
        assert type(k) is int and 0<=k<3
        line = lines[k]
        assert case["fixed_row"]==line["vector"]
        v = row(case["fixed_row"])
        scalars = case["line_scalars"]
        assert [scalars[j] for j in (0,1,3)]==[line["prefix_signs"][s] for s in ("a","b","e")]
        assert type(scalars) is list and len(scalars)==4
        assert all(type(q) is int and 1<=q<11 for q in scalars)
        for g,q in zip(marks,scalars):
            assert image(v,g)==tuple(q*x%11 for x in v)
        mover = case["ambient_moved_line"]
        j = mover["ambient_generator"]
        assert type(j) is int and 0<=j<len(ambient)
        moved_line(v,ambient[j],mover)
    tick()
    print(json.dumps(dict(status="PASS",original_job=[24,4],verified_cases=285,
        IP_failure_positions=IP_POSITIONS,nongeneration_positions=NG_POSITIONS,
        matrix_products=PRODUCTS,rank_field_operations=FIELD,field_inverses=INVERSES,
        pinned_data_read_charge_bytes=READ,seconds=time.monotonic()-START,
        qualification="Finite certificate arithmetic only; original group/model/frame/orbit and IP classification premises remain borrowed. No Lean or whole-manuscript verification."),sort_keys=True))


if __name__ == "__main__":
    main()
