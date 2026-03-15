#!/usr/bin/env python3
"""Universal MCP daemon wrapper for Claude Code."""
import os, socket, subprocess, sys, time
from pathlib import Path

PORT = int(os.environ.get("STM32_PORT", "8765"))
STATE_DIR = Path.home() / ".stm32-mcp"
PID_FILE = STATE_DIR / "daemon.pid"
LOG_FILE = STATE_DIR / "daemon.log"
STARTUP_TIMEOUT = 180

def is_port_open():
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=0.5):
            return True
    except OSError:
        return False

def is_daemon_alive():
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)
        return True
    except (ValueError, OSError):
        return False

def find_mcp_proxy():
    """Find mcp-proxy in the same environment."""
    import shutil
    proxy = shutil.which("mcp-proxy")
    if proxy:
        return proxy
    # Try relative to sys.executable
    venv_bin = Path(sys.executable).parent
    candidate = venv_bin / "mcp-proxy"
    if candidate.exists():
        return str(candidate)
    raise RuntimeError("mcp-proxy not found. Install with: pip install mcp-proxy")

def start_daemon():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    # Find the package root (where mcp_server module lives)
    import mcp_server
    pkg_root = str(Path(mcp_server.__file__).parent.parent)

    env = {**os.environ, "STM32_SERVER_MODE": "network"}
    with open(LOG_FILE, "a") as log:
        proc = subprocess.Popen(
            [sys.executable, "-m", "mcp_server.server"],
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=log,
            start_new_session=True,
            cwd=pkg_root,
        )
    PID_FILE.write_text(str(proc.pid))

def wait_for_ready():
    deadline = time.time() + STARTUP_TIMEOUT
    while time.time() < deadline:
        if is_port_open():
            return True
        time.sleep(1)
    return False

def main():
    if not is_port_open():
        if not is_daemon_alive():
            start_daemon()
        if not wait_for_ready():
            sys.stderr.write(f"STM32 MCP daemon failed to start within {STARTUP_TIMEOUT}s. Check {LOG_FILE}\n")
            sys.exit(1)

    proxy = find_mcp_proxy()
    os.execv(proxy, [proxy, "--log-level", "ERROR", "--transport", "sse", f"http://127.0.0.1:{PORT}/sse"])

if __name__ == "__main__":
    main()
