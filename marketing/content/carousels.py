"""Educational carousels (image posts, 1080x1350): one concept explained in 6 slides.
Charts and every number come from the matching video lesson in edu.py (same computed chart, same checks),
so a carousel can never say something its lesson's chart doesn't show.
Ids: cNNN_car_<topic>. Rendered by marketing/video/still.py."""
import edu
from edu import EDU_TAG, EDU_TAGS, HANDLE, SITE

L = {v["id"]: v for v in edu.V}
C = []


def state(vid, scene, bars=None, **extra):
    """Chart state for a slide, taken from one scene of the lesson (what the video shows at the end of that scene)."""
    s = [x for x in L[vid]["scenes"] if x["type"] == "chart"][scene]
    clean = lambda xs: [{k: v for k, v in x.items() if k != "at"} for x in xs]
    st = {"bars": bars or s.get("reveal", [0, len(L[vid]["charts"]["a"]["candles"])])[1], "show": s.get("show", []) + s.get("add", []),
          "levels": clean(s.get("levels", [])), "marks": clean(s.get("marks", [])), "zones": clean(s.get("zones", []))}
    st.update(extra)
    return st


def post_car(title, body, tags, pin=None, site_path="/learn/"):
    hashtags = " ".join(dict.fromkeys(tags + EDU_TAGS))
    tail = f"Save this for later and follow {HANDLE} for one trading concept a day."
    note = "Educational example on an illustrative chart. Not financial advice; trading involves risk of loss."
    return {
        "instagram": f"{body}\n\n{tail}\n\n{note}\n\n{hashtags}",
        "facebook": f"{body}\n\n{tail}\n\nFree guides and calculators: {SITE}{site_path}",
        "tiktok": f"{body} Follow for one trading concept a day. {' '.join(dict.fromkeys(tags + EDU_TAGS[:3]))}",
        "pinterest": {"title": pin or title, "description": f"{body} Trading concepts explained simply.", "link": SITE + site_path},
        "title": title,
    }


def entry_right(st):
    """Entry label at the right end, away from the arrows near the entry bar."""
    st["levels"] = [{**l, "labelPos": "right"} if l["label"] == "Entry" else l for l in st["levels"]]
    return st


def carousel(cid, vid, slides, post):
    C.append({"id": cid, "kind": "carousel", "lesson": vid, "tag": EDU_TAG, "handle": HANDLE, "site_path": post["pinterest"]["link"].replace(SITE, ""),
              "charts": L[vid]["charts"], "slides": slides, "post": post})


# ------------------------------------------------------------------ RSI
R = edu.R
gain = (R["c"][-1]["c"] / R["c"][R["first"]]["c"] - 1) * 100
carousel("c201_car_rsi", "v201_edu_rsi_70", [
    {"type": "cover", "kicker": "RSI, explained", "title": "RSI above 70 doesn't mean sell.", "chart": "a", "chartH": 620,
     "state": state("v201_edu_rsi_70", 2, marks=[m for m in state("v201_edu_rsi_70", 2)["marks"] if m["text"] == "Sell here?"])},
    {"type": "points", "title": "What RSI actually measures", "points": [
        {"b": "Recent gains vs recent losses", "t": "RSI 14 compares the average gain with the average loss of the last 14 bars, on a 0–100 scale."},
        {"b": "Above 70: gains dominated", "t": "It describes strength. It does not predict a top.", "color": "coral"},
        {"b": "Below 30: losses dominated", "t": "Same idea on the way down. Not an automatic buy.", "color": "blue"}]},
    {"type": "chart", "title": "In a trend, it can stay above 70", "chart": "a", "chartH": 600, "state": state("v201_edu_rsi_70", 2),
     "text": f"Here RSI stayed above 70 on **{R['above']} of the next {R['n']} bars**, and price rose another **{gain:.0f}%**."},
    {"type": "rows", "title": "Read it in context", "head": ["", "", ""], "rows": [
        {"cells": ["Strong trend", "", "Strength"], "good": True, "hl": True}, {"cells": ["Sideways range", "", "Stretched"]},
        {"cells": ["Price higher high, RSI lower high", "", "Fading"], "hl": True}],
     "text": "The last one is called **divergence**: a warning, not a trigger on its own."},
    {"type": "points", "title": "Common mistakes", "points": [
        {"b": "Shorting every cross above 70", "t": "In an uptrend that means fighting the move again and again.", "color": "coral"},
        {"b": "Using it alone", "t": "Check the trend and key levels first, then read RSI.", "color": "gold"},
        {"b": "Ignoring the timeframe", "t": "70 on a 1-minute chart is not 70 on a daily chart.", "color": "blue"}]},
    {"type": "end", "title": "RSI measures strength, not tops.", "text": "Decide first: is the market trending or ranging? Then read RSI in that context."},
], post_car("RSI above 70 doesn't mean sell", f"RSI compares recent gains with recent losses on a 0-100 scale. Above 70 means gains dominated: strength, not a top. In this example RSI stayed above 70 on {R['above']} of the next {R['n']} bars while price rose another {gain:.0f}%. Read it in context: trend or range.",
            ["#rsi", "#indicators"], "RSI explained: why above 70 doesn't mean sell"))

