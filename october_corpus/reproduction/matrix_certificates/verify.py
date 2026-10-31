#!/usr/bin/env python3
"""Replay 2308 accepted finite GF(11) matrix certificates using local JSON."""
import base64
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
NEW_ROW_IMAGES = 0
GRAPH_NORMALIZATIONS = 0
GRAPH_EDGES = 0
READ = 0
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
MANIFEST = {"bytes":717342,"file":"cases.json","sha256":"cd8e9c0d6d371de031d370a81c8cc26270cbbcda0a7a0785dc7e5c9504f50b10"}
IP_POSITIONS = [44,45,46,47,48,51,52,53,54,55,56,57,58,60,61,62,70,71,72,73,74,78,80,83,84,91,92,94,95,96,98,99,100,101,103,105,106,107,109,110,112,115,119,120,121,123,126,127,128,130,132,135,138,139,140,141,142,145,149,150,154,155,156,157,158,159,161,163,166,169,170,171,172,174,175,176,179,180,181,183,185,186,187,188,191,193,194,195,196,199,201,202,203,204,205,206,209,210,211,213,215,217,222,223,225,227,230,231,235,239,241,242,246,249,250,251,252,315,321,324,325,326,327,329,330,331,332,334,335,336,338,340,342,343,346,348,349,351,352,353,354,355,356,357,358,359,360,363,365,366,367,369,371,374,375,376,379,380,381,382,383,384,385,386,387,388,391,393,398,399,401,402,403,404,409,410,411,412,414,415,418,420,421,422,423,425,429,430,431,433,434,437,438,439,440,442,443,444,445,451,454,455,458,462,463,467,471,475,476,477,478,480,481,483,484,489,490,491,492,493,496,497,498,499,500,501,503,505,506,507,508,509,510,511,512,513,514,515,518,521,523,525,526,527,528,529,530,531,532,533,536,537,538,540,541,542,543,544,547,548,552,553,555,559,560,561,563,564,565,567,568,571,572,573,576,578,580,581,583,584,585,586,588,590,591,593,595,596,598,604,605,606,607,608,611,612,613,614,615,616,617,619,620,621,622,623,624,625,626,630,631,632,633,635,636,637,640,641,643,644,645,646,647,648,649,651,652,653,656,657,661,663,664,665,666,668,670,671,673,677,678,679,682,683,685,686,687,689,691,696,697,698,702,704,705,707,709,710,711,718,719,720,721,723,724,726,728,729,730,732,734,735,737,741,743,744,745,751,752,753,757,759,760,761,762,764,767,768,769,770,771,772,773,774,775,776,777,779,780,783,784,786,787,788,789,790,791,794,795,797,798,799,800,803,805,806,807,808,809,810,812,813,814,817,823,824,826,827,829,834,835,838,842,845,846,847,848,849,850,852,854,855,856,859,860,862,863,864,865,866,870,872,873,876,877,880,881,883,884,886,889,891,894,895,896,898,899,901,902,903,907,910,911,912,913,917,918,920,924,925,928,930,931,933,934,935,936,937,940,941,943,944,946,948,949,950,951,952,956,957,958,960,961,962,963,965,966,967,970,971,973,974,975,979,980,981,982,983,984,985,986,990,994,995,996,997,998,1000,1001,1003,1004,1005,1006,1007,1008,1010,1011,1013,1014,1015,1016,1017,1021,1022,1024,1025,1026,1027,1029,1030,1032,1033,1034,1035,1036,1037,1038,1040,1041,1042,1045,1047,1048,1050,1052,1054,1056,1057,1059,1062,1063,1064,1068,1069,1070,1074,1075,1077,1080,1082,1083,1084,1085,1086,1087,1088,1090,1091,1092,1094,1096,1157,1159,1162,1163,1164,1166,1167,1168,1169,1173,1174,1175,1176,1178,1179,1180,1181,1182,1183,1184,1185,1187,1189,1194,1196,1197,1198,1199,1201,1203,1205,1209,1210,1212,1213,1214,1216,1217,1218,1219,1220,1221,1223,1224,1227,1228,1229,1230,1231,1232,1234,1235,1236,1237,1239,1240,1245,1247,1249,1252,1254,1256,1257,1258,1260,1262,1263,1265,1268,1269,1272,1276,1278,1280,1282,1284,1285,1286,1287,1290,1293,1295,1296,1299,1300,1301,1303,1304,1306,1309,1315,1318,1320,1322,1323,1326,1328,1331,1332,1333,1334,1335,1337,1338,1339,1340,1344,1347,1348,1349,1352,1355,1356,1357,1358,1360,1361,1363,1369,1370,1371,1375,1377,1378,1379,1385,1387,1389,1390,1392,1396,1398,1401,1402,1403,1406,1410,1412,1413,1415,1416,1417,1421,1422,1423,1424,1425,1426,1427,1428,1430,1432,1433,1434,1435,1440,1442,1443,1445,1446,1449,1450,1455,1457,1458,1459,1460,1463,1464,1466,1467,1468,1469,1470,1473,1474,1476,1477,1478,1479,1484,1485,1488,1492,1493,1494,1496,1499,1502,1503,1504,1505,1506,1508,1510,1511,1514,1516,1517,1519,1522,1524,1525,1526,1527,1528,1531,1533,1534,1537,1538,1539,1545,1550,1552,1553,1554,1555,1556,1559,1561,1562,1563,1564,1565,1570,1572,1573,1574,1575,1576,1577,1578,1581,1582,1583,1584,1586,1587,1588,1589,1590,1591,1592,1593,1594,1595,1597,1598,1599,1600,1601,1603,1604,1606,1607,1608,1609,1610,1611,1613,1614,1616,1617,1618,1619,1620,1621,1622,1623,1624,1625,1626,1627,1628,1632,1634,1635,1636,1638,1640,1642,1644,1646,1647,1651,1652,1653,1655,1656,1657,1661,1662,1663,1665,1666,1668,1669,1670,1674,1675,1676,1678,1679,1681,1682,1685,1686,1687,1688,1689,1690,1693,1700,1702,1703,1705,1708,1709,1710,1711,1712,1713,1714,1718,1721,1722,1725,1728,1729,1730,1734,1736,1742,1743,1745,1747,1748,1750,1751,1752,1753,1759,1760,1761,1762,1763,1767,1770,1772,1774,1775,1776,1777,1778,1779,1782,1784,1787,1791,1792,1794,1795,1796,1797,1798,1799,1801,1802,1806,1807,1808,1810,1811,1812,1813,1814,1815,1816,1818,1822,1823,1824,1826,1828,1829,1830,1831,1832,1833,1834,1837,1838,1839,1840,1843,1844,1847,1848,1850,1852,1853,1854,1855,1856,1857,1858,1862,1864,1867,1868,1869,1870,1871,1872,1874,1878,1879,1880,1882,1883,1884,1887,1888,1890,1891,1893,1895,1896,1897,1898,1900,1902,1903,1904,1905,1906,1907,1909,1915,1916,1917,1920,1921,1922,1923,1924,1927,1929,1930,1932,1933,1934,1935,1936,1937,1939,1940,1941,1942,1943,1944,1945,1946,1947,1950,1951,1952,1953,1954,1956,1957,1958,1960,1963,1964,1966,1967,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1982,1983,1984,1985,1987,1990,1991,1994,1995,1997,2001,2005,2006,2007,2009,2011,2013,2017,2019,2020,2021,2023,2024,2025,2029,2030,2032,2033,2035,2036,2038,2039,2040,2046,2047,2048,2050,2055,2056,2057,2058,2059,2060,2061,2062,2063,2064,2065,2066,2067,2069,2070,2072,2073,2074,2077,2078,2080,2086,2087,2088,2092,2095,2096,2097,2100,2101,2102,2103,2105,2107,2108,2109,2110,2111,2112,2115,2119,2121,2122,2123,2125,2126,2127,2130,2132,2133,2135,2136,2141,2143,2144,2145,2147,2148,2150,2152,2153,2154,2158,2160,2161,2163,2164,2166,2168,2170,2171,2172,2173,2177,2179,2180,2181,2182,2184,2185,2188,2189,2192,2193,2194,2195,2196,2197,2198,2199,2200,2202,2207,2209,2210,2211,2215,2216,2218,2220,2221,2222,2223,2224,2225,2229,2233,2234,2235,2237,2238,2240,2243,2244,2245,2248,2249,2250,2251,2254,2255,2256,2257,2259,2260,2261,2267,2268,2269,2270,2272,2276,2278,2279,2280,2281,2284,2286,2287,2289,2290,2291,2293,2294,2296,2297,2298,2299,2300,2301,2302,2303,2304,2306,2308,2310,2311,2312,2313,2314,2317,2319,2323,2324,2325,2326,2327,2329,2333,2334,2335,2336,2337,2339,2340,2341,2342,2344,2345,2346,2349,2350,2351,2353,2354,2355,2356,2357,2360,2363,2368,2369,2370,2371,2373,2374,2375,2376,2377,2379,2380,2381,2382,2384,2385,2386,2388,2391,2392,2393,2394,2396,2397,2398,2399,2400,2401,2402,2404,2405,2406,2407,2408,2410,2412,2414,2415,2418,2419,2424,2426,2430,2432,2433,2434,2436,2440,2441,2443,2444,2445,2446,2449,2453,2454,2455,2457,2458,2459,2460,2463,2464,2465,2467,2468,2470,2472,2474,2475,2476,2477,2478,2479,2480,2481,2483,2484,2485,2486,2487,2490,2491,2493,2494,2495,2496,2499,2500,2501,2502,2503,2504,2505,2506,2510,2511,2512,2513,2514,2517,2518,2519,2521,2522,2523,2525,2527,2529,2530,2534,2535,2536,2538,2539,2541,2543,2544,2545,2546,2547,2554,2555,2556,2557,2559,2561,2564,2565,2566,2567,2568,2569,2571,2573,2575,2578,2580,2586,2587,2589,2590,2591,2592,2594,2595,2596,2597,2598,2605,2606,2608,2610,2611,2612,2613,2619,2620,2621,2623,2626,2627,2628,2629,2631,2632,2633,2634,2637,2638,2639,2640,2643,2645,2647,2648,2649,2650,2651,2652,2653,2654,2655,2656,2658,2659,2661,2663,2665,2668,2669,2670,2671,2672,2673,2674,2675,2678,2679,2681,2682,2683,2684,2685,2687,2688,2690,2691,2692,2693,2694,2697,2699,2700,2702,2703,2704,2705,2706,2709,2711,2712,2714,2716,2717,2718,2719,2720,2721,2725,2726,2727,2729,2731,2734,2735,2736,2738,2739,2740,2744,2745,2746,2747,2748,2749,2752,2755,2756,2757,2758,2761,2763,2764,2765,2767,2769,2770,2771,2772,2773,2776,2777,2779,2782,2783,2784,2790,2791,2793,2794,2796,2797,2799,2802,2804,2805,2806,2807,2808,2809,2811,2812,2814,2816,2817,2857,2858,2859,2860,2861,2862,2864,2866,2867,2869,2870,2871,2872,2873,2876,2877,2878,2880,2882,2883,2884,2886,2887,2888,2890,2893,2894,2895,2896,2898,2900,2902,2903,2905,2906,2908,2909,2910,2911,2912,2914,2915,2919,2920,2922,2924,2925,2926,2927,2928,2933,2934,2936,2939,2940,2941,2942,2943,2944,2945,2946,2948,2949,2950,2953,2954,2955,2958,2960,2963,2964,2968,2969,2971,2972,2973,2977,2978,2979,2980,2981,2983,2984,2985,2986,2987,2989,2990,2992,2995,2996,2997,2998,3000,3001,3004,3008,3009,3010,3011,3013,3015,3019,3020,3023,3024,3026,3027,3029,3032,3035,3037,3040,3041,3043,3044,3046,3047,3048,3052,3054,3057,3059,3060,3061,3062,3065,3066,3070,3071,3074,3075,3081,3082,3085,3087,3089,3091,3093,3094,3095,3098,3099,3100,3105,3107,3109,3111,3113,3114,3115,3116,3117,3118,3120,3122,3123,3126,3127,3129,3130,3132,3134,3137,3138,3141,3142,3143,3146,3150,3153,3154,3156,3158,3160,3161,3163,3165,3166,3167,3168,3169,3172,3173,3174,3175,3176,3177,3178,3179,3181,3182,3183,3185,3186,3187,3188,3191,3192,3194,3195,3196,3198,3201,3203,3205,3210,3211,3212,3213,3214,3215,3216,3219,3220,3221,3222,3224,3225,3228,3229,3230,3233,3234,3236,3237,3239,3240,3241,3242,3244,3245,3247,3248,3249,3252,3256,3259,3260,3262,3266,3267,3269,3271,3273,3274,3280,3281,3282,3284,3285,3292,3293,3296,3297,3300,3301,3303,3304,3305,3306,3307,3309,3310,3312,3313,3314,3315,3316,3317,3320,3321,3323,3324,3325,3326,3327,3328,3331,3332,3334,3335,3336,3337,3338,3341,3347,3348,3349,3350,3353,3354,3355,3356,3358,3362,3365,3366,3368,3369,3370,3371,3372,3373,3374,3375,3376,3377,3378,3381,3382,3384,3385,3391,3392,3393,3394,3395,3467,3468,3469,3470,3471,3473,3474,3475,3476,3477,3478,3479,3480,3481,3482,3483,3487,3488,3489,3491,3492,3494,3496,3501,3502,3503,3504,3505,3507,3508,3509,3510,3511,3514,3516,3517,3519,3520,3521,3522,3524,3526,3527,3529,3530,3531,3533,3534,3535,3536,3537,3540,3542,3545,3547,3549,3552,3554,3555,3557,3558,3559,3561,3563,3564,3565,3568,3569,3570,3572,3573,3574,3575,3576,3577,3580,3581,3582,3584,3585,3586,3587,3589,3593,3594,3596,3597,3600,3601,3602,3603,3604,3605,3607,3608,3609,3612,3613,3615,3617,3619,3621,3622,3623,3627,3628,3630,3632,3633,3637,3647,3648,3649,3650,3651,3652,3654,3655,3656,3661,3662,3664,3665,3667]
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


