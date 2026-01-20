#!/usr/bin/env python3
"""
키워드 및 제목 추천/선택 시스템
고수익 키워드 추출 및 인터랙티브 선택 기능
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class KeywordSelector:
    """애드센스/블로그 수익화를 위한 다국어 키워드 선택 시스템"""
    
    def __init__(self, language='ko', ai_provider='gemini'):
        self.language = language
        self.ai_provider = ai_provider.lower()
        self.load_keyword_database()
        self.load_language_config()
        
    def load_keyword_database(self):
        """키워드 데이터베이스 로드"""
        with open('config/keywords.json', 'r', encoding='utf-8') as f:
            self.keyword_db = json.load(f)
    
    def load_language_config(self):
        """언어 설정 로드"""
        with open('config/languages.json', 'r', encoding='utf-8') as f:
            self.lang_config = json.load(f)
            
        if self.language not in self.lang_config['supported_languages']:
            print(f"⚠️  '{self.language}' 언어는 지원되지 않습니다. 한국어로 설정합니다.")
            self.language = 'ko'
            
        self.current_lang = self.lang_config['supported_languages'][self.language]
    
    def analyze_topic(self, topic):
        """
        주제 분석 및 키워드 추출
        
        Args:
            topic: 사용자가 입력한 주제 (뉴스, 정책, 이슈 등)
        
        Returns:
            dict: 키워드 분석 결과
        """
        try:
            # 언어별 프롬프트 선택
            prompts = {
                'ko': self._get_korean_prompt(topic),
                'zh': self._get_chinese_prompt(topic),
                'en': self._get_english_prompt(topic),
                'ja': self._get_japanese_prompt(topic),
                'th': self._get_thai_prompt(topic)
            }
            prompt = prompts.get(self.language, prompts['ko'])
            
            if self.ai_provider == 'openai':
                # OpenAI GPT
                import openai
                
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    print("⚠️  OpenAI API 키가 없습니다. 기본 키워드를 사용합니다.")
                    return self._generate_default_keywords(topic)
                
                openai.api_key = api_key
                
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a shopping channel expert earning $20K+/month through keyword optimization."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                result_text = response.choices[0].message.content
                
            else:
                # Gemini AI (기본)
                import google.generativeai as genai
                
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    print("⚠️  Gemini API 키가 없습니다. 기본 키워드를 사용합니다.")
                    return self._generate_default_keywords(topic)
                
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                response = model.generate_content(prompt)
                result_text = response.text
            
            # JSON 파싱
            if '```json' in result_text:
                json_str = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                json_str = result_text.split('```')[1].split('```')[0].strip()
            else:
                json_str = result_text.strip()
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            print(f"⚠️  분석 실패: {str(e)}")
            return self._generate_default_keywords(topic)
    
    def _get_korean_prompt(self, topic):
        """한국어 프롬프트 - 숏폼 쇼핑 채널 전략"""
        return f"""당신은 월 2000만원 이상 수익을 내는 숏폼 쇼핑 채널 전문가입니다.

주제/제품: {topic}

다음을 수행하세요:

1. **구매 니즈 파악**: 사용자가 이 제품에서 원하는 것 (가격, 할인, 리뷰, 비교, 사용법 등)
2. **쇼핑 키워드 확장**: 고수익 쇼핑 키워드 유형
   - 구매유도형: "최저가", "쿠폰", "할인코드", "특가", "1+1"
   - 비교검증형: "VS", "비교", "리뷰", "솔직후기", "추천"
   - 긴급구매형: "품절임박", "오늘만", "한정수량", "타임세일"
3. **실제 구매 검색어**: 구매 직전 단계에서 검색하는 키워드
4. **제휴 최적화**: 쿠팡, 네이버쇼핑, 11번가 등 제휴 수익 극대화

