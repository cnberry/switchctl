from __future__ import annotations

import socket


def reachability(host: str, port: int, timeout_s: float = 1.5) -> dict:
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return {"ok": True, "host": host, "port": port}
    except OSError as exc:
        return {"ok": False, "host": host, "port": port, "error": str(exc)}
