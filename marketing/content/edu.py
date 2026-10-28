"""Educational videos (series "trading, explained"): one concept per video, an animated chart from the first frame,
a follow call at the end. Every number said or shown is computed from the chart itself (see charts.py) and checked
here with assertions, so a chart that doesn't show what the script says fails the build instead of being published."""
from charts import path, closes, ema, rsi, vwap, atr, bollinger, r2

HANDLE = "@calmedgeofficial"
EDU_TAG = "Illustrative chart · education, not financial advice"
EDU_TAGS = ["#tradingeducation", "#technicalanalysis", "#daytrading", "#trading", "#learntotrade"]
SITE = "https://amirkallas2cs-gif.github.io"
FOLLOW = {"type": "follow", "text": "Follow for one trading concept a day.", "say": "Save this, and follow for one trading concept a day."}


def post_edu(title, body, tags, pin=None, site_path="/"):
    hashtags = " ".join(dict.fromkeys(tags + EDU_TAGS))
    tail = f"Save this for later and follow {HANDLE} for one trading concept a day."
    note = "Educational example on an illustrative chart. Not financial advice; trading involves risk of loss."
    return {
        "instagram": f"{body}\n\n{tail}\n\n{note}\n\n{hashtags}",
        "tiktok": f"{body} Follow for one trading concept a day. {' '.join(dict.fromkeys(tags + EDU_TAGS[:3]))}",
        "youtube": {"title": f"{title} #shorts", "description": f"{body}\n\nFree guides and calculators: {SITE}{site_path}\n\n{note}\n\n{hashtags} #shorts"},
        "facebook": f"{body}\n\n{tail}\n\nFree guides and calculators: {SITE}{site_path}",
        "pinterest": {"title": pin or title, "description": f"{body} Trading concepts explained simply, one a day.", "link": SITE + site_path},
    }


def export(c, start=0, lines=(), bands=(), panel=None):
    """Chart data for the player: candles and indicator series from `start` (indicators were warmed up on the full series)."""
    sl = lambda xs: r2(xs[start:])
    out = {"candles": c[start:], "lines": [{**l, "values": sl(l["values"])} for l in lines],
           "bands": [{**b, "upper": sl(b["upper"]), "lower": sl(b["lower"])} for b in bands]}
    if panel:
        out["panel"] = {**panel, "lines": [{**l, "values": sl(l["values"])} for l in panel["lines"]]}
    return out


def pick(build, ok, seeds=range(1, 60)):
    """First seed whose chart satisfies the lesson's conditions (deterministic)."""
    for s in seeds:
        r = build(s)
        if ok(r):
            return r
    raise AssertionError("no chart satisfies the lesson")


