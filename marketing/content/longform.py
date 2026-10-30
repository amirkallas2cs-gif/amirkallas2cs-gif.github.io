"""Long-form YouTube lessons (16:9, 6-10 minutes, chapters, thumbnail). Ids: yNNN_long_<topic>.
Charts and numbers are reused from the short lessons in edu.py, so every figure was already checked there.
Rendered by video/render.py (format "landscape") and video/still.py (thumbnail)."""
import edu
from edu import EDU_TAG, HANDLE, SITE, words

L = {v["id"]: v for v in edu.V}
Y = []
FOLLOW_LONG = {"type": "follow", "text": "Subscribe for a new trading lesson every week.", "button": "Subscribe",
               "say": "If this helped, subscribe for a new trading lesson every week, and short lessons every day. See you in the next one."}


def lesson_marks(vid, scene):
    s = [x for x in L[vid]["scenes"] if x["type"] == "chart"][scene]
    return [{**m, "at": 0.3} for m in s.get("marks", [])], [dict(z) for z in s.get("zones", [])], [dict(l) for l in s.get("levels", [])]


def post_long(title, body, tags):
    hashtags = " ".join(dict.fromkeys(tags + ["#tradingeducation", "#daytrading", "#technicalanalysis"]))
    note = "Educational content on illustrative charts. Not financial advice; trading involves risk of loss."
    return {
        # {chapters} is replaced at publish time with the real timestamps of this render
        "youtube": {"title": title[:100], "description": f"{body}\n\n{{chapters}}\n\nFree guides and calculators: {SITE}/learn/\nShort lessons every day: {HANDLE} on Instagram and TikTok.\n\n{note}\n\n{hashtags}",
                    "tags": ["trading", "day trading", "technical analysis", "trading for beginners", "indicators", "risk management"]},
        "facebook": f"{body}\n\nNew full lesson: {title}. Follow for one trading concept a day.\n\n{note}",
        "pinterest": {"title": title[:100], "description": f"{body} Full video lesson.", "link": SITE + "/learn/"},
    }


# ------------------------------------------------------------------ 1. RSI, 20 EMA, VWAP
R, E = edu.R, edu.E
gain = round((R["c"][-1]["c"] / R["c"][R["first"]]["c"] - 1) * 100)
f = R["first"] - 14  # RSI chart starts at bar 14 of the computed series
n_rsi = len(L["v201_edu_rsi_70"]["charts"]["a"]["candles"])
n_ema = len(L["v202_edu_20ema"]["charts"]["a"]["candles"])
n_vw = len(L["v203_edu_vwap"]["charts"]["a"]["candles"])
rsi_cross, _, _ = lesson_marks("v201_edu_rsi_70", 1)
rsi_late, _, _ = lesson_marks("v201_edu_rsi_70", 2)
ema_pb, _, _ = lesson_marks("v202_edu_20ema", 1)
_, ema_zone, _ = lesson_marks("v202_edu_20ema", 2)
vw_rc, _, _ = lesson_marks("v203_edu_vwap", 1)
vw_ts, _, _ = lesson_marks("v203_edu_vwap", 2)
rc = vw_rc[0]["bar"]
cross = len(E["cross"])

