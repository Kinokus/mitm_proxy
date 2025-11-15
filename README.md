# 🚀 Awesome Cache - MITM Proxy Caching System

A powerful caching proxy using mitmproxy to intercept and cache HTTP/HTTPS traffic based on configurable patterns.

## 📋 Features

- ✅ Cache HTTP/HTTPS responses to local disk
- ✅ Configurable URL pattern matching (regex)
- ✅ Content-Type filtering
- ✅ Automatic path shortening for Windows compatibility
- ✅ Hash-based file naming for uniqueness
- ✅ Web UI (mitmweb) or command-line (mitmdump) mode
- ✅ Real-time monitoring and logs

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install SSL Certificate

For HTTPS interception to work, you need to install mitmproxy's certificate:

**For Chrome/Edge (Windows):**
- Double-click: `install_cert_windows.cmd`
- Click **YES** on security warning
- Restart browser

**For Firefox:**
- See detailed instructions in `INSTALL_CERTIFICATE.md`
- Or double-click: `open_firefox_certificates.cmd`

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

Double-click: `run_mitmweb.cmd`

- Web interface: http://127.0.0.1:8081
- Proxy address: 127.0.0.1:8080

### Option 2: Command Line

Double-click: `run_mitmdump.cmd`

- Command-line output only
- Proxy address: 127.0.0.1:8080

### Configure Your Application

Set proxy in your browser/application:
- Host: `127.0.0.1`
- Port: `8080`

## ⚙️ Configuration

### URL Patterns (`allowed_patterns.txt`)

Define which URLs to cache using regex patterns:

```regex
# Cache images from yad2
img\.yad2.*\.jpg$
img\.yad2.*\.png$

# Cache from specific CDN
cdn\.example\.com

# Cache all images
\.(jpg|jpeg|png|gif|webp)$
```

See `PATTERNS_GUIDE.md` for complete documentation and examples.

### Content-Type Patterns (`content_type_patterns.txt`)

Filter by HTTP Content-Type header:

```
# Images
image/

# JSON data
application/json

# Web assets
text/css
javascript
```

### Default Patterns (`default_patterns.txt`)

Template file with common patterns. Copy desired patterns to `allowed_patterns.txt`.

## 📂 Output Structure

Cached files are saved to:
```
cache/
├── example.com/
│   ├── images/
│   │   └── photo_abc123.jpg
│   └── api/
│       └── data_def456.json
└── cdn.example.com/
    └── assets/
        └── style_ghi789.css
```

## 📖 Documentation

- **`INSTALL_CERTIFICATE.md`** - SSL certificate installation guide
- **`PATTERNS_GUIDE.md`** - Complete pattern configuration reference
- **`default_patterns.txt`** - Template with common patterns

## 🔧 How It Works

1. **Start Proxy**: Run `run_mitmweb.cmd` or `run_mitmdump.cmd`
2. **Configure Browser**: Set proxy to 127.0.0.1:8080
3. **Browse**: Visit websites normally
4. **Filtering**: 
   - URL is checked against `allowed_patterns.txt`
   - Status code must be 200, 203, 206, or 304
   - (Optional) Content-Type is checked
5. **Caching**: Matching responses saved to `cache/` directory
6. **Monitoring**: View traffic in web UI or console logs

## 🎯 Common Use Cases

### Cache all images from a specific site
```regex
example\.com/.*\.(jpg|png|gif)$
```

### Cache API responses
```regex
/api/v1/images/
/api/v1/static/
```

### Cache CDN content
```regex
^https://cdn\.example\.com/
```

### Cache everything (use with caution!)
```regex
.*
```

## 🔍 Monitoring

### Web Interface (mitmweb)
- Open: http://127.0.0.1:8081
- View: Real-time traffic, request/response details
- Filter: By host, path, content-type

### Command Line (mitmdump)
- Console output shows cached URLs
- Format: `Content-Type: [type]    URL: [url]`

## 🛡️ Security Notes

- mitmproxy's certificate allows HTTPS interception
- Only install certificate on your own machines
- Certificate is stored in: `%USERPROFILE%\.mitmproxy\`
- Don't share the certificate with others

## 📦 Files Overview

| File | Purpose |
|------|---------|
| `awesome_cache.py` | Main caching script |
| `run_mitmweb.cmd` | Start with web UI |
| `run_mitmdump.cmd` | Start command-line mode |
| `install_cert_windows.cmd` | Install certificate for Windows browsers |
| `allowed_patterns.txt` | Active URL patterns (edit this) |
| `default_patterns.txt` | Pattern templates (reference only) |
| `content_type_patterns.txt` | Content-Type filters |
| `requirements.txt` | Python dependencies |

## 🐛 Troubleshooting

### Certificate Errors
- Install certificate using `install_cert_windows.cmd`
- See `INSTALL_CERTIFICATE.md` for detailed steps

### Port Already in Use
- Change port in CMD files from 8080 to another (e.g., 8081, 9090)

### Path Too Long Error
- Patterns automatically shortened with hash suffixes
- If still occurs, shorten URL patterns in `allowed_patterns.txt`

### Nothing Being Cached
- Check patterns in `allowed_patterns.txt` are correct regex
- Verify URLs match patterns (check logs)
- Ensure status code is 200/203/206/304

## 🔄 Updates

Patterns are loaded on each request - no restart needed!
- Edit `allowed_patterns.txt`
- Changes take effect immediately

## 📝 License

Free to use and modify for personal and commercial purposes.

## 🤝 Contributing

Feel free to:
- Add new patterns to `default_patterns.txt`
- Improve error handling
- Add features
- Report issues

---

**Happy Caching! 🎉**