def binary(a,k):
 assert type(k)is int and 0<=k<=1320
 value=identity(len(a));base=a
 while k:
  if k&1:value=mul(value,base)
  k//=2
  if k:base=mul(base,base)
 return value

def normalized(row):
 first=next(x for x in row if x)
 inverse=pow(first,9,11)
 return bytes((x*inverse)%11 for x in row)

def direct_action(point,g):
 row=[]
 for j in range(7):
  value=0
  for i in range(7):value=(value+point[i]*g[i][j])%11
  row.append(value)
 return normalized(row)

def rank_seven(rows):
    """Rank one actual 21 by 7 sign system, using the shared RREF cap."""
    global FIELD, INVERSES
    assert type(rows) is tuple and len(rows)==21
    assert all(type(r) is tuple and len(r)==7 and
               all(type(x) is int and 0<=x<11 for x in r) for r in rows)
    matrix = [list(r) for r in rows]
    rank = 0
    for column in range(7):
        tick()
        pivot = next((i for i in range(rank,21) if matrix[i][column]),None)
        if pivot is None:
            continue
        matrix[rank],matrix[pivot] = matrix[pivot],matrix[rank]
        inverse = pow(matrix[rank][column],-1,11)
        INVERSES += 1
        matrix[rank] = [inverse*x%11 for x in matrix[rank]]
        FIELD += 7
        assert FIELD<=200000
        for i in range(21):
            if i!=rank and matrix[i][column]:
                scalar = matrix[i][column]
                matrix[i] = [(x-scalar*y)%11 for x,y in zip(matrix[i],matrix[rank])]
                FIELD += 14
                assert FIELD<=200000
        rank += 1
    return rank