# ------------------------------------------------------------------ 20 EMA
E = edu.E
carousel("c202_car_20ema", "v202_edu_20ema", [
    {"type": "cover", "kicker": "Moving averages", "title": "One line that shows you the trend.", "chart": "a", "state": state("v202_edu_20ema", 1)},
    {"type": "points", "title": "What the 20 EMA is", "points": [
        {"b": "An average of recent closes", "t": "Roughly the last 20 bars, with more weight on the newest ones (exponential)."},
        {"b": "Rising, price above", "t": "The trend is up.", "color": "mint"},
        {"b": "Falling, price below", "t": "The trend is down.", "color": "coral"}]},
    {"type": "chart", "title": "Pullbacks often find buyers near it", "chart": "a", "state": state("v202_edu_20ema", 1),
     "text": "In an uptrend, dips back to a **rising** EMA are where many traders look for entries."},
    {"type": "chart", "title": "Flat EMA: no trend, no edge", "chart": "a", "state": state("v202_edu_20ema", 2),
     "text": f"It lags. When price goes sideways, the line goes flat: here price crossed it **{len(E['cross'])} times in 27 bars**."},
    {"type": "rows", "title": "How to read the 20 EMA", "head": ["", "", ""], "rows": [
        {"cells": ["Rising, price above", "", "Uptrend"], "good": True, "hl": True}, {"cells": ["Falling, price below", "", "Downtrend"]},
        {"cells": ["Flat, crossed often", "", "No trend"], "hl": True}]},
    {"type": "end", "title": "Use it as a filter, not a signal.", "text": "Trade with the slope, wait for pullbacks, and stand aside when it goes flat."},
], post_car("The 20 EMA trend filter", f"The 20 EMA is an average of recent closes that weighs the newest ones more. Rising with price above: uptrend, and pullbacks often find buyers near it. Flat: no trend; in this example price crossed it {len(E['cross'])} times in 27 bars.",
            ["#ema", "#movingaverage", "#indicators"], "How to use the 20 EMA as a trend filter"))