Y.append({"id": "y301_long_rsi_ema_vwap", "kind": "long", "format": "landscape", "tag": EDU_TAG,
          "charts": {"rsi": L["v201_edu_rsi_70"]["charts"]["a"], "ema": L["v202_edu_20ema"]["charts"]["a"], "vwap": L["v203_edu_vwap"]["charts"]["a"]},
          "thumb": {"type": "thumb", "kicker": "Full lesson", "title": "RSI, EMA, VWAP: stop misusing them", "chart": "rsi",
                    "state": {"show": ["rsi"], "marks": [m for m in rsi_late if m["text"] == "Sell here?"]}},
          "scenes": [
    # intro
    {"type": "chart", "chart": "rsi", "chapter": "Intro", "headline": "3 indicators. 3 common mistakes.", "big": True, "reveal": [12, n_rsi], "show": ["rsi"],
     "say": "RSI, the twenty EMA and VWAP are probably the three indicators day traders use most. And all three get misused in the same way: as signals, instead of context."},
    {"type": "rows", "title": "In this lesson", "head": ["", "", ""], "rows": [
        {"cells": ["1. RSI", "", "strength, not tops"]}, {"cells": ["2. 20 EMA", "", "a trend filter"]},
        {"cells": ["3. VWAP", "", "who's in control today"]}, {"cells": ["4. All three together", "", "a simple checklist"], "good": True, "hl": True}],
     "say": "In the next few minutes: what each one actually measures, the mistake most traders make with it, and how to read all three together with a simple checklist. Everything here is education on illustrative charts, not financial advice."},
    # RSI
    {"type": "chart", "chart": "rsi", "chapter": "RSI: strength, not tops", "headline": "RSI: what it measures", "reveal": [6, f - 1], "show": ["rsi"],
     "say": "Let's start with RSI, the relative strength index. The standard setting looks at the last fourteen bars."},
    {"type": "chart", "chart": "rsi", "headline": "RSI: what it measures", "reveal": [f - 1, f + 3], "show": ["rsi"], "marks": rsi_cross,
     "say": "It compares the average size of the up moves with the average size of the down moves, and puts the result on a scale from zero to one hundred. Above seventy, the up moves have been much bigger. Traders call that overbought. Below thirty, it's the opposite: oversold."},
    {"type": "rows", "title": "RSI settings", "head": ["Setting", "", "Behaviour"], "rows": [
        {"cells": ["7 bars", "", "Faster, more extremes"]}, {"cells": ["14 bars", "", "The default"], "good": True, "hl": True}, {"cells": ["21 bars", "", "Slower, fewer extremes"]}],
     "say": "A quick note on settings. Fourteen is the default. A shorter setting, like seven, reacts faster and hits the extremes more often. A longer one, like twenty-one, moves more slowly and reaches them less often. There's no magic number: what matters is using the same one consistently, so you learn how it behaves."},
    {"type": "hook", "kicker": "The key point", "text": "Overbought is a description, not a forecast.",
     "say": "But here's the key point. Overbought describes what already happened. It's not a forecast of what happens next."},
    {"type": "chart", "chart": "rsi", "headline": "In a trend, RSI can stay above 70", "pin": True, "reveal": [f + 3, n_rsi], "show": ["rsi"], "marks": rsi_late,
     "say": f"Look at this example. RSI crosses seventy here. Selling would have meant fighting the trend: RSI stayed above seventy on {words(R['above'])} of the next {words(R['n'])} bars, and price rose another {words(gain)} percent."},
    {"type": "rows", "title": "Read RSI in context", "head": ["", "", ""], "rows": [
        {"cells": ["Strong trend", "", "Strength"], "good": True, "hl": True}, {"cells": ["Sideways range", "", "Stretched"]},
        {"cells": ["Higher high, lower RSI high", "", "Fading momentum"], "hl": True}],
     "say": "So read it in context. In a strong trend, RSI above seventy usually means strength. In a sideways range, the same reading can mean price is stretched and may rotate back. And when price makes a higher high while RSI makes a lower high, that's called divergence: a warning that momentum is fading. A warning, not a trigger on its own."},
    {"type": "hook", "kicker": "Mistake number one", "text": "Shorting every cross above 70.",
     "say": "So mistake number one is using RSI as a sell signal in a trend. Decide first whether the market is trending or ranging. Then read RSI."},
    # EMA
    {"type": "chart", "chart": "ema", "chapter": "20 EMA: the trend filter", "headline": "The 20 EMA", "reveal": [8, 16], "add": ["ema"],
     "say": "The second tool is the simplest way to see the trend: the twenty period exponential moving average."},
    {"type": "chart", "chart": "ema", "headline": "Rising EMA, price above: uptrend", "reveal": [16, 32], "show": ["ema"], "marks": ema_pb,
     "say": "It's an average of roughly the last twenty closes, with more weight on the most recent ones, so it reacts faster than a simple average. When the line is rising and price stays above it, the trend is up, and pullbacks to the line are often where buyers step in. Here, twice."},
    {"type": "rows", "title": "EMA or SMA?", "head": ["", "", ""], "rows": [
        {"cells": ["Simple (SMA)", "", "Every close weighs the same"]}, {"cells": ["Exponential (EMA)", "", "Recent closes weigh more"], "good": True, "hl": True},
        {"cells": ["Result", "", "EMA turns sooner"]}],
     "say": "Why exponential? A simple moving average gives every close the same weight. The exponential one gives more weight to recent closes, so it turns sooner, but it also gets faked out a little more often. Nine, twenty and fifty periods are common choices; twenty is a good middle ground for intraday trends."},
    {"type": "chart", "chart": "ema", "headline": "Flat EMA: no trend", "reveal": [32, n_ema], "show": ["ema"], "zones": [{**z, "at": 0.55} for z in ema_zone],
     "say": f"But every moving average lags. When the market goes sideways, the line goes flat, and price crosses it again and again. In this example it crossed {words(cross)} times in twenty-seven bars."},
    {"type": "rows", "title": "How to read the 20 EMA", "head": ["", "", ""], "rows": [
        {"cells": ["Rising, price above", "", "Uptrend"], "good": True, "hl": True}, {"cells": ["Falling, price below", "", "Downtrend"]},
        {"cells": ["Flat, crossed often", "", "No trend"], "hl": True}],
     "say": "So the rules are simple. Rising, with price above: uptrend. Falling, with price below: downtrend. Flat and crossed often: no trend, and probably no edge."},
    {"type": "hook", "kicker": "Mistake number two", "text": "Trading every cross of the line.",
     "say": "Mistake number two is treating every cross of the line as a buy or sell signal. In a range, that usually means a string of small losses. Use the EMA as a filter: it tells you which direction to look for trades, and when to stand aside."},
    # VWAP
    {"type": "chart", "chart": "vwap", "chapter": "VWAP: who's in control today", "headline": "VWAP", "reveal": [6, 12], "add": ["vwap"],
     "say": "The third tool is the one almost every intraday trader has on the chart: VWAP, the volume weighted average price."},
    {"type": "hook", "kicker": "VWAP", "text": "Σ(price × volume) ÷ Σ(volume), from the open.",
     "say": "It's the average price everyone has paid today, weighted by how much was traded at each price. It starts at the session open and resets every day."},
    {"type": "hook", "kicker": "VWAP", "text": "An intraday tool. It steadies as the day goes on.",
     "say": "One more detail: standard VWAP is an intraday tool. Because it's calculated from today's open, it's most meaningful on intraday charts of liquid markets. Early in the session, with only a few bars, it can move a lot. As volume builds up through the day, it gets steadier."},
    {"type": "chart", "chart": "vwap", "headline": "Above VWAP: today's buyers in profit", "reveal": [12, rc + 1], "show": ["vwap"], "marks": vw_rc,
     "say": "Why does it matter? Above VWAP, today's average buyer is in profit. Below it, today's average buyer is losing. That's why many traders read it as the line between buyers and sellers being in control."},
    {"type": "chart", "chart": "vwap", "headline": "Reclaim, retest, hold", "reveal": [rc + 1, n_vw], "show": ["vwap"], "marks": vw_ts,
     "say": "Here price trades below VWAP for most of the morning, then reclaims it, comes back to test it, and buyers defend it. In this example, every close after the reclaim stays above."},
    {"type": "hook", "kicker": "Mistake number three", "text": "Treating VWAP as a wall.",
     "say": "Mistake number three is treating VWAP as a wall that price must bounce from. It's a reference. Price often chops around it before choosing a side, so wait for the reclaim and the retest."},
    # together
    {"type": "hook", "chapter": "Putting it together", "kicker": "Putting it together", "text": "Context first. Then the trade.",
     "say": "Now let's put the three together. None of them is a signal on its own. Together, they give you context."},
    {"type": "rows", "title": "A simple checklist", "head": ["", "", ""], "rows": [
        {"cells": ["1. Trend", "", "20 EMA slope"]}, {"cells": ["2. Today", "", "Side of VWAP"]}, {"cells": ["3. Momentum", "", "RSI in context"]}],
     "say": "One: the trend. Is the twenty EMA rising or falling, and is price on the right side of it? Two: today. Is price above or below VWAP? Three: momentum. Is RSI confirming the move, or diverging from it?"},
    {"type": "rows", "title": "When they agree, and when they don't", "head": ["", "", ""], "rows": [
        {"cells": ["All three agree", "", "Stronger context"], "good": True, "hl": True}, {"cells": ["They disagree", "", "Smaller, or no trade"], "hl": True}],
     "say": "When all three point the same way, the context is stronger. When they disagree, many traders trade smaller, or not at all. Either way, the entry and the stop still come from price: levels, not indicators."},
    {"type": "chart", "chart": "vwap", "headline": "Applying the checklist", "reveal": [n_vw - 4, n_vw], "show": ["vwap"], "marks": vw_rc + vw_ts,
     "say": "Take the VWAP example again. Before the reclaim, price was below VWAP, so there was no long context for today. After the reclaim and a retest that held, every close stayed above VWAP. That's when a long idea starts to make sense, with the stop placed below the retest low, where the idea would be proven wrong, not at a random distance."},
    {"type": "hook", "kicker": "One more thing", "text": "Write down what they said on every trade.",
     "say": "And keep a record. Note in your journal what the three indicators said on every trade. After fifty trades, your own numbers will tell you which of these rules actually help you."},
    # summary
    {"type": "rows", "chapter": "Summary", "title": "To sum up", "head": ["", "", ""], "rows": [
        {"cells": ["RSI", "", "Strength, not tops"]}, {"cells": ["20 EMA", "", "Trend filter, lags"]}, {"cells": ["VWAP", "", "Who's in control today"]}],
     "say": "To sum up. RSI measures strength, not tops. The twenty EMA is a trend filter, and it lags. VWAP tells you who's in control today. Use them for context, and let price give you the trade."},
    FOLLOW_LONG],
          "post": post_long("RSI, 20 EMA and VWAP explained: the 3 mistakes most day traders make",
                            "RSI, the 20 EMA and VWAP are the three indicators day traders use most, and all three get misused as signals instead of context. In this lesson: what each one measures, the most common mistake with each, and a simple 3-step checklist to read them together.",
                            ["#rsi", "#vwap", "#ema"])})