def prefix_line_systems(a,b,e,lines,dimensions):
    assert type(dimensions) is list and len(dimensions)==8
    assert [r["signs"] for r in dimensions]==[list(s) for s in itertools.product((1,10),repeat=3)]
    obtained = {}
    for certificate in dimensions:
        signs = certificate["signs"]
        rows = tuple(tuple((g[j][i]-sign*int(i==j))%11 for j in range(7))
                     for g,sign in zip((a,b,e),signs) for i in range(7))
        dimension = 7-rank_seven(rows)
        assert type(certificate["dimension"]) is int and dimension==certificate["dimension"]
        assert dimension in (0,1)
        matches = [line for line in lines if [line["prefix_signs"][k] for k in ("a","b","e")]==signs]
        assert len(matches)==dimension
        obtained[tuple(signs)] = dimension
    for sa,sb in itertools.product((1,10),repeat=2):
        assert sum(obtained[(sa,sb,se)] for se in (1,10))<=1
    return tuple(row(line["vector"]) for line in lines)


def require_left_line_absence(marks,lines):
    global NEW_ROW_IMAGES
    for v in lines:
        tick()
        z = image(v,marks[2])
        NEW_ROW_IMAGES += 1
        anchor = next(i for i,x in enumerate(v) if x)
        assert any((v[anchor]*z[j]-v[j]*z[anchor])%11 for j in range(7))
        assert NEW_ROW_IMAGES<=11000


