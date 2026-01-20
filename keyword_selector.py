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
    """애드센스/블로그 수익화를 위한 키워드 선택 시스템"""
    
    def __init__(self):
        self.load_keyword_database()
        
    def load_keyword_database(self):
        """키워드 데이터베이스 로드"""
        with open('config/keywords.json', 'r', encoding='utf-8') as f:
            self.keyword_db = json.load(f)
    
    def analyze_topic(self, topic):
        """
        주제 분석 및 키워드 추출
        
        Args:
            topic: 사용자가 입력한 주제 (뉴스, 정책, 이슈 등)
        
        Returns:
            dict: 키워드 분석 결과
        """
        try:
            import google.generativeai as genai
            
            if not os.getenv('GEMINI_API_KEY'):
                print("⚠️  Gemini API 키가 없습니다. 기본 키워드를 사용합니다.")
                return self._generate_default_keywords(topic)
            
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""당신은 월 1000만원 수익을 달성한 애드센스/블로그 전문 컨설턴트입니다.

주제: {topic}

다음을 수행하세요:

1. **핵심 니즈 파악**: 이 주제에서 사용자가 원하는 것 (환급, 신청, 자격, 비용, 방법 등)
2. **키워드 확장**: 3대 수익화 유형에 맞춰 확장
   - 행동 유도형: "신청방법", "다운로드", "바로가기", "조회"
   - 고연령 타겟형: 40-60대가 검색하는 키워드
   - 금융/돈 관련: "환급", "지원금", "할인", "혜택"
3. **검색 의도 매칭**: 실제 검색창에 입력할 구체적 질문
4. **롱테일 키워드**: 경쟁이 덜하면서 수요 있는 세부 키워드

JSON 형식으로 응답:
{{
  "main_keyword": "메인 키워드",
  "core_needs": ["니즈1", "니즈2", "니즈3"],
  "high_revenue_keywords": [
    {{"keyword": "키워드1", "type": "행동유도형", "competition": "low/medium/high", "cpc_potential": "높음/중간/낮음"}},
    {{"keyword": "키워드2", "type": "고연령타겟형", "competition": "low/medium/high", "cpc_potential": "높음/중간/낮음"}},
    {{"keyword": "키워드3", "type": "금융/돈관련", "competition": "low/medium/high", "cpc_potential": "높음/중간/낮음"}}
  ],
  "longtail_keywords": ["롱테일1", "롱테일2", "롱테일3", "롱테일4", "롱테일5"],
  "search_queries": [
    "실제 검색 질문1",
    "실제 검색 질문2",
    "실제 검색 질문3"
  ],
  "recommended_titles": [
    {{"title": "제목1", "hook": "훅킹 요소", "ctr_score": 85}},
    {{"title": "제목2", "hook": "훅킹 요소", "ctr_score": 90}},
    {{"title": "제목3", "hook": "훅킹 요소", "ctr_score": 88}}
  ],
  "content_strategy": {{
    "intro": "서론 전략 (훅킹 요소)",
    "body": "본론 전략 (필수 정보 및 행동 유도)",
    "conclusion": "결론 전략 (요약 및 링크 유도)"
  }}
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
            
            result = json.loads(json_str)
            return result
            
        except Exception as e:
            print(f"⚠️  분석 실패: {str(e)}")
            return self._generate_default_keywords(topic)
    
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