JSON 형식으로 응답:
{{
  "main_keyword": "메인 제품/키워드",
  "product_category": "제품 카테고리",
  "purchase_needs": ["가격 비교", "할인 정보", "리뷰"],
  "high_revenue_keywords": [
    {{"keyword": "키워드1", "type": "구매유도형", "affiliate_potential": "높음", "ctr": "8-12%"}},
    {{"keyword": "키워드2", "type": "비교검증형", "affiliate_potential": "높음", "ctr": "6-10%"}},
    {{"keyword": "키워드3", "type": "긴급구매형", "affiliate_potential": "매우높음", "ctr": "10-15%"}}
  ],
  "longtail_keywords": ["롱테일1 최저가", "롱테일2 쿠폰", "롱테일3 할인", "롱테일4 추천", "롱테일5 후기"],
  "purchase_queries": [
    "어디서 사는게 제일 싸요?",
    "이거 쿠폰 있나요?",
    "진짜 좋은가요?"
  ],
  "recommended_titles": [
    {{"title": "제목1 | 최저가 찾음 | 쿠폰까지", "hook": "가격할인", "ctr_score": 90, "affiliate_revenue": "매우높음"}},
    {{"title": "제목2 VS 제목2 | 솔직비교", "hook": "비교검증", "ctr_score": 88, "affiliate_revenue": "높음"}},
    {{"title": "이거 사지마세요 | 제목3 진실", "hook": "긴급주의", "ctr_score": 92, "affiliate_revenue": "매우높음"}}
  ],
  "shopping_strategy": {{
    "intro": "강력한 훅 (가격 충격, 품절 경고, 대박 할인)",
    "body": "제품 핵심 정보 + 가격 비교 + 쿠폰/할인 정보 + 구매 링크",
    "conclusion": "제휴 링크 클릭 유도 (\"설명란 최저가 링크\", \"댓글 쿠폰 확인\")",
    "platforms": ["쿠팡파트너스", "네이버쇼핑", "11번가", "G마켓"],
    "revenue_per_view": "조회수 1만당 10-30만원 (제휴 수수료 3-5%)"
  }}
}}

숏폼 쇼핑 채널에 최적화된 자연스러운 한국어로 작성하세요."""
    
    def _get_chinese_prompt(self, topic):
        """中文提示"""
        return f"""您是月入10万元的AdSense和博客专业顾问。

主题：{topic}

请执行以下操作：

1. **识别核心需求**：用户想要什么（退款、申请、资格、费用、方法等）
2. **关键词扩展**：按3大盈利类型扩展
   - 行动诱导型："申请方法"、"下载"、"立即前往"、"查询"
   - 高龄目标型：40-60岁人群搜索的关键词
   - 金融相关："退款"、"补助金"、"折扣"、"优惠"
3. **搜索意图匹配**：实际搜索框中输入的具体问题
4. **长尾关键词**：竞争少但有需求的细分关键词

JSON格式响应：
{{
  "main_keyword": "主关键词",
  "core_needs": ["需求1", "需求2", "需求3"],
  "high_revenue_keywords": [
    {{"keyword": "关键词1", "type": "行动诱导型", "competition": "low/medium/high", "cpc_potential": "高/中/低"}},
    {{"keyword": "关键词2", "type": "高龄目标型", "competition": "low/medium/high", "cpc_potential": "高/中/低"}},
    {{"keyword": "关键词3", "type": "金融相关", "competition": "low/medium/high", "cpc_potential": "高/中/低"}}
  ],
  "longtail_keywords": ["长尾1", "长尾2", "长尾3", "长尾4", "长尾5"],
  "search_queries": ["实际搜索问题1", "实际搜索问题2", "实际搜索问题3"],
  "recommended_titles": [
    {{"title": "标题1", "hook": "吸引元素", "ctr_score": 85}},
    {{"title": "标题2", "hook": "吸引元素", "ctr_score": 90}},
    {{"title": "标题3", "hook": "吸引元素", "ctr_score": 88}}
  ],
  "content_strategy": {{
    "intro": "引言策略（吸引注意）",
    "body": "主体策略（核心信息和行动号召）",
    "conclusion": "结论策略（总结和链接引导）"
  }}
}}

