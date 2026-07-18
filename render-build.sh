#!/usr/bin/env bash
# 1. 파이썬 의존성 설치
pip install -r requirements.txt

# 2. 브라우저만 설치 (install-deps는 제거!)
playwright install chromium
