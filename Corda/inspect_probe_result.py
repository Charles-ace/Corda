import asyncio
import json
import urllib.request
import websockets

CDP_HTTP = "http://127.0.0.1:9223"
TX_HASH = "0x62f2f62264ea3385d572d7e8516b5936685a5d112fb3cb32a2d5039f5b8ea204"

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
        
        tx_data = await ctrl.eval(f"""
        (() => {{
            const pinia = document.querySelector('#app').__vue_app__.config.globalProperties.$pinia;
            const nodeStore = pinia._s.get('nodeStore');
            
            return nodeStore.logs.slice(-10).map(l => ({{
                scope: l.scope,
                name: l.name,
                message: l.message,
                stderr: l.data ? l.data.stderr : '',
                result: l.data ? l.data.result : '',
                leader_receipt: l.data && l.data.consensus_data ? l.data.consensus_data.leader_receipt : null
            }}));
        }})()
        """)
        print("=== LATEST 10 LOGS ===")
        for l in tx_data:
            print(f"[{l['scope']}] {l['name']}: {l['message']}")
            if l['stderr']:
                print("   STDERR:", l['stderr'])
            if l['result']:
                print("   RESULT:", l['result'])
            if l['leader_receipt']:
                print("   LEADER_RECEIPT:", json.dumps(l['leader_receipt'], indent=2))

if __name__ == "__main__":
    asyncio.run(main())
