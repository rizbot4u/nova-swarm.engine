# 🐝 Nova Swarm Engine

**Event-Driven, Zero-Hallucination Multi-Agent AI Swarm for Institutional RWA Reporting.**

The Nova Swarm Engine is a production-grade, autonomous AI pipeline designed for Real-World Asset (RWA) infrastructure. It listens to the Base Mainnet blockchain 24/7, detects on-chain settlements, and automatically generates fact-checked institutional reports using a multi-agent AI architecture.

Instead of relying on LLMs to "guess" or hallucinate metrics, this engine injects live, verifiable Web3 context into the agents' system prompts, forcing them to ground their output in cryptographic truth.

## 🏗️ Architecture

1. **The Execution Layer (Smart Contracts):** Atomic Delivery-versus-Payment (DvP) contracts execute on Base Mainnet.
2. **The Event-Driven Sentinel (`listener_swarm.py`):** A Python daemon using `web3.py` constantly polls the blockchain. The millisecond a `DvPSettled` event fires, it captures the block number, transaction hash, and wallet addresses.
3. **The AI Agent Swarm (`live_swarm_engine.py`):** An asynchronous multi-agent system (Orchestrator -> Workers -> Validator) that drafts, fact-checks, and finalizes the report.

## 🚀 Production-Grade Features

*   **Zero-Hallucination Guarantee:** The AI is restricted from inventing statistics. It only cites the live on-chain data provided by the Sentinel.
*   **Async Parallelism:** Uses `asyncio` to fire multiple generation tasks simultaneously.
*   **Resilient Execution:** Includes exponential backoff for API rate limits (429 errors) and auto-continuation for token limits.
*   **Read-Only Security:** The AI agents have zero access to private keys. They can only *read* the blockchain.

## 📦 Quick Start

### 1. Install Dependencies
```bash
git clone git@github.com:rizbot4u/nova-swarm.engine.git
cd nova-swarm.engine
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2. Configure Environment

Rename .env.example to .env and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
BASE_RPC_URL=your_alchemy_base_rpc_url
```

3. Run the Swarm

```bash
python live_swarm_engine.py
```

4. Run the Live Listener

```bash
python listener_swarm.py
```

---

Built by Rizwan Ali | Founder, Nova Global Keys
