import asyncio
import json
import urllib.request
import websockets
import time

CDP_HTTP = "http://127.0.0.1:9223"

CASE_B_REPO = "https://gist.githubusercontent.com/Charles-ace/9cd83066dca0a7d5081f3a1eae4763a3/raw/case_b_code.py"
CASE_B_PRIVACY = "https://gist.githubusercontent.com/Charles-ace/9cd83066dca0a7d5081f3a1eae4763a3/raw/case_b_privacy.md"

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

async def execute_case_b():
    tab = await get_studio_tab()
    if not tab:
        print("GenLayer Studio tab not found")
        return
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        ctrl = StudioController(ws)
        
        # 1. Fill in repo_url and privacy_url
        fill_res = await ctrl.eval(f"""
        (() => {{
            const repoInput = document.querySelector('input[name="repo_url"]');
            const privacyInput = document.querySelector('input[name="privacy_url"]');
            if (!repoInput || !privacyInput) {{
                return {{ success: false, error: "Inputs not found" }};
            }}
            
            // Set values and trigger input/change events
            repoInput.value = "{CASE_B_REPO}";
            repoInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            repoInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

            privacyInput.value = "{CASE_B_PRIVACY}";
            privacyInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            privacyInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

            return {{
                success: true,
                repoValue: repoInput.value,
                privacyValue: privacyInput.value
            }};
        }})()
        """)
        print("Inputs filled:", json.dumps(fill_res, indent=2))
        await asyncio.sleep(1)

        # 2. Click "Send Transaction"
        click_send = await ctrl.eval("""
        (() => {
            const sendBtn = Array.from(document.querySelectorAll('button'))
                .find(b => b.innerText.includes('Send Transaction'));
            if (sendBtn) {
                sendBtn.click();
                return "Clicked Send Transaction";
            }
            return "Send Transaction button not found";
        })()
        """)
        print("Send click:", click_send)

        # 3. Poll for transaction completion and logs
        print("Waiting for consensus and transaction finalization (up to 45s)...")
        for i in range(45):
            await asyncio.sleep(1)
            tx_status = await ctrl.eval("""
            (() => {
                const txItems = Array.from(document.querySelectorAll('div[class*="transaction"], div[class*="item"]'))
                    .map(el => el.innerText.trim())
                    .filter(t => t && t.includes('analyze'));
                const latestLogs = Array.from(document.querySelectorAll('div[class*="log"], tr'))
                    .map(el => el.innerText.trim())
                    .filter(t => t && (t.includes('analyze') || t.includes('CONSENSUS') || t.includes('ACCEPTED') || t.includes('PROPOSING') || t.includes('COMMITTING') || t.includes('DISCLOSURE')));
                return {
                    sec: """ + str(i+1) + """,
                    txItems: txItems.slice(0, 5),
                    latestLogs: latestLogs.slice(0, 5)
                };
            })()
            """)
            print(f"[{i+1}s] Tx items: {tx_status.get('txItems')} | Logs: {len(tx_status.get('latestLogs', []))}")
            if any("ACCEPTED" in item for item in tx_status.get("txItems", [])):
                print("Transaction ACCEPTED!")
                print("Final Tx items:", tx_status["txItems"])
                print("Final Logs:", tx_status["latestLogs"])
                break

if __name__ == "__main__":
    asyncio.run(execute_case_b())
