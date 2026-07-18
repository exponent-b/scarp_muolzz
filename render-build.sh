#!/usr/bin/env bash
# 1. 파이썬 의존성 설치
pip install -r requirements.txt

# 2. 브라우저 및 시스템 종속성 설치 (필수!)
playwright install
playwright install-deps
