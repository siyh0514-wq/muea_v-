# 🚀 자동 설치 가이드

## ⚡ 초간단 설치 (1단계!)

### Windows 사용자
1. `setup.bat` 파일을 **더블클릭**
2. 끝! (자동으로 모든 것이 설치됩니다)

### Mac/Linux 사용자
1. 터미널을 열고:
   ```bash
   bash setup.sh
   ```
2. 끝! (자동으로 모든 것이 설치됩니다)

---

## 📋 자동 설치 스크립트가 하는 일

### ✅ 자동으로 확인/설치:
1. **Python 확인** - 설치 여부 확인
2. **pip 확인** - 패키지 관리자 확인
3. **Python 패키지 설치**:
   - google-generativeai (Gemini AI)
   - pillow (이미지 처리)
   - python-dotenv (환경 변수)
   - requests (API 호출)
   - flask (웹 UI)
4. **.env 파일 생성** - API 키 입력 파일
5. **디렉토리 구조 생성** - 필요한 폴더들

### ⏱️ 소요 시간: 1-2분

---

## 🔑 설치 후 해야 할 것 (단 1가지!)

### API 키 입력하기

설치가 끝나면 `.env` 파일이 생성됩니다.

#### Windows:
```
메모장으로 .env 파일 열기
→ API 키 입력
→ 저장
```

#### Mac/Linux:
```bash
# 편집기로 열기
nano .env
# 또는
vi .env

# API 키 입력 후 저장
```

### API 키 받는 곳

#### 1. Gemini API (필수 - 무료!)
1. https://makersuite.google.com/app/apikey 접속
2. Google 계정 로그인
3. "Create API Key" 클릭
4. 키 복사해서 `.env` 파일에 붙여넣기

#### 2. D-ID API (필수 - 무료 체험!)
1. https://www.d-id.com/ 접속
2. 회원가입
3. Dashboard → API Keys
4. 키 복사해서 `.env` 파일에 붙여넣기

---

## ✅ 설치 확인

### 모든 것이 제대로 설치되었는지 확인:

```bash
# Python 확인
python --version
# 결과: Python 3.8.0 이상

# 패키지 확인
pip list | grep google-generativeai
# 결과: google-generativeai가 보임

# .env 파일 확인
cat .env  # Mac/Linux
type .env # Windows
# 결과: API 키들이 보임
```

---

## 🚀 바로 실행하기

설치 완료 후 바로 실행:

```bash
# 일반 모드
python main.py

# 웹 UI 모드 (클릭으로 키워드 선택)
python main.py --web

# 자동 영상 생성 (한국어)
python auto_video_creator.py --lang ko

# 자동 영상 생성 (중국어)
python auto_video_creator.py --lang zh

# 자동 영상 생성 (영어)
python auto_video_creator.py --lang en
```

---

## ❓ 문제 해결

### Python이 없다고 나오면?

#### Windows:
1. https://www.python.org/downloads/ 에서 다운로드
2. 설치 시 **"Add Python to PATH"** 반드시 체크!
3. 설치 후 컴퓨터 재시작
4. `setup.bat` 다시 실행

#### Mac:
```bash
# Homebrew 설치 (없으면)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python3
```

#### Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### 권한 오류가 나면?

#### Windows:
- 명령 프롬프트를 **관리자 권한**으로 실행
- `setup.bat` 다시 실행

#### Mac/Linux:
```bash
# 권한 주기
chmod +x setup.sh

# 실행
bash setup.sh

# pip 권한 오류 시
pip install --user -r requirements.txt
```

### 패키지 설치 오류가 나면?

```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 재시도
pip install -r requirements.txt
```

---

## 📚 다음 단계

설치가 완료되었나요?

1. **API 키 입력**: `.env` 파일 수정
2. **첫 실행**: [START_NOW.md](./START_NOW.md) 참고
3. **영상 만들기**: [INSTALLATION.md](./INSTALLATION.md) 참고
4. **설명란 사용**: [docs/DESCRIPTION_GUIDE.md](./docs/DESCRIPTION_GUIDE.md) 참고

---

## 💡 팁

### 여러 컴퓨터에 설치하기
1. 이 폴더를 USB나 클라우드에 복사
2. 새 컴퓨터에서 `setup.bat` 또는 `setup.sh` 실행
3. `.env` 파일만 다시 수정
4. 완료!

### 업데이트하기
```bash
# Git으로 업데이트 받기
git pull

# 패키지 재설치 (변경사항 있을 때)
pip install -r requirements.txt --upgrade
```

---

**🎉 설치 완료하셨나요? 이제 YouTube 숏폼을 자동으로 만들어보세요!**
