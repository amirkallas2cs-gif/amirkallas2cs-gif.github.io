"""Content bank: video specs + post texts for every channel. Run to (re)write content/videos/*.json.
Numbers come from the demo journal shown in the app (verified against the spreadsheet edition).
Every video that shows numbers carries the "Example journal · demo data" tag."""
import json, pathlib

OUT = pathlib.Path(__file__).parent / "videos"
TAG = "Example journal · demo data"
LINK = "https://kallas8.gumroad.com/l/axltbh"
BASE_TAGS = ["#tradingjournal", "#daytrading", "#trading", "#tradingpsychology", "#futurestrading"]

CTA = lambda text="A calm, honest record of every trade.": {
    "type": "cta", "title": "Trading Journal AI", "sub": "Desktop app · Windows & Mac", "text": text, "button": "Link in bio",
    "say": "Trading Journal AI. Link in bio."}
ONECLICK = {"type": "shot", "img": "oneclick", "title": "One click. Your AI reviews your week.", "ring": "btn_claude",
            "chips": [{"text": "Claude", "color": "mint"}, {"text": "ChatGPT", "color": "blue"}, {"text": "Gemini", "color": "gold"}],
            "say": "Then one click, and your own AI reviews your week."}


def post(title, body, tags, pin=None):
    """Texts for each channel. `title` is also the YouTube title; `pin` the Pinterest title."""
    hashtags = " ".join(dict.fromkeys(tags + BASE_TAGS))
    return {
        "instagram": f"{body}\n\nTrading Journal AI: desktop app for Windows & Mac, with a one-click AI review. Link in bio.\n\n{hashtags}",
        "tiktok": f"{body} {' '.join(dict.fromkeys(tags + BASE_TAGS[:3]))}",
        "youtube": {"title": f"{title} #shorts", "description": f"{body}\n\nTrading Journal AI (Windows & Mac): {LINK}\n\nExample journal with demo data. Not financial advice.\n\n{hashtags} #shorts"},
        "facebook": f"{body}\n\nTrading Journal AI: {LINK}",
        "pinterest": {"title": pin or title, "description": f"{body} Trading journal app for Windows & Mac with AI weekly review.", "link": LINK},
    }


V = []

V.append({"id": "v001_rule_breaks", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Trading journal", "text": "Breaking your own rules has a price. Do you know yours?",
     "say": "Breaking your own rules has a price. Do you know yours?"},
    {"type": "shot", "img": "add_trade", "title": "Ten fields per trade. The rest is automatic.",
     "chips": [{"html": "R <b>+2.00R</b>"}, {"html": "P&amp;L <b>+$77.52</b>"}, {"html": "<b>Win</b>"}],
     "say": "Log every trade in ten fields. Risk, R and P and L calculate themselves."},
    {"type": "rows", "title": "Did you follow your plan?", "head": ["My plan", "Trades", "Net P&L"],
     "rows": [{"cells": ["Followed", "73", "+$2,033"], "good": True}, {"cells": ["Broke a rule", "16", "−$555"], "hl": True}],
     "say": "Mark whether you followed your plan. In this example, sixteen rule breaks cost five hundred and fifty five dollars."},
    {"type": "rows", "title": "Your costliest mistakes", "head": ["Mistake", "Times", "Net P&L"],
     "rows": [{"cells": ["FOMO entry", "5", "−$609"], "hl": True}, {"cells": ["No setup", "3", "−$122"]}, {"cells": ["Chased price", "1", "−$65"]}],
     "say": "And you see which mistake costs the most. Here, it's FOMO entries."},
    ONECLICK,
    {"type": "chat", "me": "Weekly review, last 14 days.",
     "ai": ["Net P&amp;L <span class='m'>+385.28</span> · win rate <b>67%</b> · profit factor <b>3.80</b>",
            "Your best hours: <b>10:00–12:00</b>, 7 wins out of 8. One rule for next week: <b>no trades before 10:00.</b>"],
     "say": "Claude, ChatGPT or Gemini, working from your real numbers."},
    CTA()],
    "post": post("What breaking your trading rules really costs", "Breaking your own rules has a price. In this example journal, 16 rule breaks cost $555, and FOMO entries were the costliest mistake.",
                 ["#riskmanagement", "#tradingrules"], "How much do broken trading rules cost you?")})

