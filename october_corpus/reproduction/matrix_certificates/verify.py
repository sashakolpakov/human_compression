#!/usr/bin/env python3
"""Replay 1595 accepted finite GF(11) matrix certificates using local JSON."""
import hashlib
import itertools
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
DETERMINANT_TERMS = 0
READ = 0
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
MANIFEST = {"bytes":691801,"file":"cases.json","sha256":"4fce668f6e7b954ec1e958eab6dcb1b8dfc335fbae4da9626506d6ce54e7538c"}
IP_POSITIONS = [45,48,52,54,55,58,60,70,71,72,73,78,80,84,91,92,94,96,98,100,101,107,109,112,126,127,128,130,135,141,154,158,159,161,163,169,174,176,179,180,181,183,185,186,188,191,193,194,195,196,201,202,205,209,211,215,217,222,223,227,230,231,235,239,241,246,249,250,251,252,325,327,329,331,332,334,335,336,340,348,351,352,354,355,356,357,358,359,360,365,366,367,371,374,376,381,382,383,384,387,391,393,398,399,401,403,404,409,410,412,415,418,420,423,429,430,434,437,438,439,442,443,444,445,462,463,467,478,483,484,489,490,491,492,493,496,497,499,500,505,508,510,511,512,514,515,518,521,523,527,528,530,532,537,538,540,542,543,544,548,560,561,564,567,568,571,572,573,578,580,581,584,586,588,591,593,595,598,608,611,612,613,614,615,616,619,620,622,624,630,632,633,635,636,637,640,641,643,644,645,648,649,651,653,656,657,663,665,666,668,670,671,673,677,678,682,685,689,691,696,698,702,705,707,710,711,718,719,720,724,728,734,735,737,741,743,744,745,751,753,757,759,761,764,768,769,770,773,774,775,776,777,779,780,783,784,786,788,789,790,794,795,798,799,805,806,809,810,812,813,814,817,824,826,827,829,834,842,848,849,852,855,859,862,864,865,866,873,880,881,889,895,898,899,901,910,911,918,924,928,933,934,936,937,940,946,948,949,950,951,952,956,957,958,963,965,966,970,973,974,975,979,980,983,985,986,990,995,996,997,1000,1004,1006,1007,1010,1013,1014,1015,1016,1017,1021,1024,1026,1027,1029,1033,1034,1035,1037,1038,1040,1045,1047,1048,1050,1052,1054,1056,1057,1062,1064,1069,1070,1074,1077,1080,1083,1085,1086,1087,1091,1092,1157,1162,1164,1166,1167,1169,1173,1174,1175,1176,1178,1179,1180,1181,1182,1183,1185,1194,1199,1201,1203,1205,1209,1212,1213,1214,1216,1217,1218,1220,1221,1224,1227,1228,1229,1230,1232,1234,1236,1239,1240,1247,1252,1254,1256,1260,1262,1263,1268,1269,1276,1278,1280,1282,1284,1286,1287,1290,1293,1295,1296,1299,1300,1301,1318,1322,1323,1328,1331,1332,1333,1334,1335,1340,1352,1355,1356,1358,1360,1361,1370,1375,1377,1378,1379,1385,1387,1390,1396,1402,1403,1410,1412,1413,1417,1421,1422,1423,1424,1425,1433,1435,1443,1449,1450,1457,1459,1464,1469,1470,1474,1477,1478,1479,1485,1488,1492,1493,1494,1496,1503,1505,1506,1508,1511,1517,1519,1522,1526,1527,1528,1534,1538,1539,1545,1550,1552,1553,1562,1565,1572,1573,1575,1577,1582,1586,1587,1589,1590,1594,1597,1598,1599,1600,1601,1603,1604,1607,1608,1611,1613,1616,1617,1618,1619,1620,1621,1622,1624,1625,1626,1627,1632,1635,1638,1640,1642,1644,1655,1661,1663,1668,1669,1675,1676,1681,1686,1693,1700,1705,1708,1709,1711,1712,1713,1714,1721,1722,1725,1728,1729,1734,1736,1743,1747,1751,1752,1753,1759,1761,1762,1767,1772,1774,1775,1776,1777,1778,1779,1784,1787,1792,1794,1795,1796,1797,1798,1799,1806,1807,1808,1811,1812,1813,1814,1816,1823,1826,1828,1829,1830,1832,1833,1837,1838,1839,1840,1843,1844,1852,1857,1858,1864,1867,1868,1869,1871,1872,1879,1882,1883,1884,1887,1888,1890,1893,1896,1897,1898,1900,1902,1903,1904,1906,1907,1915,1916,1917,1920,1924,1927,1929,1930,1933,1934,1939,1940,1941,1942,1944,1945,1946,1947,1950,1952,1953,1954,1958,1960,1963,1966,1967,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1983,1984,1985,1987,1991,1994,1995,2001,2005,2009,2011,2017,2019,2021,2023,2024,2025,2030,2033,2035,2036,2038,2047,2048,2056,2057,2058,2059,2064,2065,2066,2067,2073,2077,2078,2080,2086,2088,2092,2095,2096,2097,2100,2102,2103,2105,2109,2110,2112,2115,2119,2126,2132,2133,2136,2143,2145,2148,2150,2152,2153,2158,2160,2163,2166,2170,2171,2179,2180,2181,2184,2185,2188,2189,2192,2193,2194,2195,2196,2197,2200,2209,2210,2211,2215,2216,2218,2221,2222,2223,2234,2235,2238,2240,2243,2245,2248,2249,2251,2254,2255,2256,2257,2260,2261,2267,2268,2269,2270,2272,2278,2281,2286,2291,2293,2296,2300,2301,2303,2304,2308,2314,2319,2325,2327,2334,2336,2339,2340,2341,2345,2350,2351,2353,2354,2355,2357,2360,2363,2368,2371,2374,2375,2379,2380,2381,2382,2384,2385,2388,2391,2392,2394,2396,2399,2400,2401,2404,2405,2406,2407,2410,2412,2414,2415,2418,2424,2426,2433,2434,2436,2441,2446,2453,2455,2458,2459,2463,2464,2470,2472,2476,2478,2481,2483,2484,2485,2486,2487,2490,2491,2493,2495,2496,2500,2501,2502,2503,2504,2506,2511,2512,2513,2514,2517,2518,2519,2521,2525,2527,2529,2530,2534,2538,2539,2543,2544,2545,2546,2547,2554,2556,2559,2565,2567,2569,2573,2578,2589,2590,2591,2592,2594,2595,2596,2597,2598,2605,2606,2610,2611,2613,2619,2620,2621,2626,2627,2628,2629,2631,2632,2633,2634,2638,2639,2640,2643,2645,2647,2648,2649,2650,2651,2652,2653,2655,2656,2658,2661,2665,2668,2670,2671,2672,2675,2682,2684,2688,2690,2691,2692,2693,2697,2699,2700,2703,2704,2706,2709,2711,2712,2717,2718,2719,2720,2721,2725,2726,2727,2734,2739,2740,2745,2746,2747,2748,2749,2755,2757,2761,2763,2767,2771,2773,2779,2784,2793,2794,2796,2797,2802,2804,2805,2807,2808,2809,2811,2812,2814,2816,2817,2858,2859,2860,2861,2862,2864,2869,2871,2872,2880,2882,2883,2886,2887,2890,2895,2896,2898,2902,2903,2905,2906,2909,2911,2914,2915,2919,2920,2922,2924,2925,2926,2927,2928,2933,2934,2936,2939,2940,2941,2942,2944,2946,2948,2949,2950,2953,2954,2963,2964,2969,2972,2973,2977,2978,2983,2984,2986,2987,2990,2992,2995,2996,2997,2998,3000,3001,3004,3008,3009,3010,3011,3015,3019,3024,3026,3027,3029,3032,3037,3040,3041,3043,3044,3046,3047,3052,3054,3057,3061,3065,3070,3071,3074,3081,3082,3089,3094,3098,3099,3100,3109,3113,3114,3116,3117,3118,3120,3127,3129,3130,3132,3134,3137,3138,3141,3146,3154,3156,3160,3163,3165,3166,3167,3168,3169,3172,3176,3177,3178,3179,3181,3182,3183,3185,3186,3187,3188,3192,3194,3195,3196,3198,3201,3203,3211,3212,3213,3214,3215,3216,3219,3220,3222,3224,3228,3229,3230,3233,3234,3237,3239,3240,3241,3242,3245,3248,3252,3256,3259,3260,3262,3266,3267,3269,3271,3273,3274,3280,3281,3285,3292,3296,3297,3301,3303,3306,3307,3312,3313,3316,3317,3320,3323,3324,3325,3326,3327,3328,3331,3332,3334,3335,3336,3337,3349,3350,3353,3354,3355,3362,3368,3369,3371,3372,3373,3374,3377,3378,3381,3382,3384,3385,3391,3392,3393,3395,3468,3469,3471,3473,3474,3475,3478,3479,3480,3481,3482,3483,3487,3488,3492,3494,3496,3501,3502,3504,3505,3511,3514,3517,3519,3522,3524,3526,3527,3529,3530,3531,3534,3536,3545,3547,3549,3557,3558,3559,3561,3563,3564,3565,3568,3572,3574,3575,3581,3582,3584,3585,3587,3589,3593,3594,3596,3597,3602,3607,3608,3609,3613,3615,3619,3621,3623,3628,3633,3637,3649,3650,3652,3654,3655,3656,3661,3665,3667]
LEGACY_IP_POSITIONS = [511,741,970,1199,1449,1676,1915,2126,2353,2793,3271,3517]
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