请使用母语者听起来自然的中文。"""
    
    def _get_english_prompt(self, topic):
        """English prompt - Short-form Shopping Channel Strategy"""
        return f"""You are a short-form shopping channel expert earning $20K+/month.

Topic/Product: {topic}

Perform the following:

1. **Identify Purchase Needs**: What users want (price, discounts, reviews, comparisons, how-to)
2. **Shopping Keyword Expansion**: High-revenue shopping keyword types
   - Purchase-inducing: "best price", "coupon code", "discount", "deal", "BOGO"
   - Comparison-validation: "VS", "comparison", "review", "honest opinion", "recommendation"
   - Urgent-purchase: "selling out", "today only", "limited stock", "flash sale"
3. **Actual Purchase Searches**: Keywords searched right before purchase
4. **Affiliate Optimization**: Amazon Associates, ClickBank, ShareASale revenue maximization

Respond in JSON format:
{{
  "main_keyword": "main product/keyword",
  "product_category": "product category",
  "purchase_needs": ["price comparison", "discount info", "reviews"],
  "high_revenue_keywords": [
    {{"keyword": "keyword1", "type": "purchase-inducing", "affiliate_potential": "high", "ctr": "8-12%"}},
    {{"keyword": "keyword2", "type": "comparison-validation", "affiliate_potential": "high", "ctr": "6-10%"}},
    {{"keyword": "keyword3", "type": "urgent-purchase", "affiliate_potential": "very high", "ctr": "10-15%"}}
  ],
  "longtail_keywords": ["longtail1 best price", "longtail2 coupon", "longtail3 discount", "longtail4 recommended", "longtail5 review"],
  "purchase_queries": ["Where to buy cheapest?", "Any coupon codes?", "Is it really good?"],
  "recommended_titles": [
    {{"title": "Title1 | Found Lowest Price | Plus Coupon", "hook": "price discount", "ctr_score": 90, "affiliate_revenue": "very high"}},
    {{"title": "Title2 VS Title2 | Honest Comparison", "hook": "comparison validation", "ctr_score": 88, "affiliate_revenue": "high"}},
    {{"title": "Don't Buy This | Title3 Truth", "hook": "urgent warning", "ctr_score": 92, "affiliate_revenue": "very high"}}
  ],
  "shopping_strategy": {{
    "intro": "Strong hook (price shock, stock warning, huge discount)",
    "body": "Product key info + price comparison + coupon/discount info + purchase link",
    "conclusion": "Affiliate link click guidance (\"Link in description\", \"Check pinned comment for coupon\")",
    "platforms": ["Amazon Associates", "ClickBank", "ShareASale", "CJ Affiliate"],
    "revenue_per_view": "$10-30 per 10K views (3-5% commission)"
  }}
}}

Write in natural English optimized for short-form shopping channels."""
    
    def _get_japanese_prompt(self, topic):
        """日本語プロンプト - ショート動画ショッピングチャンネル戦略"""
        return f"""あなたは月収200万円以上を稼ぐショート動画ショッピングチャンネルの専門家です。

トピック/商品：{topic}

以下を実行してください：

1. **購入ニーズの特定**：ユーザーが求めるもの（価格、割引、レビュー、比較、使い方など）
2. **ショッピングキーワード拡張**：高収益ショッピングキーワードタイプ
   - 購入誘導型：「最安値」、「クーポン」、「割引コード」、「特価」、「セール」
   - 比較検証型：「VS」、「比較」、「レビュー」、「本音」、「おすすめ」
   - 緊急購入型：「在庫わずか」、「今日だけ」、「限定」、「タイムセール」
3. **実際の購入検索語**：購入直前に検索するキーワード
4. **アフィリエイト最適化**：楽天、Amazon、Yahoo!ショッピング等の収益最大化

