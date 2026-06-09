# Ethereum Flow Scanning Notes

## Key lesson

Etherscan is not the right primitive for scanning all of Ethereum for repeated transaction patterns. It is useful for address-level lookups, contracts, labels, and verification, but broad from-to pair mining needs indexed datasets.

## Lanes

### Public RPC live sample

Use for immediate proof or fresh blocks. Pull recent blocks with `eth_getBlockByNumber(..., true)` and filter transactions where native ETH `value` exceeds the USD threshold.

Working public RPC endpoints found:

- `https://ethereum-rpc.publicnode.com`
- `https://rpc.flashbots.net`
- `https://eth-mainnet.public.blastapi.io`

Endpoints that may fail without auth or block clients:

- `https://ethereum.publicnode.com` → 403 observed
- `https://rpc.ankr.com/eth` → API key required observed
- `https://cloudflare-eth.com` → 403 observed
- `https://eth.llamarpc.com` → 503 observed

### BigQuery full-chain

Use Google public Ethereum dataset for real chain-wide scans:

- `bigquery-public-data.crypto_ethereum.transactions`
- `bigquery-public-data.crypto_ethereum.token_transfers`
- optionally `traces` for internal ETH flows
- optionally `accounts`/labels from external sources for contract/EOA classification

Core query shape:

1. Build ETH flows from `transactions`.
2. Build ERC20 flows from `token_transfers` for USDC, USDT, DAI, WETH.
3. Normalize token values by decimals.
4. Approximate USD:
   - stablecoins = 1 USD
   - ETH/WETH = current or fixed ETH/USD used for the run
5. Filter `amount_usd >= threshold_usd`.
6. Group by `from_address`, `to_address`, `asset`.
7. Keep groups with `COUNT(*) >= min_repeat`.
8. Order by `tx_count DESC, total_usd DESC`.

## First verified local run

A local RPC run over recent blocks returned repeated high-value pairs successfully.

Example output fields:

- `from`, `to`
- `tx_count`
- `total_eth`, `total_usd`, `avg_usd`
- `first_utc`, `last_utc`, `span_minutes`
- `pattern`
- `sample_txs`

Observed pattern labels:

- `burst`: repeated transfers inside 15 minutes
- `dense recurring`: repeated transfers inside 3 hours
- `same-day recurring`: repeated transfers inside 24 hours
- `long-window recurring`: wider window

## Reporting style for Harry

Be direct:

- Say scope first: chain, blocks/days, assets, threshold.
- Then give counts: high-value pairs, repeated pairs.
- Then top 5-10 pairs.
- End with next hard step, not vague caveats.
