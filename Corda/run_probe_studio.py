import asyncio
import json
import urllib.request
import websockets

CDP_HTTP = "http://127.0.0.1:9223"
TEST_URL = "https://gist.githubusercontent.com/Charles-ace/9cd83066dca0a7d5081f3a1eae4763a3/raw/case_b_privacy.md"

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
        
        # 1. Click test_probe button
        clicked = await ctrl.eval("""
        (() => {
            const btn = Array.from(document.querySelectorAll('span, div, button'))
                .find(el => el.innerText && el.innerText.trim() === 'test_probe');
            if (btn) {
                (btn.closest('button, div[role="button"]') || btn).click();
                return "Clicked test_probe";
            }
            return "test_probe not found";
        })()
        """)
        print(clicked)
        await asyncio.sleep(1)

        # 2. Inspect all visible inputs in the left panel
        inputs = await ctrl.eval("""
        (() => {
            return Array.from(document.querySelectorAll('input'))
                .map(i => ({ name: i.name, placeholder: i.placeholder, type: i.type, id: i.id }));
        })()
        """)
        print("Available inputs:", json.dumps(inputs, indent=2))

        # 3. Fill in the input named 'url' or first text input
        fill = await ctrl.eval(f"""
        (() => {{
            const input = document.querySelector('input[name="url"]') || Array.from(document.querySelectorAll('input[type="text"]')).find(i => i.placeholder.includes('string'));
            if (input) {{
                input.value = "{TEST_URL}";
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return "Filled URL successfully: " + input.name;
            }}
            return "No text input found";
        }})()
        """)
        print(fill)
        await asyncio.sleep(1)

        # 4. Click Send Transaction
        send = await ctrl.eval("""
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send Transaction'));
            if (btn) {
                btn.click();
                return "Clicked Send Transaction";
            }
            return "Send Transaction button not found";
        })()
        """)
        print(send)

        # 5. Monitor logs and GenVM result
        print("Waiting for transaction execution...")
        for i in range(35):
            await asyncio.sleep(1)
            tx = await ctrl.eval("""
            (() => {
                const pinia = document.querySelector('#app').__vue_app__.config.globalProperties.$pinia;
                const txStore = pinia._s.get('transactionsStore');
                const nodeStore = pinia._s.get('nodeStore');
                const latestTx = txStore.allTransactions[0];
                const latestLogs = nodeStore.logs.slice(-3).map(l => ({
                    scope: l.scope,
                    name: l.name,
                    message: l.message,
                    stderr: l.data ? l.data.stderr : null,
                    result: l.data ? l.data.result : null
                }));
                return {
                    status: latestTx ? latestTx.statusName : null,
                    type: latestTx ? latestTx.type : null,
                    hash: latestTx ? latestTx.hash : null,
                    latestLogs
                };
            })()
            """)
            print(f"[{i+1}s] Tx {tx.get('type')} status: {tx.get('status')}")
            if tx.get("status") in ["ACCEPTED", "FINALIZED"] and tx.get("type") == "method":
                print("Method transaction completed!")
                print(json.dumps(tx, indent=2))
                break

if __name__ == "__main__":
    asyncio.run(main())