JSON形式で応答：
{{
  "main_keyword": "メイン商品/キーワード",
  "product_category": "商品カテゴリー",
  "purchase_needs": ["価格比較", "割引情報", "レビュー"],
  "high_revenue_keywords": [
    {{"keyword": "キーワード1", "type": "購入誘導型", "affiliate_potential": "高", "ctr": "8-12%"}},
    {{"keyword": "キーワード2", "type": "比較検証型", "affiliate_potential": "高", "ctr": "6-10%"}},
    {{"keyword": "キーワード3", "type": "緊急購入型", "affiliate_potential": "非常に高", "ctr": "10-15%"}}
  ],
  "longtail_keywords": ["ロングテール1 最安値", "ロングテール2 クーポン", "ロングテール3 割引", "ロングテール4 おすすめ", "ロングテール5 口コミ"],
  "purchase_queries": ["どこが一番安い？", "クーポンある？", "本当にいい？"],
  "recommended_titles": [
    {{"title": "タイトル1 | 最安値発見 | クーポンも", "hook": "価格割引", "ctr_score": 90, "affiliate_revenue": "非常に高"}},
    {{"title": "タイトル2 VS タイトル2 | 本音比較", "hook": "比較検証", "ctr_score": 88, "affiliate_revenue": "高"}},
    {{"title": "これ買うな | タイトル3 真実", "hook": "緊急注意", "ctr_score": 92, "affiliate_revenue": "非常に高"}}
  ],
  "shopping_strategy": {{
    "intro": "強力なフック（価格衝撃、在庫警告、大幅割引）",
    "body": "商品の重要情報 + 価格比較 + クーポン/割引情報 + 購入リンク",
    "conclusion": "アフィリエイトリンククリック誘導（「概要欄に最安値リンク」、「コメント欄クーポン確認」）",
    "platforms": ["楽天アフィリエイト", "Amazonアソシエイト", "Yahoo!ショッピング", "A8.net"],
    "revenue_per_view": "1万再生で10-30万円（アフィリエイト報酬3-5%）"
  }}
}}

ショート動画ショッピングチャンネルに最適化された自然な日本語で書いてください。"""
    
    def _get_thai_prompt(self, topic):
        """คำแนะนำภาษาไทย - กลยุทธ์ช่องช้อปปิ้งวิดีโอสั้น"""
        return f"""คุณเป็นผู้เชี่ยวชาญช่องช้อปปิ้งวิดีโอสั้นที่มีรายได้เดือนละ 2 ล้านบาทขึ้นไป

หัวข้อ/สินค้า: {topic}

กรุณาดำเนินการดังนี้:

1. **ระบุความต้องการซื้อ**：ผู้ใช้ต้องการอะไร（ราคา ส่วนลด รีวิว เปรียบเทียบ วิธีใช้）
2. **ขยายคำหลักช้อปปิ้ง**：คำหลักช้อปปิ้งรายได้สูง
   - กระตุ้นการซื้อ："ราคาถูกที่สุด"、"คูปอง"、"โค้ดส่วนลด"、"ราคาพิเศษ"、"ซื้อ 1 แถม 1"
   - เปรียบเทียบตรวจสอบ："VS"、"เปรียบเทียบ"、"รีวิว"、"ความคิดเห็นจริง"、"แนะนำ"
   - ซื้อด่วน："เหลือน้อย"、"วันนี้เท่านั้น"、"จำนวนจำกัด"、"เซลล์ด่วน"
3. **คำค้นหาก่อนซื้อจริง**：คำหลักที่ค้นหาก่อนซื้อ
4. **เพิ่มประสิทธิภาพพันธมิตร**：Lazada, Shopee, JD Central รายได้สูงสุด