def words(n):
    """Small integers in words for the voice."""
    w = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
    t = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
    if n < 20:
        return w[n]
    return t[n // 10 * 10] + ("" if n % 10 == 0 else "-" + w[n % 10])


V = []

# ------------------------------------------------------------------ 1. RSI above 70


def _rsi(seed):
    c = path([(0, 100), (10, 99.5), (18, 103.5), (21, 102.8), (29, 107.5), (32, 106.6), (39, 111), (42, 110.2), (49, 114.5), (52, 113.6), (59, 118)],
             seed=seed, noise=0.45, wick=0.4)
    r = rsi(closes(c))
    first = next(i for i, x in enumerate(r) if x is not None and x > 70)
    above = sum(1 for x in r[first:] if x > 70)
    return dict(c=c, r=r, first=first, above=above, n=len(c) - first)


R = pick(_rsi, lambda d: d["first"] >= 20 and d["above"] / d["n"] >= 0.85 and max(x for x in d["r"] if x) < 86)
S = 14
gain = (R["c"][-1]["c"] / R["c"][R["first"]]["c"] - 1) * 100
assert gain > 8
ch = export(R["c"], S, panel={"id": "rsi", "label": "RSI 14", "min": 0, "max": 100, "levels": [{"y": 70, "label": "70", "color": "coral"}, {"y": 30, "label": "30", "color": "mint"}],
                              "lines": [{"id": "rsi", "color": "violet", "values": R["r"]}]})
f = R["first"] - S
V.append({"id": "v201_edu_rsi_70", "tag": EDU_TAG, "site_path": "/learn/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "RSI above 70 doesn't mean sell.", "reveal": [10, f], "show": ["rsi"],
     "say": "RSI above seventy doesn't mean sell. Watch this."},
    {"type": "chart", "chart": "a", "headline": "RSI above 70 doesn't mean sell.", "reveal": [f, f + 8], "show": ["rsi"],
     "marks": [{"bar": f, "panel": True, "value": round(R["r"][R["first"]], 1), "dir": "up", "text": "Crosses 70", "color": "coral", "at": 0.15}],
     "say": "RSI compares recent up moves with recent down moves, from zero to one hundred. Above seventy is called overbought."},
    {"type": "chart", "chart": "a", "headline": "RSI above 70 doesn't mean sell.", "reveal": [f + 8, len(ch["candles"])], "show": ["rsi"],
     "marks": [{"bar": f, "dir": "down", "text": "Sell here?", "color": "coral", "at": 0.05},
               {"bar": len(ch["candles"]) - 1, "dir": "down", "text": f"+{gain:.0f}% later", "color": "mint", "at": 0.85}],
     "say": f"But in a strong trend it can stay there. Here RSI stayed above seventy on {words(R['above'])} of the next {words(R['n'])} bars, and price rose another {words(round(gain))} percent."},
    {"type": "rows", "title": "RSI above 70 usually means…", "head": ["", "", ""], "rows": [
        {"cells": ["Strong trend", "", "Strength"], "good": True, "hl": True}, {"cells": ["Sideways range", "", "Stretched"]}],
     "say": "So in a trend, read it as strength. In a sideways range, it can mean price is stretched."},
    FOLLOW],
    "post": post_edu("RSI above 70 doesn't mean sell", f"RSI above 70 is called overbought, but in a strong trend it can stay there for a long time. In this example RSI stayed above 70 on {R['above']} of the next {R['n']} bars while price rose another {gain:.0f}%. Read it as strength in a trend, as stretched in a range.",
                     ["#rsi", "#indicators"], "RSI above 70 doesn't mean sell (explained)")})

# ------------------------------------------------------------------ 2. 20 EMA trend filter


def _ema(seed):
    c = path([(0, 100), (9, 103.5), (13, 101.2), (21, 106), (25, 103.6), (33, 108.4), (37, 106), (45, 110.6), (49, 108.4), (53, 110.8), (57, 108.3), (61, 110.6),
              (65, 108.2), (69, 110.5), (73, 108.6), (76, 110)], seed=seed, noise=0.3, wick=0.3)
    e = ema(closes(c), 20)
    touch = [i for i in (25, 37) if c[i]["l"] <= e[i] + 0.1 and c[i]["c"] > e[i] - 0.05]
    trend_ok = all(c[i]["c"] > e[i] for i in range(19, 46))
    cross = [i for i in range(50, 77) if (c[i]["c"] - e[i]) * (c[i - 1]["c"] - e[i - 1]) < 0]
    return dict(c=c, e=e, touch=touch, ok=trend_ok, cross=cross)


