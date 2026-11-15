#!/bin/bash
# Mac (Apple Silicon) için tek seferlik kurulum
set -e
command -v brew >/dev/null || { echo "Önce Homebrew kur: https://brew.sh"; exit 1; }
command -v node >/dev/null || brew install node
command -v ffmpeg >/dev/null || brew install ffmpeg
python3 -c "import numpy" 2>/dev/null || pip3 install --user numpy || brew install numpy
npm install
npx playwright install chromium
[ -d .git ] || { git init -q && git add -A && git commit -qm "Stüdyo başlangıcı: Zeyno ile Fıstık"; }
echo "Kurulum tamam. Deneme: npm run render -- projeler/zeyno-ile-fistik"