# ------------------------------------------------------------------ VWAP
carousel("c203_car_vwap", "v203_edu_vwap", [
    {"type": "cover", "kicker": "Day trading", "title": "Why every day trader watches VWAP.", "chart": "a", "state": state("v203_edu_vwap", 2)},
    {"type": "formula", "title": "What VWAP is", "formula": "VWAP = Σ(price × volume) ÷ Σ(volume)",
     "small": "From the session open · price = (high + low + close) ÷ 3", "text": "The **average price everyone paid today**, weighted by how much was traded at each price."},
    {"type": "chart", "title": "Reclaim, retest, hold", "chart": "a", "state": state("v203_edu_vwap", 2),
     "text": "Price gets back above VWAP, comes back to test it, and buyers defend it. In this example **every close after the reclaim stays above**."},
    {"type": "rows", "title": "Reading VWAP", "head": ["", "", ""], "rows": [
        {"cells": ["Above VWAP", "", "Buyers ahead"], "good": True, "hl": True}, {"cells": ["Below VWAP", "", "Sellers ahead"]},
        {"cells": ["Chopping around it", "", "No control"], "hl": True}],
     "text": "Above it, today's average buyer is in profit. Below it, today's average buyer is losing."},
    {"type": "points", "title": "Keep in mind", "points": [
        {"b": "It resets every session", "t": "Intraday VWAP starts again at the open. Yesterday's line is a different thing.", "color": "blue"},
        {"b": "It's a reference, not a wall", "t": "Price often chops around it before choosing a side.", "color": "gold"},
        {"b": "Pair it with structure", "t": "A reclaim means more when it also breaks a level.", "color": "mint"}]},
    {"type": "end", "title": "VWAP tells you who's in control today.", "text": "Watch the reclaim, then the retest. A hold is the confirmation."},
], post_car("VWAP explained for day traders", "VWAP is the average price everyone paid today, weighted by volume, starting from the session open. Above it, today's average buyer is in profit; below it, the average buyer is losing. A reclaim followed by a retest that holds is one of the cleanest things to watch intraday.",
            ["#vwap", "#daytradingtips"], "VWAP explained in 6 slides"))

# ------------------------------------------------------------------ support / resistance flip
carousel("c204_car_sr_flip", "v204_edu_sr_flip", [
    {"type": "cover", "kicker": "Price action", "title": "Old resistance becomes new support.", "chart": "a", "state": state("v204_edu_sr_flip", 2)},
    {"type": "points", "title": "Three ideas, one level", "points": [
        {"b": "Resistance", "t": "A price where sellers keep showing up and push price back down.", "color": "coral"},
        {"b": "Support", "t": "A price where buyers keep showing up and push price back up.", "color": "mint"},
        {"b": "The flip", "t": "After a clean break, the same level often swaps its role.", "color": "gold"}]},
    {"type": "chart", "title": "Three tries. Sellers win each time.", "chart": "a", "state": state("v204_edu_sr_flip", 1),
     "text": "Price hits the same level **three times** and gets rejected every time."},
    {"type": "chart", "title": "Break, then retest from above", "chart": "a", "state": state("v204_edu_sr_flip", 2),
     "text": "A close above the level, then a pullback that **holds** on the same price. Buyers who missed the break are waiting there."},
    {"type": "points", "title": "How traders use it", "points": [
        {"b": "Wait for the close", "t": "A candle closing above the level, not a wick poking through."},
        {"b": "Let price come back", "t": "The retest shows whether the level now holds.", "color": "blue"},
        {"b": "Know where you're wrong", "t": "A close back below the level means the idea failed.", "color": "coral"}]},
    {"type": "end", "title": "Break, retest, hold.", "text": "The level that stopped price on the way up often supports it on the way back."},
], post_car("Old resistance becomes new support", "A level that rejected price three times breaks, and on the retest it holds from above. Wait for the close above, let price come back, and know where you're wrong: a close back below the level.",
            ["#supportandresistance", "#priceaction"], "Support and resistance flip explained"))

