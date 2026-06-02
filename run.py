"""
run.py
──────
Starts the Trip Advisor multi-agent application.

Launches two processes:
  1. Neuro SAN HTTP server  — runs the agent network (port 8080)
  2. nsflow UI              — web chat interface + API  (port 4173)

Usage:
    python run.py

Then open http://localhost:5173 (React frontend)
  OR  http://localhost:4173 (nsflow built-in UI)
"""

import ctypes
import os
import signal
import subprocess
import sys
import threading
import time

from dotenv import load_dotenv


def short_path(long_path: str) -> str:
    """
    Return the Windows 8.3 short path (no spaces) for a given path.
    This is needed because neuro-san splits AGENT_MANIFEST_FILE on spaces,
    so any path containing spaces would be broken without this conversion.
    Falls back to the original path on non-Windows systems.
    """
    if sys.platform != "win32":
        return long_path
    buf = ctypes.create_unicode_buffer(512)
    ctypes.windll.kernel32.GetShortPathNameW(long_path, buf, 512)
    return buf.value or long_path


# ── Load .env from this directory ─────────────────────────────────────────────
ROOT_DIR       = os.path.dirname(os.path.abspath(__file__))
# short_path only the DIRECTORY — never the filename.
# The neuro-san server splits AGENT_MANIFEST_FILE on spaces, so the directory
# must have no spaces. But it also checks file_path.endswith(".hocon"), so the
# filename must stay intact (short-path would truncate "manifest.hocon" → "MANIFE~1.HOC").
ROOT_DIR_SHORT = short_path(ROOT_DIR)
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# ── Environment setup ──────────────────────────────────────────────────────────
os.environ["PYTHONPATH"]            = ROOT_DIR_SHORT
os.environ["AGENT_MANIFEST_FILE"]   = os.path.join(ROOT_DIR_SHORT, "manifest.hocon")
os.environ["AGENT_TOOL_PATH"]       = ROOT_DIR_SHORT
os.environ["NEURO_SAN_SERVER_CONNECTION"]          = "http"
os.environ["NEURO_SAN_SERVER_HOST"]                = os.getenv("NEURO_SAN_SERVER_HOST", "localhost")
os.environ["NEURO_SAN_SERVER_HTTP_PORT"]           = os.getenv("NEURO_SAN_SERVER_HTTP_PORT", "8080")
os.environ["NSFLOW_HOST"]                          = os.getenv("NSFLOW_HOST", "localhost")
os.environ["NSFLOW_PORT"]                          = os.getenv("NSFLOW_PORT", "4173")
os.environ["AGENT_MANIFEST_UPDATE_PERIOD_SECONDS"] = "5"
os.environ["LOG_LEVEL"]                            = "info"

# Thinking file (where agents log their internal reasoning)
THINKING_DIR = os.path.join(ROOT_DIR, "logs", "thinking_dir")
os.makedirs(THINKING_DIR, exist_ok=True)
os.environ["THINKING_DIR"]  = os.path.join(ROOT_DIR_SHORT, "logs", "thinking_dir")
os.environ["THINKING_FILE"] = os.path.join(ROOT_DIR_SHORT, "logs", "agent_thinking.txt")

HTTP_PORT   = int(os.environ["NEURO_SAN_SERVER_HTTP_PORT"])
NSFLOW_HOST = os.environ["NSFLOW_HOST"]
NSFLOW_PORT = int(os.environ["NSFLOW_PORT"])

os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)

print("\n" + "=" * 55)
print("  Trip Advisor — starting up")
print("=" * 55)
print(f"  PYTHONPATH        : {ROOT_DIR}")
print(f"  AGENT_MANIFEST    : {os.environ['AGENT_MANIFEST_FILE']}")
print(f"  AGENT_TOOL_PATH   : {os.environ['AGENT_TOOL_PATH']}")
print(f"  Neuro SAN server  : http://localhost:{HTTP_PORT}")
print(f"  nsflow UI         : http://{NSFLOW_HOST}:{NSFLOW_PORT}")
print("=" * 55 + "\n")

server_process = None
nsflow_process = None


def stream_output(pipe, log_path, prefix):
    """Forward subprocess stdout/stderr to console and log file."""
    with open(log_path, "a", encoding="utf-8") as log:
        for line in iter(pipe.readline, ""):
            msg = f"[{prefix}] {line.rstrip()}"
            print(msg)
            log.write(msg + "\n")
    pipe.close()


def start_process(command, name, log_filename):
    """Start a subprocess and stream its output."""
    log_path = os.path.join(ROOT_DIR, "logs", log_filename)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Starting {name}...\n")

    kwargs = dict(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )
    if sys.platform != "win32":
        kwargs["start_new_session"] = True

    proc = subprocess.Popen(command, **kwargs)
    print(f"Started {name} with PID {proc.pid}")

    threading.Thread(target=stream_output, args=(proc.stdout, log_path, name), daemon=True).start()
    threading.Thread(target=stream_output, args=(proc.stderr, log_path, name), daemon=True).start()
    return proc


def signal_handler(signum, frame):
    print("\nShutting down...")
    if server_process:
        server_process.terminate()
    if nsflow_process:
        nsflow_process.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT,  signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ── Start Neuro SAN server ─────────────────────────────────────────────────────
server_process = start_process(
    command=[sys.executable, "-u", "-m",
             "neuro_san.service.main_loop.server_main_loop",
             "--http_port", str(HTTP_PORT)],
    name="NeuroSan",
    log_filename="server.log",
)
print(f"Neuro SAN server started on port {HTTP_PORT}")

# Give the server a moment before starting nsflow
time.sleep(2)

# ── Start nsflow UI ────────────────────────────────────────────────────────────
nsflow_process = start_process(
    command=[sys.executable, "-u", "-m",
             "uvicorn", "nsflow.backend.main:app",
             "--host", NSFLOW_HOST,
             "--port", str(NSFLOW_PORT),
             "--reload"],
    name="nsflow",
    log_filename="nsflow.log",
)
print(f"nsflow UI started on http://{NSFLOW_HOST}:{NSFLOW_PORT}")

print("\n" + "=" * 55)
print("  Both services running. Press Ctrl+C to stop.")
print(f"  React frontend : http://localhost:5173")
print(f"  nsflow UI      : http://{NSFLOW_HOST}:{NSFLOW_PORT}")
print("=" * 55 + "\n")

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
        # Restart server if it crashes
        if server_process.poll() is not None:
            print("[!] Neuro SAN server stopped unexpectedly. Restarting...")
            server_process = start_process(
                command=[sys.executable, "-u", "-m",
                         "neuro_san.service.main_loop.server_main_loop",
                         "--http_port", str(HTTP_PORT)],
                name="NeuroSan",
                log_filename="server.log",
            )
except KeyboardInterrupt:
    signal_handler(None, None)
