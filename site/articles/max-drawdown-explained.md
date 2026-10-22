---
{"slug": "max-drawdown-explained", "date": "2026-10-20", "minutes": 5,
 "title": "Max drawdown explained: the number that decides if you survive",
 "seo_title": "Max drawdown explained: how to calculate and limit it",
 "description": "What maximum drawdown is, how to calculate it from your equity curve, why recovery is harder than the loss, and how to keep drawdowns survivable.",
 "faq": [
  ["How is max drawdown calculated?", "Track your account equity after every trade, and its highest value so far (the peak). Drawdown is equity minus peak. Max drawdown is the most negative value of that difference."],
  ["What is an acceptable max drawdown?", "It depends on your goals and risk tolerance. What matters is that you decide a limit in advance and size your positions so a normal losing streak stays well inside it."],
  ["Why is recovering from a drawdown hard?", "Because the gain needed is bigger than the loss: after −20% you need +25% to get back, after −50% you need +100%."]
 ]}
---
Profit tells you how much you can make. **Max drawdown** tells you how much pain you have to sit through to make it, and whether your account survives the bad stretch that always comes.

## What is drawdown?

After every trade, your account has a value (equity). The highest value it has reached so far is the **peak**. **Drawdown** is how far you are below that peak right now. **Max drawdown** is the deepest drop on record.

<div class="formula">Drawdown = equity − highest equity so far&nbsp;&nbsp;·&nbsp;&nbsp;Max drawdown = the lowest drawdown</div>

In a sample journal that starts at $10,000 and ends at $11,479 after 89 trades, the deepest drop from a peak was **−$611.70**: about 6% of the account. The longest losing streak was 4 trades.

## Recovery is harder than the loss

| Drawdown | Gain needed to recover |
|---|---|
| −10% | +11% |
| −20% | +25% |
| −30% | +43% |
| −50% | +100% |

This asymmetry is why risk management matters more than finding the perfect entry. Small, consistent risk per trade keeps drawdowns in the zone where recovery is realistic.

## How position size controls drawdown

If you risk 1% of your account per trade, a streak of 8 losses costs about 8%. Risk 5% per trade and the same streak costs about a third of the account. Streaks of 6 to 10 losses happen to profitable traders; plan for them. The [position size calculator](/tools/position-size-calculator/) shows exactly how many contracts or shares keep each trade inside your limit.

{{app}}

## Practical rules

- **Decide your maximum acceptable drawdown before you trade**, not during one.
- **Size from risk, not from conviction.** The same percentage on every trade.
- **Know your longest losing streak** and expect a longer one eventually.
- **Have a circuit breaker:** for example, stop for the day after −2R, and cut size in half after a −10% drawdown until you recover.
- **Watch the equity curve, not just the balance.** A rising curve with shallow dips is a healthy one.