# ------------------------------------------------------------------ failed breakout
carousel("c205_car_failed_breakout", "v205_edu_failed_breakout", [
    {"type": "cover", "kicker": "Price action", "title": "This candle traps buyers every day.", "chart": "a", "state": state("v205_edu_failed_breakout", 1)},
    {"type": "chart", "title": "A wick above is not a breakout", "chart": "a", "state": state("v205_edu_failed_breakout", 1),
     "text": "Price pokes above resistance, buyers jump in, and the candle **closes back below** the level."},
    {"type": "points", "title": "Why it often drops after", "points": [
        {"b": "Buyers are trapped", "t": "Everyone who bought the poke is now losing.", "color": "coral"},
        {"b": "Their stops sit below", "t": "Usually just under the level or the candle's low.", "color": "gold"},
        {"b": "Stops add fuel", "t": "When they get hit, they become market sell orders.", "color": "coral"}]},
    {"type": "chart", "title": "Trapped buyers become sellers", "chart": "a", "state": state("v205_edu_failed_breakout", 2)},
    {"type": "rows", "title": "Before you buy a breakout", "head": ["", "", ""], "rows": [
        {"cells": ["Wick above the level", "", "Not yet"], "hl": True}, {"cells": ["Close above the level", "", "Breakout"], "good": True, "hl": True},
        {"cells": ["Close back below", "", "Failed"]}]},
    {"type": "end", "title": "Wait for the close, not the wick.", "text": "A breakout is a candle that closes beyond the level. Everything else is a poke."},
], post_car("The candle that traps breakout buyers", "Price pokes above resistance, buyers jump in, and the candle closes back below: a failed breakout. Trapped buyers' stops add fuel to the drop. Wait for a close above the level, not just a wick.",
            ["#breakout", "#priceaction"], "Failed breakout (bull trap) explained"))

# ------------------------------------------------------------------ double top
D = edu.D
assert D["target"] == round(D["neck"] - (D["hi1"] - D["neck"]), 2)
carousel("c206_car_double_top", "v206_edu_double_top", [
    {"type": "cover", "kicker": "Chart patterns", "title": "The double top, and when it's real.", "chart": "a", "state": state("v206_edu_double_top", 2)},
    {"type": "chart", "title": "Two highs. One neckline.", "chart": "a", "state": state("v206_edu_double_top", 1),
     "text": "Two highs at about the same price, and a low between them: that low is the **neckline**."},
    {"type": "chart", "title": "Confirmed only below the neckline", "chart": "a", "state": state("v206_edu_double_top", 2),
     "text": "Until a candle **closes below the neckline**, it's just two highs."},
    {"type": "formula", "title": "The classic target", "formula": "Neckline − (Top − Neckline)",
     "small": f"Here: {D['neck']:.2f} − ({D['hi1']:.2f} − {D['neck']:.2f}) = {D['target']:.2f}",
     "text": "The pattern's height, measured down from the neckline. In this example price got there, **but many double tops don't**."},
    {"type": "points", "title": "Common mistakes", "points": [
        {"b": "Calling it too early", "t": "Before the neckline breaks there's no pattern.", "color": "coral"},
        {"b": "Expecting the target", "t": "It's a reference, not a promise.", "color": "gold"},
        {"b": "Ignoring the bigger trend", "t": "In a strong uptrend, many double tops simply fail.", "color": "blue"}]},
    {"type": "end", "title": "No neckline break, no double top.", "text": "Wait for the close below, then manage risk like any other trade."},
], post_car("Double top: when is it real?", f"Two highs at about the same price and a low between them, the neckline. It's only confirmed by a close below the neckline. The classic target is the pattern's height measured down from it: here {D['neck']:.2f} − ({D['hi1']:.2f} − {D['neck']:.2f}) = {D['target']:.2f}. Many double tops fail.",
            ["#chartpatterns", "#doubletop"], "Double top pattern explained"))

