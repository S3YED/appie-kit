#!/usr/bin/env python3
"""
Froggo Ethereum high-value repeated-flow scanner.

Two lanes:
1) rpc: live sample scan via public Ethereum RPC, no API key, native ETH only.
2) sql: prints BigQuery SQL for true chain-wide analysis over ETH + major ERC20s.

Examples:
  python3 scripts/eth_flow_scanner.py rpc --blocks 1000 --threshold-usd 5000 --min-repeat 2
  python3 scripts/eth_flow_scanner.py sql --days 30 --threshold-usd 5000 --min-repeat 5 > /tmp/eth_patterns.sql
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import sys
import time
import urllib.request
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

DEFAULT_RPC = "https://ethereum-rpc.publicnode.com"
COINGECKO_ETH_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

TOKEN_DECIMALS = {
    "USDC": ("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", 6),
    "USDT": ("0xdac17f958d2ee523a2206206994597c13d831ec7", 6),
    "DAI": ("0x6b175474e89094c44da98b954eedeac495271d0f", 18),
    "WETH": ("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", 18),
}


def http_json(url: str, data: Any = None, timeout: int = 30) -> Any:
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "froggo-eth-flow-scanner/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read())


def get_eth_usd(fallback: Decimal = Decimal("2123.11")) -> Decimal:
    try:
        data = http_json(COINGECKO_ETH_PRICE_URL, timeout=10)
        return Decimal(str(data["ethereum"]["usd"]))
    except Exception:
        return fallback


def rpc_call(rpc_url: str, method: str, params: List[Any], timeout: int = 30) -> Any:
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    data = http_json(rpc_url, payload, timeout=timeout)
    if "error" in data:
        raise RuntimeError(f"RPC error {data['error']}")
    return data["result"]


def rpc_batch(rpc_url: str, calls: List[Tuple[str, List[Any]]], timeout: int = 60) -> List[Any]:
    payload = [
        {"jsonrpc": "2.0", "method": method, "params": params, "id": idx}
        for idx, (method, params) in enumerate(calls)
    ]
    data = http_json(rpc_url, payload, timeout=timeout)
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected RPC batch response: {data}")
    return data


def short_addr(address: str) -> str:
    return f"{address[:8]}...{address[-5:]}"


def classify_pattern(count: int, span_seconds: int) -> str:
    if count <= 1:
        return "single"
    if span_seconds <= 15 * 60:
        return "burst"
    if span_seconds <= 3 * 60 * 60:
        return "dense recurring"
    if span_seconds <= 24 * 60 * 60:
        return "same-day recurring"
    return "long-window recurring"


def scan_rpc(args: argparse.Namespace) -> Dict[str, Any]:
    eth_usd = Decimal(str(args.eth_usd)) if args.eth_usd else get_eth_usd()
    threshold_eth = Decimal(str(args.threshold_usd)) / eth_usd
    threshold_wei = int(threshold_eth * Decimal(10**18))

    latest = int(rpc_call(args.rpc_url, "eth_blockNumber", []), 16)
    start = max(0, latest - args.blocks + 1)
    pairs: Dict[Tuple[str, str], Dict[str, Any]] = collections.defaultdict(
        lambda: {"count": 0, "wei": 0, "first": None, "last": None, "txs": []}
    )

    blocks_done = 0
    for block_start in range(start, latest + 1, args.batch_size):
        block_numbers = list(range(block_start, min(block_start + args.batch_size, latest + 1)))
        calls = [("eth_getBlockByNumber", [hex(number), True]) for number in block_numbers]
        for attempt in range(3):
            try:
                responses = rpc_batch(args.rpc_url, calls)
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(1 + attempt)
        by_id = {item.get("id"): item.get("result") for item in responses if "result" in item}
        for idx, _number in enumerate(block_numbers):
            block = by_id.get(idx)
            if not block:
                continue
            timestamp = int(block["timestamp"], 16)
            for tx in block.get("transactions", []):
                to_address = tx.get("to")
                if not to_address:
                    continue
                value_wei = int(tx.get("value", "0x0"), 16)
                if value_wei < threshold_wei:
                    continue
                from_address = tx["from"].lower()
                to_address = to_address.lower()
                row = pairs[(from_address, to_address)]
                row["count"] += 1
                row["wei"] += value_wei
                row["first"] = timestamp if row["first"] is None else min(row["first"], timestamp)
                row["last"] = timestamp if row["last"] is None else max(row["last"], timestamp)
                if len(row["txs"]) < args.sample_txs:
                    row["txs"].append(tx["hash"])
            blocks_done += 1

    results = []
    for (from_address, to_address), row in pairs.items():
        if row["count"] < args.min_repeat:
            continue
        total_eth = Decimal(row["wei"]) / Decimal(10**18)
        total_usd = total_eth * eth_usd
        span_seconds = max(1, int(row["last"] - row["first"]))
        results.append(
            {
                "from": from_address,
                "to": to_address,
                "from_short": short_addr(from_address),
                "to_short": short_addr(to_address),
                "tx_count": row["count"],
                "total_eth": float(round(total_eth, 6)),
                "total_usd": float(round(total_usd, 2)),
                "avg_usd": float(round(total_usd / Decimal(row["count"]), 2)),
                "first_utc": dt.datetime.utcfromtimestamp(row["first"]).isoformat() + "Z",
                "last_utc": dt.datetime.utcfromtimestamp(row["last"]).isoformat() + "Z",
                "span_minutes": round(span_seconds / 60, 2),
                "pattern": classify_pattern(row["count"], span_seconds),
                "sample_txs": row["txs"],
            }
        )

    results.sort(key=lambda item: (item["tx_count"], item["total_usd"]), reverse=True)
    return {
        "mode": "rpc",
        "chain": "ethereum",
        "rpc_url": args.rpc_url,
        "latest_block": latest,
        "block_range": [start, latest],
        "blocks_scanned": blocks_done,
        "eth_usd": float(eth_usd),
        "threshold_usd": args.threshold_usd,
        "threshold_eth": float(threshold_eth),
        "min_repeat": args.min_repeat,
        "high_value_pairs_total": len(pairs),
        "repeated_pairs_count": len(results),
        "results": results[: args.limit],
    }


def write_outputs(output: Dict[str, Any], args: argparse.Namespace) -> None:
    if args.out_json:
        path = Path(args.out_json).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    if args.out_csv:
        path = Path(args.out_csv).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = output.get("results", [])
        fieldnames = ["from", "to", "tx_count", "total_eth", "total_usd", "avg_usd", "first_utc", "last_utc", "span_minutes", "pattern"]
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: row.get(key) for key in fieldnames})


def bigquery_sql(args: argparse.Namespace) -> str:
    token_rows = ",\n    ".join(
        f"STRUCT('{symbol}' AS symbol, '{address}' AS token_address, {decimals} AS decimals)"
        for symbol, (address, decimals) in TOKEN_DECIMALS.items()
    )
    eth_usd_expr = str(args.eth_usd or 2123.11)
    return f"""
