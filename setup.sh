#!/bin/bash

# 🚀 YouTube 숏폼 자동화 시스템 - 자동 설치 스크립트 (Mac/Linux)
# 실행 방법: bash setup.sh

echo "=========================================="
echo "🚀 YouTube 숏폼 자동화 시스템 설치 시작!"
echo "=========================================="
echo ""

# Python 버전 확인
echo "📋 1단계: Python 확인 중..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python이 설치되어 있습니다: $PYTHON_VERSION"
else
    echo "❌ Python이 설치되어 있지 않습니다!"
    echo ""
    echo "Python을 먼저 설치해주세요:"
    echo "  Mac: brew install python3"
    echo "  Linux: sudo apt install python3"
    echo ""
    exit 1
fi

echo ""

# pip 확인
echo "📋 2단계: pip 확인 중..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip이 설치되어 있습니다"
else
    echo "⚠️ pip이 없습니다. 설치 중..."
    python3 -m ensurepip --upgrade
fi

echo ""

# Python 패키지 설치
echo "📦 3단계: Python 패키지 설치 중..."
echo "  - google-generativeai (Gemini AI)"
echo "  - pillow (이미지 처리)"
echo "  - python-dotenv (환경 변수)"
echo "  - requests (API 호출)"
echo "  - flask (웹 UI)"
echo ""

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "✅ 패키지 설치 완료!"
else
    echo "⚠️ requirements.txt가 없습니다. 수동 설치 중..."
    pip3 install google-generativeai pillow python-dotenv requests flask
    echo "✅ 패키지 설치 완료!"
fi

echo ""

# .env 파일 생성
echo "🔑 4단계: API 키 설정 파일 생성 중..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Gemini API 키 (필수)
# https://makersuite.google.com/app/apikey 에서 무료로 발급
GEMINI_API_KEY=여기에_제미나이_API_키_입력

# D-ID API 키 (비디오 생성에 필요)
# https://www.d-id.com/ 에서 무료 체험 20크레딧
DID_API_KEY=여기에_D-ID_API_키_입력

# OpenAI API 키 (선택사항 - 더 높은 품질 원하면)
# OPENAI_API_KEY=여기에_OpenAI_API_키_입력

# Google Custom Search (선택사항 - 제품 리서치용)
# GOOGLE_API_KEY=여기에_구글_API_키_입력
# GOOGLE_CSE_ID=여기에_커스텀_서치_엔진_ID_입력
EOF
    echo "✅ .env 파일이 생성되었습니다!"
    echo ""
    echo "⚠️ 중요: .env 파일을 열어서 API 키를 입력해주세요!"
    echo "   vi .env  또는  nano .env"
else
    echo "✅ .env 파일이 이미 존재합니다"
fi

echo ""

# 디렉토리 구조 확인
echo "📁 5단계: 디렉토리 구조 확인 중..."
mkdir -p input/images
mkdir -p input/scripts
mkdir -p output/videos
mkdir -p output/thumbnails
mkdir -p output/optimized
echo "✅ 디렉토리 생성 완료!"

echo ""
echo "=========================================="
echo "🎉 설치 완료!"
echo "=========================================="
echo ""
echo "다음 단계:"
echo ""
echo "1. API 키 입력하기:"
echo "   vi .env  또는  nano .env"
echo ""
echo "2. Gemini API 키 받기 (무료!):"
echo "   https://makersuite.google.com/app/apikey"
echo ""
echo "3. D-ID API 키 받기 (무료 체험!):"
echo "   https://www.d-id.com/"
echo ""
echo "4. 실행하기:"
echo "   python3 main.py"
echo ""
echo "5. 웹 UI로 키워드 선택:"
echo "   python3 main.py --web"
echo ""
echo "6. 자동 영상 생성 (다국어):"
echo "   python3 auto_video_creator.py --lang ko"
echo ""
echo "📚 자세한 사용법: README.md 참고"
echo ""