V.append({"id": "v002_best_setup", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Your edge", "text": "Your favourite setup might be the one losing you money.",
     "say": "Your favourite setup might be the one losing you money."},
    {"type": "rows", "title": "Average R by setup", "head": ["Setup", "Trades", "Avg R"],
     "rows": [{"cells": ["Trend pullback", "16", "+0.89R"], "good": True, "hl": True}, {"cells": ["Opening range", "29", "+0.63R"]},
              {"cells": ["VWAP reclaim", "24", "+0.11R"]}, {"cells": ["Failed breakout", "20", "−0.41R"], "hl": True}],
     "say": "In this example journal, trend pullbacks earn almost one R per trade. Failed breakouts lose almost half an R, every time."},
    {"type": "stat", "label": "Failed breakouts, 20 trades", "value": -713, "prefix": "$", "color": "coral", "sub": "20% win rate",
     "say": "Twenty trades, seven hundred and thirteen dollars gone."},
    {"type": "shot", "img": "by_setup", "title": "Every setup, with its sample size.", "ring": "setup_worst",
     "say": "The journal ranks every setup for you, so you know what's real and what's noise."},
    ONECLICK, CTA("Know your edge, setup by setup.")],
    "post": post("Your favourite trading setup might be losing you money", "Rank your setups by average R, not by feel. In this example journal, one setup made +0.89R per trade and another lost -0.41R.",
                 ["#tradingstrategy", "#edge"], "Find your best trading setup by average R")})

V.append({"id": "v003_emotions", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Trading psychology", "text": "Six frustrated trades. $674 gone.",
     "say": "Six frustrated trades. Six hundred and seventy four dollars, gone."},
    {"type": "rows", "title": "Net P&L by emotion", "head": ["Emotion", "Trades", "Net P&L"],
     "rows": [{"cells": ["Calm", "55", "+$1,994"], "good": True, "hl": True}, {"cells": ["Confident", "18", "+$39"]},
              {"cells": ["Anxious", "5", "−$114"]}, {"cells": ["Frustrated", "6", "−$674"], "hl": True}],
     "say": "In this example journal, calm trades made almost two thousand dollars. Six frustrated ones lost six hundred and seventy four."},
    {"type": "stat", "label": "Win rate when frustrated", "value": 0, "suffix": "%", "color": "coral", "sub": "0 wins out of 6",
     "say": "Zero wins out of six. Your mood leaves a trace in your numbers."},
    ONECLICK, CTA("See what your emotions cost you.")],
    "post": post("Your emotions are in your trading numbers", "Tag each trade with how you felt. In this example journal, 55 calm trades made +$1,994 and 6 frustrated trades lost -$674.",
                 ["#mindset", "#tradingmindset"], "How emotions affect trading results")})

V.append({"id": "v004_profit_factor", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Trading maths", "text": "A 51% win rate tells you almost nothing.",
     "say": "A fifty one percent win rate tells you almost nothing."},
    {"type": "stat", "label": "Profit factor", "value": 1.43, "decimals": 2, "color": "mint", "sub": "gross profit ÷ gross loss",
     "say": "Profit factor does. It's everything you won, divided by everything you lost."},
    {"type": "rows", "title": "How to read it", "head": ["Profit factor", "", "Meaning"],
     "rows": [{"cells": ["Below 1", "", "Losing"], "hl": True}, {"cells": ["1 to 1.5", "", "Thin edge"]}, {"cells": ["Above 1.5", "", "Solid edge"], "good": True, "hl": True}],
     "say": "Below one, you're losing money. Above one and a half, you have a solid edge."},
    {"type": "shot", "img": "kpis", "title": "Calculated for you, for any period.", "ring": "kpi_pf",
     "say": "Your journal calculates it for any period, with win rate, R and drawdown."},
    CTA("Your real numbers, not your feelings.")],
    "post": post("Profit factor explained in 30 seconds", "Win rate alone tells you almost nothing. Profit factor = gross profit / gross loss. Below 1 you're losing, above 1.5 you have a solid edge.",
                 ["#tradingeducation", "#profitfactor"], "Profit factor explained for traders")})

