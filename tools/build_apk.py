#!/usr/bin/env python3
"""Baut aus einer Web-App (index.html) eine signierte Android-APK.

Die App läuft offline in einer WebView. Benötigt: Android SDK (platform 34,
build-tools 34.0.0), JDK, Python mit Pillow.

    python3 tools/build_apk.py apps/haltepunkt-klavier

Umgebungsvariablen: ANDROID_HOME (Standard /opt/android),
KEYSTORE / KS_PASS (Standard: build/release.jks, wird bei Bedarf erzeugt).
"""
import json, os, re, shutil, subprocess, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SDK = Path(os.environ.get("ANDROID_HOME", "/opt/android"))
BT = SDK / "build-tools/34.0.0"
JAR = SDK / "platforms/android-34/android.jar"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def sh(*cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Fehler bei {cmd[0]}:\n{r.stdout}\n{r.stderr}")
    return r.stdout

def offline_html(html, assets):
    """Lädt Google Fonts lokal herunter, damit die App ohne Internet läuft."""
    m = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">', html)
    html = re.sub(r'<link rel="preconnect"[^>]*>\n?', "", html)
    if m:
        url = m.group(1).replace("&amp;", "&")
        css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read().decode()
        (assets / "fonts").mkdir(parents=True, exist_ok=True)
        out = []
        for sub, block in re.findall(r"/\* (\S+) \*/\s*(@font-face \{.*?\})", css, re.S):
            if sub != "latin":
                continue
            furl = re.search(r"url\((.*?)\)", block).group(1)
            fam = re.search(r"font-family: '(.*?)'", block).group(1).replace(" ", "")
            w = re.search(r"font-weight: (\d+)", block).group(1)
            name = f"fonts/{fam}-{w}.woff2"
            (assets / name).write_bytes(urllib.request.urlopen(furl).read())
            out.append(block.replace(furl, name))
        html = html.replace(m.group(0), "<style>\n" + "\n".join(out) + "\n</style>")
    html = html.replace("in deinem Browser", "auf deinem Gerät")
    assert "googleapis" not in html
    return html

def icon(kind, path):
    im = Image.new("RGB", (192, 192), "#16141c"); d = ImageDraw.Draw(im)
    if kind == "haltepunkt":
        for k in range(5): d.rectangle([20 + k*31, 70, 47 + k*31, 172], fill="#efe9df")
        for k in [0, 1, 3]: d.rectangle([40 + k*31, 70, 58 + k*31, 128], fill="#121017")
        d.rectangle([94, 22, 98, 172], fill="#f2a541")
        d.polygon([(82, 22), (110, 22), (96, 42)], fill="#f2a541")
    else:
        for row, col in enumerate(["#ff6b5a", "#ffc94a", "#5ad1c4"]):
            y = 26 + row*50
            d.rectangle([22, y, 170, y + 40], fill=col)
            for k in range(1, 6): d.line([22 + k*24.7, y, 22 + k*24.7, y + 40], fill="#16141c", width=3)
            for k in [0, 1, 3, 4]: d.rectangle([38 + k*24.7, y, 50 + k*24.7, y + 22], fill="#16141c")
    for dens, px in [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)]:
        p = path / f"mipmap-{dens}"; p.mkdir(parents=True, exist_ok=True)
        im.resize((px, px), Image.LANCZOS).save(p / "ic_launcher.png")

