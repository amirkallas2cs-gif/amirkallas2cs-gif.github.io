---
{"slug": "r-multiple-explained", "date": "2026-10-22", "minutes": 6,
 "title": "R multiple explained: the one number every trader should track",
 "seo_title": "R multiple explained (with examples and formula)",
 "description": "What an R multiple is, how to calculate it for longs and shorts, why it beats tracking dollars, and how average R tells you if you have an edge.",
 "faq": [
  ["What does 1R mean in trading?", "1R is the amount you risk on a trade: the distance from entry to stop, times your size and point value. A trade that makes twice that amount is +2R; a full stop-out is −1R."],
  ["What is a good average R per trade?", "Any average above zero over a large sample means a positive edge. Many traders consider +0.2R per trade or more a meaningful edge, but the sample size matters as much as the number."],
  ["How do I calculate R for a short trade?", "Risk is stop minus entry. R = (entry − exit) × size × point value ÷ risk. Use the <a href=\"/tools/r-multiple-calculator/\">R multiple calculator</a> to check."]
 ]}
---
If you only track profit in dollars, every trade looks different. A $300 win on a big position and a $60 win on a small one tell you nothing about the quality of the decision. **R multiples** fix that by measuring every trade against the one thing you control before you enter: your risk.

## What is an R multiple?

**R** is the amount of money you're risking on a trade: the distance from your entry to your stop, multiplied by your position size and the instrument's point value. The **R multiple** of a trade is what it made, divided by that risk.

<div class="formula">R multiple = P&amp;L ÷ money at risk</div>

- Risk $40 and make $80: **+2R**
- Risk $40 and lose $40 at your stop: **−1R**
- Risk $40 and close at breakeven, paying $2.48 in fees: **−0.06R**

That's it. Every trade, whatever its size, market or account, becomes comparable.

## How to calculate R, step by step

Take a long trade on the Micro E-mini S&P (MES), where one point is worth $5:

| | Value |
|---|---|
| Entry | 5,000 |
| Stop | 4,996 |
| Exit | 5,008 |
| Size | 2 contracts |

1. **Risk per contract** = (5,000 − 4,996) × $5 = $20
2. **Money at risk** = $20 × 2 contracts = $40
3. **P&L** = (5,008 − 5,000) × $5 × 2 = $80
4. **R multiple** = $80 ÷ $40 = **+2R**

For a **short**, flip the direction: risk is stop minus entry, and profit is entry minus exit. You can check any trade with the free [R multiple calculator](/tools/r-multiple-calculator/).

## Why R beats dollars

**It separates the decision from the size.** Doubling your position doubles your dollars, but it doesn't make the trade a better idea. In R, a good trade is a good trade.

**It makes your results comparable over time.** As your account grows, your dollar risk grows too. Your R statistics stay on the same scale, so you can compare this month with last year.

**It shows your edge directly.** Your **average R per trade** is your expectancy in units of risk. If it's above zero over a large sample, your method makes money on average. If it's +0.3R and you risk $100 per trade, you can expect about $30 per trade over time, with a lot of noise along the way.

**It exposes bad habits.** Losses bigger than −1R mean you moved your stop, skipped it, or got slippage. Wins that are always below +1R suggest you cut winners too early.

## Average R, by setup

R becomes really useful when you group it. Here's a sample journal of 89 trades, grouped by setup:

| Setup | Trades | Win rate | Avg R |
|---|---|---|---|
| Trend pullback | 16 | 69% | +0.89R |
| Opening range breakout | 29 | 66% | +0.63R |
| VWAP reclaim | 24 | 46% | +0.11R |
| Failed breakout | 20 | 20% | −0.41R |

The trader's overall average is +0.30R per trade, which looks fine. But one setup loses almost half a risk unit every time it's taken. Dropping it, or fixing it, would change the whole account. You'd never see this by looking at the dollar total.

{{app}}

## Common mistakes with R

**Not having a stop.** Without a stop there's no defined risk, so there's no R. If you trade without hard stops, decide on a "mental stop" before entry and write it down.

**Changing the stop after entry.** R is measured against the *original* stop. If you widen it, the loss in R gets bigger than −1R, and your journal should show that.

**Ignoring fees.** Commissions and fees are part of the result. A scratch trade with fees is a small negative R, not zero.

**Judging on tiny samples.** Ten trades with a +1R average can be pure luck. Look at 30 trades as an early signal and 100 or more before drawing conclusions.

## Track R automatically

You can calculate R in a spreadsheet, but it's easy to make mistakes and hard to keep up. A trading journal that calculates risk, R and P&L as you type, and then groups them by setup, weekday, hour and mistake, does the boring part for you so you can focus on the decisions.
