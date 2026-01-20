#!/usr/bin/env python3
"""
다국어 키워드 선택 시스템
여러 언어와 버전 생성 지원
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MultilingualKeywordSelector:
    """다국어 키워드 및 버전 관리 시스템"""
    
    def __init__(self, language='ko'):
        self.language = language
        self.load_language_config()
        self.load_keyword_database()
        
    def load_language_config(self):
        """언어 설정 로드"""
        with open('config/languages.json', 'r', encoding='utf-8') as f:
            self.lang_config = json.load(f)
            
        if self.language not in self.lang_config['supported_languages']:
            print(f"⚠️  '{self.language}' 언어는 지원되지 않습니다. 한국어로 설정합니다.")
            self.language = 'ko'
            
        self.current_lang = self.lang_config['supported_languages'][self.language]
        
    def load_keyword_database(self):
        """키워드 데이터베이스 로드"""
        with open('config/keywords.json', 'r', encoding='utf-8') as f:
            self.keyword_db = json.load(f)
    
    def analyze_topic(self, topic, target_language=None):
        """
        다국어 주제 분석
        
        Args:
            topic: 입력 주제
            target_language: 출력 언어 (None이면 입력 언어와 동일)
        
        Returns:
            dict: 키워드 분석 결과
        """
        if target_language:
            self.language = target_language
            self.load_language_config()
            
        try:
            import google.generativeai as genai
            
            if not os.getenv('GEMINI_API_KEY'):
                print(f"⚠️  Gemini API 키가 없습니다. 기본 {self.current_lang['name']} 키워드를 사용합니다.")
                return self._generate_default_keywords(topic)
            
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 언어별 프롬프트
            prompts = {
                'ko': self._get_korean_prompt(topic),
                'zh': self._get_chinese_prompt(topic),
                'en': self._get_english_prompt(topic),
                'ja': self._get_japanese_prompt(topic),
                'th': self._get_thai_prompt(topic)
            }
            
            prompt = prompts.get(self.language, prompts['ko'])
            response = model.generate_content(prompt)
            
            return self._parse_ai_response(response.text)
            
        except Exception as e:
            print(f"❌ AI 분석 오류: {e}")
            return self._generate_default_keywords(topic)
    
    def _get_korean_prompt(self, topic):
        """한국어 프롬프트"""
        return f"""당신은 월 1000만원 수익을 달성한 애드센스/블로그 전문 컨설턴트입니다.

주제: {topic}

다음을 JSON 형식으로 출력하세요:

{{
  "main_keyword": "메인 키워드",
  "keywords": [
    {{"text": "키워드1", "type": "action", "cpc": "high", "competition": "medium"}},
    {{"text": "키워드2", "type": "finance", "cpc": "high", "competition": "low"}},
    (8개)
  ],
  "titles": [
    {{"text": "제목1", "ctr_score": 90, "hook": "손실 회피"}},
    {{"text": "제목2", "ctr_score": 88, "hook": "시간 절약"}},
    {{"text": "제목3", "ctr_score": 85, "hook": "타겟 특정"}}
  ],
  "content_strategy": {{
    "intro": "훅킹 요소",
    "body": "핵심 정보",
    "conclusion": "행동 유도"
  }}
}}

한국어로 작성하고, 행동유도형/금융관련/고연령타겟 키워드를 포함하세요."""

    def _get_chinese_prompt(self, topic):
        """중国语提示"""
        return f"""您是月入10万元的广告和博客专业顾问。

主题：{topic}

请以JSON格式输出以下内容：

{{
  "main_keyword": "主关键词",
  "keywords": [
    {{"text": "关键词1", "type": "action", "cpc": "high", "competition": "medium"}},
    {{"text": "关键词2", "type": "finance", "cpc": "high", "competition": "low"}},
    （8个）
  ],
  "titles": [
    {{"text": "标题1", "ctr_score": 90, "hook": "损失规避"}},
    {{"text": "标题2", "ctr_score": 88, "hook": "节省时间"}},
    {{"text": "标题3", "ctr_score": 85, "hook": "目标定位"}}
  ],
  "content_strategy": {{
    "intro": "吸引注意",
    "body": "核心信息",
    "conclusion": "行动号召"
  }}
}}

