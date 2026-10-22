---
{"slug": "profit-factor-explained", "date": "2026-10-22", "minutes": 6,
 "title": "Profit factor explained: why your win rate isn't enough",
 "seo_title": "Profit factor explained: formula, good values and examples",
 "description": "What profit factor is, how to calculate it, what counts as a good profit factor, and why a high win rate can still lose money.",
 "faq": [
  ["What is a good profit factor for day trading?", "Above 1.0 is profitable before you look at anything else. Between 1.0 and 1.5 is a thin edge; above 1.5 is generally solid; very high values on few trades are usually luck. Always check the number of trades behind it."],
  ["Can profit factor be too high?", "A profit factor of 3 or more over hundreds of trades is rare. On a small sample it usually means a few big winners haven't been balanced by normal losing periods yet."],
  ["Is profit factor the same as risk/reward?", "No. Risk/reward is planned for a single trade. Profit factor is measured on the results of many trades, including the ones that didn't go to plan."]
 ]}
---
A 70% win rate sounds great until you notice that the 30% of losing trades are three times bigger than the winners. **Profit factor** is the simplest number that catches this.

## The formula

<div class="formula">Profit factor = gross profit ÷ gross loss</div>

Add up every winning trade. Add up every losing trade (as a positive number). Divide the first by the second.

- **Below 1.0:** you lose more than you make
- **1.0 to 1.5:** a thin edge, easily erased by fees, slippage or a bad month
- **Above 1.5:** a solid edge, if the sample is large enough

## An example

Take a sample journal of 89 trades:

| | Value |
|---|---|
| Win rate | 51% |
| Average win | $108.89 |
| Average loss | −$77.76 |
| Profit factor | **1.43** |
| Net P&L | +$1,478.64 |

With barely more winners than losers, this trader is profitable because the average win is about 40% bigger than the average loss. The profit factor of 1.43 says: for every dollar lost, $1.43 came back.

## Why win rate alone misleads you

Win rate only counts how often you're right. It ignores **how much** you make when you're right and **how much** you lose when you're wrong.

| Trader | Win rate | Avg win | Avg loss | Profit factor |
|---|---|---|---|---|
| A | 70% | $50 | $150 | 0.78 |
| B | 40% | $200 | $80 | 1.67 |

Trader A wins most of the time and loses money. Trader B loses most of the time and makes money. This is why the breakeven win rate matters:

<div class="formula">Breakeven win rate = average loss ÷ (average win + average loss)</div>

Trader A needs to win 75% of the time just to break even. Trader B needs only 29%. You can test your own numbers with the free [profit factor calculator](/tools/profit-factor-calculator/).

## Profit factor and expectancy

Profit factor tells you the *ratio*. **Expectancy** tells you the *amount* per trade:

<div class="formula">Expectancy = win rate × average win − loss rate × average loss</div>

For the sample journal: 0.51 × $108.89 − 0.49 × $77.76 ≈ $17 per trade. Expressed in R, the same journal averages +0.30R per trade. If you keep your risk constant, the two tell the same story; see [R multiple explained](/learn/r-multiple-explained/).

{{app}}

## How to use profit factor in your journal

**Look at it by setup.** An overall profit factor of 1.43 can hide a setup at 2.5 and another at 0.6. The second one is where the money leaks.

**Look at it by period.** A falling profit factor month after month tells you the market changed or your execution slipped, long before your account balance does.

**Respect the sample size.** Profit factor on 12 trades is a first impression. On 100 trades it starts to mean something.

**Include fees.** Calculate it on net results, after commissions. A strategy at 1.1 before fees can be below 1.0 after them.

## The bottom line

Win rate is how often you're right. Profit factor is whether being right pays. Track both, by setup and by period, and you'll know where your edge really is.