def exact_order_from_certificate(value,order):
    assert type(order) is int and 2<=order<=1320 and 1320%order==0
    assert binary(value,order)==identity(7)
    for prime in (2,3,5,11):
        if order%prime==0:
            assert binary(value,order//prime)!=identity(7)


def require_empty_prefix_centralizer(marks,S,witnesses=None):
    assert witnesses is None or (type(witnesses) is list and len(witnesses)==9)
    for k,t in enumerate(S):
        left,right = mul(t,marks[2]),mul(marks[2],t)
        assert left!=right
        if witnesses is not None:
            i,j,delta = witnesses[3*k:3*k+3]
            assert type(i) is int and type(j) is int and 0<=i<7 and 0<=j<7
            assert type(delta) is int and 1<=delta<11
            assert (left[i][j]-right[i][j])%11==delta


def verify_left19(case,marks):
    word = case["word19"]
    assert type(word) is list and 1<=len(word)<=64
    assert all(type(g) is int and g in (0,1,2) for g in word)
    assert type(case["cofactor19"]) is int and case["cofactor19"]==7
    assert type(case["prime19"]) is int and case["prime19"]==19
    value = identity(7)
    for g in word:
        value = mul(value,marks[g])
    prime = linpow(value,7)
    assert prime!=identity(7) and linpow(prime,19)==identity(7)


def verify_reachable_graph(graph,case,marks):
    global NEW_ROW_IMAGES, GRAPH_NORMALIZATIONS, GRAPH_EDGES
    assert graph["original_position"]==case["position"]==1556
    assert graph["representative_J_index"]==case["representative_J_index"]
    assert graph["marks_sha256"]==case["marks_sha256"]
    assert graph["left19_word"]==case["word19"] and graph["left19_cofactor"]==7
    assert graph["left19_prime"]==19
    assert graph["middle_rotation_order"]==case["middle_rotation_order"]==10
    assert graph["middle_dihedral_order"]==case["middle_dihedral_order"]==20
    assert case["threshold"]==graph["threshold"]==8779
    assert graph["distinct_reachable_lines"]==8779 and graph["orbit_closed"] is False
    exact_order_from_certificate(mul(marks[1],marks[2]),10)
    v = row(graph["right_fixed_row"])
    for g in (marks[1],marks[2]):
        z = image(v,g)
        NEW_ROW_IMAGES += 1
        assert z in (v,tuple(-x%11 for x in v))
    text = graph["records_base64"]
    assert type(text) is str and text.isascii() and len(text)<=131072
    wire = base64.b64decode(text,validate=True)
    assert len(wire)==87790 and hashlib.sha256(wire).hexdigest()==graph["records_sha256"]
    points = [wire[10*i:10*i+7] for i in range(8779)]
    assert len(set(points))==8779
    assert points[0]==normalized(v)==bytes(graph["seed_line"])
    GRAPH_NORMALIZATIONS += 1
    assert wire[7:10]==bytes([255,255,255])
    for i,point in enumerate(points):
        tick()
        assert len(point)==7 and any(point) and all(x<11 for x in point)
        assert next(x for x in point if x)==1
        if i:
            parent = wire[10*i+7]+256*wire[10*i+8]
            label = wire[10*i+9]
            assert 0<=parent<i and 0<=label<3
            assert direct_action(points[parent],marks[label])==point
            GRAPH_NORMALIZATIONS += 1
            GRAPH_EDGES += 1
            NEW_ROW_IMAGES += 1
            assert NEW_ROW_IMAGES<=11000
    assert GRAPH_NORMALIZATIONS==8779 and GRAPH_EDGES==8778


def main():
    manifest = document(MANIFEST)
    assert manifest["schema"]=="HUMAN_COMPRESSION_Q11_MATRIX_CERTIFICATES_V4"
    assert manifest["field"]==11 and manifest["dimension"]==7
    assert manifest["original_job"]==[24,4]
    assert set(manifest["files"])=={"domain","prefix","ambient_frame","spread_proof","line_orbit"}
    domain = document(manifest["files"]["domain"])
    prefix = document(manifest["files"]["prefix"])
    frame = document(manifest["files"]["ambient_frame"])
    proof = document(manifest["files"]["spread_proof"])
    graph = document(manifest["files"]["line_orbit"])
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
        manifest["short_word_IP_cases"]] + [r[0] for r in manifest["spectrum_IP_cases"]] +
        [manifest["special_LEFT19_cases"][k]["position"] for k in ("order4","line_orbit")])==IP_POSITIONS
    assert len(IP_POSITIONS)==len(set(IP_POSITIONS))==2035
    assert [r["position"] for r in manifest["nongeneration_cases"]]==NG_POSITIONS
    assert set(IP_POSITIONS).isdisjoint(NG_POSITIONS)
    assert manifest["accepted_dispositions"]["IP_failure"]==2035
    assert manifest["accepted_dispositions"]["nongeneration"]==273
    assert manifest["accepted_dispositions"]["total"]==2308
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
    # The complete U=S identity and classification are explicit imported premises.
    imports = manifest["prefix_spectrum_imports"]
    assert imports["full_centralizer_U_equals_S_is_borrowed"] is True
    assert imports["finite_split_Levi_and_maximal_cover_are_borrowed"] is True
    assert imports["centralizer_acceptance_sha256"]=="9d2f9c739a8a5f4282d80c86204358834b2e34a9d085a37927d77b7d28368563"
    assert imports["parent_prefix_order"]==6 and imports["S_order"]==4
    AB = mul(a,b)
    z = linpow(AB,3)
    assert linpow(AB,6)==I and z!=I and linpow(AB,2)!=I
    S = (z,e,mul(z,e))
    assert len(set(S))==3 and all(t!=I and mul(t,t)==I for t in S)
    assert all(mul(t,g)==mul(g,t) for t in S for g in (a,b,e))
    left_lines = prefix_line_systems(a,b,e,lines,manifest["prefix_sign_kernel_dimensions"])
    spectral = manifest["spectrum_IP_cases"]
    assert type(spectral) is list and len(spectral)==711
    assert [r[0] for r in spectral]==sorted(set(r[0] for r in spectral))
    for certificate in spectral:
        tick()
        assert type(certificate) is list and len(certificate)==12
        assert all(type(x) is int for x in certificate)
        p,J,order = certificate[:3]
        marks = check_marks(p,J,domain,a,b,e,R,IR)
        require_empty_prefix_centralizer(marks,S,certificate[3:])
        require_left_line_absence(marks,left_lines)
        exact_order_from_certificate(mul(marks[1],marks[2]),order)
        assert (((order%5==0 or order%11==0) and order not in (5,10,11,15)) or order%24==0)
    special = manifest["special_LEFT19_cases"]
    assert type(special) is dict and set(special)=={"order4","line_orbit"}
    for kind,position in (("order4",3630),("line_orbit",1556)):
        case = special[kind]
        assert case["position"]==position
        marks = check_marks(position,case["representative_J_index"],domain,a,b,e,R,IR)
        assert hashlib.sha256(can(marks)).hexdigest()==case["marks_sha256"]
        require_empty_prefix_centralizer(marks,S)
        require_left_line_absence(marks,left_lines)
        verify_left19(case,marks)
        if kind=="order4":
            assert case["order4_word"]==[1,2,1,2] and case["middle_rotation_order"]==8
            value = I
            for g in case["order4_word"]:
                value = mul(value,marks[g])
            assert linpow(value,4)==I and mul(value,value)!=I
        else:
            verify_reachable_graph(graph,case,marks)
    tick()
    print(json.dumps(dict(status="PASS",original_job=[24,4],verified_cases=2308,
        IP_failure_positions=IP_POSITIONS,nongeneration_positions=NG_POSITIONS,
        matrix_products=PRODUCTS,rank_field_operations=FIELD,field_inverses=INVERSES+GRAPH_NORMALIZATIONS,
        determinant_terms=DETERMINANT_TERMS,
        determinant_scalar_products=6*DETERMINANT_TERMS,
        RREF_scope="Twelve inherited IP certificates and eight common prefix sign systems.",
        new_row_images=NEW_ROW_IMAGES,graph_normalizations=GRAPH_NORMALIZATIONS,
        reachable_graph_parent_edges=GRAPH_EDGES,
        pinned_data_read_charge_bytes=READ,seconds=time.monotonic()-START,
        qualification="Finite certificate arithmetic only; original group/model/frame/orbit and IP classification premises remain borrowed. No Lean or whole-manuscript verification."),sort_keys=True))


if __name__ == "__main__":
    main()