ตอบกลับในรูปแบบ JSON:
{{
  "main_keyword": "สินค้า/คำหลักหลัก",
  "product_category": "หมวดสินค้า",
  "purchase_needs": ["เปรียบเทียบราคา", "ข้อมูลส่วนลด", "รีวิว"],
  "high_revenue_keywords": [
    {{"keyword": "คำหลัก1", "type": "กระตุ้นการซื้อ", "affiliate_potential": "สูง", "ctr": "8-12%"}},
    {{"keyword": "คำหลัก2", "type": "เปรียบเทียบตรวจสอบ", "affiliate_potential": "สูง", "ctr": "6-10%"}},
    {{"keyword": "คำหลัก3", "type": "ซื้อด่วน", "affiliate_potential": "สูงมาก", "ctr": "10-15%"}}
  ],
  "longtail_keywords": ["ลองเทล1 ราคาถูกที่สุด", "ลองเทล2 คูปอง", "ลองเทล3 ส่วนลด", "ลองเทล4 แนะนำ", "ลองเทล5 รีวิว"],
  "purchase_queries": ["ซื้อที่ไหนถูกที่สุด?", "มีคูปองไหม?", "ดีจริงไหม?"],
  "recommended_titles": [
    {{"title": "หัวข้อ1 | เจอราคาถูกสุด | มีคูปองด้วย", "hook": "ส่วนลดราคา", "ctr_score": 90, "affiliate_revenue": "สูงมาก"}},
    {{"title": "หัวข้อ2 VS หัวข้อ2 | เปรียบเทียบจริง", "hook": "เปรียบเทียบตรวจสอบ", "ctr_score": 88, "affiliate_revenue": "สูง"}},
    {{"title": "อย่าซื้ออันนี้ | ความจริงหัวข้อ3", "hook": "เตือนด่วน", "ctr_score": 92, "affiliate_revenue": "สูงมาก"}}
  ],
  "shopping_strategy": {{
    "intro": "ดึงดูดแรง（ราคาช็อก คำเตือนสต็อก ส่วนลดใหญ่）",
    "body": "ข้อมูลสินค้าสำคัญ + เปรียบเทียบราคา + คูปอง/ส่วนลด + ลิงก์ซื้อ",
    "conclusion": "นำทางคลิกลิงก์พันธมิตร（\"ลิงก์ในคำอธิบาย\"、\"ดูคูปองในคอมเมนต์\"）",
    "platforms": ["Lazada Affiliate", "Shopee Affiliate", "JD Central", "AccessTrade"],
    "revenue_per_view": "1 หมื่นวิว ได้ 1-3 หมื่นบาท（ค่าคอมมิชชั่น 3-5%）"
  }}
}}