E = pick(_ema, lambda d: d["ok"] and len(d["touch"]) == 2 and len(d["cross"]) >= 5)
S = 15
ch = export(E["c"], S, lines=[{"id": "ema", "label": "20 EMA", "color": "gold", "values": E["e"]}])
n = len(ch["candles"]); t1, t2 = (i - S for i in E["touch"]); rng0 = 50 - S
V.append({"id": "v202_edu_20ema", "tag": EDU_TAG, "site_path": "/learn/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "One line that shows you the trend.", "big": True, "reveal": [8, 16], "add": ["ema"], "addAt": 0.2,
     "say": "One line that shows you the trend: the twenty EMA."},
    {"type": "chart", "chart": "a", "headline": "Price above a rising 20 EMA: uptrend.", "reveal": [16, rng0 - 3], "show": ["ema"],
     "marks": [{"bar": t1, "dir": "up", "text": "Pullback", "color": "mint", "at": 0.35}, {"bar": t2, "dir": "up", "text": "Pullback", "color": "mint", "at": 0.7}],
     "say": "It's an average of recent closes that weighs the newest ones more. Above a rising EMA, the trend is up, and pullbacks often find buyers near it."},
    {"type": "chart", "chart": "a", "headline": "Flat EMA: no trend, no edge.", "reveal": [rng0 - 3, n], "show": ["ema"],
     "zones": [{"from": rng0, "to": n - 1, "lo": min(b["l"] for b in ch["candles"][rng0:]), "hi": max(b["h"] for b in ch["candles"][rng0:]), "color": "coral",
                "label": f"Crossed {len(E['cross'])} times", "at": 0.6}],
     "say": f"But it lags. When price goes sideways, the line goes flat, and price crossed it {words(len(E['cross']))} times in {words(77 - 50)} bars."},
    {"type": "rows", "title": "How to read the 20 EMA", "head": ["", "", ""], "rows": [
        {"cells": ["Rising, price above", "", "Uptrend"], "good": True, "hl": True}, {"cells": ["Falling, price below", "", "Downtrend"]},
        {"cells": ["Flat, crossed often", "", "No trend"], "hl": True}],
     "say": "Use it as a trend filter, not as a signal on its own."},
    FOLLOW],
    "post": post_edu("The 20 EMA trend filter in 30 seconds", f"The 20 EMA is an average of recent closes that weighs the newest ones more. Price above a rising EMA: uptrend, and pullbacks often find buyers near it. When it goes flat, it lags: here price crossed it {len(E['cross'])} times in 27 bars. Use it as a filter, not a signal.",
                     ["#ema", "#movingaverage", "#indicators"], "How to use the 20 EMA as a trend filter")})

# ------------------------------------------------------------------ 3. VWAP


def _vwap(seed):
    c = path([(0, 100), (4, 100.6), (12, 98.3), (19, 100.4), (22, 101.2), (26, 100.5), (34, 102.6), (40, 103.2)], seed=seed, noise=0.22, wick=0.22)
    v = vwap(c)
    below = [i for i in range(len(c)) if c[i]["c"] < v[i]]
    reclaim = next((i for i in range(12, 30) if c[i]["c"] > v[i] and c[i - 1]["c"] < v[i - 1]), None)
    test = [i for i in range(reclaim + 4, 32) if c[i]["l"] <= v[i] + 0.05 and c[i]["c"] > v[i]] if reclaim else []
    after = all(c[i]["c"] > v[i] for i in range(reclaim, len(c))) if reclaim else False
    return dict(c=c, v=v, reclaim=reclaim, test=test, after=after, below=below)


W = pick(_vwap, lambda d: d["reclaim"] and d["after"] and len(d["test"]) >= 1 and len(d["below"]) >= 8)
ch = export(W["c"], 0, lines=[{"id": "vwap", "label": "VWAP", "color": "blue", "values": W["v"]}])
n = len(ch["candles"]); rc, ts = W["reclaim"], W["test"][0]
V.append({"id": "v203_edu_vwap", "tag": EDU_TAG, "site_path": "/learn/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "Why every day trader watches this line.", "big": True, "reveal": [7, rc - 2], "add": ["vwap"], "addAt": 0.1,
     "say": "Why every day trader watches this blue line."},
    {"type": "chart", "chart": "a", "headline": "VWAP: the average price paid today.", "reveal": [rc - 2, rc + 1], "show": ["vwap"],
     "marks": [{"bar": rc, "dir": "up", "text": "Reclaimed", "color": "mint", "at": 0.5}],
     "say": "VWAP is the average price everyone paid today, weighted by volume. Above it, today's average buyer is in profit."},
    {"type": "chart", "chart": "a", "headline": "Reclaim, retest, hold.", "reveal": [rc + 1, n], "show": ["vwap"],
     "marks": [{"bar": ts, "dir": "up", "text": "Retest holds", "color": "mint", "at": 0.35}],
     "say": "Here price reclaims VWAP, comes back to test it, and buyers defend it. Every close after that stays above."},
    {"type": "rows", "title": "Reading VWAP", "head": ["", "", ""], "rows": [
        {"cells": ["Above VWAP", "", "Buyers in control"], "good": True, "hl": True}, {"cells": ["Below VWAP", "", "Sellers in control"]},
        {"cells": ["Chopping around it", "", "No control"], "hl": True}],
     "say": "Above it, buyers have the upper hand. Below it, sellers do. Chopping around it, nobody does."},
    FOLLOW],
    "post": post_edu("VWAP explained in 30 seconds", "VWAP is the average price everyone paid today, weighted by volume. Above it, today's average buyer is in profit; below it, the average seller is. A reclaim followed by a retest that holds is one of the cleanest things to watch intraday.",
                     ["#vwap", "#daytradingtips"], "VWAP explained for day traders")})

