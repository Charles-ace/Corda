import urllib.request
import json
import asyncio
import websockets
import base64

CDP_HTTP = "http://127.0.0.1:9223"

async def test_audit():
    # Find localhost:8080 tab
    resp = urllib.request.urlopen(f"{CDP_HTTP}/json/list")
    tabs = json.loads(resp.read().decode())
    tab = next((t for t in tabs if "localhost:8080" in t.get("url", "")), None)
    if not tab:
        print("Tab not found")
        return

    ws_url = tab.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url) as ws:
        def send_cmd(method, params=None, msg_id=1):
            return ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))

        async def recv_resp(msg_id):
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                if data.get("id") == msg_id:
                    return data

        # Ensure we are in console view and trigger audit for Case A
        await send_cmd("Runtime.evaluate", {"expression": "showView('console'); loadPreset('case_a'); document.getElementById('audit-form').requestSubmit();", "returnByValue": True}, 1)
        await recv_resp(1)
        print("Triggered audit form submit...")

        # Wait for consensus steps and response
        await asyncio.sleep(3.5)

        # Check result text
        await send_cmd("Runtime.evaluate", {"expression": "[document.getElementById('verdict-title').innerText, document.getElementById('res-tx').innerText]", "returnByValue": True}, 2)
        r2 = await recv_resp(2)
        res = r2.get("result", {}).get("result", {}).get("value")
        print("Audit Result on-screen:", res)

        # Screenshot result
        await send_cmd("Page.captureScreenshot", {"format": "jpeg", "quality": 85}, 3)
        r3 = await recv_resp(3)
        img_data = r3.get("result", {}).get("data")
        if img_data:
            with open("C:/Builds/Genlayer/Corda/screenshot_audit_result.jpg", "wb") as f:
                f.write(base64.b64decode(img_data))
            print("Captured screenshot_audit_result.jpg!")

asyncio.run(test_audit())