用中文写，包括行动诱导/金融相关/中老年目标关键词。"""

    def _get_english_prompt(self, topic):
        """English prompt"""
        return f"""You are an AdSense/blog consultant earning $100K+/year.

Topic: {topic}

Output in JSON format:

{{
  "main_keyword": "main keyword",
  "keywords": [
    {{"text": "keyword1", "type": "action", "cpc": "high", "competition": "medium"}},
    {{"text": "keyword2", "type": "finance", "cpc": "high", "competition": "low"}},
    (8 items)
  ],
  "titles": [
    {{"text": "title1", "ctr_score": 90, "hook": "loss aversion"}},
    {{"text": "title2", "ctr_score": 88, "hook": "time saving"}},
    {{"text": "title3", "ctr_score": 85, "hook": "target specific"}}
  ],
  "content_strategy": {{
    "intro": "hook element",
    "body": "core information",
    "conclusion": "call to action"
  }}
}}

Write in English, include action-inducing/finance-related/senior-targeting keywords."""

    def _get_japanese_prompt(self, topic):
        """日本語プロンプト"""
        return f"""あなたは月収1000万円を達成したアドセンス・ブログの専門コンサルタントです。

トピック：{topic}

JSON形式で以下を出力してください：

{{
  "main_keyword": "メインキーワード",
  "keywords": [
    {{"text": "キーワード1", "type": "action", "cpc": "high", "competition": "medium"}},
    {{"text": "キーワード2", "type": "finance", "cpc": "high", "competition": "low"}},
    （8個）
  ],
  "titles": [
    {{"text": "タイトル1", "ctr_score": 90, "hook": "損失回避"}},
    {{"text": "タイトル2", "ctr_score": 88, "hook": "時間節約"}},
    {{"text": "タイトル3", "ctr_score": 85, "hook": "ターゲット特定"}}
  ],
  "content_strategy": {{
    "intro": "フック要素",
    "body": "核心情報",
    "conclusion": "行動喚起"
  }}
}}

日本語で書き、行動誘導型・金融関連・シニア向けキーワードを含めてください。
原語民が聞いても自然な日本語表現を使用してください。"""

    def _get_thai_prompt(self, topic):
        """คำแนะนำภาษาไทย"""
        return f"""คุณเป็นที่ปรึกษามืออาชีพด้าน AdSense และบล็อกที่มีรายได้เดือนละ 1 ล้านบาท

หัวข้อ: {topic}

กรุณาส่งออกในรูปแบบ JSON:

{{
  "main_keyword": "คำหลัก",
  "keywords": [
    {{"text": "คำหลัก1", "type": "action", "cpc": "high", "competition": "medium"}},
    {{"text": "คำหลัก2", "type": "finance", "cpc": "high", "competition": "low"}},
    (8 รายการ)
  ],
  "titles": [
    {{"text": "หัวข้อ1", "ctr_score": 90, "hook": "การหลีกเลี่ยงการสูญเสีย"}},
    {{"text": "หัวข้อ2", "ctr_score": 88, "hook": "ประหยัดเวลา"}},
    {{"text": "หัวข้อ3", "ctr_score": 85, "hook": "กลุ่มเป้าหมายเฉพาะ"}}
  ],
  "content_strategy": {{
    "intro": "ดึงดูดความสนใจ",
    "body": "ข้อมูลหลัก",
    "conclusion": "เรียกร้องให้ดำเนินการ"
  }}
}}

