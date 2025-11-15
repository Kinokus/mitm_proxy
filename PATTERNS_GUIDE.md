# 📋 Cache Patterns Configuration Guide

## Overview

The caching proxy uses two types of filters:

1. **URL Patterns** (`allowed_patterns.txt`) - Match URLs to cache
2. **Content-Type Patterns** (`content_type_patterns.txt`) - Match by HTTP Content-Type header

## 📝 URL Patterns (`allowed_patterns.txt`)

### Format
- One regex pattern per line
- Lines starting with `#` are comments
- Empty lines are ignored
- Uses Python regex syntax

### Current Active Patterns

```regex
gw\.yad2                    # Match URLs containing "gw.yad2"
img\.yad2.*\.jpg$          # Match JPG images from img.yad2
img\.yad2.*\.jpeg$         # Match JPEG images from img.yad2
img\.yad2.*\.png$          # Match PNG images from img.yad2
img\.yad2.*\.webp$         # Match WebP images from img.yad2
```

### Pattern Examples

#### Match specific domain
```regex
^https://example\.com/
cdn\.example\.com
static\.example\.com
```

#### Match specific paths
```regex
/api/images/
/static/css/
/cdn/
```

#### Match file extensions
```regex
\.css$              # CSS files
\.js$               # JavaScript files
\.woff2?$          # Font files (.woff, .woff2)
\.svg$             # SVG images
\.(jpg|jpeg|png|webp|gif)$  # All image types
```

#### Match multiple domains
```regex
(cdn|static|assets)\.example\.com
```

#### Match query parameters
```regex
\?size=large
\?format=json
```

## 🎨 Content-Type Patterns (`content_type_patterns.txt`)

### Format
- One substring per line
- Lines starting with `#` are comments
- Matches if substring found in Content-Type header
- Case-insensitive matching

### Common Content Types

#### Images
```
image/              # All images
image/jpeg         # JPEG only
image/png          # PNG only
image/webp         # WebP only
```

#### Web Content
```
text/html
text/css
javascript
application/javascript
```

#### Fonts
```
font/
application/font
application/x-font-woff
```

#### Data Formats
```
application/json
application/xml
text/xml
```

#### Binary Files
```
application/octet-stream
application/pdf
application/zip
```

## 🔧 How Filtering Works

1. **Status Code Check**: Only cache 200, 203, 206, 304 responses
2. **URL Pattern Match**: URL must match at least one pattern in `allowed_patterns.txt`
3. **Content-Type Match** (if enabled): Content-Type must match patterns in `content_type_patterns.txt`

## 📊 Testing Patterns

### Test a URL pattern in Python
```python
import re
pattern = re.compile(r"img\.yad2.*\.jpg$")
test_url = "https://img.yad2.co.il/image.jpg"
if pattern.search(test_url):
    print("Match!")
```

### Common Regex Syntax
```
^       - Start of string
$       - End of string
.       - Any character (use \. for literal dot)
*       - Zero or more
+       - One or more
?       - Zero or one
[]      - Character class
()      - Grouping
|       - OR
\       - Escape special characters
```

## 💡 Tips

1. **Start Specific**: Begin with specific patterns and expand as needed
2. **Test First**: Test patterns with a few URLs before deploying
3. **Use Comments**: Document why each pattern exists
4. **Monitor Logs**: Check mitmweb logs to see what's being cached
5. **Avoid Broad Patterns**: Patterns like `.*` will match everything

## 🚀 Examples by Use Case

### Cache all images from any domain
```regex
\.(jpg|jpeg|png|gif|webp|svg)(\?.*)?$
```

### Cache specific CDN
```regex
^https://cdn\.example\.com/
```

### Cache API responses
```regex
/api/v1/images/
/api/v1/static/
```

### Cache fonts and CSS
```regex
\.(woff2?|ttf|eot)$
\.(css|scss)$
```

## 📂 File Locations

- **URL Patterns**: `allowed_patterns.txt`
- **Content Types**: `content_type_patterns.txt`
- **Main Script**: `awesome_cache.py`
- **Cached Files**: `cache/` directory

## 🔄 Reloading Configuration

Changes to pattern files are loaded automatically for each new request.
No need to restart mitmproxy!

## ⚠️ Important Notes

- Patterns are regex, not wildcards (use `\.` not just `.`)
- One pattern per line
- Comments start with `#`
- Patterns are case-sensitive by default
- Test patterns before production use