V.append({"id": "v005_r_multiple", "scenes": [
    {"type": "hook", "kicker": "Trading maths", "text": "Stop counting dollars. Count R.",
     "say": "Stop counting dollars. Count R."},
    {"type": "rows", "title": "One trade, in R", "head": ["", "", "Value"],
     "rows": [{"cells": ["Risk (entry to stop)", "", "$40"]}, {"cells": ["Result", "", "+$80"], "good": True}, {"cells": ["R multiple", "", "+2.00R"], "good": True, "hl": True}],
     "say": "R is what a trade made, divided by what you risked. Risk forty, make eighty: that's plus two R."},
    {"type": "hook", "text": "R lets you compare every trade, whatever the size.",
     "say": "R lets you compare every trade, whatever the size, the market or the account."},
    {"type": "shot", "img": "add_trade", "title": "Your journal does the maths.",
     "chips": [{"html": "Risk <b>$40</b>"}, {"html": "R <b>+2.00R</b>"}],
     "say": "Type entry, stop and exit. The R appears as you type."},
    CTA("Every trade in R, automatically.")],
    "post": post("R multiple explained: the number pro traders track", "R = what a trade made / what you risked. Risk $40, make $80: +2R. It lets you compare every trade, whatever the size.",
                 ["#tradingeducation", "#riskmanagement"], "R multiple explained for day traders")})

V.append({"id": "v006_time_of_day", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Your edge", "text": "When do you actually make money?",
     "say": "When do you actually make money? Most traders guess."},
    {"type": "rows", "title": "Net P&L by time of day", "head": ["Hours", "Trades", "Net P&L"],
     "rows": [{"cells": ["09–10 h", "26", "+$471"]}, {"cells": ["10–12 h", "39", "+$315"]}, {"cells": ["12–14 h", "11", "+$145"]},
              {"cells": ["14–17 h", "13", "+$548"], "good": True, "hl": True}],
     "say": "In this example journal, the afternoon made the most with the fewest trades. Thirteen trades, five hundred and forty eight dollars."},
    {"type": "shot", "img": "by_hour", "title": "By hour and by weekday.", "ring": "hour_best",
     "say": "Your journal splits every result by hour and by weekday."},
    ONECLICK, CTA("Trade your best hours.")],
    "post": post("When do you actually make money trading?", "Split your results by hour. In this example journal, 13 afternoon trades made more than 39 trades in the late morning.",
                 ["#daytrader", "#tradingtips"], "Best time of day to trade? Check your journal")})

V.append({"id": "v007_drawdown", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Risk", "text": "The number that decides if you survive.",
     "say": "There's one number that decides if you survive as a trader."},
    {"type": "stat", "label": "Max drawdown", "value": -612, "prefix": "$", "color": "coral", "sub": "on a $10,000 account · 6.1%",
     "say": "Max drawdown: the biggest drop from a peak. In this example, six hundred and twelve dollars."},
    {"type": "shot", "img": "equity", "title": "Your equity curve, trade by trade.",
     "say": "Your equity curve shows every peak and every dip."},
    {"type": "stat", "label": "Longest losing streak", "value": 4, "suffix": " trades", "color": "gold",
     "say": "Know your longest losing streak before it surprises you."},
    CTA("Know your risk before the market tells you.")],
    "post": post("Max drawdown: the number that decides if you survive", "Max drawdown is the biggest drop from a peak in your account. Track it, together with your longest losing streak.",
                 ["#riskmanagement", "#drawdown"], "Max drawdown explained for traders")})

