---
name: onchain-analysis
description: Analyze blockchain/on-chain transaction flows for repeated counterparties, high-value transfers, wallet behavior, whale movement, exchange/mixer/bridge patterns, and chain-wide Ethereum scans. Use when the user asks to scan Etherscan, Ethereum, wallets, transactions, crypto flows, repeated from-to payments, $5k+ filters, whale tracking, or suspicious on-chain patterns.
---

# Onchain Analysis

## Operating stance

Work like Froggo: concise, sharp, practical, and suspicious by default. For Harry in Telegram, keep Dutch responses caveman-short unless he asks for detail.

## First rule: choose the right data lane

Do not claim Etherscan can cheaply “scan all of Ethereum.” Etherscan API is mainly address/contract oriented and rate-limited.

Use this lane selector:

1. **Single wallet/address** → Etherscan API or RPC address history/indexer.
2. **Recent live sample, no API key** → public Ethereum RPC block scan. Native ETH only unless decoding logs.
3. **Chain-wide repeated-flow analysis** → BigQuery public Ethereum dataset, Dune, Flipside, or owned indexer.
4. **Deep forensic labeling** → add labels from Etherscan, Arkham/Nansen-style sources, CEX hot-wallet lists, bridge/mixer lists.

## Default repeated-flow workflow

When the user wants wallets that repeatedly send high amounts to the same destination:

1. Set default threshold to **$5,000+ per transfer** if not specified.
2. Define repeat threshold:
   - short live sample: `min_repeat=2`
   - 7 to 30 days: `min_repeat=5`
   - 90 to 365 days: `min_repeat=10+`
3. Group by `(from_address, to_address, asset)`.
4. Return:
   - from → to
   - tx count
   - total USD
   - average USD
   - first/last seen
   - span minutes/days
   - pattern label: burst / dense recurring / same-day / weekly / long-window
   - sample tx hashes
5. Flag likely interpretations but avoid overclaiming:
   - CEX deposit/hot-wallet flow
   - treasury/vendor/salary-like recurring flow
   - MEV/bot flow
   - bridge/mixer-like flow
   - possible laundering burst

## Use bundled resources

- `scripts/eth_flow_scanner.py`: deterministic scanner with two modes:
  - `rpc`: recent public-RPC native ETH scan, no key
  - `sql`: generate BigQuery SQL for chain-wide ETH + USDC/USDT/DAI/WETH repeated-flow analysis
- `references/ethereum-flow-scanning.md`: notes from the first working implementation, endpoints, limits, and query shape.

## Commands

Live sample, cheap and immediate:

```bash
python3 scripts/eth_flow_scanner.py rpc \
  --blocks 1000 \
  --threshold-usd 5000 \
  --min-repeat 2 \
  --limit 50 \
  --out-json reports/eth_patterns_latest.json \
  --out-csv reports/eth_patterns_latest.csv
```

Generate full-chain BigQuery SQL:

```bash
python3 scripts/eth_flow_scanner.py sql \
  --days 30 \
  --threshold-usd 5000 \
  --min-repeat 5 \
  --limit 1000 > reports/froggo_eth_patterns_bigquery.sql
```

## Pitfalls

- Public RPC scans are live samples, not full-chain history.
- Native RPC transaction scans miss ERC20 transfers unless logs are decoded.
- ETH/USD threshold depends on price source; record the price used.
- Public RPC endpoints may 403/503. Try alternate endpoints before giving up.
- BigQuery scans can cost money; confirm window and assets before running huge queries.
- Do not accuse addresses of crime from pattern alone. Say “resembles” or “possible,” then support with labels and downstream flows.
