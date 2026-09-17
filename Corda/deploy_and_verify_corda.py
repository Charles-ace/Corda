import asyncio
import json
import urllib.request
import websockets

CDP_HTTP = "http://127.0.0.1:9223"
CORDA_PATH = r"C:\Builds\Genlayer\Corda\contracts\Corda.py"

CASE_B_REPO = "https://gist.githubusercontent.com/Charles-ace/9cd83066dca0a7d5081f3a1eae4763a3/raw/case_b_code.py"
CASE_B_PRIVACY = "https://gist.githubusercontent.com/Charles-ace/9cd83066dca0a7d5081f3a1eae4763a3/raw/case_b_privacy.md"

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
        
        # 1. Navigate to contracts
        await ctrl.eval("window.location.href = '/contracts'")
        await asyncio.sleep(2)

        # 2. Upload updated Corda.py
        doc = await ctrl.cdp("DOM.getDocument")
        root_node_id = doc["result"]["root"]["nodeId"]
        file_input_node = await ctrl.cdp("DOM.querySelector", {
            "nodeId": root_node_id,
            "selector": 'input[type="file"]'
        })
        input_node_id = file_input_node["result"]["nodeId"]
        await ctrl.cdp("DOM.setFileInputFiles", {
            "nodeId": input_node_id,
            "files": [CORDA_PATH]
        })
        await ctrl.eval("""
        (() => {
            const input = document.querySelector('input[type="file"]');
            if (input) input.dispatchEvent(new Event('change', { bubbles: true }));
        })()
        """)
        print("Uploaded updated Corda.py")
        await asyncio.sleep(2)

        # 3. Navigate to /run-debug
        await ctrl.eval("window.location.href = '/run-debug'")
        await asyncio.sleep(2)

        # 4. Ensure Corda.py is selected
        await ctrl.eval("""
        (() => {
            const tabs = Array.from(document.querySelectorAll('*')).filter(el => el.innerText && el.innerText.trim() === 'Corda.py');
            if (tabs.length > 0) (tabs[0].closest('button, div[role="button"]') || tabs[0]).click();
        })()
        """)
        await asyncio.sleep(1)

        # 5. Deploy new instance
        print("Triggering deployment...")
        deploy_res = await ctrl.eval("""
        (() => {
            const deployBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Deploy'));
            if (deployBtn) {
                deployBtn.click();
                return "Clicked Deploy: " + deployBtn.innerText;
            }
            return "Deploy button not found";
        })()
        """)
        print(deploy_res)

        # 6. Wait for deployment to finalize
        print("Waiting for Corda deployment to finalize...")
        deploy_tx = None
        new_address = None
        for i in range(25):
            await asyncio.sleep(1)
            status = await ctrl.eval("""
            (() => {
                const pinia = document.querySelector('#app').__vue_app__.config.globalProperties.$pinia;
                const txStore = pinia._s.get('transactionsStore');
                const latestTx = txStore.allTransactions[0];
                const addrEl = Array.from(document.querySelectorAll('*')).find(el => el.textContent && el.textContent.includes('0x') && el.closest('[data-testid="deployed-contract-info"]'));
                
                // Explorer address link
                const expLink = Array.from(document.querySelectorAll('a[href*="/address/0x"]')).map(a => a.href);
                return {
                    status: latestTx ? latestTx.statusName : null,
                    hash: latestTx ? latestTx.hash : null,
                    type: latestTx ? latestTx.type : null,
                    expLink
                };
            })()
            """)
            print(f"[{i+1}s] Deploy status: {status.get('status')} | Hash: {status.get('hash')}")
            if status.get("status") in ["ACCEPTED", "FINALIZED"] and status.get("type") == "deploy":
                deploy_tx = status.get("hash")
                links = status.get("expLink", [])
                if links:
                    new_address = links[0].split("/address/")[-1]
                print(f"DEPLOYMENT SUCCESSFUL! Tx: {deploy_tx}, Address: {new_address}")
                break

        if not new_address:
            # Extract address from explorer links
            links = await ctrl.eval("""
            (() => Array.from(document.querySelectorAll('a[href*="/address/0x"]')).map(a => a.href))()
            """)
            if links:
                new_address = links[0].split("/address/")[-1]
                print("Extracted address:", new_address)

        # 7. EXECUTE CASE B (MISMATCH)
        print("\n--- EXECUTING CASE B (MISMATCH) ---")
        # Open analyze method
        await ctrl.eval("""
        (() => {
            const btn = Array.from(document.querySelectorAll('span, div, button'))
                .find(el => el.innerText && el.innerText.trim() === 'analyze');
            if (btn) (btn.closest('button, div[role="button"]') || btn).click();
        })()
        """)
        await asyncio.sleep(1)

        # Fill inputs for Case B
        await ctrl.eval(f"""
        (() => {{
            const repoInput = document.querySelector('input[name="repo_url"]');
            const privacyInput = document.querySelector('input[name="privacy_url"]');
            if (repoInput && privacyInput) {{
                repoInput.value = "{CASE_B_REPO}";
                repoInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                repoInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

                privacyInput.value = "{CASE_B_PRIVACY}";
                privacyInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                privacyInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }})()
        """)
        await asyncio.sleep(1)

        # Click Send Transaction
        await ctrl.eval("""
        (() => {
            const sendBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send Transaction'));
            if (sendBtn) sendBtn.click();
        })()
        """)
        print("Sent Case B transaction. Waiting for consensus and execution...")

        case_b_tx = None
        case_b_result = None
        for i in range(45):
            await asyncio.sleep(1)
            tx_info = await ctrl.eval("""
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
            print(f"[{i+1}s] Case B status: {tx_info.get('status')} | Hash: {tx_info.get('hash')}")
            if tx_info.get("status") in ["ACCEPTED", "FINALIZED"] and tx_info.get("type") == "method":
                case_b_tx = tx_info.get("hash")
                case_b_result = tx_info.get("execResult")
                print("Case B Finalized!")
                print("GenVM Result:", case_b_result)
                print("GenVM Stderr:", tx_info.get("stderr"))
                break

        # 8. EXECUTE CASE A (MATCH)
        print("\n--- EXECUTING CASE A (MATCH) ---")
        # Ensure analyze is open
        await ctrl.eval("""
        (() => {
            const btn = Array.from(document.querySelectorAll('span, div, button'))
                .find(el => el.innerText && el.innerText.trim() === 'analyze');
            if (btn) (btn.closest('button, div[role="button"]') || btn).click();
        })()
        """)
        await asyncio.sleep(1)

        # Fill inputs for Case A
        await ctrl.eval(f"""
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
            }}
        }})()
        """)
        await asyncio.sleep(1)

        # Click Send Transaction
        await ctrl.eval("""
        (() => {
            const sendBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send Transaction'));
            if (sendBtn) sendBtn.click();
        })()
        """)
        print("Sent Case A transaction. Waiting for consensus and execution...")

        case_a_tx = None
        case_a_result = None
        for i in range(45):
            await asyncio.sleep(1)
            tx_info = await ctrl.eval("""
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
            print(f"[{i+1}s] Case A status: {tx_info.get('status')} | Hash: {tx_info.get('hash')}")
            if tx_info.get("status") in ["ACCEPTED", "FINALIZED"] and tx_info.get("type") == "method":
                case_a_tx = tx_info.get("hash")
                case_a_result = tx_info.get("execResult")
                print("Case A Finalized!")
                print("GenVM Result:", case_a_result)
                print("GenVM Stderr:", tx_info.get("stderr"))
                break

        print("\n=== COMPLETE RUN SUMMARY ===")
        print(f"Contract Address: {new_address}")
        print(f"Deployment Tx: {deploy_tx}")
        print(f"Case B Tx: {case_b_tx} | Result: {case_b_result}")
        print(f"Case A Tx: {case_a_tx} | Result: {case_a_result}")

if __name__ == "__main__":
    asyncio.run(main())
