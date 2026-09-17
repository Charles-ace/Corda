import asyncio
import json
import urllib.request
import websockets

CDP_HTTP = "http://127.0.0.1:9223"

CASE_A_REPO = "https://gist.githubusercontent.com/Charles-ace/3da2ae80f931867f18df331549a287bf/raw/case_a_code.py"
CASE_A_PRIVACY = "https://gist.githubusercontent.com/Charles-ace/3da2ae80f931867f18df331549a287bf/raw/case_a_privacy.md"

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

async def execute_case_a():
    tab = await get_studio_tab()
    if not tab:
        print("GenLayer Studio tab not found")
        return
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        ctrl = StudioController(ws)
        
        # 1. Ensure analyze method section is open
        click_analyze = await ctrl.eval("""
        (() => {
            const analyzeBtn = Array.from(document.querySelectorAll('button, div, span'))
                .find(el => el.innerText && el.innerText.trim() === 'analyze');
            if (analyzeBtn) {
                const target = analyzeBtn.closest('button, div[role="button"]') || analyzeBtn;
                target.click();
                return "Clicked analyze";
            }
            return "analyze button not found";
        })()
        """)
        print("Analyze open:", click_analyze)
        await asyncio.sleep(1)

        # 2. Fill in Case A URLs
        fill_res = await ctrl.eval(f"""
        (() => {{
            const repoInput = document.querySelector('input[name="repo_url"]');
            const privacyInput = document.querySelector('input[name="privacy_url"]');
            if (!repoInput || !privacyInput) {{
                return {{ success: false, error: "Inputs not found" }};
            }}
            
            repoInput.value = "{CASE_A_REPO}";
            repoInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            repoInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

            privacyInput.value = "{CASE_A_PRIVACY}";
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

        # 3. Click "Send Transaction"
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

        # 4. Monitor transaction until FINALIZED or ACCEPTED
        print("Waiting for Case A consensus and transaction finalization...")
        for i in range(45):
            await asyncio.sleep(1)
            tx_status = await ctrl.eval("""
            (() => {
                const txItems = Array.from(document.querySelectorAll('div[class*="transaction"], div[class*="item"]'))
                    .map(el => el.innerText.trim())
                    .filter(t => t && t.includes('analyze'));
                
                const allHashes = Array.from(document.querySelectorAll('*'))
                    .map(el => el.innerText || '')
                    .filter(t => t.match(/0x[a-fA-F0-9]{64}/));

                return {
                    sec: """ + str(i+1) + """,
                    txItems: txItems.slice(0, 5),
                    hashes: Array.from(new Set(allHashes))
                };
            })()
            """)
            print(f"[{i+1}s] Tx items: {tx_status.get('txItems')}")
            # Check if there are 2 analyze transactions now (Case B and Case A)
            if len(tx_status.get("txItems", [])) >= 2:
                # If the first item in txItems (latest) is ACCEPTED or FINALIZED
                latest = tx_status["txItems"][0]
                if "ACCEPTED" in latest or "FINALIZED" in latest:
                    print("Case A transaction finalized!")
                    print("All Hashes:", tx_status["hashes"])
                    break

if __name__ == "__main__":
    asyncio.run(execute_case_a())
