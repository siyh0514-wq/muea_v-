# 🎬 완전 자동화 구조 설명

## 📌 전체 자동화 흐름

```
사용자 입력 (이미지만!)
    ↓
[1단계] 이미지 분석 (Gemini Vision)
    ↓
[2단계] 키워드 자동 추출 (언어별 AI)
    ↓
[3단계] 최적 키워드 자동 선택
    ↓
[4단계] 대본 자동 생성 (3가지 버전)
    ↓
[5단계] 고화질 비디오 생성 (D-ID)
    ↓
완성된 숏폼 영상 3개!
```

## 🔍 상세 단계별 설명

### 1단계: 이미지 분석
**파일**: `auto_video_creator.py` - `analyze_image_with_gemini()`

```python
# 입력: 이미지 파일 (예: product.jpg)
# AI 분석:
- 제품명 감지
- 제품 여부 확인
- 카테고리 분류
- 주요 특징 3가지

# 출력 예시 (중국어):
{
  "detected_subject": "苹果AirPods Pro",
  "is_product": true,
  "description": "无线耳机，降噪功能",
  "suggested_category": "electronics",
  "key_features": ["降噪", "无线", "长续航"]
}
```

### 2단계: 키워드 자동 추출
**파일**: `keyword_selector.py` 또는 `multilingual_selector.py` - `analyze_topic()`

**언어별 프롬프트**:

#### 한국어 (월 2000만원 숏폼 쇼핑 채널 전략)
```
주제: AirPods Pro

AI가 자동 추출:
- 구매유도형: "최저가", "쿠폰", "할인코드"
- 비교검증형: "VS", "리뷰", "솔직후기"
- 긴급구매형: "품절임박", "오늘만", "한정수량"

추천 제목:
1. "에어팟 프로 최저가 찾음 | 쿠폰까지 | 지금 사세요" (CTR: 90)
2. "에어팟 프로 VS 일반 에어팟 | 솔직비교" (CTR: 88)
3. "이거 사지마세요 | 에어팟 프로 진실" (CTR: 92)
```

#### 中文 (月入20万短视频购物频道)
```
主题: AirPods Pro

AI自动提取:
- 购买诱导型: "最低价", "优惠券", "折扣码"
- 比较验证型: "VS", "评测", "真实评价"
- 紧急购买型: "即将售罄", "今日限定", "限量"

推荐标题:
1. "AirPods Pro找到最低价 | 还有优惠券 | 快买" (CTR: 90)
2. "AirPods Pro VS 普通AirPods | 真实对比" (CTR: 88)
3. "别买这个 | AirPods Pro真相" (CTR: 92)
```

#### English (Earning $20K+/month)
```
Topic: AirPods Pro

AI extracts:
- Purchase-inducing: "best price", "coupon code", "discount"
- Comparison-validation: "VS", "review", "honest opinion"
- Urgent-purchase: "selling out", "today only", "limited"

Recommended titles:
1. "AirPods Pro Best Price Found | Plus Coupon | Buy Now" (CTR: 90)
2. "AirPods Pro VS Regular AirPods | Honest Comparison" (CTR: 88)
3. "Don't Buy This | AirPods Pro Truth" (CTR: 92)
```

#### 日本語 (月収200万円)
```
トピック: AirPods Pro

AI抽出:
- 購入誘導型: "最安値", "クーポン", "割引コード"
- 比較検証型: "VS", "レビュー", "本音"
- 緊急購入型: "在庫わずか", "今日だけ", "限定"

推奨タイトル:
1. "AirPods Pro 最安値発見 | クーポンも | 今すぐ" (CTR: 90)
2. "AirPods Pro VS 普通のAirPods | 本音比較" (CTR: 88)
3. "これ買うな | AirPods Pro真実" (CTR: 92)
```

#### ภาษาไทย (รายได้ 2 ล้านบาท/เดือน)
```
หัวข้อ: AirPods Pro

AI สกัด:
- กระตุ้นการซื้อ: "ราคาถูกที่สุด", "คูปอง", "โค้ดส่วนลด"
- เปรียบเทียบ: "VS", "รีวิว", "ความคิดเห็นจริง"
- ซื้อด่วน: "เหลือน้อย", "วันนี้เท่านั้น", "จำกัด"

แนะนำหัวข้อ:
1. "AirPods Pro เจอราคาถูกสุด | มีคูปองด้วย | ซื้อเลย" (CTR: 90)
2. "AirPods Pro VS AirPods ธรรมดา | เปรียบเทียบจริง" (CTR: 88)
3. "อย่าซื้ออันนี้ | ความจริง AirPods Pro" (CTR: 92)
```