# ------------------------------------------------------------------ 4. Support/resistance flip


def _flip(seed):
    wp = [(0, 101), (7, 104.4), (11, 102.2), (16, 104.5), (20, 102.6), (25, 104.4), (28, 103.6), (32, 106.3), (36, 107.6), (41, 105.6), (47, 108.4), (52, 109.6)]
    c = path(wp, seed=seed, noise=0.25, wick=0.25, force={7: {"h": 105.0}, 16: {"h": 104.98}, 25: {"h": 105.0}, 41: {"l": 105.06}})
    brk = next(i for i, b in enumerate(c) if b["c"] > 105)
    hits = [i for i in range(brk) if c[i]["h"] >= 104.95]
    ok = max(b["h"] for b in c[:brk]) <= 105.0 and min(b["l"] for b in c[brk + 2:]) >= 105.0 and brk >= 29
    return dict(c=c, brk=brk, hits=hits, ok=ok)


F = pick(_flip, lambda d: d["ok"] and len(d["hits"]) == 3)
ch = export(F["c"]); n = len(ch["candles"]); b = F["brk"]
V.append({"id": "v204_edu_sr_flip", "tag": EDU_TAG, "site_path": "/learn/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "Old resistance becomes new support.", "big": True, "reveal": [8, 18],
     "levels": [{"price": 105, "to": b, "label": "Resistance", "color": "coral", "below": True, "at": 0.25}],
     "say": "Old resistance becomes new support. Here's how it looks."},
    {"type": "chart", "chart": "a", "headline": "Three tries. Sellers win each time.", "reveal": [18, b - 1],
     "levels": [{"price": 105, "to": b, "label": "Resistance", "color": "coral", "below": True}],
     "marks": [{"bar": h, "dir": "down", "color": "coral", "at": 0.1 + 0.25 * k} for k, h in enumerate(F["hits"])],
     "say": "Price hits the same level three times, and sellers push it back down every time."},
    {"type": "chart", "chart": "a", "headline": "Break, then retest from above.", "reveal": [b - 1, n],
     "levels": [{"price": 105, "label": "Now support", "color": "mint", "below": True}],
     "marks": [{"bar": b, "dir": "up", "text": "Break", "color": "mint", "at": 0.1}, {"bar": 41, "dir": "up", "text": "Retest", "color": "mint", "at": 0.55}],
     "say": "Then it breaks and closes above. When price comes back, the same level often holds as support, because buyers who missed the breakout are waiting there."},
    FOLLOW],
    "post": post_edu("Old resistance becomes new support", "A level that rejected price three times breaks, and on the retest it holds from above. Buyers who missed the breakout often wait at the old level. Wait for the close above, then watch the retest.",
                     ["#supportandresistance", "#priceaction"], "Support and resistance flip explained")})

# ------------------------------------------------------------------ 5. Failed breakout


def _fail(seed):
    wp = [(0, 102), (6, 104.5), (10, 103.2), (14, 104.5), (18, 103.6), (21, 104.7), (22, 104.45), (27, 102.8), (30, 103.3), (36, 100.8)]
    c = path(wp, seed=seed, noise=0.22, wick=0.22, force={6: {"h": 105.0}, 14: {"h": 104.99}, 22: {"o": 104.75, "h": 105.92, "l": 104.35, "c": 104.45}})
    ok = all(x["c"] < 105 for x in c) and all(x["h"] <= 105.0 for i, x in enumerate(c) if i != 22) and c[23]["c"] < 105
    return dict(c=c, ok=ok)


