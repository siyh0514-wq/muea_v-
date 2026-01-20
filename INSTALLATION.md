# 🔧 설치 가이드 (초간단!)

## 📋 필요한 것

### 1️⃣ Python (필수)
- **버전**: Python 3.8 이상
- **확인 방법**: 
  ```bash
  python --version
  ```
- **설치 안되어 있다면**:
  - Windows: https://www.python.org/downloads/ 에서 다운로드
  - Mac: `brew install python3`
  - Linux: `sudo apt install python3`

---

### 2️⃣ Python 패키지 (필수)
터미널에서 한 줄만 실행하세요:

```bash
pip install google-generativeai pillow python-dotenv requests flask
```

**또는** (추천):
```bash
pip install -r requirements.txt
```

**설치되는 패키지들**:
- `google-generativeai` - Gemini AI 사용
- `pillow` - 이미지 처리
- `python-dotenv` - 환경 변수 관리
- `requests` - API 호출
- `flask` - 웹 UI (선택사항)

---

### 3️⃣ API 키 (필수)
무료로 받을 수 있습니다!

#### Gemini API 키 (무료!) ⭐
1. https://makersuite.google.com/app/apikey 접속
2. Google 계정으로 로그인
3. "Create API Key" 클릭
4. API 키 복사

#### D-ID API 키 (무료 체험 20크레딧)
1. https://www.d-id.com/ 접속
2. 회원가입
3. Dashboard → API Keys
4. API 키 복사

---

### 4️⃣ .env 파일 설정 (필수)
프로젝트 폴더에 `.env` 파일을 만들고 API 키를 입력하세요:

```bash
# .env 파일 내용
GEMINI_API_KEY=여기에_제미나이_API_키_붙여넣기
DID_API_KEY=여기에_D-ID_API_키_붙여넣기
```

**방법 1: 직접 만들기**
1. 메모장이나 텍스트 에디터로 새 파일 만들기
2. 위 내용 복사 + API 키 붙여넣기
3. 파일 이름을 `.env`로 저장

**방법 2: 터미널에서 만들기**
```bash
# Windows
echo GEMINI_API_KEY=여기에_키_붙여넣기 > .env
echo DID_API_KEY=여기에_키_붙여넣기 >> .env

# Mac/Linux
echo "GEMINI_API_KEY=여기에_키_붙여넣기" > .env
echo "DID_API_KEY=여기에_키_붙여넣기" >> .env
```

---

## ✅ 설치 완료 확인

모든 것이 제대로 설치되었는지 확인:

```bash
# 1. Python 버전 확인
python --version
# 결과: Python 3.8.0 이상이면 OK

# 2. 패키지 설치 확인
pip list | grep google-generativeai
# 결과: google-generativeai가 보이면 OK

# 3. .env 파일 확인 (Windows)
type .env
# 결과: API 키들이 보이면 OK

# 3. .env 파일 확인 (Mac/Linux)
cat .env
# 결과: API 키들이 보이면 OK
```

---

## 🚀 바로 실행해보기

설치가 끝났으면 바로 테스트!

```bash
# 자동화 시스템 실행
python main.py
```

**시뮬레이션 모드**로 실행됩니다:
- ✅ 이미지 분석 (기본값)
- ✅ 키워드 최적화
- ✅ 썸네일 생성
- ⚠️ 비디오는 시뮬레이션 (실제 생성 안됨)

**실제 비디오 생성**하려면:
- D-ID API 키가 필요합니다 (무료 체험 가능!)

---

## 🎯 완전 설치 체크리스트

- [ ] Python 3.8+ 설치됨
- [ ] pip 패키지 설치됨 (`pip install -r requirements.txt`)
- [ ] Gemini API 키 받음
- [ ] D-ID API 키 받음 (선택사항 - 실제 비디오 생성시 필요)
- [ ] `.env` 파일에 API 키 입력
- [ ] `python main.py` 실행 성공

**모두 체크되면 완료! 🎉**

---

## 💡 선택사항 (더 많은 기능)

### OpenAI GPT-4o (더 높은 품질 원하면)
```bash
# .env 파일에 추가
OPENAI_API_KEY=여기에_OpenAI_API_키
```
- https://platform.openai.com/api-keys 에서 발급
- 유료이지만 품질이 더 좋음

### Google Custom Search (제품 리서치 원하면)
```bash
# .env 파일에 추가
GOOGLE_API_KEY=여기에_구글_API_키
GOOGLE_CSE_ID=여기에_커스텀_서치_엔진_ID
```

---

## ❓ 문제 해결

### pip가 안된다면?
```bash
python -m pip install --upgrade pip
```

### Python 명령어가 안된다면?
```bash
# python3로 시도
python3 --version
python3 main.py
```

### 권한 오류가 난다면?
```bash
# Mac/Linux
sudo pip install -r requirements.txt

# Windows는 관리자 권한으로 터미널 실행
```

### .env 파일이 안보인다면?
숨김 파일이라 안보일 수 있습니다:
- Windows: 파일 탐색기에서 "보기 → 숨김 항목" 체크
- Mac: Finder에서 `Cmd + Shift + .` 누르기
- Linux: 터미널에서 `ls -la` 실행

---

## 🎬 다음 단계

설치 완료하셨나요?

1. **첫 영상 만들기**: [START_NOW.md](./START_NOW.md)
2. **설명란 사용법**: [docs/DESCRIPTION_GUIDE.md](./docs/DESCRIPTION_GUIDE.md)
3. **API 자세한 설정**: [docs/API_SETUP_GUIDE.md](./docs/API_SETUP_GUIDE.md)

**질문이 있으시면 언제든지 물어보세요! 😊**