# ------------------------------------------------------------------ ATR stop
carousel("c207_car_atr_stop", "v207_edu_atr_stop", [
    {"type": "cover", "kicker": "Risk management", "title": "Why your stop keeps getting hit.", "chart": "a", "state": entry_right(state("v207_edu_atr_stop", 1))},
    {"type": "formula", "title": "ATR: how far price normally moves", "formula": "True range = max(H − L, |H − Cₚ|, |L − Cₚ|)",
     "small": "Cₚ = previous close · ATR 14 = Wilder average of 14 true ranges", "text": "ATR is the **average true range**: the normal size of one bar, gaps included."},
    {"type": "chart", "title": "Half an ATR: inside normal noise", "chart": "a", "state": entry_right(state("v207_edu_atr_stop", 1)),
     "text": "A stop half an ATR from entry gets taken out by an **ordinary dip**."},
    {"type": "chart", "title": "1.5 ATR: the same dip is just noise", "chart": "a", "state": state("v207_edu_atr_stop", 2)},
    {"type": "formula", "title": "Same dollar risk", "formula": "Contracts = $ risk ÷ (stop × $ per point)",
     "text": "**Wider stop, smaller size.** The dollar risk per trade stays the same."},
    {"type": "end", "title": "Place stops outside normal noise.", "text": "Measure noise with ATR, then size the position to the stop."},
], post_car("Why your stop keeps getting hit", "ATR, the average true range, is how far price normally moves in one bar. A stop at half an ATR sits inside normal noise; at 1.5 ATR an ordinary dip doesn't reach it. Wider stop, smaller size, same dollar risk.",
            ["#atr", "#stoploss", "#riskmanagement"], "ATR stop loss explained", "/tools/position-size-calculator/"))

# ------------------------------------------------------------------ Bollinger squeeze
B = edu.B
ratio = int(B["ratio"])
carousel("c208_car_bollinger", "v208_edu_bollinger_squeeze", [
    {"type": "cover", "kicker": "Volatility", "title": "When the bands pinch, get ready.", "chart": "a", "state": state("v208_edu_bollinger_squeeze", 1)},
    {"type": "formula", "title": "Bollinger Bands", "formula": "Middle = 20-bar average", "small": "Upper and lower band = middle ± 2 standard deviations",
     "text": "The bands **widen** when price moves a lot and **narrow** when it goes quiet."},
    {"type": "chart", "title": "Low volatility: the squeeze", "chart": "a", "state": state("v208_edu_bollinger_squeeze", 1)},
    {"type": "chart", "title": "Quiet markets don't stay quiet", "chart": "a", "state": state("v208_edu_bollinger_squeeze", 2),
     "text": f"Low volatility tends to be followed by expansion: here the bands ended up **more than {ratio}× wider**."},
    {"type": "points", "title": "How to read a squeeze", "points": [
        {"b": "Squeeze = low volatility", "t": "Price is coiling in a narrow range.", "color": "gold"},
        {"b": "Expansion tends to follow", "t": "Not always right away, and not always big.", "color": "blue"},
        {"b": "Direction is unknown", "t": "The squeeze says a move may come, not which way. Wait for the break.", "color": "coral"}]},
    {"type": "end", "title": "Pinched bands: prepare, don't predict.", "text": "Mark the range, wait for price to leave it, then follow."},
], post_car("The Bollinger Band squeeze", f"Bollinger Bands sit two standard deviations around a 20-bar average. When price goes quiet they squeeze together, and low volatility tends to be followed by expansion: here the bands ended up more than {ratio}x wider. The squeeze doesn't tell you the direction.",
            ["#bollingerbands", "#volatility", "#indicators"], "Bollinger Band squeeze explained"))