V.append({"id": "v008_ai_review", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "AI for traders", "text": "Your AI can review your trading week. In one click.",
     "say": "Your AI can review your trading week. In one click."},
    {"type": "shot", "img": "oneclick", "title": "Pick a period. Pick your AI.", "ring": "btn_claude",
     "chips": [{"text": "Claude", "color": "mint"}, {"text": "ChatGPT", "color": "blue"}, {"text": "Gemini", "color": "gold"}],
     "say": "Pick a period and your AI. It opens with your numbers already in the chat."},
    {"type": "chat", "me": "Weekly review, last 14 days.",
     "ai": ["Net P&amp;L <span class='m'>+385.28</span> · win rate <b>67%</b> · profit factor <b>3.80</b>",
            "Calm trades: <span class='m'>+395</span>. One FOMO entry: <span class='c'>−2.48</span>. It's the habit, not the amount."],
     "say": "No uploads, no prompts. It uses the same numbers you see in the journal."},
    {"type": "hook", "text": "No signals. No predictions. Just what you actually did.",
     "say": "No signals, no predictions. Just an honest look at what you actually did."},
    CTA("Uses the AI you already have.")],
    "post": post("Let your AI review your trading week in one click", "Pick a period, click Claude, ChatGPT or Gemini, and your AI reviews your week from your real numbers. No uploads, no prompts.",
                 ["#ai", "#chatgpt", "#claude"], "AI trading journal review in one click")})

V.append({"id": "v009_calendar", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "P&L calendar", "text": "Your month, one glance.",
     "say": "Your trading month, in one glance."},
    {"type": "shot", "img": "calendar", "title": "Green days. Red days. Weekly totals.",
     "say": "Green days, red days, and the total for every week."},
    {"type": "stat", "label": "October, 18 trades", "value": 598, "prefix": "+$", "color": "mint",
     "say": "In this example, October closed up five hundred and ninety eight dollars."},
    CTA("See your month at a glance.")],
    "post": post("A P&L calendar for your trading month", "Green days, red days and weekly totals, built from your trades automatically.",
                 ["#pnl", "#tradingcalendar"], "Trading P&L calendar")})

V.append({"id": "v010_position_size", "scenes": [
    {"type": "hook", "kicker": "Risk management", "text": "Position size in three numbers.",
     "say": "Position size, in three numbers."},
    {"type": "rows", "title": "Example: MES futures", "head": ["", "", "Value"],
     "rows": [{"cells": ["Risk per trade", "", "$100"]}, {"cells": ["Stop distance", "", "4 points"]}, {"cells": ["Point value", "", "$5"]}],
     "say": "How much you'll risk, how far your stop is, and what one point is worth."},
    {"type": "stat", "label": "Contracts = 100 ÷ (4 × 5)", "value": 5, "suffix": " contracts", "color": "mint",
     "say": "Risk divided by stop times point value. Here, five contracts."},
    {"type": "hook", "text": "Same risk on every trade. That's what makes R honest.",
     "say": "Same risk on every trade. That's what makes your results comparable."},
    CTA("Point values for futures, stocks, forex and crypto.")],
    "post": post("Position size in 3 numbers (futures example)", "Contracts = risk / (stop distance x point value). $100 risk, 4-point stop on MES ($5/point) = 5 contracts.",
                 ["#positionsizing", "#riskmanagement", "#futures"], "How to calculate position size for futures")})