JAVA_MAIN = '''package {pkg};
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.WindowManager;
import android.webkit.ValueCallback;
import android.webkit.WebSettings;
import android.webkit.WebView;

public class MainActivity extends Activity {{
  static final int PICK = 41;
  WebView web;
  ValueCallback<Uri[]> pending;

  @Override protected void onCreate(Bundle state) {{
    super.onCreate(state);
    getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    web = new WebView(this);
    WebSettings s = web.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    s.setAllowFileAccess(true);
    s.setMediaPlaybackRequiresUserGesture(false);
    s.setSupportZoom(false);
    web.setOverScrollMode(WebView.OVER_SCROLL_NEVER);
    web.setWebViewClient(new LinkClient(this));
    web.setWebChromeClient(new Chooser(this));
    setContentView(web);
    if (state != null) web.restoreState(state);
    else web.loadUrl("file:///android_asset/index.html");
  }}

  @Override protected void onActivityResult(int req, int res, Intent data) {{
    if (req == PICK && pending != null) {{
      Uri u = (res == RESULT_OK && data != null) ? data.getData() : null;
      pending.onReceiveValue(u == null ? null : new Uri[]{{u}});
      pending = null;
    }} else super.onActivityResult(req, res, data);
  }}
  @Override protected void onSaveInstanceState(Bundle o) {{ super.onSaveInstanceState(o); web.saveState(o); }}
  @Override protected void onPause() {{ super.onPause(); web.onPause(); }}
  @Override protected void onResume() {{ super.onResume(); web.onResume(); }}
}}
'''
JAVA_CHOOSER = '''package {pkg};
import android.content.Intent;
import android.net.Uri;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebView;

/** Öffnet die Android-Dateiauswahl, wenn die Web-App eine Audiodatei laden will. */
public class Chooser extends WebChromeClient {{
  private final MainActivity a;
  public Chooser(MainActivity a) {{ this.a = a; }}
  @Override public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, WebChromeClient.FileChooserParams p) {{
    if (a.pending != null) a.pending.onReceiveValue(null);
    a.pending = cb;
    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
    i.addCategory(Intent.CATEGORY_OPENABLE);
    i.setType("*/*");
    i.putExtra(Intent.EXTRA_MIME_TYPES, new String[]{{{mimes}}});
    try {{ a.startActivityForResult(Intent.createChooser(i, "{title}"), MainActivity.PICK); }}
    catch (Exception e) {{ a.pending = null; return false; }}
    return true;
  }}
}}
'''
JAVA_LINKS = '''package {pkg};
import android.content.Intent;
import android.net.Uri;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/** Interne Seiten bleiben in der App, externe Links öffnen im Browser. */
public class LinkClient extends WebViewClient {{
  private final MainActivity a;
  public LinkClient(MainActivity a) {{ this.a = a; }}
  @Override public boolean shouldOverrideUrlLoading(WebView v, String url) {{
    if (url.startsWith("file:")) return false;
    try {{ a.startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); }} catch (Exception e) {{}}
    return true;
  }}
}}
'''
MANIFEST = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{pkg}"
    android:versionCode="{vc}" android:versionName="{vn}">
  <uses-sdk android:minSdkVersion="24" android:targetSdkVersion="34"/>
  <application android:label="{label}" android:icon="@mipmap/ic_launcher"
      android:theme="@android:style/Theme.Black.NoTitleBar" android:hardwareAccelerated="true">
    <activity android:name=".MainActivity" android:exported="true" android:screenOrientation="fullUser"
        android:configChanges="orientation|screenSize|keyboardHidden|screenLayout|smallestScreenSize">
      <intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>
    </activity>
  </application>
</manifest>
'''

def main(app_dir):
    app = (ROOT / app_dir).resolve()
    cfg = json.loads((app / "app.json").read_text())
    pkg = cfg["package"]; name = app.name
    b = ROOT / "build" / name
    shutil.rmtree(b, ignore_errors=True)
    assets, res, src = b / "assets", b / "res", b / "src" / pkg.replace(".", "/")
    for p in (assets, res, src, b / "classes", b / "dex"): p.mkdir(parents=True)
    (assets / "index.html").write_text(offline_html((app / "index.html").read_text(), assets))
    icon(cfg["icon"], res)
    (b / "AndroidManifest.xml").write_text(MANIFEST.format(pkg=pkg, vc=cfg["versionCode"], vn=cfg["version"], label=cfg["label"]))
    mimes = ", ".join(f'"{m}"' for m in cfg["mime"])
    (src / "MainActivity.java").write_text(JAVA_MAIN.format(pkg=pkg))
    (src / "Chooser.java").write_text(JAVA_CHOOSER.format(pkg=pkg, mimes=mimes, title=cfg["chooserTitle"]))
    (src / "LinkClient.java").write_text(JAVA_LINKS.format(pkg=pkg))

    sh(BT / "aapt2", "compile", "--dir", res, "-o", b / "res.zip")
    sh(BT / "aapt2", "link", "-o", b / "base.apk", "-I", JAR, "--manifest", b / "AndroidManifest.xml",
       "-A", assets, b / "res.zip", "--java", b / "gen", "--min-sdk-version", 24, "--target-sdk-version", 34)
    javas = [str(p) for p in (b / "gen").rglob("*.java")] + [str(p) for p in src.glob("*.java")]
    sh("javac", "-nowarn", "-source", "8", "-target", "8", "-bootclasspath", JAR, "-classpath", JAR, "-d", b / "classes", *javas)
    sh(BT / "d8", "--min-api", 24, "--lib", JAR, "--output", b / "dex", *[str(p) for p in (b / "classes").rglob("*.class")])
    shutil.copy(b / "base.apk", b / "unsigned.apk")
    sh("zip", "-q", "../unsigned.apk", "classes.dex", cwd=b / "dex")
    sh(BT / "zipalign", "-f", 4, b / "unsigned.apk", b / "aligned.apk")

    ks = Path(os.environ.get("KEYSTORE", ROOT / "build" / "release.jks")); pw = os.environ.get("KS_PASS", "portfolio")
    if not ks.exists():
        sh("keytool", "-genkeypair", "-keystore", ks, "-storepass", pw, "-keypass", pw, "-alias", "app",
           "-keyalg", "RSA", "-keysize", 2048, "-validity", 10000, "-dname", "CN=Dirk Flasche")
    out = ROOT / "releases" / f"{name}-{cfg['version']}.apk"
    sh(BT / "apksigner", "sign", "--ks", ks, "--ks-pass", f"pass:{pw}", "--key-pass", f"pass:{pw}", "--out", out, b / "aligned.apk")
    sh(BT / "apksigner", "verify", out)
    print(f"OK {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    for a in sys.argv[1:]: main(a)