# ------------------------------------------------------------------ risk:reward and win rate
be = lambda r: 100 / (1 + r)
assert round(be(1), 1) == 50.0 and round(be(2), 1) == 33.3 and round(be(3), 1) == 25.0 and round(0.4 * 2 - 0.6, 2) == 0.2
carousel("c209_car_risk_reward", "v209_edu_risk_reward", [
    {"type": "cover", "kicker": "Risk management", "title": "Wrong 60% of the time, still profitable.", "chart": "a", "state": state("v209_edu_risk_reward", 1)},
    {"type": "formula", "title": "The break-even win rate", "formula": "Break-even = 1 ÷ (1 + R)", "small": "R = what you aim to make ÷ what you risk",
     "text": "The bigger your reward compared with your risk, the **fewer winners you need**."},
    {"type": "rows", "title": "Win rate you need to break even", "head": ["Reward : risk", "", "Break-even"], "rows": [
        {"cells": ["1 : 1", "", "50%"]}, {"cells": ["2 : 1", "", "33.3%"], "good": True, "hl": True}, {"cells": ["3 : 1", "", "25%"]}],
     "text": "Before commissions and slippage."},
    {"type": "rows", "title": "10 trades, 40% winners, 2 : 1", "head": ["", "", ""], "rows": [
        {"cells": ["4 wins × 2R", "", "+8R"]}, {"cells": ["6 losses × 1R", "", "−6R"]}, {"cells": ["Per 10 trades", "", "+2R"], "good": True, "hl": True}],
     "text": "That's **+0.2R per trade** on average."},
    {"type": "points", "title": "The fine print", "points": [
        {"b": "Costs raise the bar", "t": "Commissions and slippage push the break-even win rate up.", "color": "coral"},
        {"b": "Targets must be realistic", "t": "A 3 : 1 target that's rarely hit lowers your win rate.", "color": "gold"},
        {"b": "Track both numbers", "t": "Win rate means nothing without your average win and loss.", "color": "blue"}]},
    {"type": "end", "title": "Win rate only matters next to R.", "text": "Know your reward to risk, then you know how often you need to be right."},
], post_car("Wrong 60% of the time and still profitable", "Break-even win rate = 1 ÷ (1 + R). At 2:1 you only need to win 1 trade in 3 (33.3%, before costs). Win 4 out of 10: +8R − 6R = +2R every ten trades, or +0.2R per trade.",
            ["#riskreward", "#riskmanagement", "#tradingpsychology"], "Win rate vs risk reward explained", "/tools/r-multiple-calculator/"))

# ------------------------------------------------------------------ position size in futures
carousel("c210_car_position_size", "v210_edu_position_size", [
    {"type": "cover", "kicker": "Futures", "title": "How many contracts? Three numbers.", "chart": "a", "state": state("v210_edu_position_size", 0)},
    {"type": "rows", "title": "1. How much you can lose", "head": ["", "", ""], "rows": [
        {"cells": ["Account", "", "$50,000"]}, {"cells": ["Risk per trade", "", "1%"]}, {"cells": ["Max loss", "", "$500"], "good": True, "hl": True}]},
    {"type": "rows", "title": "2. What one contract risks", "head": ["Contract", "$ per point", "4-point stop"], "rows": [
        {"cells": ["Micro (MES)", "$5", "$20"]}, {"cells": ["E-mini (ES)", "$50", "$200"]}],
     "text": "Micro E-mini and E-mini S&P 500 futures."},
    {"type": "rows", "title": "3. Divide and round down", "head": ["", "", "Contracts"], "rows": [
        {"cells": ["$500 ÷ $20", "", "25 micros"], "good": True, "hl": True}, {"cells": ["$500 ÷ $200 = 2.5", "", "2 E-minis"]}]},
    {"type": "points", "title": "Good habits", "points": [
        {"b": "Always round down", "t": "2.5 contracts is 2, never 3.", "color": "gold"},
        {"b": "Include costs", "t": "Commissions and slippage are part of the risk.", "color": "coral"},
        {"b": "Same % every trade", "t": "The stop changes, the dollar risk doesn't.", "color": "mint"}]},
    {"type": "end", "title": "Size comes from the stop, not the mood.", "text": "Max loss ÷ risk per contract. Every trade, before you click."},
], post_car("How many futures contracts should you trade?", "1) Max loss: 1% of $50,000 = $500. 2) Risk per contract: a 4-point stop is $20 on the Micro E-mini S&P ($5/point) and $200 on the E-mini ($50/point). 3) Divide and round down: 25 micros or 2 E-minis.",
            ["#positionsizing", "#futurestrading", "#riskmanagement"], "Futures position size in 3 numbers", "/tools/position-size-calculator/"))
