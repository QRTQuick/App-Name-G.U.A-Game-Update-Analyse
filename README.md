# G.U.A (Game Update Analyse)

A modern mobile application for game updates, screenshots, and analysis.

## Features
- Latest game updates and news
- High-quality official screenshots
- Game ratings, genres, and platforms
- Trending and popular games
- Search and category browsing
- Clean, fast, and lightweight design

## Tech Stack
- **Language**: Python
- **Framework**: Kivy + KivyMD
- **API**: RAWG API
- **Platform**: Android

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API key:
   - Copy `.env.example` to `.env`
   - Get your RAWG API key from https://rawg.io/apidocs
   - Add your API key to `.env` file

3. Run the app:
```bash
python main.py
```

## Build for Android

1. Install Buildozer:
```bash
pip install buildozer
```

2. Build APK:
```bash
buildozer android debug
```

3. Deploy to device:
```bash
buildozer android deploy run
```

## Project Structure
```
.
├── main.py              # Main application file
├── config.py            # API configuration
├── requirements.txt     # Python dependencies
├── buildozer.spec       # Android build configuration
└── README.md           # This file
```

## License
See LICENSE file for details.