V.append({"id": "v011_weekday", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Your edge", "text": "Is there a day you should just not trade?",
     "say": "Is there a day of the week you should just not trade?"},
    {"type": "rows", "title": "Net P&L by weekday", "head": ["Day", "Trades", "Net P&L"],
     "rows": [{"cells": ["Monday", "22", "+$841"], "good": True, "hl": True}, {"cells": ["Tuesday", "16", "+$320"]}, {"cells": ["Wednesday", "19", "+$267"]},
              {"cells": ["Thursday", "17", "−$30"], "hl": True}, {"cells": ["Friday", "15", "+$80"]}],
     "say": "In this example journal, Mondays made the most. Thursdays lost money over seventeen trades."},
    {"type": "hook", "text": "Small samples lie. Your journal shows the count.",
     "say": "Careful with small samples. Your journal always shows how many trades are behind each number."},
    ONECLICK, CTA()],
    "post": post("Is there a day you should not trade?", "Split your results by weekday, and always check the sample size. In this example journal, Thursdays lost money over 17 trades.",
                 ["#daytrader", "#tradingtips"], "Best day of the week to trade? Check your data")})

V.append({"id": "v012_privacy", "scenes": [
    {"type": "hook", "kicker": "Trading journal", "text": "Your trades are nobody's business.",
     "say": "Your trades are nobody's business."},
    {"type": "rows", "title": "Trading Journal AI", "head": ["", "", ""],
     "rows": [{"cells": ["Stored on your computer", "", "✓"], "good": True}, {"cells": ["No account, no cloud", "", "✓"], "good": True},
              {"cells": ["Daily backups", "", "✓"], "good": True}, {"cells": ["Export to CSV", "", "✓"], "good": True}],
     "say": "Your journal lives on your computer. No account, no cloud, daily backups, and you can export everything."},
    {"type": "shot", "img": "kpis", "title": "A desktop app for Windows and Mac.",
     "say": "A fast desktop app for Windows and Mac."},
    CTA("Private by design.")],
    "post": post("A private trading journal: your data stays on your computer", "No account, no cloud. Your trading journal lives on your computer, with daily backups and CSV export.",
                 ["#privacy", "#tradingtools"], "Private trading journal app for Windows and Mac")})

V.append({"id": "v013_long_short", "tag": TAG, "scenes": [
    {"type": "hook", "kicker": "Your edge", "text": "Long or short: where's your edge?",
     "say": "Long or short. Where's your edge, really?"},
    {"type": "rows", "title": "By side", "head": ["Side", "Trades", "Net P&L"],
     "rows": [{"cells": ["Long", "58", "+$1,119"]}, {"cells": ["Short", "31", "+$360"]}],
     "say": "In this example journal, longs made more in total, but there were almost twice as many of them."},
    {"type": "hook", "text": "Compare per trade, not just in total.",
     "say": "Compare per trade, not just in total. That's what average R is for."},
    ONECLICK, CTA()],
    "post": post("Long vs short: where is your trading edge?", "Compare long and short trades per trade, not just in total. Average R tells you where your edge really is.",
                 ["#tradingstrategy"], "Long vs short trading edge")})

V.append({"id": "v014_habit", "scenes": [
    {"type": "hook", "kicker": "Trading habit", "text": "A trading journal you'll actually keep.",
     "say": "A trading journal you'll actually keep."},
    {"type": "shot", "img": "add_trade", "title": "Ten fields. Thirty seconds.",
     "chips": [{"html": "<b>Date</b>"}, {"html": "<b>Entry</b>"}, {"html": "<b>Stop</b>"}, {"html": "<b>Exit</b>"}],
     "say": "Ten fields per trade. About thirty seconds after you close it."},
    {"type": "shot", "img": "kpis", "title": "Everything else fills in.",
     "say": "Dashboard, calendar, setups and mistakes fill in by themselves."},
    ONECLICK, CTA()],
    "post": post("A trading journal you'll actually keep", "Ten fields per trade, about 30 seconds. Dashboard, calendar, setups and mistakes fill in by themselves.",
                 ["#tradinghabits"], "Simple trading journal app")})


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for v in V:
        v.setdefault("voice", "andrew_up")
        (OUT / f"{v['id']}.json").write_text(json.dumps(v, indent=1, ensure_ascii=False))
    print(len(V), "videos written")
