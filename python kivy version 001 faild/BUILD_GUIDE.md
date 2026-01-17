# G.U.A - APK Build Guide

## Complete Guide to Building Android APK

---

## ⚠️ IMPORTANT: Windows Users

**Buildozer does NOT work natively on Windows!**

You have 3 options:
1. **Use WSL (Windows Subsystem for Linux)** - Recommended
2. **Use a Linux Virtual Machine**
3. **Use a Linux computer**

---

## Option 1: Build on Windows using WSL (Recommended)

### Step 1: Install WSL

```powershell
# Open PowerShell as Administrator and run:
wsl --install
```

Restart your computer after installation.

### Step 2: Open WSL Ubuntu

```powershell
# Open WSL
wsl
```

### Step 3: Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 4: Install Dependencies

```bash
# Install Python and build tools
sudo apt install -y python3 python3-pip python3-venv git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install Cython
pip3 install --upgrade cython
```

### Step 5: Install Buildozer

```bash
pip3 install --upgrade buildozer
```

### Step 6: Copy Your Project to WSL

```bash
# Create a directory in WSL
mkdir -p ~/projects
cd ~/projects

# Copy from Windows to WSL
# From Windows: E:\code base\App-Name-G.U.A-Game-Update-Analyse
# To WSL: /home/yourusername/projects/gua

# Option A: Use Windows Explorer
# Type in address bar: \\wsl$\Ubuntu\home\yourusername\projects
# Then copy your project folder there

# Option B: Use command
cp -r /mnt/e/code\ base/App-Name-G.U.A-Game-Update-Analyse ~/projects/gua
cd ~/projects/gua
```

### Step 7: Build the APK

```bash
# First time build (takes 30-60 minutes)
buildozer android debug

# Subsequent builds (faster)
buildozer android debug
```

### Step 8: Find Your APK

```bash
# APK location
ls -lh bin/*.apk

# Copy APK to Windows
cp bin/*.apk /mnt/e/
```

---

## Option 2: Build on Linux (Native)

### Step 1: Install Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install Cython
pip3 install --upgrade cython

# Install Buildozer
pip3 install --upgrade buildozer
```

### Step 2: Navigate to Project

```bash
cd /path/to/App-Name-G.U.A-Game-Update-Analyse
```

### Step 3: Build APK

```bash
buildozer android debug
```

---

## Option 3: Use Google Colab (Online - Free)

### Step 1: Upload Project to Google Drive

### Step 2: Open Google Colab
Visit: https://colab.research.google.com/

### Step 3: Run This Code

```python
# Install Buildozer
!pip install buildozer

# Install dependencies
!sudo apt update
!sudo apt install -y openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Navigate to your project
%cd /content/drive/MyDrive/your-project-folder

# Build APK
!buildozer android debug

# Download APK
from google.colab import files
files.download('bin/gua-1.0.0-debug.apk')
```

---

## Buildozer Configuration

Your `buildozer.spec` file is already configured. Key settings:

```ini
[app]
title = G.U.A
package.name = gua
package.domain = org.gua
version = 1.0.0

requirements = python3,kivy,kivymd,requests,pillow,python-dotenv

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
```

---

## Build Process Timeline

### First Build (30-60 minutes)
1. Download Android SDK (5-10 min)
2. Download Android NDK (5-10 min)
3. Download Python-for-Android (2-5 min)
4. Compile dependencies (15-30 min)
5. Build APK (5-10 min)

### Subsequent Builds (5-10 minutes)
- Only recompiles changed code
- Much faster

---

## Common Issues & Solutions

### Issue 1: "buildozer: command not found"

```bash
# Add to PATH
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Issue 2: "Java not found"

```bash
# Install Java
sudo apt install openjdk-17-jdk

# Set JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc
```

### Issue 3: Build fails with "Permission denied"

```bash
# Fix permissions
chmod +x buildozer.spec
buildozer android clean
buildozer android debug
```

### Issue 4: "No space left on device"

```bash
# Clean buildozer cache
buildozer android clean

# Or remove .buildozer folder
rm -rf .buildozer
```

### Issue 5: Python module not found

```bash
# Update requirements in buildozer.spec
# Add missing module to requirements line
requirements = python3,kivy,kivymd,requests,pillow,python-dotenv,missing-module
```

---

