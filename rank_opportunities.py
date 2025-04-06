import requests

# Asignar puntuaciones base a protocolos conocidos
protocol_scores = {
    "velodrome-v2": 10,
    "uniswap-v3": 9,
    "beefy": 8,
    "extra-finance-leverage-farming": 7,
    "aave-v3": 10,
    "curve": 9
}

def rank(pool):
    apy = pool.get("apy", 0)
    tvl = pool.get("tvlUsd", 0)
    protocol = pool.get("project", "unknown")

    score = (
        apy * 0.5 +
        (tvl / 1_000_000) * 0.3 +
        protocol_scores.get(protocol, 5) * 0.2
    )
    return round(score, 2)

# ✅ Esta función es lo que necesita tu loop_agent
def get_ranked_opportunities():
    url = "https://yields.llama.fi/pools"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ No se pudo acceder a DefiLlama.")
        return []

    data = response.json()["data"]
    optimism_pools = [
        p for p in data
        if p['chain'] == "Optimism" and p.get("apy", 0) > 10 and p.get("tvlUsd", 0) > 500_000
    ]

    for pool in optimism_pools:
        pool["score"] = rank(pool)

    sorted_pools = sorted(optimism_pools, key=lambda x: x["score"], reverse=True)
    return sorted_pools[:10]
