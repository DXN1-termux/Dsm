from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .network import NetworkAgent
from .system import SystemAgent


HTML_PAGE = """<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>DSM v6 Localhost</title>
<style>
:root{--bg:#07111f;--panel:#0d1a2d;--panel2:#13233a;--txt:#e8f1ff;--muted:#8ba1c7;--acc:#6ae4ff;--line:#1f3557}
*{box-sizing:border-box}body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:radial-gradient(circle at top,#10233f, var(--bg));color:var(--txt)}
.wrap{max-width:1100px;margin:0 auto;padding:28px}header{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:20px}
.brand{font-size:28px;font-weight:800;letter-spacing:.5px}.tag{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:16px}
.card{background:linear-gradient(180deg,var(--panel),#0a1526);border:1px solid var(--line);border-radius:20px;padding:18px;box-shadow:0 12px 40px rgba(0,0,0,.25)}
.span4{grid-column:span 4}.span6{grid-column:span 6}.span12{grid-column:span 12}h2{margin:0 0 10px;font-size:18px}.muted{color:var(--muted)}
.kpi{font-size:40px;font-weight:800}.row{display:flex;gap:12px;flex-wrap:wrap}.pill{padding:8px 12px;border-radius:999px;background:var(--panel2);border:1px solid var(--line)}
input,button{border-radius:14px;border:1px solid var(--line);background:#0b1728;color:var(--txt);padding:12px 14px;font-size:15px}button{background:linear-gradient(180deg,#143156,#0e223d);cursor:pointer}
button:hover{transform:translateY(-1px)}pre{white-space:pre-wrap;word-break:break-word;background:#07111f;border:1px solid var(--line);border-radius:16px;padding:14px;min-height:220px}
@media(max-width:900px){.span4,.span6,.span12{grid-column:span 12}.brand{font-size:22px}}
</style>
</head>
<body>
<div class='wrap'>
  <header>
    <div>
      <div class='brand'>DSM v6 Localhost</div>
      <div class='tag'>Clean browser dashboard for system status and network recon</div>
    </div>
    <div class='pill'>Port: {port}</div>
  </header>

  <div class='grid'>
    <section class='card span4'>
      <h2>System</h2>
      <div class='kpi' id='cpu'>--</div>
      <div class='muted'>CPU load</div>
    </section>
    <section class='card span4'>
      <h2>Memory</h2>
      <div class='kpi' id='mem'>--</div>
      <div class='muted'>RAM usage</div>
    </section>
    <section class='card span4'>
      <h2>Disk</h2>
      <div class='kpi' id='disk'>--</div>
      <div class='muted'>Storage usage</div>
    </section>

    <section class='card span6'>
      <h2>Fast actions</h2>
      <div class='row'>
        <button onclick="runScan('quick')">Quick scan</button>
        <button onclick="runScan('service')">Service scan</button>
        <button onclick="runScan('intense')">Deep scan</button>
      </div>
      <div style='height:12px'></div>
      <input id='target' placeholder='Target IP or hostname' style='width:100%' />
    </section>

    <section class='card span6'>
      <h2>Toolbox</h2>
      <div id='tools' class='row'></div>
      <div class='muted' style='margin-top:10px'>Detected tools on this device</div>
    </section>

    <section class='card span12'>
      <h2>Output</h2>
      <pre id='output'>Ready.</pre>
    </section>
  </div>
</div>
<script>
async function refresh(){
  const r = await fetch('/api/status');
  const j = await r.json();
  document.getElementById('cpu').textContent = j.cpu_percent.toFixed(1) + '%';
  document.getElementById('mem').textContent = j.memory_percent.toFixed(1) + '%';
  document.getElementById('disk').textContent = j.disk_percent.toFixed(1) + '%';
  const tools = document.getElementById('tools');
  tools.innerHTML = '';
  for (const [k,v] of Object.entries(j.tools)) {
    const d = document.createElement('div'); d.className='pill'; d.textContent = k + ': ' + (v ? 'ready' : 'missing'); tools.appendChild(d);
  }
}
async function runScan(mode){
  const target = document.getElementById('target').value.trim();
  if(!target){ document.getElementById('output').textContent = 'Enter a target first.'; return; }
  const r = await fetch(`/api/scan?mode=${encodeURIComponent(mode)}&target=${encodeURIComponent(target)}`);
  const j = await r.json();
  document.getElementById('output').textContent = j.output || JSON.stringify(j, null, 2);
}
refresh(); setInterval(refresh, 3000);
</script>
</body>
</html>"""


class DashboardServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765) -> None:
        self.host = host
        self.port = port
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self.network = NetworkAgent()
        self.system = SystemAgent()

    def start(self) -> str:
        server = self

        class Handler(BaseHTTPRequestHandler):
            def _send(self, status: int, content_type: str, body: str | bytes) -> None:
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                if isinstance(body, str):
                    body = body.encode("utf-8")
                self.wfile.write(body)

            def do_GET(self) -> None:
                parsed = urlparse(self.path)
                if parsed.path == "/":
                    self._send(200, "text/html; charset=utf-8", HTML_PAGE.format(port=server.port))
                    return
                if parsed.path == "/api/status":
                    payload = server.network.system_status_payload()
                    self._send(200, "application/json", json.dumps(payload, indent=2))
                    return
                if parsed.path == "/api/scan":
                    qs = parse_qs(parsed.query)
                    target = qs.get("target", [""])[0]
                    mode = qs.get("mode", ["intense"])[0]
                    result = server.network.nmap_scan(target, mode=mode)
                    payload = {
                        "target": target,
                        "mode": mode,
                        "nmap_found": result.nmap_found,
                        "command": result.command,
                        "output": result.output,
                    }
                    self._send(200, "application/json", json.dumps(payload, indent=2))
                    return
                self._send(404, "text/plain; charset=utf-8", "Not found")

            def log_message(self, format: str, *args) -> None:
                return

        self._server = ThreadingHTTPServer((self.host, self.port), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return f"http://{self.host}:{self.port}"

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
