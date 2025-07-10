import os, platform, urllib.request, zipfile, shutil

def download_and_extract(urls, extract_to, bin_name):
    os.makedirs(extract_to, exist_ok=True)
    for url in urls:
        try:
            print(f"  ↳ Trying: {url}")
            zp = os.path.join(extract_to, "temp.zip")
            urllib.request.urlretrieve(url, zp)
            with zipfile.ZipFile(zp, "r") as z: z.extractall(extract_to)
            os.remove(zp)
            if platform.system().lower() == "linux":
                for root, _, files in os.walk(extract_to):
                    if bin_name in files:
                        os.chmod(os.path.join(root, bin_name), 0o755)
            return True
        except Exception as e:
            print(f"    ✘ {e}")
    return False

def detect_arch():
    sys, mach = platform.system().lower(), platform.machine().lower()
    if os.path.exists("/data/data/com.termux"):
        return "linux_arm64"
    if sys == "linux":
        return "linux_x64" if "x86_64" in mach else "linux_arm64"
    if sys == "windows":
        return "win_x64"
    if sys == "darwin":
        return "mac_arm64" if "arm64" in mach else "mac_x64"
    raise RuntimeError(f"Unsupported platform: {sys}/{mach}")

def install_chromium():
    print("[*] Detecting platform/architecture...")
    tag = detect_arch()
    print(f"[*] Platform → {tag}")

    base = os.getcwd()
    chrome_dir = os.path.join(base, "chrome")
    shutil.rmtree(chrome_dir, ignore_errors=True)

    chrome_map = {
        "linux_x64": [
            # Chromium 138 & 134 snapshots
            "https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1462098/chrome-linux.zip",
            "https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1458563/chrome-linux.zip",
        ],
        "linux_arm64": [
            "https://github.com/codes4education/termux-chromium-arm64/releases/download/v1.0/chrome-arm64.zip",
            "https://archive.org/download/chromium-arm64/chromium-arm64.zip"
        ],
        "win_x64": [
            "https://github.com/macchrome/winchrome/releases/download/v138.0.7174.0-r1458563/Chrome-bin.zip",
            "https://github.com/macchrome/winchrome/releases/download/v134.0.6742.84-r1250166/Chrome-bin.zip"
        ],
        "mac_x64": [
            "https://github.com/ungoogled-software/ungoogled-chromium-macos/releases/download/138.0.7204.96-1/ungoogled-chromium_138.0.7204.96-1.mac_x64.zip"
        ],
        "mac_arm64": [
            "https://github.com/ungoogled-software/ungoogled-chromium-macos/releases/download/138.0.7204.96-1/ungoogled-chromium_138.0.7204.96-1.mac_arm64.zip"
        ],
    }

    urls = chrome_map.get(tag)
    if not urls or not download_and_extract(urls, chrome_dir, "chrome" + (".exe" if "win" in tag else "")):
        raise RuntimeError("❌ Chromium download failed for all links.")
    print("[✓] Chromium ready.")
