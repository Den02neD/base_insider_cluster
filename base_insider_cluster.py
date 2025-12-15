import requests, time
from collections import defaultdict

def insider_cluster():
    print("Base — Insider Cluster Detector (10+ new wallets from same creator pattern)")
    creators = defaultdict(int)

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            for pair in r.json().get("pairs", []):
                age = time.time() - pair.get("pairCreatedAt", 0) / 1000
                if age > 300: continue  # only fresh tokens

                tx_hash = pair.get("pairCreatedTxHash")
                if not tx_hash: continue

                tx = requests.get(f"https://api.basescan.org/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}").json()
                creator = tx["result"]["from"].lower()

                creators[creator] += 1

                if creators[creator] >= 10:
                    token = pair["baseToken"]["symbol"]
                    print(f"INSIDER CLUSTER ALERT\n"
                          f"Wallet {creator[:10]}... created {creators[creator]} pools today\n"
                          f"Latest: {token}\n"
                          f"https://dexscreener.com/base/{pair['pairAddress']}\n"
                          f"https://basescan.org/address/{creator}\n"
                          f"→ Factory farmer or coordinated launch group\n"
                          f"→ Follow for next drops or avoid rugs\n"
                          f"{'CLUSTER'*25}")
                    creators[creator] = 0  # reset after alert

        except:
            pass
        time.sleep(8.5)

if __name__ == "__main__":
    insider_cluster()
