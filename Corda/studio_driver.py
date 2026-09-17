"""
Corda Studio CDP Inspector & Automation Driver
Connects via Chrome DevTools Protocol to inspect and interact with the GenLayer Studio tab.
"""

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

async def send_cdp_command(ws, method, params=None, msg_id=1):
    req = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(req))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data

async def evaluate_js(ws, script, msg_id=1):
    res = await send_cdp_command(ws, "Runtime.evaluate", {
        "expression": script,
        "returnByValue": True,
        "awaitPromise": True
    }, msg_id=msg_id)
    return res.get("result", {}).get("result", {}).get("value")

async def inspect_studio():
    tab = await get_studio_tab()
    if not tab:
        print("ERROR: GenLayer Studio tab not found in CDP list.")
        return

    ws_url = tab.get("webSocketDebuggerUrl")
    print(f"Connecting to Studio tab at {ws_url}...")
    async with websockets.connect(ws_url) as ws:
        # Check current URL and Title
        url = await evaluate_js(ws, "window.location.href", 1)
        title = await evaluate_js(ws, "document.title", 2)
        body_text = await evaluate_js(ws, "document.body.innerText", 3)
        print(f"Page URL: {url}")
        print(f"Page Title: {title}")
        print("Page Body Excerpt (first 500 chars):")
        print("---")
        print((body_text or "")[:500])
        print("---")

        # Check for buttons, modals, or file upload elements
        elements_info = await evaluate_js(ws, """
        (() => {
            const buttons = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
            const inputs = Array.from(document.querySelectorAll('input')).map(i => i.placeholder || i.name || i.type);
            const textContent = document.body.innerText;
            const hasCloudflare = textContent.includes('challenge') || textContent.includes('Turnstile') || !!document.querySelector('iframe[src*="challenge"]');
            return { buttons, inputs, hasCloudflare };
        })()
        """, 4)
        print("Elements info:", json.dumps(elements_info, indent=2))

if __name__ == "__main__":
    asyncio.run(inspect_studio())