### 3단계: 최적 키워드 자동 선택
**파일**: `auto_video_creator.py` - `auto_generate_from_image()`

```python
# AI가 자동으로 선택 (사용자 개입 없음!)
- CTR 점수 가장 높은 제목 선택
- 상위 3개 키워드 자동 선택

# 예시:
selected_title = "AirPods Pro 最低价 找到了 | 还有优惠券"
selected_keywords = ["最低价", "优惠券", "真实评测"]
```

### 4단계: 대본 자동 생성 (3가지 버전)
**파일**: `multilingual_selector.py` - `generate_versions()`

#### 버전 1: 초단축 (10-15초)
**언어별 자연스러운 대본**:

```python
# 한국어
"안녕하세요! AirPods Pro 최저가 지금 확인하세요!"

# 中文  
"大家好！AirPods Pro最低价 赶快查看！"

# English
"Hey there! AirPods Pro best price Check it out!"

# 日本語
"皆さん、こんにちは！AirPods Pro最安値 ぜひチェックしてください！"

# ภาษาไทย
"สวัสดีครับ/ค่ะ! AirPods Pro ราคาถูกที่สุด ไปดูกันเลย!"
```

#### 버전 2: 표준 (20-30초)
```python
# 한국어 (캐주얼 톤)
"안녕하세요~ 오늘은 AirPods Pro 이야기입니다. 최저가 궁금하시죠? 
그리고 쿠폰도 함께 알아봐요. 지금 확인하세요!"

# 中文 (轻松语气)
"大家好～今天说说AirPods Pro。最低价大家关心吗？
还有优惠券也一起看看。赶快查看！"

# English (Casual tone)
"Hey there! Today we're talking about AirPods Pro. Curious about the best price?
Plus, let's look at coupons too. Check it out!"

# 日本語 (カジュアル)
"皆さん、こんにちは～今日はAirPods Proのお話です。最安値気になりますよね？
クーポンも一緒に見ていきましょう。ぜひチェックしてください！"

# ภาษาไทย (สบายๆ)
"สวัสดีครับ/ค่ะ~ วันนี้เรื่อง AirPods Pro อยากรู้ราคาถูกที่สุดไหม?
มาดูคูปองด้วยกัน ไปดูกันเลย!"
```

#### 버전 3: 상세 (40-60초)
```python
# 한국어 (공식적 톤)
"안녕하세요. 오늘은 AirPods Pro에 대해 상세히 알아보겠습니다. 
최저가가 가장 중요한 포인트입니다. 그리고 쿠폰에 대해서도 살펴보겠습니다. 
특히 실제 사용 후기를 통해 더 많은 정보를 얻으실 수 있습니다. 
지금 바로 확인해보세요."

# 中文 (正式语气)
"大家好。今天详细介绍AirPods Pro。最低价是最重要的要点。
也看看优惠券。特别是通过真实评价可以获得更多信息。
赶快查看。"

# English (Formal tone)
"Hey there. Today we'll cover AirPods Pro in detail. 
The best price is the most important point. We'll also look at coupons. 
Importantly, you can get more info through real reviews. Check it out."

# 日本語 (フォーマル)
"皆さん、こんにちは。今日はAirPods Proについて詳しく見ていきましょう。
最安値が最も重要なポイントです。クーポンについても見ていきます。
実際のレビューを通じてより多くの情報が得られます。
ぜひチェックしてください。"

# ภาษาไทย (เป็นทางการ)
"สวัสดีครับ/ค่ะ วันนี้เรามาดู AirPods Pro อย่างละเอียด
ราคาถูกที่สุดเป็นประเด็นที่สำคัญที่สุด ดูคูปองด้วย
ผ่านรีวิวจริงจะได้ข้อมูลเพิ่มเติม ไปดูกันเลย"
```

### 5단계: 고화질 비디오 생성
**파일**: `auto_video_creator.py` - `create_high_quality_video()`

