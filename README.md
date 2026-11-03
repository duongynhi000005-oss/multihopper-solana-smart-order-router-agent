# MultiHopper Solana Smart Order Router & x402 AI Execution Agent

**Submission for Superteam Earn: MultiHopper Build & Route Challenge (Up to $50,000 Revenue Share + $5,000 USDC Pool)**

## Overview
An institutional-grade Solana Multi-Hop Smart Order Router (SOR) and autonomous AI execution engine engineered for:
- **Modified Bellman-Ford & Convex Split-Routing** across **Raydium CLMM**, **Meteora DLMM**, **Orca Whirlpools**, and **Phoenix Orderbooks**.
- **Strict Solana Runtime Constraint Enforcement**: Keeps multi-hop route execution within the `1,400,000` Compute Unit (CU) ceiling and `64` Address Lookup Table (ALT) account lock limits.
- **Pre-Trade Honeypot, Freeze/Mint Authority & Rug-Pull Screening**: Powered by our live sub-20ms Cloudflare Edge API (`https://rapidapi-evm-solana-honeypot-token-auditor-worker.duongynhi000005.workers.dev/openapi.json`).
- **Dynamic Priority Fee & Jito Tip Optimization**: Powered by `https://rapidapi-solana-jupiter-slippage-priority-fee.duongynhi000005.workers.dev/openapi.json`.
