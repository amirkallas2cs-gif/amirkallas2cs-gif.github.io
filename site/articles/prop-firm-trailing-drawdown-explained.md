---
{"slug": "prop-firm-trailing-drawdown-explained", "date": "2026-10-27", "minutes": 7,
 "title": "Prop firm trailing drawdown explained: end-of-day, intraday and the lock",
 "seo_title": "Prop firm trailing drawdown explained (EOD vs intraday)",
 "description": "How prop firm loss limits really move: end-of-day vs intraday trailing drawdown, when the limit locks, what changes after a payout, and how consistency rules change your target.",
 "faq": [
  ["What is the difference between end-of-day and intraday trailing drawdown?", "An end-of-day limit moves up only with your closing balance. An intraday limit follows the highest balance you reach during the session, open profit included, so a winning trade you give back can still raise it."],
  ["When does a trailing drawdown stop trailing?", "It depends on the firm and the account: at your starting balance (Topstep Combine), at starting balance plus $100 (many funded accounts), at the profit target balance (some evaluations), or never. Check your firm's help center for your exact account."],
  ["Can I lose the account in the middle of the day with an end-of-day drawdown?", "Yes. The level is recalculated at the close, but most firms enforce it in real time, open P&L included. If your balance touches the limit during the session, the account is breached."],
  ["How does a consistency rule work?", "It caps how much of your profit can come from your best day. At Topstep the best day should stay within 55% of the target, otherwise the target rises to best day ÷ 0.55. At Apex, for payouts, no day can be 50% or more of the profit since the last payout."]
 ]}
---
Most prop accounts aren't lost to one terrible trade. They're lost to a loss limit that moved while the trader wasn't looking. Here is how the main kinds of limits actually move, with real numbers from the firms' own help centers.

## Static vs trailing

A **static** loss limit never moves: on a $50,000 account with a $2,000 limit you're out at $48,000, whatever happens. A **trailing** limit follows your account up, keeping the same distance from your best balance, and never comes back down. The good news is that most trailing limits stop trailing at some point: that's the **lock**.

## End-of-day (EOD) trailing

The limit is recalculated once a day on your **closing balance**. Apex's own 50K example (drawdown $2,000):

| Day | Closing balance | Limit for the next day |
|---|---|---|
| 1 | $50,800 | $48,800 |
| 2 | $51,600 | $49,600 |
| 3 | $50,900 | $49,600 (unchanged) |
| 4 | $52,000 | $50,000 |

Two details catch people out. First, the level is set at the close but **enforced in real time, open P&L included**: touch it during the session and the account is gone, even if price comes back. Second, a red day doesn't lower the limit, so your room shrinks after a loss.

## Intraday trailing

An intraday limit follows the **highest balance you reach during the session, including open profit**. In Apex's example a 50K account peaks at $50,900 while a trade is open: the limit jumps to $48,900, and stays there even if the trade closes at $50,200. A winner you give back costs you room twice. This is why intraday accounts feel tighter than the same dollar amount on an EOD account.

## When the limit locks

| Where it stops | Example |
|---|---|
| At the starting balance | Topstep Combine 50K: once you close above $52,000, the limit stays at $50,000 |
| At starting balance + $100 | Apex, Lucid and Tradeify funded accounts: on a 50K, the limit stops at $50,100 |
| At the profit target balance | Apex evaluations on Rithmic: stops at $53,000 on a 50K |
| Never | Apex evaluations on Tradovate keep trailing |

Know which one applies to **your** account and platform. After the lock, your room grows with every profitable day instead of staying fixed.

## What changes after a payout

Some firms move the limit when you withdraw. At Topstep, after the first Express Funded payout the limit goes to $0 for good. At Lucid, requesting a payout locks it at start + $100. At MyFundedFutures Pro, it becomes static at start + $100. A payout is not just money out: plan the room you'll have left.

## Consistency rules change the target

Many firms cap how much of your profit can come from one day:

- **Topstep Combine:** the best day should stay within 55% of the target. Make $1,800 in one day on a 50K and the $3,000 target becomes about $3,273.
- **Apex payouts:** no single day can be 50% or more of the profit since your last payout. A $1,500 best day means you need more than $3,000 of net profit before you can request.
- **MyFundedFutures evaluations:** 50% (30% on Rapid EOD), so on a $3,000 target the best day can be $1,500.

The practical question every morning is: **how much can I make today without breaking the rule?** It's simple arithmetic, but easy to get wrong under pressure.

{{prop}}

## A simple daily routine

- After the close, write down the **new limit** and your **room before breach**, not just your P&L.
- On intraday accounts, note the **highest balance of the day**: that's what moved your limit.
- Size the next day so that **two bad days in a row** still leave the account alive.
- Before a big day, check your **consistency cap**.
- Rules change often. Your firm's dashboard and help center are always the final word.