T = pick(_fail, lambda d: d["ok"])
ch = export(T["c"]); n = len(ch["candles"])
drop = 104.45 - T["c"][-1]["c"]
V.append({"id": "v205_edu_failed_breakout", "tag": EDU_TAG, "site_path": "/learn/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "This candle traps buyers every day.", "big": True, "reveal": [6, 21],
     "levels": [{"price": 105, "label": "Resistance", "color": "coral", "at": 0.2}],
     "say": "This candle traps buyers every single day."},
    {"type": "chart", "chart": "a", "headline": "A wick above is not a breakout.", "reveal": [21, 23],
     "levels": [{"price": 105, "label": "Resistance", "color": "coral"}],
     "marks": [{"bar": 22, "dir": "up", "text": "Closes back below", "color": "coral", "at": 0.55}],
     "say": "Price pokes above resistance, buyers jump in, and the candle closes back below the level. That's a failed breakout."},
    {"type": "chart", "chart": "a", "headline": "Trapped buyers become sellers.", "reveal": [23, n],
     "levels": [{"price": 105, "label": "Resistance", "color": "coral"}],
     "say": "Everyone who bought the poke is now losing, and their stops add fuel to the drop."},
    {"type": "rows", "title": "Before you buy a breakout", "head": ["", "", ""], "rows": [
        {"cells": ["Wick above the level", "", "Not yet"], "hl": True}, {"cells": ["Close above the level", "", "Breakout"], "good": True, "hl": True},
        {"cells": ["Close back below", "", "Failed"]}],
     "say": "So wait for a candle to close above the level, not just a wick."},
    FOLLOW],
    "post": post_edu("The candle that traps breakout buyers", "Price pokes above resistance, buyers jump in, and the candle closes back below: a failed breakout. Trapped buyers' stops add fuel to the drop. Wait for a close above the level, not just a wick.",
                     ["#breakout", "#priceaction"], "Failed breakout (bull trap) explained")})

# ------------------------------------------------------------------ 6. Double top


def _dt(seed):
    c = path([(0, 103), (12, 109.6), (19, 106.4), (26, 109.5), (31, 105.6), (34, 106.3), (42, 101.8)], seed=seed, noise=0.28, wick=0.25,
             force={12: {"h": 110.0}, 19: {"l": 106.0}, 26: {"h": 109.92}})
    hi1 = max(x["h"] for x in c[:20]); hi2 = max(x["h"] for x in c[20:30])
    neck = min(x["l"] for x in c[13:26])
    brk = next(i for i in range(27, len(c)) if c[i]["c"] < neck)
    target = round(neck - (hi1 - neck), 2)
    return dict(c=c, hi1=hi1, hi2=hi2, neck=neck, brk=brk, target=target, reached=min(x["l"] for x in c[brk:]) <= target)


D = pick(_dt, lambda d: d["hi1"] == 110.0 and d["hi2"] == 109.92 and d["neck"] == 106.0 and d["reached"])
ch = export(D["c"]); n = len(ch["candles"])
V.append({"id": "v206_edu_double_top", "tag": EDU_TAG, "site_path": "/learn/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "The double top, and when it's real.", "big": True, "reveal": [8, 20],
     "say": "The double top, and the moment it actually becomes real."},
    {"type": "chart", "chart": "a", "headline": "Two highs. One neckline.", "reveal": [20, 28],
     "marks": [{"bar": 12, "dir": "down", "text": "Top 1", "color": "coral", "at": 0.05}, {"bar": 26, "dir": "down", "text": "Top 2", "color": "coral", "at": 0.6}],
     "levels": [{"price": 106.0, "label": "Neckline", "color": "gold", "below": True, "at": 0.3}],
     "say": "Two highs at about the same price, with a low between them. That low is the neckline."},
    {"type": "chart", "chart": "a", "headline": "Confirmed only below the neckline.", "reveal": [28, n],
     "levels": [{"price": 106.0, "label": "Neckline", "color": "gold"}, {"price": D["target"], "label": "Classic target", "color": "blue", "below": True, "at": 0.3}],
     "marks": [{"bar": D["brk"], "dir": "down", "text": "Close below", "color": "coral", "at": 0.12}],
     "say": "It only counts when a candle closes below the neckline. The classic target is the pattern's height, measured down from the neckline. In this example price got there, but many double tops don't."},
    FOLLOW],
    "post": post_edu("Double top: when is it real?", "Two highs at about the same price and a low between them, the neckline. The pattern is only confirmed by a close below the neckline; the classic target is the pattern's height measured down from it. Many double tops fail, so wait for the close.",
                     ["#chartpatterns", "#doubletop"], "Double top pattern explained")})

