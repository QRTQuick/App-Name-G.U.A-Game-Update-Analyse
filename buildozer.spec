[app]
title = G.U.A
package.name = gua
package.domain = org.gua

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

# Fixed Python version and pinned library versions
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests==2.31.0,pillow==10.2.0,python-dotenv==1.0.0,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 21b

[buildozer]
log_level = 2
warn_on_root = 1