```python
# D-ID API 설정
quality_settings = {
    "high": {
        "resolution": "1920x1080",  # Full HD
        "bitrate": "5000k",
        "fps": 30,
        "description": "YouTube 숏폼 최적"
    },
    "ultra": {
        "resolution": "3840x2160",  # 4K
        "bitrate": "10000k",
        "fps": 30,
        "description": "프리미엄 고화질"
    }
}

# D-ID API 호출
payload = {
    "source_url": "이미지_base64",
    "script": {
        "type": "text",
        "input": "생성된 대본",
        "provider": {
            "type": "microsoft",
            "voice_id": "ko-KR-SunHiNeural"  # 언어별 음성
        }
    },
    "config": {
        "stitch": True,
        "result_format": "mp4",
        "fluent": True
    }
}

# 결과:
- 비디오 1: v1_10초_캐주얼_HD.mp4
- 비디오 2: v2_25초_표준_HD.mp4
- 비디오 3: v3_50초_상세_HD.mp4
```

## 🚀 사용 방법

### 방법 1: 완전 자동 (추천!)
```bash
# 1. 이미지를 input/images/ 폴더에 넣기
cp my_product.jpg input/images/

# 2. 언어 선택하고 실행
python auto_video_creator.py --lang ko      # 한국어
python auto_video_creator.py --lang zh      # 中文
python auto_video_creator.py --lang en      # English
python auto_video_creator.py --lang ja      # 日本語
python auto_video_creator.py --lang th      # ภาษาไทย

# 3. 화질 선택 (선택사항)
python auto_video_creator.py --lang zh --quality ultra  # 4K

# 끝! 3개 버전 비디오 자동 생성됨
```

### 방법 2: 특정 이미지만
```bash
python auto_video_creator.py --lang zh --image path/to/product.jpg
```

### 방법 3: 키워드 선택 후 수동
```bash
python main.py --keyword --lang zh
```

## 📁 출력 구조

```
output/
├── videos/
│   ├── product_v1_10s_HD.mp4      # 버전1: 초단축
│   ├── product_v2_25s_HD.mp4      # 버전2: 표준
│   └── product_v3_50s_HD.mp4      # 버전3: 상세
├── thumbnails/
│   └── product_thumbnail.png
├── results/
│   └── result_zh_20260120_103000.json
└── optimized/
    └── product_metadata.json

input/
├── images/              # 여기에 이미지 넣기!
└── completed/           # 처리된 이미지 자동 이동
```

## 💰 비용 (1개 이미지당)

```
Gemini Vision (이미지 분석):     $0.006
Gemini AI (키워드 추출):         $0.002
D-ID (비디오 3개):               $0.24 (3 x $0.08)
─────────────────────────────────────
총 비용:                        $0.248

vs 수동 제작: $20-50 (80-200배 저렴!)
```

## ⏱️ 시간 (1개 이미지당)

```
이미지 분석:        10초
키워드 추출:        15초
대본 생성:          5초
비디오 생성 (3개):  180-300초 (3-5분)
─────────────────────────────
총 시간:           4-6분

vs 수동 제작: 1-2시간 (20-30배 빠름!)
```

## 🎯 핵심 포인트

1. **이미지만 넣으면 끝**: 나머지 100% 자동
2. **언어만 선택**: 5개 언어 완벽 지원
3. **3가지 버전 자동 생성**: 10초, 25초, 50초
4. **고화질**: 1080p 또는 4K
5. **원어민 수준**: 각 언어별 자연스러운 표현
6. **쇼핑 채널 최적화**: 제휴 수익 극대화

## 📝 대본 생성 프롬프트 위치

### 각 언어별 대본 생성 메서드:
- `multilingual_selector.py`:
  - `_generate_korean_script()` - 한국어 대본
  - `_generate_chinese_script()` - 中文 대본
  - `_generate_english_script()` - English 대본
  - `_generate_japanese_script()` - 日本語 대본
  - `_generate_thai_script()` - ภาษาไทย 대본

### 자연스러운 표현 DB:
- `config/languages.json`:
  - `natural_expressions`: 각 언어별 자연스러운 전환 표현
  - `intro`: 시작 표현
  - `transition`: 전환 표현
  - `emphasis`: 강조 표현
  - `conclusion`: 마무리 표현
