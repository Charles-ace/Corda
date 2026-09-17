import asyncio
import json
import urllib.request
import websockets

CDP_HTTP = "http://127.0.0.1:9223"

async def get_studio_tab():
    resp = urllib.request.urlopen(f"{CDP_HTTP}/json/list")
    tabs = json.loads(resp.read().decode())
    for t in tabs:
        if "studio.genlayer.com" in t.get("url", ""):
            return t
    return None

class StudioController:
    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 0

    async def cdp(self, method, params=None):
        self.msg_id += 1
        curr_id = self.msg_id
        req = {"id": curr_id, "method": method, "params": params or {}}
        await self.ws.send(json.dumps(req))
        while True:
            resp = await self.ws.recv()
            data = json.loads(resp)
            if data.get("id") == curr_id:
                return data

    async def eval(self, js):
        res = await self.cdp("Runtime.evaluate", {
            "expression": js,
            "returnByValue": True,
            "awaitPromise": True
        })
        if "result" in res and "result" in res["result"]:
            return res["result"]["result"].get("value")
        return res

async def main():
    tab = await get_studio_tab()
    if not tab:
        print("GenLayer Studio tab not found")
        return
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        ctrl = StudioController(ws)
        
        tx_data = await ctrl.eval("""
        (() => {
            const pinia = document.querySelector('#app').__vue_app__.config.globalProperties.$pinia;
            const txStore = pinia._s.get('transactionsStore');
            if (!txStore) return null;
            return txStore.allTransactions.map(t => ({
                hash: t.hash,
                type: t.type,
                statusName: t.statusName,
                contractAddress: t.contractAddress,
                method: t.data && t.data.data && t.data.data.calldata ? t.data.data.calldata.method : null,
                result: t.result,
                consensusData: t.consensusData || t.consensus
            }));
        })()
        """)
        print("=== TRANSACTIONS SUMMARY ===")
        print(json.dumps(tx_data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