-- Froggo high-value repeated-flow scanner, Ethereum mainnet.
-- Run in BigQuery against `bigquery-public-data.crypto_ethereum`.
-- Window: last {args.days} day(s). Threshold: ${args.threshold_usd}+ per transfer. Min repeat: {args.min_repeat}.

DECLARE threshold_usd FLOAT64 DEFAULT {float(args.threshold_usd)};
DECLARE min_repeat INT64 DEFAULT {int(args.min_repeat)};
DECLARE eth_usd FLOAT64 DEFAULT {eth_usd_expr};

WITH token_meta AS (
  SELECT * FROM UNNEST([
    {token_rows}
  ])
),
eth_flows AS (
  SELECT
    LOWER(from_address) AS from_address,
    LOWER(to_address) AS to_address,
    'ETH' AS asset,
    SAFE_CAST(value AS BIGNUMERIC) / 1e18 AS amount,
    SAFE_CAST(value AS BIGNUMERIC) / 1e18 * eth_usd AS amount_usd,
    block_timestamp,
    `hash` AS tx_hash
  FROM `bigquery-public-data.crypto_ethereum.transactions`
  WHERE block_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {int(args.days)} DAY)
    AND to_address IS NOT NULL
    AND receipt_status = 1
    AND SAFE_CAST(value AS BIGNUMERIC) / 1e18 * eth_usd >= threshold_usd
),
erc20_flows AS (
  SELECT
    LOWER(t.from_address) AS from_address,
    LOWER(t.to_address) AS to_address,
    m.symbol AS asset,
    SAFE_CAST(t.value AS BIGNUMERIC) / POW(10, m.decimals) AS amount,
    CASE
      WHEN m.symbol IN ('USDC','USDT','DAI') THEN SAFE_CAST(t.value AS BIGNUMERIC) / POW(10, m.decimals)
      WHEN m.symbol = 'WETH' THEN SAFE_CAST(t.value AS BIGNUMERIC) / POW(10, m.decimals) * eth_usd
    END AS amount_usd,
    t.block_timestamp,
    t.transaction_hash AS tx_hash
  FROM `bigquery-public-data.crypto_ethereum.token_transfers` t
  JOIN token_meta m ON LOWER(t.token_address) = m.token_address
  WHERE t.block_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {int(args.days)} DAY)
),
all_flows AS (
  SELECT * FROM eth_flows
  UNION ALL
  SELECT * FROM erc20_flows WHERE amount_usd >= threshold_usd
),
pair_stats AS (
  SELECT
    from_address,
    to_address,
    asset,
    COUNT(*) AS tx_count,
    SUM(amount_usd) AS total_usd,
    AVG(amount_usd) AS avg_usd,
    MIN(block_timestamp) AS first_seen,
    MAX(block_timestamp) AS last_seen,
    TIMESTAMP_DIFF(MAX(block_timestamp), MIN(block_timestamp), MINUTE) AS span_minutes,
    ARRAY_AGG(tx_hash ORDER BY block_timestamp DESC LIMIT 3) AS sample_txs
  FROM all_flows
  GROUP BY from_address, to_address, asset
  HAVING tx_count >= min_repeat
)
SELECT
  *,
  CASE
    WHEN span_minutes <= 15 THEN 'burst'
    WHEN span_minutes <= 180 THEN 'dense recurring'
    WHEN span_minutes <= 1440 THEN 'same-day recurring'
    WHEN span_minutes <= 10080 THEN 'weekly recurring'
    ELSE 'long-window recurring'
  END AS pattern
