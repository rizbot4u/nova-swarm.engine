import asyncio
import os
import json
import httpx
from rich.console import Console
from rich.panel import Panel
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
console = Console()
API_KEY = os.getenv("GROQ_API_KEY", "")
BASE_RPC = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
w3 = Web3(Web3.HTTPProvider(BASE_RPC))

DVP_CONTRACT = "0xB850729c96e7eC7e38bf188a6392F44602C96e4F"
DVP_ABI = [{"anonymous": False,"inputs": [{"indexed": True, "name": "orderId", "type": "bytes32"},{"indexed": True, "name": "settlementId", "type": "bytes32"},{"indexed": True, "name": "buyer", "type": "address"},{"indexed": False, "name": "seller", "type": "address"},{"indexed": False, "name": "dkhyrAmount", "type": "uint256"},{"indexed": False, "name": "shareAmount", "type": "uint256"},{"indexed": False, "name": "timestamp", "type": "uint256"}],"name": "DvPSettled","type": "event"}]
contract = w3.eth.contract(address=DVP_CONTRACT, abi=DVP_ABI)

async def call_llm(prompt: str) -> str:
    if not API_KEY: return "Mock AI report."
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=60.0)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]

async def listen_for_events():
    console.print("[bold yellow]🎧 Listening for DvPSettled events...[/bold yellow]")
    last_block = w3.eth.block_number
    
    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                events = contract.events.DvPSettled().get_logs(from_block=last_block + 1, to_block=current_block)
                for event in events:
                    # FIXED: Using .hex() for transaction hash
                    tx_hash = event['transactionHash'].hex()
                    console.print(f"\n[bold green]🚨 NEW SETTLEMENT:[/bold green] Block {event['blockNumber']} | Tx: https://basescan.org/tx/{tx_hash}")
                    prompt = f"Write a short press release for this DvP trade. Buyer: {event['args']['buyer']}, Amount: {w3.from_wei(event['args']['dkhyrAmount'], 'ether')} DKHYR."
                    report = await call_llm(prompt)
                    console.print(Panel(report, title="AI Report", border_style="cyan"))
                last_block = current_block
        except Exception as e:
            pass # Ignore RPC rate limits
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(listen_for_events())
