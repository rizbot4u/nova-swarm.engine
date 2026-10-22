import asyncio
import os
import json
import httpx
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from dotenv import load_dotenv

load_dotenv()
console = Console()
API_KEY = os.getenv("GROQ_API_KEY", "")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

EVIDENCE_LEDGER = """
VERIFIED FACTS - You may ONLY cite these facts. Do not invent numbers, dates, audits, partners, or comparisons.
- Atomic DvP settlement: 500 DKHYR + 5 NVP-1 shares in one transaction on Base Mainnet. Tx: 0x69aaa0cc
- Gas cost per settlement: $0.0014
- Whitelist-gated transfers enforced at the smart contract level.
- Per-tenant encrypted vault using AES-256-GCM.
- Bybit Level 3 Institutional Broker.
If a claim isn't on this list, write around it in general terms. NEVER invent statistics, percentages, or auditor names.
"""

async def call_llm(prompt: str) -> str:
    if not API_KEY: return "Mock mode: AI response here."
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.5, "max_tokens": 1000}
    
    for attempt in range(3):
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(API_URL, headers=headers, json=payload, timeout=60.0)
                if res.status_code == 429:
                    await asyncio.sleep(10)
                    continue
                res.raise_for_status()
                return res.json()["choices"][0]["message"]["content"]
        except Exception:
            await asyncio.sleep(5)
    return "API call failed."

async def run_swarm():
    console.print("[bold yellow]Starting Nova Agent Swarm...[/bold yellow]")
    main_prompt = f"Generate 3 distinct marketing angles for an Atomic DvP RWA platform. {EVIDENCE_LEDGER}"
    
    # In a real run, this would parallelize. Here we simplify for the clean repo.
    console.print("[dim]Generating response...[/dim]")
    result = await call_llm(main_prompt)
    
    console.print("\n[bold cyan]--- FINAL OUTPUT ---[/bold cyan]")
    console.print(Panel(result, border_style="green"))

if __name__ == "__main__":
    asyncio.run(run_swarm())