เขียนเป็นภาษาไทย รวมคำหลักที่กระตุ้นการดำเนินการ/การเงิน/กลุ่มผู้สูงอายุ
ใช้ภาษาไทยที่เป็นธรรมชาติและเหมาะสมกับเจ้าของภาษา"""
    
    def _parse_ai_response(self, response_text):
        """AI 응답 파싱"""
        try:
            # JSON 추출
            import re
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                return json.loads(json_match.group())
            return None
        except:
            return None
    
    def _generate_default_keywords(self, topic):
        """기본 키워드 생성"""
        keyword_types = self.current_lang['keyword_types']
        ctr_phrases = self.current_lang['ctr_phrases']
        
        keywords = []
        for i, action in enumerate(keyword_types['action'][:3], 1):
            keywords.append({
                "text": f"{topic} {action}",
                "type": "action",
                "cpc": "high",
                "competition": "medium"
            })
        
        for i, finance in enumerate(keyword_types['finance'][:3], 1):
            keywords.append({
                "text": f"{topic} {finance}",
                "type": "finance",
                "cpc": "high",
                "competition": "low"
            })
        
        titles = [
            {
                "text": f"{ctr_phrases[0]}! {topic} {keyword_types['action'][0]}",
                "ctr_score": 90,
                "hook": ctr_phrases[0]
            },
            {
                "text": f"{ctr_phrases[1]} {topic} {keyword_types['finance'][0]}",
                "ctr_score": 88,
                "hook": ctr_phrases[1]
            },
            {
                "text": f"{ctr_phrases[2]} {topic}",
                "ctr_score": 85,
                "hook": ctr_phrases[2]
            }
        ]
        
        return {
            "main_keyword": topic,
            "keywords": keywords,
            "titles": titles,
            "content_strategy": {
                "intro": "Attention hook",
                "body": "Core information",
                "conclusion": "Call to action"
            }
        }
    
    def generate_versions(self, topic, selected_keywords, selected_title, num_versions=3):
        """
        여러 버전의 스크립트 생성
        
        Args:
            topic: 주제
            selected_keywords: 선택된 키워드 리스트
            selected_title: 선택된 제목
            num_versions: 생성할 버전 수
        
        Returns:
            list: 생성된 버전들
        """
        versions = []
        version_templates = self.lang_config['version_templates']
        
        for i, style in enumerate(version_templates['style_variants'][:num_versions], 1):
            for j, tone in enumerate(version_templates['tone_variants'][:1], 1):  # 각 스타일당 1개 톤
                version_id = f"v{len(versions)+1}"
                
                script = self._generate_script_for_version(
                    topic, selected_keywords, selected_title,
                    style, tone
                )
                
                version = {
                    "version_id": version_id,
                    "language": self.language,
                    "style": style['name'],
                    "tone": tone['name'],
                    "title": f"{selected_title} [{style['name']}]",
                    "script": script,
                    "duration": style['duration_range'][1],
                    "voice_id": self.current_lang['voices'][0],
                    "created_at": datetime.now().isoformat()
                }
                
                versions.append(version)
                
        return versions
    
    def _generate_script_for_version(self, topic, keywords, title, style, tone):
        """버전별 자연스러운 스크립트 생성 (원어민 수준)"""
        natural_exp = self.current_lang.get('natural_expressions', {})
        
        # 원어민 표현 가져오기
        intro = natural_exp.get('intro', [''])[0]
        transition = natural_exp.get('transition', [''])[0]
        emphasis = natural_exp.get('emphasis', [''])[0]
        conclusion = natural_exp.get('conclusion', [''])[0]
        
        # 언어별 자연스러운 스크립트 생성
        if self.language == 'ko':
            script = self._generate_korean_script(topic, keywords, title, style, tone, intro, transition, emphasis, conclusion)
        elif self.language == 'zh':
            script = self._generate_chinese_script(topic, keywords, title, style, tone, intro, transition, emphasis, conclusion)
        elif self.language == 'en':
            script = self._generate_english_script(topic, keywords, title, style, tone, intro, transition, emphasis, conclusion)
        elif self.language == 'ja':
            script = self._generate_japanese_script(topic, keywords, title, style, tone, intro, transition, emphasis, conclusion)
        elif self.language == 'th':
            script = self._generate_thai_script(topic, keywords, title, style, tone, intro, transition, emphasis, conclusion)
        else:
            script = f"{intro} {title}. {keywords[0]}."
            
        return script
    
    def _generate_korean_script(self, topic, keywords, title, style, tone, intro, transition, emphasis, conclusion):
        """한국어 자연스러운 스크립트"""
        if style['id'] == 'v1_short':
            if tone['id'] == 'urgent':
                return f"{intro}! {keywords[0]} {emphasis} 중요합니다. {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}~ {keywords[0]} 알아볼까요? {conclusion}!"
            else:
                return f"{intro}. {keywords[0]}를 소개합니다. {conclusion}."
        elif style['id'] == 'v2_standard':
            if tone['id'] == 'urgent':
                return f"{intro}! {topic}에 대해 알려드립니다. {emphasis} {keywords[0]}는 {emphasis} 필수입니다. {transition} {keywords[1]}도 중요하죠. {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}~ 오늘은 {topic} 이야기입니다. {keywords[0]} 궁금하시죠? {transition} {keywords[1]}도 함께 알아봐요. {conclusion}!"
            else:
                return f"{intro}. {topic}에 대해 알아보겠습니다. {keywords[0]}가 {emphasis} 핵심입니다. {transition} {keywords[1]}도 확인하세요. {conclusion}."
        else:  # detailed
            if tone['id'] == 'urgent':
                return f"{intro}! {topic}에 대한 중요한 정보입니다. 먼저 {keywords[0]}부터 {emphasis} 확인하세요. {transition} {keywords[1]}는 놓치면 안 됩니다. {keywords[2]}까지 모두 체크하셔야 합니다. {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}~ 오늘 주제는 {topic}이에요. {keywords[0]}에 대해 자세히 알아볼게요. {transition} {keywords[1]}도 재미있는 부분이죠. {keywords[2]}도 빼놓을 수 없어요. {conclusion}!"
            else:
                return f"{intro}. 오늘은 {topic}에 대해 상세히 알아보겠습니다. {keywords[0]}가 가장 중요한 포인트입니다. {transition} {keywords[1]}에 대해서도 살펴보겠습니다. {emphasis} {keywords[2]}를 통해 더 많은 정보를 얻으실 수 있습니다. {conclusion}."
    
    def _generate_chinese_script(self, topic, keywords, title, style, tone, intro, transition, emphasis, conclusion):
        """中文自然脚本"""
        if style['id'] == 'v1_short':
            if tone['id'] == 'urgent':
                return f"{intro}！{keywords[0]}{emphasis}很重要。{conclusion}！"
            elif tone['id'] == 'casual':
                return f"{intro}～我们来了解{keywords[0]}吧。{conclusion}！"
            else:
                return f"{intro}。今天介绍{keywords[0]}。{conclusion}。"
        elif style['id'] == 'v2_standard':
            if tone['id'] == 'urgent':
                return f"{intro}！关于{topic}的重要信息。{emphasis}{keywords[0]}是必须的。{transition}{keywords[1]}也很重要。{conclusion}！"
            elif tone['id'] == 'casual':
                return f"{intro}～今天说说{topic}。{keywords[0]}大家关心吗？{transition}{keywords[1]}也一起看看。{conclusion}！"
            else:
                return f"{intro}。我们了解一下{topic}。{keywords[0]}是{emphasis}核心。{transition}{keywords[1]}也请确认。{conclusion}。"
        else:
            if tone['id'] == 'urgent':
                return f"{intro}！关于{topic}的重要消息。首先{keywords[0]}{emphasis}必须确认。{transition}{keywords[1]}千万不要错过。{keywords[2]}也要全部检查。{conclusion}！"
            elif tone['id'] == 'casual':
                return f"{intro}～今天的话题是{topic}。详细了解{keywords[0]}。{transition}{keywords[1]}也很有趣。{keywords[2]}也不能错过。{conclusion}！"
            else:
                return f"{intro}。今天详细介绍{topic}。{keywords[0]}是最重要的要点。{transition}也看看{keywords[1]}。{emphasis}通过{keywords[2]}可以获得更多信息。{conclusion}。"
    
    def _generate_english_script(self, topic, keywords, title, style, tone, intro, transition, emphasis, conclusion):
        """Natural English script"""
        if style['id'] == 'v1_short':
            if tone['id'] == 'urgent':
                return f"{intro}! {keywords[0]} is {emphasis} crucial. {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}! Let's check out {keywords[0]}. {conclusion}!"
            else:
                return f"{intro}. Here's {keywords[0]}. {conclusion}."
        elif style['id'] == 'v2_standard':
            if tone['id'] == 'urgent':
                return f"{intro}! Important info about {topic}. {emphasis}, {keywords[0]} is essential. {transition}, {keywords[1]} matters too. {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}! Today we're talking about {topic}. Curious about {keywords[0]}? {transition}, let's look at {keywords[1]} too. {conclusion}!"
            else:
                return f"{intro}. Let's explore {topic}. {keywords[0]} is the {emphasis} key point. {transition}, check out {keywords[1]} as well. {conclusion}."
        else:
            if tone['id'] == 'urgent':
                return f"{intro}! Critical info on {topic}. First, {emphasis} verify {keywords[0]}. {transition}, don't miss {keywords[1]}. Check all including {keywords[2]}. {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}! Today's topic is {topic}. Let's dive into {keywords[0]}. {transition}, {keywords[1]} is interesting too. Can't skip {keywords[2]}. {conclusion}!"
            else:
                return f"{intro}. Today we'll cover {topic} in detail. {keywords[0]} is the most important point. {transition}, we'll also look at {keywords[1]}. {emphasis}, you can get more info through {keywords[2]}. {conclusion}."
    
    def _generate_japanese_script(self, topic, keywords, title, style, tone, intro, transition, emphasis, conclusion):
        """自然な日本語スクリプト"""
        if style['id'] == 'v1_short':
            if tone['id'] == 'urgent':
                return f"{intro}！{keywords[0]}は{emphasis}重要です。{conclusion}！"
            elif tone['id'] == 'casual':
                return f"{intro}～{keywords[0]}について見てみましょう。{conclusion}！"
            else:
                return f"{intro}。{keywords[0]}をご紹介します。{conclusion}。"
        elif style['id'] == 'v2_standard':
            if tone['id'] == 'urgent':
                return f"{intro}！{topic}についての重要な情報です。{emphasis}{keywords[0]}は必須です。{transition}{keywords[1]}も大切ですね。{conclusion}！"
            elif tone['id'] == 'casual':
                return f"{intro}～今日は{topic}のお話です。{keywords[0]}気になりますよね？{transition}{keywords[1]}も一緒に見ていきましょう。{conclusion}！"
            else:
                return f"{intro}。{topic}について見ていきます。{keywords[0]}が{emphasis}ポイントです。{transition}{keywords[1]}も確認してください。{conclusion}。"
        else:
            if tone['id'] == 'urgent':
                return f"{intro}！{topic}についての大事な情報です。まず{keywords[0]}を{emphasis}確認してください。{transition}{keywords[1]}は見逃せません。{keywords[2]}まで全部チェックが必要です。{conclusion}！"
            elif tone['id'] == 'casual':
                return f"{intro}～今日のテーマは{topic}です。{keywords[0]}について詳しく見ていきますね。{transition}{keywords[1]}も面白いポイントです。{keywords[2]}も外せません。{conclusion}！"
            else:
                return f"{intro}。今日は{topic}について詳しく見ていきましょう。{keywords[0]}が最も重要なポイントです。{transition}{keywords[1]}についても見ていきます。{emphasis}{keywords[2]}を通じてより多くの情報が得られます。{conclusion}。"
    
    def _generate_thai_script(self, topic, keywords, title, style, tone, intro, transition, emphasis, conclusion):
        """สคริปต์ภาษาไทยที่เป็นธรรมชาติ"""
        if style['id'] == 'v1_short':
            if tone['id'] == 'urgent':
                return f"{intro}! {keywords[0]}{emphasis}สำคัญมาก {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}~ มาดู{keywords[0]}กันนะคะ {conclusion}!"
            else:
                return f"{intro} วันนี้มา{keywords[0]} {conclusion}"
        elif style['id'] == 'v2_standard':
            if tone['id'] == 'urgent':
                return f"{intro}! ข้อมูลสำคัญเกี่ยวกับ{topic} {emphasis}{keywords[0]}จำเป็นมาก {transition}{keywords[1]}ก็สำคัญเช่นกัน {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}~ วันนี้เรื่อง{topic} อยากรู้เรื่อง{keywords[0]}ไหม? {transition}มาดู{keywords[1]}ด้วยกัน {conclusion}!"
            else:
                return f"{intro} เรามาดู{topic}กัน {keywords[0]}เป็น{emphasis}ประเด็นหลัก {transition}ตรวจสอบ{keywords[1]}ด้วย {conclusion}"
        else:
            if tone['id'] == 'urgent':
                return f"{intro}! ข้อมูลสำคัญเกี่ยวกับ{topic} อันดับแรก{keywords[0]}{emphasis}ต้องตรวจสอบ {transition}{keywords[1]}พลาดไม่ได้ ต้องเช็ค{keywords[2]}ทั้งหมด {conclusion}!"
            elif tone['id'] == 'casual':
                return f"{intro}~ วันนี้หัวข้อเรื่อง{topic} เรามาดู{keywords[0]}กันอย่างละเอียด {transition}{keywords[1]}ก็น่าสนใจนะ ไม่พลาด{keywords[2]} {conclusion}!"
            else:
                return f"{intro} วันนี้เรามาดู{topic}อย่างละเอียด {keywords[0]}เป็นประเด็นที่สำคัญที่สุด {transition}ดู{keywords[1]}ด้วย {emphasis}ผ่าน{keywords[2]}จะได้ข้อมูลเพิ่มเติม {conclusion}"
    
    def save_versions(self, versions):
        """버전들을 파일로 저장"""
        output_dir = Path('input/scripts/versions')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        for version in versions:
            filename = f"{version['language']}_{version['version_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(version, f, ensure_ascii=False, indent=2)
            
            saved_files.append(str(filepath))
            print(f"✅ 저장됨: {filepath}")
        
        return saved_files
    
    def interactive_select(self, topic):
        """인터랙티브 선택 인터페이스"""
        print("\n" + "="*60)
        print(f"🌍 {self.current_lang['name']} 고수익 키워드 선택 시스템")
        print("="*60)
        
        # 1. 주제 분석
        print(f"\n📊 주제 분석 중: {topic}")
        analysis = self.analyze_topic(topic)
        
        if not analysis:
            print("❌ 분석 실패")
            return None
        
        # 2. 키워드 표시
        print(f"\n🎯 핵심 공략 키워드")
        print(f"메인: {analysis['main_keyword']}\n")
        
        print("💸 돈 되는 세부 키워드 리스트")
        for i, kw in enumerate(analysis['keywords'], 1):
            print(f"[{i}] {kw['text']} ({kw['type']} | CPC: {kw['cpc']})")
        
        # 3. 제목 표시
        print(f"\n✍️ 클릭을 부르는 제목 추천")
        for i, title in enumerate(analysis['titles'], 1):
            star = "⭐" if title['ctr_score'] >= 88 else ""
            print(f"[{i}] {title['text']} (CTR: {title['ctr_score']}) {star}")
        
        # 4. 사용자 선택
        print("\n" + "="*60)
        keyword_input = input("선택할 키워드 번호 (쉼표로 구분, 예: 1,2,4): ").strip()
        title_input = input("선택할 제목 번호 (1-3): ").strip()
        
        try:
            keyword_indices = [int(x.strip())-1 for x in keyword_input.split(',')]
            title_index = int(title_input) - 1
            
            selected_keywords = [analysis['keywords'][i]['text'] for i in keyword_indices]
            selected_title = analysis['titles'][title_index]['text']
            
            print(f"\n✅ 선택 완료!")
            print(f"   키워드: {', '.join(selected_keywords)}")
            print(f"   제목: {selected_title}")
            
            # 5. 버전 생성
            print(f"\n🎬 여러 버전 생성 중...")
            versions = self.generate_versions(topic, selected_keywords, selected_title)
            
            # 6. 저장
            saved_files = self.save_versions(versions)
            
            print(f"\n✅ 총 {len(versions)}개 버전 생성 완료!")
            for version in versions:
                print(f"   - {version['version_id']}: {version['style']} / {version['tone']}")
            
            return {
                'versions': versions,
                'files': saved_files
            }
            
        except Exception as e:
            print(f"❌ 오류: {e}")
            return None

def main():
    """메인 실행 함수"""
    import sys
    
    print("\n" + "="*60)
    print("🌍 다국어 YouTube 숏폼 키워드 선택 시스템")
    print("="*60)
    
    # 언어 선택
    print("\n지원 언어:")
    print("1. 한국어 (ko)")
    print("2. 中文 (zh)")
    print("3. English (en)")
    print("4. 日本語 (ja)")
    print("5. ภาษาไทย (th)")
    
    lang_choice = input("\n언어 선택 (1-5): ").strip()
    lang_map = {'1': 'ko', '2': 'zh', '3': 'en', '4': 'ja', '5': 'th'}
    language = lang_map.get(lang_choice, 'ko')
    
    # 주제 입력
    topic = input("\n주제 입력: ").strip()
    
    if not topic:
        print("❌ 주제를 입력해주세요")
        return
    
    # 선택 시작
    selector = MultilingualKeywordSelector(language)
    result = selector.interactive_select(topic)
    
    if result:
        print("\n" + "="*60)
        print("🎉 완료! 생성된 버전들을 확인하세요.")
        print("="*60)

if __name__ == "__main__":
    main()
