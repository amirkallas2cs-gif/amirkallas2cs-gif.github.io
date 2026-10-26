---
{"slug": "trading-expectancy-explained", "date": "2026-10-26", "minutes": 7,
 "title": "Trading expectancy explained: is your strategy worth trading?",
 "seo_title": "Trading expectancy formula explained (with examples in R)",
 "description": "What trading expectancy is, the formula in dollars and in R, worked examples, why win rate alone misleads you, and how many trades you need before trusting the number.",
 "faq": [
  ["What is a good expectancy in trading?", "Any expectancy above zero, measured over a large sample and after fees, means the method made money on average. Many traders treat +0.2R per trade or more as a meaningful edge, but the number only means something once you have enough trades behind it."],
  ["Is expectancy the same as average R?", "Yes. If every trade is measured in R (P&amp;L divided by the money at risk), the average R per trade is your expectancy in units of risk. See <a href=\"/learn/r-multiple-explained/\">R multiple explained</a>."],
  ["Can a strategy with a low win rate have positive expectancy?", "Yes. A 40% win rate with winners averaging +2R and losers averaging −1R gives +0.2R per trade. What matters is the win rate together with the size of wins and losses."],
  ["How many trades do I need to measure expectancy?", "Treat 30 trades as an early signal and 100 or more as a more reliable estimate. The more your results vary from trade to trade, the more trades you need."]
 ]}
---
Every trader eventually asks the same question: *does my strategy actually make money, or have I just been lucky?* Win rate can't answer it. Total P&L can't either, because a few big days can hide a losing method. The number that answers it is **expectancy**: what you make, on average, every time you take a trade.

## What is trading expectancy?

Expectancy is the average result per trade over many trades. It combines three things: how often you win, how much you win when you win, and how much you lose when you lose.

<div class="formula">Expectancy = (win rate × average win) − (loss rate × average loss)</div>

If the result is above zero, the method made money on average over that sample. If it's below zero, it lost money, no matter how good the win rate looks.

## Expectancy in R: the version that travels

You can calculate expectancy in dollars, but dollars change with your position size and account. Measuring it in **R**, where 1R is the money you risked on a trade, makes it comparable across months, markets and sizes.

<div class="formula">Expectancy (R) = (win rate × average winning R) − (loss rate × average losing R)</div>

Even simpler: if every trade in your journal already has an R multiple, your expectancy is just the **average R per trade**. If you're new to R, start with [R multiple explained](/learn/r-multiple-explained/) or check single trades with the [R multiple calculator](/tools/r-multiple-calculator/).

## Worked examples

**A low win rate that works.**

| | Value |
|---|---|
| Win rate | 40% |
| Average win | +2.0R |
| Average loss | −1.0R |

Expectancy = (0.40 × 2.0) − (0.60 × 1.0) = 0.80 − 0.60 = **+0.20R per trade**. You lose more often than you win, and you still come out ahead on average.

**A high win rate that goes nowhere.**

| | Value |
|---|---|
| Win rate | 60% |
| Average win | +0.8R |
| Average loss | −1.2R |

Expectancy = (0.60 × 0.8) − (0.40 × 1.2) = 0.48 − 0.48 = **0R per trade**. Six wins out of ten feels great, but after fees this method slowly loses money. Small winners and losses bigger than the planned stop are the usual cause.

**A real sample journal.** In a sample journal of 89 trades, the win rate is 51% and the average is **+0.30R per trade**, with a profit factor of 1.43. A win rate of 51% sounds like a coin flip. The edge comes from winners that are larger than losers, which only shows up when you look at R.

## Turning expectancy into a rough dollar figure

Once you know your expectancy in R, multiply it by what you usually risk:

<div class="formula">Expected P&amp;L per trade ≈ expectancy (R) × risk per trade</div>

At +0.30R and $100 of risk per trade, that's about $30 per trade **on average, over a large number of trades**. Any single trade will be far from that, and so will most single weeks. Expectancy describes the average, not the path. The path is where [drawdowns](/learn/max-drawdown-explained/) live, which is why risk per trade still matters.

{{app}}

## Why win rate alone misleads you

Win rate is the easiest number to feel, so traders optimise for it. The common ways to push it up all hurt expectancy:

- **Taking profits early** raises the win rate and shrinks the average win.
- **Moving or removing stops** turns some losers into small winners, and a few into very large losses.
- **Adding to losers** "fixes" trades that should have been −1R, until one doesn't come back.

Expectancy catches all three, because it weighs how often you win against how much each win and loss is worth.

## How many trades do you need?

Expectancy from ten trades is mostly noise. A rough guide:

- **Under 30 trades:** don't draw conclusions, keep logging.
- **30 to 100 trades:** an early signal. Look for problems, like one setup with a clearly negative average.
- **100+ trades:** a more reliable estimate, especially if you keep the same rules the whole time.

The more your results swing from trade to trade, the more trades you need before the average settles. If you change your rules halfway through, start counting again for the new version.

## Break it down by setup, time and mistake

One expectancy number for your whole account hides a lot. Split it:

- **By setup:** a single setup with a negative average can drag down an otherwise good method.
- **By hour and weekday:** some traders have a clear edge in one session and none in another.
- **By mistake or rule break:** trades where you broke your plan usually have a much lower average than trades where you followed it.

This is where a journal earns its keep. Each group needs enough trades to mean something, but even a rough split often shows exactly where your edge comes from and where it leaks.

## Track expectancy without the spreadsheet work

You can calculate all of this in a spreadsheet if you log entry, stop, exit, size and fees for every trade. A journal that calculates R automatically and groups your average R by setup, weekday, hour, emotion and mistake turns expectancy from a one-off calculation into something you check every week.

*Educational content only, not financial advice. Past results in a journal don't guarantee future results.*