# ------------------------------------------------------------------ 7. ATR stop


def _atr(seed):
    wp = [(0, 100), (8, 101.5), (12, 100.9), (20, 103.2), (25, 104.0), (29, 103.3), (33, 104.6), (44, 107.4)]
    c0 = path(wp, seed=seed, noise=0.3, wick=0.3)
    a = atr(c0)[25]; e = c0[25]["c"]
    c = path(wp, seed=seed, noise=0.3, wick=0.3, force={29: {"l": round(e - 1.0 * a, 2)}})
    a = atr(c)[25]; tight, wide = e - 0.5 * a, e - 1.5 * a
    lows = [x["l"] for x in c[26:]]
    hit_tight = next((i for i in range(26, len(c)) if c[i]["l"] <= tight), None)
    return dict(c=c, a=a, e=e, tight=round(tight, 2), wide=round(wide, 2), hit=hit_tight, ok=min(lows) >= wide + 0.25 * a and hit_tight is not None and c[-1]["c"] > e + 2)


A = pick(_atr, lambda d: d["ok"])
ch = export(A["c"]); n = len(ch["candles"])
V.append({"id": "v207_edu_atr_stop", "tag": EDU_TAG, "site_path": "/tools/position-size-calculator/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "Why your stop keeps getting hit.", "big": True, "reveal": [6, 26],
     "levels": [{"price": A["e"], "from": 25, "label": "Entry", "color": "blue", "at": 0.6}],
     "say": "Why your stop keeps getting hit, right before price goes your way."},
    {"type": "chart", "chart": "a", "headline": "A stop inside normal noise.", "reveal": [26, A["hit"] + 6],
     "levels": [{"price": A["e"], "from": 25, "label": "Entry", "color": "blue"}, {"price": A["tight"], "from": 25, "label": "Tight stop", "color": "coral", "below": True, "labelPos": "right"}],
     "marks": [{"bar": A["hit"], "dir": "down", "text": "Stopped out", "color": "coral", "at": 0.45}],
     "say": "This stop sits half an ATR below entry. ATR is the average true range, how far price normally moves in one bar. An ordinary dip takes it out."},
    {"type": "chart", "chart": "a", "headline": "Stop at 1.5 ATR, smaller size.", "reveal": [A["hit"] + 6, n],
     "levels": [{"price": A["e"], "from": 25, "label": "Entry", "color": "blue"}, {"price": A["wide"], "from": 25, "label": "1.5 ATR stop", "color": "mint", "below": True}],
     "say": "At one and a half ATR, the same dip is just noise. Make the stop wider and the position smaller, so the dollar risk stays the same."},
    FOLLOW],
    "post": post_edu("Why your stop keeps getting hit", "ATR, the average true range, is how far price normally moves in one bar. A stop at half an ATR sits inside normal noise; at 1.5 ATR an ordinary dip doesn't reach it. Wider stop, smaller size, same dollar risk.",
                     ["#atr", "#stoploss", "#riskmanagement"], "ATR stop loss explained", "/tools/position-size-calculator/")})

# ------------------------------------------------------------------ 8. Bollinger squeeze


def _bb(seed):
    wp = [(0, 100), (5, 103), (9, 99), (14, 102.5), (19, 100.2), (23, 101.3), (27, 100.9), (31, 101.2), (35, 100.95), (39, 101.15), (42, 101.05), (47, 104.2), (53, 106.6)]
    c = path(wp, seed=seed, noise=0.18, wick=0.18)
    m, u, l = bollinger(closes(c))
    width = [None if x is None else (u[i] - l[i]) for i, x in enumerate(m)]
    lo_i = min(range(19, 43), key=lambda i: width[i])
    end = len(c) - 1
    return dict(c=c, m=m, u=u, l=l, width=width, lo_i=lo_i, ratio=width[end] / width[lo_i], early=width[19] / width[lo_i])


