import urllib.request
import json
import asyncio
import websockets
import base64

CDP_HTTP = "http://127.0.0.1:9223"

async def test_frontend():
    # Create or find tab for localhost:8080
    req = urllib.request.Request(f"{CDP_HTTP}/json/new?http://localhost:8080/", method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab = json.loads(resp.read().decode())
    
    ws_url = tab.get("webSocketDebuggerUrl")
    print(f"Connected to tab: {tab.get('id')}")

    async with websockets.connect(ws_url) as ws:
        # Wait for load
        await asyncio.sleep(2)

        # Check document title & headline
        def send_cmd(method, params=None, msg_id=1):
            return ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))

        async def recv_resp(msg_id):
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                if data.get("id") == msg_id:
                    return data

        await send_cmd("Runtime.evaluate", {"expression": "document.title", "returnByValue": True}, 1)
        r1 = await recv_resp(1)
        title = r1.get("result", {}).get("result", {}).get("value")
        print("Page Title:", title)

        await send_cmd("Runtime.evaluate", {"expression": "document.querySelector('h1').innerText", "returnByValue": True}, 2)
        r2 = await recv_resp(2)
        h1 = r2.get("result", {}).get("result", {}).get("value")
        print("H1 Text:\n", h1)

        # Test switching to Console
        await send_cmd("Runtime.evaluate", {"expression": "showView('console')", "returnByValue": True}, 3)
        await recv_resp(3)
        await asyncio.sleep(0.5)

        await send_cmd("Runtime.evaluate", {"expression": "document.getElementById('view-console').classList.contains('hidden')", "returnByValue": True}, 4)
        r4 = await recv_resp(4)
        is_hidden = r4.get("result", {}).get("result", {}).get("value")
        print("Console hidden state after showView('console'):", is_hidden)

        # Test loading preset
        await send_cmd("Runtime.evaluate", {"expression": "loadPreset('case_b'); [document.getElementById('repo_url').value, document.getElementById('privacy_url').value]", "returnByValue": True}, 5)
        r5 = await recv_resp(5)
        presets = r5.get("result", {}).get("result", {}).get("value")
        print("Preset values loaded:", presets)

        # Capture screenshot of Console
        await send_cmd("Page.captureScreenshot", {"format": "jpeg", "quality": 85}, 6)
        r6 = await recv_resp(6)
        img_data = r6.get("result", {}).get("data")
        if img_data:
            with open("C:/Builds/Genlayer/Corda/screenshot_console.jpg", "wb") as f:
                f.write(base64.b64decode(img_data))
            print("Captured screenshot_console.jpg successfully!")

        # Switch back to Marketing
        await send_cmd("Runtime.evaluate", {"expression": "showView('marketing')", "returnByValue": True}, 7)
        await recv_resp(7)
        await asyncio.sleep(0.5)

        # Capture screenshot of Marketing Hero
        await send_cmd("Page.captureScreenshot", {"format": "jpeg", "quality": 85}, 8)
        r8 = await recv_resp(8)
        img_data_mkt = r8.get("result", {}).get("data")
        if img_data_mkt:
            with open("C:/Builds/Genlayer/Corda/screenshot_marketing.jpg", "wb") as f:
                f.write(base64.b64decode(img_data_mkt))
            print("Captured screenshot_marketing.jpg successfully!")

asyncio.run(test_frontend())
