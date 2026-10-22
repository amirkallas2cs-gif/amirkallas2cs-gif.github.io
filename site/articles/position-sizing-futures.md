---
{"slug": "position-sizing-futures", "date": "2026-10-19", "minutes": 5,
 "title": "Position sizing for futures: MES, ES, MNQ and NQ with examples",
 "seo_title": "Position sizing for futures (MES, ES, MNQ, NQ) with examples",
 "description": "How to size futures positions from your risk: point values for MES, ES, MNQ, NQ and MGC, the formula, worked examples and the mistakes to avoid.",
 "faq": [
  ["How much is one point on MES?", "One point on the Micro E-mini S&amp;P 500 (MES) is worth $5 per contract. On ES it's $50, on MNQ $2, on NQ $20."],
  ["Why trade micros instead of minis?", "Micros are a tenth of the size, so you can size much more precisely. With a small account, the minis often make it impossible to keep risk at 1% per trade."],
  ["Should I include fees in the risk?", "For precision, yes: add the round-trip commission per contract to the risk per contract before dividing."]
 ]}
---
In futures, the same 4-point stop can cost $8 or $200 depending on the contract. Position sizing turns "how many contracts?" into simple arithmetic.

## Point values

| Contract | One point is worth | One tick |
|---|---|---|
| MES (Micro E-mini S&P 500) | $5 | 0.25 = $1.25 |
| ES (E-mini S&P 500) | $50 | 0.25 = $12.50 |
| MNQ (Micro E-mini Nasdaq-100) | $2 | 0.25 = $0.50 |
| NQ (E-mini Nasdaq-100) | $20 | 0.25 = $5 |
| MGC (Micro Gold) | $10 | 0.10 = $1 |

Always confirm contract specifications with your broker or the exchange.

## The formula

<div class="formula">Contracts = money at risk ÷ (stop distance in points × point value)</div>

Round **down**, so the stop-out never costs more than planned.

## Worked examples

**$10,000 account, 1% risk ($100), MES, 4-point stop:**
100 ÷ (4 × $5) = **5 contracts**. A stop-out costs $100.

**Same trade on ES:**
100 ÷ (4 × $50) = 0.5 → **0 contracts**. The trade is too big for the risk; use MES or a tighter stop.

**$25,000 account, 0.5% risk ($125), NQ vs MNQ, 10-point stop:**
NQ: 125 ÷ (10 × $20) = 0.6 → 0 contracts. MNQ: 125 ÷ (10 × $2) = 6.25 → **6 contracts**, real risk $120.

Run your own numbers in the free [position size calculator](/tools/position-size-calculator/).

{{app}}

## Mistakes to avoid

- **Sizing from conviction.** "This one looks great" is how one trade wipes out a week.
- **Fixed size, variable stop.** Two contracts with a 3-point stop and two contracts with a 12-point stop are very different risks.
- **Forgetting fees on micros.** On small targets, commissions are a real share of the result.
- **Not recording the stop.** Without it, your journal can't calculate your R; see [R multiple explained](/learn/r-multiple-explained/).