## Build Commands Reference

```bash
# Clean build (removes cache)
buildozer android clean

# Debug build (for testing)
buildozer android debug

# Release build (for Play Store)
buildozer android release

# Deploy to connected device
buildozer android debug deploy run

# View logs
buildozer android logcat

# List targets
buildozer --version
```

---

## APK Output Location

```
your-project/
└── bin/
    └── gua-1.0.0-debug.apk  ← Your APK file
```

---

## Installing APK on Android Device

### Method 1: USB Transfer
1. Connect phone to computer
2. Copy APK to phone
3. Open APK on phone
4. Allow "Install from Unknown Sources"
5. Install

### Method 2: Direct Deploy

```bash
# Connect phone via USB
# Enable USB Debugging on phone
buildozer android debug deploy run
```

### Method 3: Cloud Transfer
1. Upload APK to Google Drive/Dropbox
2. Download on phone
3. Install

---

## Optimizing APK Size

### Current Size: ~50-80 MB

### Reduce Size:

1. **Remove unused dependencies**
```ini
# In buildozer.spec
requirements = python3,kivy,kivymd,requests,pillow,python-dotenv
# Remove any unused modules
```

2. **Enable ProGuard**
```ini
android.enable_proguard = True
```

3. **Use release build**
```bash
buildozer android release
```

---

## Testing the APK

### Before Building:
- ✅ Test all features on desktop
- ✅ Check all screens work
- ✅ Verify API calls
- ✅ Test login/logout
- ✅ Check cache system

### After Building:
- ✅ Install on real device
- ✅ Test all features
- ✅ Check performance
- ✅ Monitor crashes
- ✅ Test on different devices

---

## Quick Start (WSL)

```bash
# 1. Install WSL
wsl --install

# 2. Open WSL and install dependencies
sudo apt update && sudo apt install -y python3 python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 3. Install Buildozer
pip3 install buildozer

# 4. Copy project to WSL
cp -r /mnt/e/code\ base/App-Name-G.U.A-Game-Update-Analyse ~/gua
cd ~/gua

# 5. Build APK
buildozer android debug

# 6. Get APK
cp bin/*.apk /mnt/e/
```

---

## Troubleshooting Checklist

- [ ] WSL installed and updated
- [ ] All dependencies installed
- [ ] Java installed (openjdk-17)
- [ ] Buildozer installed
- [ ] Project copied to WSL
- [ ] buildozer.spec exists
- [ ] .env file present
- [ ] Internet connection active
- [ ] Enough disk space (10GB+)

---

## Support & Resources

**Buildozer Documentation:**
https://buildozer.readthedocs.io/

**Kivy Documentation:**
https://kivy.org/doc/stable/

**KivyMD Documentation:**
https://kivymd.readthedocs.io/

**Python-for-Android:**
https://python-for-android.readthedocs.io/

---

## Expected Build Output

```
# Buildozer initialized
# Android SDK found
# Android NDK found
# Installing platform
# Compiling recipes
# Building APK
# APK created successfully

BUILD SUCCESSFUL

APK: /home/user/gua/bin/gua-1.0.0-debug.apk
```

---

## Next Steps After Building

1. **Test APK** on real device
2. **Fix any issues** found
3. **Optimize performance**
4. **Create release build**
5. **Sign APK** for Play Store
6. **Upload to Play Store**

---

## Play Store Release (Future)

### Requirements:
- Signed release APK
- App icon (512x512)
- Screenshots (multiple sizes)
- Privacy policy
- App description
- Developer account ($25 one-time)

### Command:
```bash
buildozer android release
```

Then sign with your keystore.

---

## Estimated Times

| Task | Time |
|------|------|
| WSL Setup | 10-15 min |
| Install Dependencies | 5-10 min |
| First Build | 30-60 min |
| Subsequent Builds | 5-10 min |
| Testing | 15-30 min |
| **Total (First Time)** | **1-2 hours** |

---

## Success! 🎉

Once you see:
```
BUILD SUCCESSFUL
APK: bin/gua-1.0.0-debug.apk
```

Your app is ready to install on Android devices!

---

**Need Help?**
- Check buildozer logs: `buildozer android debug -v`
- Clean and rebuild: `buildozer android clean && buildozer android debug`
- Check WSL is running: `wsl --status`
