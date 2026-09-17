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
        
        contracts = await ctrl.eval("""
        (() => {
            const pinia = document.querySelector('#app').__vue_app__.config.globalProperties.$pinia;
            const cStore = pinia._s.get('contractsStore');
            if (!cStore) return "No contractsStore";
            return cStore.contracts.map(c => ({
                name: c.name,
                content: c.content
            }));
        })()
        """)
        for c in contracts:
            print(f"=== CONTRACT: {c['name']} ===")
            if "web" in c["content"] or "get(" in c["content"] or "request(" in c["content"]:
                print("Found web usage in", c['name'])
                # Print lines containing web
                for line in c["content"].splitlines():
                    if any(w in line for w in ["web", "http", "nondet", "prompt", "eq_principle"]):
                        print("  ", line)

if __name__ == "__main__":
    asyncio.run(main())
