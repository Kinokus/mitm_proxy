# save_cache.py — кладе відповіді у cache/<host>/<path>
from mitmproxy import http
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import hashlib
import os

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

def load_patterns_from_file(filename="allowed_patterns.txt"):
    patterns = []
    try:
        if not os.path.exists(filename):
            print(f"Pattern file '{filename}' not found, using default patterns.")
            pattern_lines = [r"\.png$"]
        else:
            with open(filename, encoding="utf-8") as f:
                pattern_lines = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]
        for pat in pattern_lines:
            patterns.append(re.compile(pat))
    except Exception as e:
        print(f"Error loading patterns: {e}")
        patterns = [ re.compile(r"\.png$") ]
    return patterns


def responseheaders(flow: http.HTTPFlow):
    """
    This hook runs BEFORE the response body is received.
    We disable streaming for responses we want to cache.
    """
    # Load allowed cache URL patterns
    allow_cache_url_patterns = load_patterns_from_file()
    
    # Check if URL matches our caching patterns
    if any(pattern.search(flow.request.url) for pattern in allow_cache_url_patterns):
        # Check for successful status codes
        if flow.response.status_code in (200, 203, 206, 304):
            # Disable streaming so content is buffered and available in response hook
            flow.response.stream = False
            print(f"[Buffering] {flow.request.url}")


def response(flow: http.HTTPFlow):
    # тільки успішні/кешовані типи; за бажанням розширте
    if flow.response.status_code not in (200, 203, 206, 304):
        return
    ct = (flow.response.headers.get("Content-Type") or "").lower()

    # Load allowed cache URL patterns from a file
    allow_cache_url_patterns = load_patterns_from_file()

    if not any(pattern.search(flow.request.url) for pattern in allow_cache_url_patterns):
        return

    print(f"Content-Type: {ct}\tURL: {flow.request.url}")
    

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
    print(f"Caching to {out}")
    

    print(f"Response content: {flow.response}")
    # Check if response content exists
    if flow.response.data.content is None:
        print(f"No content to cache for {flow.request.url}")
        return
    
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        # пишемо «сирі» байти
        out.write_bytes(flow.response.data.content)

    except (OSError, FileNotFoundError) as e:
        # Log error but don't crash - path might still be too long
        from mitmproxy import ctx
        ctx.log.warn(f"Failed to cache {flow.request.url}: {e}")
