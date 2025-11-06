# save_cache.py — кладе відповіді у cache/<host>/<path>
from mitmproxy import http
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import hashlib

SAFE = re.compile(r"[^A-Za-z0-9._-]+")

def safe_name(s: str, max_len: int = 80) -> str:
    """Convert string to safe filename, with hash suffix if truncated."""
    s = unquote(s)
    safe = SAFE.sub("_", s)
    
    if len(safe) <= max_len:
        return safe or "_"
    
    # If too long, truncate and add hash to ensure uniqueness
    hash_suffix = hashlib.md5(s.encode()).hexdigest()[:8]
    return safe[:max_len-9] + "_" + hash_suffix

def response(flow: http.HTTPFlow):
    # тільки успішні/кешовані типи; за бажанням розширте
    if flow.response.status_code not in (200, 203, 206):
        return
    ct = (flow.response.headers.get("Content-Type") or "").lower()
    # приклад: кешуємо html, css, js, зображення, шрифти
    if not any(x in ct for x in (
        "text/html", "text/css", "javascript", "application/javascript",
        "image/", "font/", "application/font", "application/octet-stream"
    )):
        return

    u = urlsplit(flow.request.url)
    host = safe_name(u.hostname or "unknown")
    path = u.path or "/"
    # додаємо ім’я файлу; якщо шлях закінчується на '/', називаємо index
    if path.endswith("/"):
        fname = "index"
        dpath = path
    else:
        dpath, _, fname = path.rpartition("/")
        dpath = dpath + "/"
    # додаємо розширення за content-type, якщо у файлу немає
    if "." not in fname:
        if "html" in ct: fname += ".html"
        elif "css" in ct: fname += ".css"
        elif "javascript" in ct: fname += ".js"

    # кодуємо query у суфікс, щоб розрізняти варіанти
    q = ("_" + safe_name(u.query, max_len=40)) if u.query else ""
    # Use shorter limits for path components to avoid Windows path length issues
    rel = f"{safe_name(dpath, max_len=60).strip('_')}/{safe_name(fname, max_len=60)}{q}"
    rel = rel.replace("//", "/")

    out = Path("cache") / host / rel
    
    try:
        out.parent.mkdir(parents=True, exist_ok=True)

        # пишемо «сирі» байти
        out.write_bytes(flow.response.content)

        # опціонально — метадані (заголовки) поряд
        meta = out.with_suffix(out.suffix + ".headers.txt")
        meta.write_text(
            f"URL: {flow.request.url}\n"
            f"Status: {flow.response.status_code}\n"
            + "\n".join(f"{k}: {v}" for k, v in flow.response.headers.items()),
            encoding="utf-8"
        )
    except (OSError, FileNotFoundError) as e:
        # Log error but don't crash - path might still be too long
        from mitmproxy import ctx
        ctx.log.warn(f"Failed to cache {flow.request.url}: {e}")
