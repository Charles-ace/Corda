# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class Probe(gl.Contract):
    def __init__(self):
        pass

    @gl.public.write
    def test_probe(self, url: str) -> str:
        def run_nondet():
            resp = gl.nondet.web.get(url)
            resp_attrs = dir(resp)
            web_attrs = dir(gl.nondet.web)
            
            # Extract text safely
            text_val = ""
            if hasattr(resp, 'text'):
                text_val = str(resp.text)
            elif hasattr(resp, 'body'):
                text_val = str(resp.body)
            elif hasattr(resp, 'content'):
                text_val = str(resp.content)
            else:
                text_val = str(resp)

            summary = gl.nondet.exec_prompt(f"Say OK if text is received: {text_val[:50]}")
            return f"RESP_ATTRS: {resp_attrs} | WEB_ATTRS: {web_attrs} | LLM: {summary}"

        result = gl.eq_principle.prompt_comparative(
            run_nondet,
            principle="The output must contain RESP_ATTRS, WEB_ATTRS, and LLM confirmation."
        )
        return result