FROM pair_stats
ORDER BY tx_count DESC, total_usd DESC
LIMIT {int(args.limit)};
""".strip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ethereum repeated high-value flow scanner")
    sub = parser.add_subparsers(dest="mode", required=True)

    rpc = sub.add_parser("rpc", help="scan recent blocks via public RPC, native ETH only")
    rpc.add_argument("--rpc-url", default=DEFAULT_RPC)
    rpc.add_argument("--blocks", type=int, default=1000)
    rpc.add_argument("--batch-size", type=int, default=25)
    rpc.add_argument("--threshold-usd", type=float, default=5000)
    rpc.add_argument("--eth-usd", type=float, default=None)
    rpc.add_argument("--min-repeat", type=int, default=2)
    rpc.add_argument("--limit", type=int, default=50)
    rpc.add_argument("--sample-txs", type=int, default=3)
    rpc.add_argument("--out-json", default=None)
    rpc.add_argument("--out-csv", default=None)

    sql = sub.add_parser("sql", help="print BigQuery SQL for full-chain ETH + ERC20 analysis")
    sql.add_argument("--days", type=int, default=30)
    sql.add_argument("--threshold-usd", type=float, default=5000)
    sql.add_argument("--min-repeat", type=int, default=5)
    sql.add_argument("--limit", type=int, default=1000)
    sql.add_argument("--eth-usd", type=float, default=None)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.mode == "rpc":
        output = scan_rpc(args)
        write_outputs(output, args)
        print(json.dumps(output, indent=2))
        return 0
    if args.mode == "sql":
        print(bigquery_sql(args), end="")
        return 0
    parser.error("unknown mode")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