B = pick(_bb, lambda d: d["ratio"] >= 3 and d["early"] >= 2 and 32 <= d["lo_i"] <= 42)
S = 12
ch = export(B["c"], S, lines=[{"id": "mid", "color": "muted", "values": B["m"], "dash": True}], bands=[{"id": "bb", "label": "Bollinger Bands 20, 2", "color": "blue", "upper": B["u"], "lower": B["l"]}])
n = len(ch["candles"]); li = B["lo_i"] - S; ratio = int(B["ratio"])
V.append({"id": "v208_edu_bollinger_squeeze", "tag": EDU_TAG, "site_path": "/learn/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "When the bands pinch, get ready.", "big": True, "reveal": [8, 18], "add": ["bb", "mid"], "addAt": 0.15,
     "say": "When these bands pinch together, get ready."},
    {"type": "chart", "chart": "a", "headline": "Low volatility: the squeeze.", "reveal": [18, li + 2], "show": ["bb", "mid"],
     "marks": [{"bar": li, "dir": "down", "text": "Squeeze", "color": "gold", "at": 0.7}],
     "say": "Bollinger Bands sit two standard deviations around a twenty bar average. When price goes quiet, they squeeze together."},
    {"type": "chart", "chart": "a", "headline": "Quiet markets don't stay quiet.", "reveal": [li + 2, n], "show": ["bb", "mid"],
     "marks": [{"bar": n - 1, "dir": "down", "text": f"{ratio}x wider", "color": "mint", "at": 0.85}],
     "say": f"Low volatility tends to be followed by expansion. Here the bands ended up more than {words(ratio)} times wider. But the squeeze tells you a move may come, not which way."},
    FOLLOW],
    "post": post_edu("The Bollinger Band squeeze", f"Bollinger Bands sit two standard deviations around a 20-bar average. When price goes quiet they squeeze together, and low volatility tends to be followed by expansion: here the bands ended up more than {ratio}x wider. The squeeze doesn't tell you the direction.",
                     ["#bollingerbands", "#volatility", "#indicators"], "Bollinger Band squeeze explained")})

# ------------------------------------------------------------------ 9. Risk:reward and win rate


def _rr(seed):
    c = path([(0, 98.6), (8, 99.7), (12, 99.2), (18, 100.0), (22, 99.45), (27, 100.8), (30, 100.5), (36, 102.15)], seed=seed, noise=0.18, wick=0.16)
    hit_t = next((i for i in range(19, len(c)) if c[i]["h"] >= 102.0), None)
    ok = c[18]["c"] == 100.0 and min(x["l"] for x in c[19:]) > 99.0 and hit_t is not None
    return dict(c=c, hit=hit_t, ok=ok)


Q = pick(_rr, lambda d: d["ok"])
ch = export(Q["c"]); n = len(ch["candles"])
be = lambda r: 100 / (1 + r)
assert round(be(2), 1) == 33.3 and round(0.4 * 2 - 0.6 * 1, 2) == 0.2
V.append({"id": "v209_edu_risk_reward", "tag": EDU_TAG, "site_path": "/tools/r-multiple-calculator/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "Wrong 60% of the time, still profitable.", "big": True, "reveal": [8, 19],
     "zones": [{"from": 18, "to": n - 1, "lo": 100.0, "hi": 102.0, "color": "mint", "label": "Reward 2R", "at": 0.45},
               {"from": 18, "to": n - 1, "lo": 99.0, "hi": 100.0, "color": "coral", "at": 0.45}],
     "say": "You can be wrong sixty percent of the time and still make money. Here's the math."},
    {"type": "chart", "chart": "a", "headline": "Risk 1 to make 2.", "reveal": [19, n],
     "zones": [{"from": 18, "to": n - 1, "lo": 100.0, "hi": 102.0, "color": "mint", "label": "Reward 2R"}, {"from": 18, "to": n - 1, "lo": 99.0, "hi": 100.0, "color": "coral"}],
     "levels": [{"price": 99.0, "from": 18, "label": "Stop: 1R", "color": "coral", "below": True}],
     "say": "Risk one unit to make two. That's a reward to risk of two to one."},
    {"type": "rows", "title": "Win rate you need to break even", "head": ["Reward : risk", "", "Break-even"], "rows": [
        {"cells": ["1 : 1", "", "50%"]}, {"cells": ["2 : 1", "", "33.3%"], "good": True, "hl": True}, {"cells": ["3 : 1", "", "25%"]}],
     "say": "At two to one you only need to win one trade in three to break even, before costs."},
    {"type": "rows", "title": "Win 40% at 2 : 1", "head": ["", "", ""], "rows": [
        {"cells": ["4 wins × 2R", "", "+8R"]}, {"cells": ["6 losses × 1R", "", "−6R"]}, {"cells": ["Per 10 trades", "", "+2R"], "good": True, "hl": True}],
     "say": "Win four out of ten: plus eight R, minus six R. Plus two R every ten trades."},
    FOLLOW],
    "post": post_edu("Wrong 60% of the time and still profitable", "With a 2:1 reward to risk you only need to win 1 trade in 3 to break even (33.3%, before costs). Win 4 out of 10: +8R − 6R = +2R every ten trades. Your win rate only means something next to your reward to risk.",
                     ["#riskreward", "#riskmanagement", "#tradingpsychology"], "Win rate vs risk reward explained", "/tools/r-multiple-calculator/")})