กรุณาเขียนภาษาไทยที่เหมาะกับช่องช้อปปิ้งวิดีโอสั้นและเป็นธรรมชาติ"""
    
    def _generate_default_keywords(self, topic):
        """기본 키워드 생성 (API 없을 때)"""
        return {
            "main_keyword": topic,
            "core_needs": ["신청", "조회", "방법"],
            "high_revenue_keywords": [
                {"keyword": f"{topic} 신청방법", "type": "행동유도형", "competition": "medium", "cpc_potential": "높음"},
                {"keyword": f"{topic} 환급", "type": "금융/돈관련", "competition": "medium", "cpc_potential": "높음"},
                {"keyword": f"{topic} 자격조건", "type": "고연령타겟형", "competition": "low", "cpc_potential": "중간"}
            ],
            "longtail_keywords": [
                f"{topic} 신청 바로가기",
                f"{topic} 대상자 확인",
                f"{topic} 지급일",
                f"{topic} 온라인 신청",
                f"{topic} 서류"
            ],
            "search_queries": [
                f"{topic} 어떻게 신청하나요?",
                f"{topic} 언제 받나요?",
                f"{topic} 자격이 어떻게 되나요?"
            ],
            "recommended_titles": [
                {"title": f"{topic} 신청방법 총정리 | 5분만에 완료하는 방법", "hook": "시간 절약", "ctr_score": 85},
                {"title": f"놓치면 손해! {topic} 꼭 확인하세요", "hook": "손실 회피", "ctr_score": 90},
                {"title": f"{topic} 대상자라면 꼭 보세요 | 신청 가이드", "hook": "타겟 특정", "ctr_score": 88}
            ],
            "content_strategy": {
                "intro": "독자의 관심을 끄는 질문이나 통계로 시작",
                "body": "신청 방법, 자격 조건, 필요 서류 등 구체적 정보 제공",
                "conclusion": "요약 및 신청 링크 유도"
            }
        }
    
    def display_and_select(self, analysis_result):
        """
        분석 결과를 보여주고 사용자가 선택하도록 함
        
        Args:
            analysis_result: analyze_topic()의 결과
        
        Returns:
            dict: 사용자가 선택한 키워드와 제목
        """
        print("\n" + "="*80)
        print("🎯 키워드 및 제목 분석 결과")
        print("="*80)
        
        # 1. 핵심 공략 키워드
        print("\n### 1. 🎯 핵심 공략 키워드")
        print(f"**메인 키워드**: {analysis_result['main_keyword']}")
        print(f"**핵심 니즈**: {', '.join(analysis_result['core_needs'])}")
        
        # 2. 돈 되는 세부 키워드 리스트
        print("\n### 2. 💸 돈 되는 세부 키워드 리스트")
        print("\n**고수익 키워드 (선택 가능):**")
        high_revenue = analysis_result['high_revenue_keywords']
        for i, kw in enumerate(high_revenue, 1):
            print(f"   [{i}] {kw['keyword']}")
            print(f"       유형: {kw['type']} | 경쟁도: {kw['competition']} | CPC: {kw['cpc_potential']}")
        
        print("\n**롱테일 키워드 (선택 가능):**")
        longtail = analysis_result['longtail_keywords']
        for i, kw in enumerate(longtail, 1):
            print(f"   [{i + len(high_revenue)}] {kw}")
        
        print("\n**실제 검색 질문:**")
        for query in analysis_result['search_queries']:
            print(f"   • {query}")
        
        # 3. 클릭을 부르는 제목 추천
        print("\n### 3. ✍️ 클릭을 부르는 제목 추천")
        titles = analysis_result['recommended_titles']
        for i, title_info in enumerate(titles, 1):
            print(f"\n   [{i}] {title_info['title']}")
            print(f"       훅킹 요소: {title_info['hook']} | CTR 점수: {title_info['ctr_score']}/100")
        
        # 4. 수익형 본문 구성 전략
        print("\n### 4. 📝 수익형 본문 구성 전략")
        strategy = analysis_result['content_strategy']
        print(f"   **서론**: {strategy['intro']}")
        print(f"   **본론**: {strategy['body']}")
        print(f"   **결론**: {strategy['conclusion']}")
        
        # 사용자 선택 받기
        print("\n" + "="*80)
        print("📌 원하는 항목을 선택하세요")
        print("="*80)
        
        # 키워드 선택
        print("\n🔑 키워드 선택 (쉼표로 구분, 예: 1,3,5):")
        print(f"   선택 가능: 1-{len(high_revenue) + len(longtail)}")
        
        try:
            keyword_input = input("선택할 키워드 번호: ").strip()
            if keyword_input:
                selected_keyword_indices = [int(x.strip()) - 1 for x in keyword_input.split(',')]
            else:
                selected_keyword_indices = [0, 1, 2]  # 기본값: 처음 3개
            
            # 선택된 키워드 추출
            all_keywords = []
            for kw in high_revenue:
                all_keywords.append(kw['keyword'])
            all_keywords.extend(longtail)
            
            selected_keywords = [all_keywords[i] for i in selected_keyword_indices if i < len(all_keywords)]
            
        except (ValueError, IndexError):
            print("⚠️  잘못된 입력입니다. 기본값을 사용합니다.")
            selected_keywords = [kw['keyword'] for kw in high_revenue[:3]]
        
        # 제목 선택
        print(f"\n📰 제목 선택 (1-{len(titles)}):")
        
        try:
            title_input = input("선택할 제목 번호: ").strip()
            if title_input:
                selected_title_index = int(title_input) - 1
            else:
                selected_title_index = 1  # 기본값: 2번째 (가장 높은 CTR)
            
            selected_title = titles[selected_title_index]['title']
            
        except (ValueError, IndexError):
            print("⚠️  잘못된 입력입니다. 기본값을 사용합니다.")
            selected_title = titles[1]['title']
        
        # 선택 결과 출력
        print("\n" + "="*80)
        print("✅ 선택 완료")
        print("="*80)
        print(f"\n**선택된 키워드** ({len(selected_keywords)}개):")
        for kw in selected_keywords:
            print(f"   ✓ {kw}")
        
        print(f"\n**선택된 제목**:")
        print(f"   ✓ {selected_title}")
        
        # 자동으로 스크립트 파일 생성 제안
        print("\n💡 이 내용을 YouTube 숏폼 스크립트로 자동 생성하시겠습니까? (y/n)")
        auto_generate = input("선택: ").strip().lower()
        
        result = {
            'selected_keywords': selected_keywords,
            'selected_title': selected_title,
            'main_keyword': analysis_result['main_keyword'],
            'content_strategy': analysis_result['content_strategy'],
            'auto_generate': auto_generate == 'y'
        }
        
        return result
    
    def generate_script_from_selection(self, selection_result):
        """
        선택된 키워드와 제목으로 YouTube 숏폼 스크립트 자동 생성
        
        Args:
            selection_result: display_and_select()의 결과
        
        Returns:
            dict: YouTube 숏폼용 스크립트
        """
        try:
            import google.generativeai as genai
            
            if not os.getenv('GEMINI_API_KEY'):
                return self._generate_default_script(selection_result)
            
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""다음 정보로 YouTube 숏폼 대본을 작성하세요:

제목: {selection_result['selected_title']}
키워드: {', '.join(selection_result['selected_keywords'])}
주제: {selection_result['main_keyword']}

요구사항:
- 15-30초 분량
- 첫 3초에 강력한 훅 (호기심 유발)
- 핵심 정보 3-5개 포인트
- 행동 유도 (CTA): 구독, 좋아요, 댓글
- 자연스러운 한국어
- 고연령층(40-60대)도 이해하기 쉽게

JSON 형식으로 응답:
{{
  "script_text": "전체 대본",
  "duration": 25,
  "hook": "첫 3초 대사",
  "key_points": ["포인트1", "포인트2", "포인트3"],
  "cta": "행동 유도 멘트"
}}
"""
            
            response = model.generate_content(prompt)
            result_text = response.text
            
            # JSON 파싱
            if '```json' in result_text:
                json_str = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                json_str = result_text.split('```')[1].split('```')[0].strip()
            else:
                json_str = result_text.strip()
            
            script_data = json.loads(json_str)
            
            # 전체 스크립트 구성
            full_script = {
                "title": selection_result['selected_title'],
                "script_text": script_data['script_text'],
                "duration": script_data['duration'],
                "voice_id": "ko-KR-SunHiNeural",
                "category": "finance",  # 대부분 애드센스 콘텐츠는 재테크/정보
                "hashtags": ['#' + kw.replace(' ', '') for kw in selection_result['selected_keywords'][:5]],
                "description": f"{selection_result['main_keyword']} 관련 정보를 빠르게 알려드립니다. " + 
                              f"키워드: {', '.join(selection_result['selected_keywords'])}",
                "thumbnail_text": {
                    "main": selection_result['main_keyword'],
                    "sub": "꿀팁"
                }
            }
            
            return full_script
            
        except Exception as e:
            print(f"⚠️  스크립트 생성 실패: {str(e)}")
            return self._generate_default_script(selection_result)
    
    def _generate_default_script(self, selection_result):
        """기본 스크립트 생성"""
        keywords = ', '.join(selection_result['selected_keywords'][:3])
        
        script_text = f"""여러분, {selection_result['main_keyword']} 정보 알아보시죠! 
첫 번째, {selection_result['selected_keywords'][0]}입니다. 
두 번째, {selection_result['selected_keywords'][1] if len(selection_result['selected_keywords']) > 1 else '자세한 내용'}을 확인하세요. 
세 번째, {selection_result['selected_keywords'][2] if len(selection_result['selected_keywords']) > 2 else '신청 방법'}도 있습니다. 
지금 바로 확인하세요! 구독과 좋아요 부탁드려요!"""
        
        return {
            "title": selection_result['selected_title'],
            "script_text": script_text,
            "duration": 20,
            "voice_id": "ko-KR-SunHiNeural",
            "category": "finance",
            "hashtags": ['#' + kw.replace(' ', '') for kw in selection_result['selected_keywords'][:5]],
            "description": f"{selection_result['main_keyword']} 관련 정보입니다.",
            "thumbnail_text": {
                "main": selection_result['main_keyword'],
                "sub": "필수 확인"
            }
        }
    
    def save_script(self, script_data, filename=None):
        """스크립트를 JSON 파일로 저장"""
        scripts_dir = Path('input/scripts')
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        if not filename:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"keyword_selected_{timestamp}.json"
        
        filepath = scripts_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 스크립트 저장 완료: {filepath}")
        return str(filepath)


