#!/usr/bin/env bash
pip install -r requirements.txt
# 브라우저를 특정 폴더(ms-playwright)에 강제로 설치
PLAYWRIGHT_BROWSERS_PATH=ms-playwright playwright install chromium
