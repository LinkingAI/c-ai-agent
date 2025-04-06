import requests

# Llamar a DefiLlama Yields API
url = "https://yields.llama.fi/pools"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()["data"]

    print("\n🔍 Analizando oportunidades en Optimism desde DefiLlama...\n")

    # Filtrar solo pools en la red Optimism
    optimism_pools = [pool for pool in data if pool['chain'] == "Optimism"]

    count = 0
    for pool in optimism_pools:
        project = pool.get("project", "N/A")
        symbol = pool.get("symbol", "N/A")
        apy = pool.get("apy", 0)
        tvl_usd = pool.get("tvlUsd", 0)
        url = pool.get("url", "")

        # Filtros HIM básicos
        if apy > 10 and tvl_usd > 500_000:
            count += 1
            print(f"✅ Oportunidad #{count}")
            print(f"🔸 Protocolo: {project}")
            print(f"🔹 Token(s): {symbol}")
            print(f"💰 APY: {apy:.2f}%")
            print(f"📊 TVL: ${tvl_usd:,.2f}")
            print(f"🔗 Link: {url}")
            print("-" * 40)

    if count == 0:
        print("⚠️ No se encontraron oportunidades relevantes en Optimism por ahora.")

else:
    print("❌ No se pudo conectar con la API de DefiLlama.")
