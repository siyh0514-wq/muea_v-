# API 설정 가이드

## 필수 API 설정

### 1. Gemini AI (Google) - 메인 AI 엔진
**용도**: 이미지 분석, 키워드 추출, 대본 최적화

**설정 방법**:
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. "Get API Key" 클릭
3. API 키 복사
4. 환경변수에 추가: `GEMINI_API_KEY=your-key`

**비용**: 매우 저렴 (GPT 대비 1/50)
- 입력: $0.000075/1K tokens
- 출력: $0.0003/1K tokens
- 이미지: $0.00001315/image

**무료 할당량**: 
- 60 requests/minute
- 1,500 requests/day

---

### 2. D-ID API - 비디오 생성 (핵심!)
**용도**: 정적 이미지를 말하는 비디오로 변환

**설정 방법**:
1. [D-ID 웹사이트](https://www.d-id.com/) 접속
2. 회원가입 및 로그인
3. Dashboard → API Keys에서 키 생성
4. 환경변수에 추가: `DID_API_KEY=your-key`

**비용**: 
- 크레딧 기반: ~$0.05-0.20/video
- 무료 체험: 20 크레딧 (약 10-20개 영상)
- 구독: $49/month (400 크레딧)

**한국어 음성 옵션**:
- `ko-KR-SunHiNeural` (여성, 밝고 친근함) - 추천
- `ko-KR-InJoonNeural` (남성, 전문적)
- `ko-KR-BongJinNeural` (남성, 뉴스 앵커 스타일)

---

### 3. YouTube Data API v3 - 자동 업로드
**용도**: YouTube에 자동 업로드

**설정 방법**:
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성
3. "API 및 서비스" → "라이브러리" → "YouTube Data API v3" 검색 및 활성화
4. "사용자 인증 정보" → "OAuth 2.0 클라이언트 ID" 생성
5. 애플리케이션 유형: "데스크톱 앱" 또는 "웹 애플리케이션"
6. JSON 파일 다운로드
7. 환경변수에 추가:
   ```
   YOUTUBE_CLIENT_ID=your-client-id
   YOUTUBE_CLIENT_SECRET=your-client-secret
   ```

**비용**: 완전 무료
- 할당량: 10,000 units/day (업로드 1개 = ~1,600 units)
- 일일 약 6개 영상 무료 업로드

---

### 4. Google Custom Search API - 제품 리서치
**용도**: 역이미지 검색, 제품 판매 여부 확인

**설정 방법**:
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. "API 및 서비스" → "라이브러리" → "Custom Search API" 활성화
3. "사용자 인증 정보" → "API 키" 생성
4. [Programmable Search Engine](https://programmablesearchengine.google.com/) 설정
5. 검색 엔진 ID 복사
6. 환경변수에 추가:
   ```
   GOOGLE_SEARCH_API_KEY=your-api-key
   GOOGLE_SEARCH_ENGINE_ID=your-engine-id
   ```

**비용**:
- 무료: 100 queries/day
- 유료: $5/1,000 queries

---

## 추천 API 설정 (선택사항)

### 5. Naver Search API - 한국 시장 특화
**용도**: 네이버 쇼핑 검색, 한국 시장 분석

**설정 방법**:
1. [네이버 개발자센터](https://developers.naver.com/main/) 접속
2. 애플리케이션 등록
3. "검색" API 선택
4. Client ID, Client Secret 발급
5. 환경변수에 추가:
   ```
   NAVER_CLIENT_ID=your-client-id
   NAVER_CLIENT_SECRET=your-client-secret
   ```

**비용**: 완전 무료
- 25,000 calls/day
- 한국 시장 필수!

---

### 6. SerpAPI - 고급 제품 리서치 (선택)
**용도**: Google Shopping, 역이미지 검색, 경쟁 분석

**설정 방법**:
1. [SerpAPI](https://serpapi.com/) 접속
2. 회원가입
3. API 키 발급
4. 환경변수에 추가: `SERPAPI_KEY=your-key`

**비용**:
- Free: 100 searches/month
- Starter: $50/month (5,000 searches)

**참고**: Google Custom Search + Naver로 충분하면 불필요

---

### 7. OpenAI GPT (백업용)
**용도**: Gemini 실패시 백업

**설정 방법**:
1. [OpenAI Platform](https://platform.openai.com/) 접속
2. API Keys → "Create new secret key"
3. 환경변수에 추가: `OPENAI_API_KEY=your-key`

**비용**:
- gpt-4o-mini: $0.15/1M input tokens, $0.60/1M output tokens
- Gemini보다 비싸므로 백업용으로만 사용

---

### 8. Google Search Console (트렌드 분석)
**용도**: 실시간 검색 트렌드, 키워드 발굴

**설정 방법**:
1. [Google Search Console](https://search.google.com/search-console/) 접속
2. 웹사이트 등록 (있는 경우)
3. API 액세스 권한 부여
4. OAuth 2.0 설정

**비용**: 완전 무료

**참고**: 자신의 웹사이트가 없어도 공개 트렌드 데이터 활용 가능

---

## 환경변수 설정 (.env 파일)

```bash
# 필수 API
GEMINI_API_KEY=your-gemini-api-key-here
DID_API_KEY=your-d-id-api-key-here
YOUTUBE_CLIENT_ID=your-youtube-client-id
YOUTUBE_CLIENT_SECRET=your-youtube-client-secret
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# 제품 리서치
GOOGLE_SEARCH_API_KEY=your-google-search-key
GOOGLE_SEARCH_ENGINE_ID=your-engine-id
NAVER_CLIENT_ID=your-naver-client-id
NAVER_CLIENT_SECRET=your-naver-client-secret

# 선택사항
OPENAI_API_KEY=your-openai-key-here
SERPAPI_KEY=your-serpapi-key-here
```

---

## 노코드 플랫폼 설정

### Make.com 설정
1. [Make.com](https://www.make.com/) 회원가입
2. New Scenario 생성
3. 모듈 추가:
   - Google Drive (트리거)
   - HTTP Request (Gemini API)
   - HTTP Request (D-ID API)
   - YouTube (업로드)
4. API 키를 각 모듈에 입력
5. 워크플로우 활성화

**비용**: Free tier (1,000 operations/month)

---

### Zapier 설정
1. [Zapier](https://zapier.com/) 회원가입
2. Create Zap
3. 트리거: Google Drive (새 파일)
4. 액션: 
   - Webhooks (Gemini API 호출)
   - Webhooks (D-ID API 호출)
   - Gmail (알림)
5. Zap 활성화

**비용**: Free tier (100 tasks/month)

---

## API 비용 최적화 팁

### 1. Gemini를 메인으로 사용
- GPT 대신 Gemini 사용으로 50배 비용 절감
- 한국어 품질도 우수

### 2. 배치 처리
- 여러 이미지를 한번에 처리
- API 호출 최소화

### 3. 캐싱 활용
- 중복 요청 방지
- 동일한 키워드 재사용

### 4. 무료 할당량 활용
- Google Search: 100 queries/day 무료
- Naver: 25,000 calls/day 무료
- YouTube: 10,000 units/day 무료

### 5. 비용 모니터링
- 각 API의 사용량 정기 확인
- 예산 알림 설정

---

## 예상 월간 비용 (100개 영상 기준)

| API | 사용량 | 비용 |
|-----|--------|------|
| Gemini | 300 requests | $0.90 |
| D-ID | 100 videos | $8.00 |
| Google Search | 100 queries | $0.00 (무료 할당량) |
| Naver | 100 queries | $0.00 (무료) |
| YouTube | 100 uploads | $0.00 (무료) |
| **총 비용** | - | **$8.90** |

**예상 수익**: $3,000-5,000
**ROI**: 33,600-56,000%

---

## 트러블슈팅

### Gemini API 오류
- **Rate Limit 초과**: 60 requests/min 제한 확인
- **Invalid API Key**: 키 재생성 및 확인

### D-ID API 오류
- **크레딧 부족**: 대시보드에서 크레딧 확인
- **이미지 품질**: 최소 1024x1024 해상도 사용

### YouTube API 오류
- **Quota 초과**: 다음날까지 대기 또는 할당량 증가 요청
- **OAuth 오류**: 토큰 재생성

---

## 다음 단계
1. 필수 API 키 모두 발급
2. `.env` 파일 또는 노코드 플랫폼에 설정
3. 테스트 실행: 이미지 1개로 전체 워크플로우 테스트
4. 성공하면 배치 처리 시작

**질문이나 문제가 있으면 각 API의 공식 문서 참조하세요!**
