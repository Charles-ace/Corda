import asyncio
import json
import urllib.request
import websockets

CDP_HTTP = "http://127.0.0.1:9223"
CONTRACT_ADDR = "0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92"

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

async def main():
    tab = await get_studio_tab()
    if not tab:
        print("GenLayer Studio tab not found")
        return
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        ctrl = StudioController(ws)
        
        # 1. Open analyze method under Write Methods
        await ctrl.eval("""
        (() => {
            const btn = Array.from(document.querySelectorAll('span, div, button'))
                .find(el => el.innerText && el.innerText.trim() === 'analyze');
            if (btn) (btn.closest('button, div[role="button"]') || btn).click();
        })()
        """)
        await asyncio.sleep(1)

        # 2. Fill in Case A URLs
        fill = await ctrl.eval(f"""
        (() => {{
            const repoInput = document.querySelector('input[name="repo_url"]');
            const privacyInput = document.querySelector('input[name="privacy_url"]');
            if (repoInput && privacyInput) {{
                repoInput.value = "{CASE_A_REPO}";
                repoInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                repoInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

                privacyInput.value = "{CASE_A_PRIVACY}";
                privacyInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                privacyInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return "Filled Case A inputs";
            }}
            return "Inputs not found";
        }})()
        """)
        print(fill)
        await asyncio.sleep(1)

        # 3. Click Send Transaction
        await ctrl.eval("""
        (() => {
            const sendBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send Transaction'));
            if (sendBtn) sendBtn.click();
        })()
        """)
        print("Triggered Case A transaction...")

        # 4. Wait for new transaction to appear and finalize
        case_a_tx = None
        case_a_result = None
        for i in range(45):
            await asyncio.sleep(1)
            status = await ctrl.eval("""
            (() => {
                const pinia = document.querySelector('#app').__vue_app__.config.globalProperties.$pinia;
                const txStore = pinia._s.get('transactionsStore');
                const nodeStore = pinia._s.get('nodeStore');
                const latestTx = txStore.allTransactions[0];
                const execFinished = nodeStore.logs.filter(l => l.name === 'execution_finished').slice(-1)[0];

                return {
                    status: latestTx ? latestTx.statusName : null,
                    type: latestTx ? latestTx.type : null,
                    hash: latestTx ? latestTx.hash : null,
                    execResult: execFinished && execFinished.data ? execFinished.data.result : null,
                    stderr: execFinished && execFinished.data ? execFinished.data.stderr : null
                };
            })()
            """)
            print(f"[{i+1}s] Case A status: {status.get('status')} | Hash: {status.get('hash')}")
            # Ensure it's not the Case B hash (0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099)
            if status.get("hash") != "0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099":
                if status.get("status") in ["ACCEPTED", "FINALIZED"]:
                    case_a_tx = status.get("hash")
                    case_a_result = status.get("execResult")
                    print("Case A FINALIZED!")
                    print("Case A Tx Hash:", case_a_tx)
                    print("GenVM Result:", case_a_result)
                    print("GenVM Stderr:", status.get("stderr"))
                    break

if __name__ == "__main__":
    asyncio.run(main())