def determinant6(value):
    """Use the explicit Leibniz sum; count its work apart from RREF."""
    global DETERMINANT_TERMS
    assert type(value) is tuple and len(value)==6
    assert all(type(r) is tuple and len(r)==6 and
               all(type(x) is int and 0<=x<11 for x in r) for r in value)
    answer = 0
    for permutation in itertools.permutations(range(6)):
        tick()
        odd = sum(permutation[i]>permutation[j]
                  for i in range(6) for j in range(i+1,6)) % 2
        term = -1 if odd else 1
        for i in range(6):
            term = term*value[i][permutation[i]] % 11
        answer = (answer+term) % 11
        DETERMINANT_TERMS += 1
        assert DETERMINANT_TERMS <= 943200
    return answer


def supplied_rank6_row(Y, case):
    """A nonzero left kernel row and a nonzero six-minor force rank six."""
    v = row(case["fixed_row"])
    assert image(v,Y)==v
    witness = case["rank6_minor"]
    assert type(witness) is dict and set(witness)=={"rows","columns","determinant"}
    rows, columns = witness["rows"], witness["columns"]
    for indices in (rows,columns):
        assert type(indices) is list and len(indices)==6
        assert all(type(i) is int and 0<=i<7 for i in indices)
        assert indices==sorted(set(indices))
    value = tuple(tuple((Y[i][j]-int(i==j))%11 for j in columns) for i in rows)
    carried = witness["determinant"]
    assert type(carried) is int and 1<=carried<11
    assert determinant6(value)==carried
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
    assert manifest["schema"]=="HUMAN_COMPRESSION_Q11_MATRIX_CERTIFICATES_V3"
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
    assert [r["position"] for r in manifest["IP_cases"]]==LEGACY_IP_POSITIONS
    assert [r["position"] for r in manifest["short_word_IP_cases"]]==sorted(set(
        r["position"] for r in manifest["short_word_IP_cases"]))
    assert sorted(LEGACY_IP_POSITIONS + [r["position"] for r in
        manifest["short_word_IP_cases"]])==IP_POSITIONS
    assert len(IP_POSITIONS)==len(set(IP_POSITIONS))==1322
    assert [r["position"] for r in manifest["nongeneration_cases"]]==NG_POSITIONS
    assert set(IP_POSITIONS).isdisjoint(NG_POSITIONS)
    assert manifest["accepted_dispositions"]["IP_failure"]==1322
    assert manifest["accepted_dispositions"]["nongeneration"]==273
    assert manifest["accepted_dispositions"]["total"]==1595
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
    pool = [[[0,1,2],[0,1,2,1],[0,1,2,1,2]],
            [[1,2,3],[1,2,1,2,3],[1,2,3,2,3]]]
    assert len(manifest["short_word_IP_cases"])==1310
    for case in manifest["short_word_IP_cases"]:
        tick()
        assert case["acceptance"]=="short_end37_batch_0001"
        marks = check_marks(case["position"],case["representative_J_index"],domain,a,b,e,R,IR)
        assert hashlib.sha256(can(marks)).hexdigest()==case["marks_sha256"]
        end, index = case["end_index"],case["pool_index"]
        assert type(end) is int and end in (0,1)
        assert type(index) is int and 0<=index<3
        assert case["end"]==("left" if end==0 else "right")
        allowed = (0,1,2) if end==0 else (1,2,3)
        word = case["word"]
        assert type(word) is list and word==pool[end][index]
        assert all(type(j) is int and j in allowed for j in word)
        assert type(case["cofactor"]) is int and case["cofactor"]==3
        assert type(case["prime"]) is int and case["prime"]==37
        W = I
        for j in word:
            W = mul(W,marks[j])
        Y = linpow(W,3)
        assert Y!=I and linpow(Y,37)==I
        v = supplied_rank6_row(Y,case)
        j = case["moved"]["generator"]
        assert type(j) is int and j in allowed
        moved_line(v,marks[j],case["moved"])
        omitted = 3 if end==0 else 0
        assert type(case["omitted_mark"]) is int and case["omitted_mark"]==omitted
        assert marks[omitted]!=I
    assert DETERMINANT_TERMS==943200
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
    print(json.dumps(dict(status="PASS",original_job=[24,4],verified_cases=1595,
        IP_failure_positions=IP_POSITIONS,nongeneration_positions=NG_POSITIONS,
        matrix_products=PRODUCTS,rank_field_operations=FIELD,field_inverses=INVERSES,
        determinant_terms=DETERMINANT_TERMS,
        determinant_scalar_products=6*DETERMINANT_TERMS,
        RREF_scope="Only the 12 inherited IP certificates; new cases use explicit minors.",
        pinned_data_read_charge_bytes=READ,seconds=time.monotonic()-START,
        qualification="Finite certificate arithmetic only; original group/model/frame/orbit and IP classification premises remain borrowed. No Lean or whole-manuscript verification."),sort_keys=True))


if __name__ == "__main__":
    main()