# ------------------------------------------------------------------ 10. Position size in futures


risk_usd = 50000 * 0.01; stop_pts = 4
mes = risk_usd / (stop_pts * 5); es = int(risk_usd // (stop_pts * 50))
assert mes == 25 and es == 2 and stop_pts * 50 * es <= risk_usd


def _ps(seed):
    c = path([(0, 5812), (8, 5818), (12, 5815), (20, 5821), (24, 5820), (34, 5829)], seed=seed, noise=0.9, wick=0.8)
    ok = c[20]["c"] == 5821 and min(x["l"] for x in c[21:]) > 5817.5
    return dict(c=c, ok=ok)


P = pick(_ps, lambda d: d["ok"])
ch = export(P["c"]); n = len(ch["candles"])
V.append({"id": "v210_edu_position_size", "tag": EDU_TAG, "site_path": "/tools/position-size-calculator/", "charts": {"a": ch}, "scenes": [
    {"type": "chart", "chart": "a", "headline": "How many contracts? Three numbers.", "big": True, "reveal": [8, 21],
     "levels": [{"price": 5821, "from": 20, "label": "Entry", "color": "blue", "at": 0.5}, {"price": 5817, "from": 20, "label": "Stop: 4 points", "color": "coral", "below": True, "at": 0.65}],
     "say": "How many contracts should you trade? You only need three numbers."},
    {"type": "rows", "title": "1. How much you can lose", "head": ["", "", ""], "rows": [
        {"cells": ["Account", "", "$50,000"]}, {"cells": ["Risk per trade", "", "1%"]}, {"cells": ["Max loss", "", "$500"], "good": True, "hl": True}],
     "say": "One: how much you can lose. One percent of fifty thousand dollars is five hundred."},
    {"type": "rows", "title": "2. What one contract risks", "head": ["Contract", "$ per point", "4-point stop"], "rows": [
        {"cells": ["Micro (MES)", "$5", "$20"]}, {"cells": ["E-mini (ES)", "$50", "$200"]}],
     "say": "Two: what one contract loses at your stop. Four points is twenty dollars on the micro, two hundred on the E-mini."},
    {"type": "rows", "title": "3. Divide", "head": ["", "", "Contracts"], "rows": [
        {"cells": ["$500 ÷ $20", "", "25 micros"], "good": True, "hl": True}, {"cells": ["$500 ÷ $200 = 2.5", "", "2 E-minis"]}],
     "say": "Three: divide. Twenty-five micros, or two E-minis. Always round down."},
    FOLLOW],
    "post": post_edu("How many futures contracts should you trade?", "1) Max loss: 1% of $50,000 = $500. 2) Risk per contract: a 4-point stop is $20 on the Micro E-mini S&P ($5/point) and $200 on the E-mini ($50/point). 3) Divide and round down: 25 micros or 2 E-minis.",
                     ["#positionsizing", "#futurestrading", "#riskmanagement"], "Futures position size in 3 numbers", "/tools/position-size-calculator/")})