def run_keyword_selector():
    """키워드 선택 시스템 실행"""
    import time
    
    print("\n" + "="*80)
    print("🎯 고수익 키워드 추천 및 선택 시스템")
    print("="*80)
    print("\n월 1000만원 블로그 수익화 전문 시스템")
    print("애드센스 고단가 키워드를 추출하고 YouTube 숏폼 스크립트를 자동 생성합니다.\n")
    
    selector = KeywordSelector()
    
    # 주제 입력
    print("📝 분석할 주제를 입력하세요 (뉴스, 정책, 이슈 등):")
    print("예시: 청년도약계좌, 전기차 보조금, 근로장려금, 건강보험 환급")
    topic = input("\n주제: ").strip()
    
    if not topic:
        print("⚠️  주제가 입력되지 않았습니다. 종료합니다.")
        return
    
    # 주제 분석
    print(f"\n🔍 '{topic}' 분석 중...")
    analysis_result = selector.analyze_topic(topic)
    
    # 결과 표시 및 선택
    selection_result = selector.display_and_select(analysis_result)
    
    # 자동 스크립트 생성
    if selection_result['auto_generate']:
        print("\n🎬 YouTube 숏폼 스크립트 생성 중...")
        script_data = selector.generate_script_from_selection(selection_result)
        
        # 저장
        script_path = selector.save_script(script_data)
        
        print("\n" + "="*80)
        print("🎉 완료!")
        print("="*80)
        print(f"\n다음 단계:")
        print(f"1. 이미지를 준비하세요 (제품 사진 또는 관련 이미지)")
        print(f"2. input/images/ 폴더에 '{Path(script_path).stem}.jpg' 이름으로 저장")
        print(f"3. python main.py 실행하여 자동 비디오 생성")
        print(f"\n💡 또는 지금 바로 main.py를 실행하시겠습니까? (y/n)")
        
        run_main = input("선택: ").strip().lower()
        if run_main == 'y':
            print("\n⚠️  먼저 이미지를 업로드해주세요!")
            print(f"   위치: input/images/{Path(script_path).stem}.jpg")
    else:
        print("\n✅ 키워드 선택 완료! 수동으로 스크립트를 작성하세요.")


if __name__ == '__main__':
    run_keyword_selector()
