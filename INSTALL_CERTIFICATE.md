# 🔐 Install mitmproxy Certificate in Firefox

## Why is this needed?

Mitmproxy intercepts HTTPS traffic by acting as a "man-in-the-middle" proxy. Firefox needs to trust mitmproxy's certificate authority to allow this.

## 📍 Certificate Location

Your mitmproxy CA certificate is located at:
```
%USERPROFILE%\.mitmproxy\mitmproxy-ca-cert.cer
```

Full path: `C:\Users\user\.mitmproxy\mitmproxy-ca-cert.cer`

## 🚀 Installation Steps

### For Chrome / Edge / Windows Browsers (EASIEST)

**Just double-click:** `install_cert_windows.cmd`

This will:
1. Install the certificate to Windows Trusted Root CA store
2. Automatically work for Chrome, Edge, Internet Explorer, and all Windows apps
3. You'll see a security warning - click **YES** to install

**OR manually:**
1. Double-click `C:\Users\user\.mitmproxy\mitmproxy-ca-cert.cer`
2. Click **Install Certificate...**
3. Select **Current User** → Click **Next**
4. Select **Place all certificates in the following store** → Click **Browse**
5. Select **Trusted Root Certification Authorities** → Click **OK**
6. Click **Next** → Click **Finish**
7. Click **Yes** on the security warning
8. Restart Chrome/Edge

---

## 🚀 Installation Steps for Firefox

### Method 1: Direct Install (Easiest)

1. **Open Firefox**

2. **Go to Settings** → Type in address bar:
   ```
   about:preferences#privacy
   ```

3. **Scroll down** to "Certificates" section

4. **Click "View Certificates"** button

5. **Go to "Authorities" tab**

6. **Click "Import..."** button

7. **Browse to** `C:\Users\user\.mitmproxy\mitmproxy-ca-cert.cer`

8. **Check both boxes:**
   - ✅ Trust this CA to identify websites
   - ✅ Trust this CA to identify email users

9. **Click OK**

10. **Restart Firefox**

### Method 2: Alternative - Visit mitm.it

1. Make sure mitmproxy is running
2. Set Firefox proxy to `127.0.0.1:8080`
3. Visit: http://mitm.it
4. Click on the Firefox/Windows icon to download certificate
5. Follow installation prompts

## ✅ Verify Installation

After installing:
1. Restart Firefox
2. Configure proxy: `127.0.0.1:8080`
3. Visit any HTTPS site
4. Should work without certificate errors!

## 🔧 Troubleshooting

If you still get errors:
- Make sure mitmproxy is running
- Verify Firefox proxy is set to `127.0.0.1:8080`
- Try restarting Firefox
- Check that the certificate is actually imported in Firefox settings

## 📝 Notes

- This certificate is only valid for intercepting your own traffic
- It's stored locally on your machine
- You may need to repeat this for other browsers (Chrome, Edge, etc.)

