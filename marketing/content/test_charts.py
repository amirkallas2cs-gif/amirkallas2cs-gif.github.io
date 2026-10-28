"""Indicator checks against published reference values. python3 marketing/content/test_charts.py"""
import math, statistics, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from charts import ema, sma, rsi, bollinger, vwap, atr, macd, path

fails = []
def eq(a, b, tol, msg):
    if a is None or abs(a - b) > tol: fails.append(f"{msg}: {a} != {b}")

# Wilder RSI, StockCharts worked example (cs-rsi): first RSI(14) 70.53, then 66.32, 66.55, 69.41, 66.36
X = [44.3389, 44.0902, 44.1497, 43.6124, 44.3278, 44.8264, 45.0955, 45.4245, 45.8433, 46.0826, 45.8931, 46.0328, 45.6140, 46.2820,
     46.2820, 46.0028, 46.0328, 46.4116, 46.2222]
r = rsi(X, 14)
for i, ref in zip(range(14, 19), [70.53, 66.32, 66.55, 69.41, 66.36]):
    eq(r[i], ref, 0.01, f"RSI[{i}]")
assert all(v is None for v in r[:14])

# EMA: seed = SMA, then k = 2/(n+1)
xs = [22.27, 22.19, 22.08, 22.17, 22.18, 22.13, 22.23, 22.43, 22.24, 22.29, 22.15, 22.39, 22.38, 22.61, 23.36]
e = ema(xs, 10)
seed = sum(xs[:10]) / 10
eq(e[9], seed, 1e-9, "EMA seed")
eq(e[10], 22.15 * 2 / 11 + seed * 9 / 11, 1e-9, "EMA step")
eq(e[9], 22.221, 0.001, "EMA(10) StockCharts seed 22.22")
eq(e[10], 22.208, 0.001, "EMA(10) StockCharts 22.21")

# SMA / Bollinger (population standard deviation)
s = sma(xs, 5); eq(s[4], sum(xs[:5]) / 5, 1e-9, "SMA")
m, u, l = bollinger(xs, 10, 2)
w = xs[5:15]; eq(u[14], statistics.mean(w) + 2 * statistics.pstdev(w), 1e-9, "Bollinger upper")
eq(l[14], statistics.mean(w) - 2 * statistics.pstdev(w), 1e-9, "Bollinger lower")

# VWAP and ATR on a tiny hand example
c = [{"o": 10, "h": 11, "l": 9, "c": 10, "v": 100}, {"o": 10, "h": 13, "l": 10, "c": 12, "v": 300}, {"o": 12, "h": 12.5, "l": 8, "c": 9, "v": 100}]
v = vwap(c)
eq(v[1], (10 * 100 + (35 / 3) * 300) / 400, 1e-9, "VWAP")
a = atr(c, 2)  # TRs: 2, 3, max(4.5, 0.5, 4) = 4.5 -> first ATR (2+3)/2 = 2.5, then (2.5*1 + 4.5)/2 = 3.5
eq(a[1], 2.5, 1e-9, "ATR first"); eq(a[2], 3.5, 1e-9, "ATR Wilder")

# MACD = EMA12 - EMA26, signal = EMA9 of MACD
ys = [100 + math.sin(i / 5) * 5 + i * 0.1 for i in range(80)]
line, sig, hist = macd(ys)
from charts import ema as E
eq(line[40], E(ys, 12)[40] - E(ys, 26)[40], 1e-9, "MACD line")
assert line[24] is None and line[25] is not None and sig[33] is not None and sig[32] is None, "MACD warm-up"

# paths: deterministic, turning points exact, candles consistent
p1, p2 = path([(0, 100), (20, 110), (40, 104)], seed=3), path([(0, 100), (20, 110), (40, 104)], seed=3)
assert p1 == p2 and len(p1) == 41 and p1[20]["c"] == 110 and p1[40]["c"] == 104
assert all(b["l"] <= min(b["o"], b["c"]) and b["h"] >= max(b["o"], b["c"]) for b in p1)

if fails:
    print("FAIL\n" + "\n".join(fails)); sys.exit(1)
print("charts OK")
