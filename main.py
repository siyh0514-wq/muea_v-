#!/usr/bin/env python3
"""
YouTube 숏폼 자동화 메인 스크립트
사용법: python main.py
"""

import os
import json
import time
import base64
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class YouTubeAutomation:
    def __init__(self):
        self.config = self.load_config()
        self.check_api_keys()
        
    def load_config(self):
        """설정 파일 로드"""
        with open('config/config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_api_keys(self):
        """필수 API 키 확인"""
        required_keys = {
            'GEMINI_API_KEY': '제미나이 AI',
            'DID_API_KEY': 'D-ID',
        }
        
        missing_keys = []
        for key, name in required_keys.items():
            if not os.getenv(key):
                missing_keys.append(f"{name} ({key})")
        
        if missing_keys:
            print("\n" + "="*60)
            print("⚠️  API 키가 설정되지 않았습니다")
            print("="*60)
            print("\n🔑 필요한 API 키:")
            for key in missing_keys:
                print(f"   - {key}")
            print("\n💡 시뮬레이션 모드로 실행됩니다:")
            print("   ✓ 이미지 분석 (기본값)")
            print("   ✓ 키워드 최적화 (기본값)")
            print("   ✓ 썸네일 생성")
            print("   ✗ 비디오 생성 (실제 생성 안됨)")
            print("\n📝 실제 사용하려면:")
            print("   1. .env 파일 생성")
            print("   2. GEMINI_API_KEY=your-key 입력")
            print("   3. DID_API_KEY=your-key 입력")
            print("\n⏸️  계속하려면 Enter, 종료하려면 Ctrl+C")
            try:
                input()
            except KeyboardInterrupt:
                print("\n\n종료합니다.")
                exit(0)
            print("\n시뮬레이션 모드로 계속합니다...\n")
    
    def scan_input_folder(self):
        """input 폴더에서 새 파일 스캔"""
        images_dir = Path('input/images')
        scripts_dir = Path('input/scripts')
        
        if not images_dir.exists() or not scripts_dir.exists():
            print("❌ input/images 또는 input/scripts 폴더가 없습니다.")
            return []
        
        # 이미지 파일 찾기
        image_files = list(images_dir.glob('*.jpg')) + \
                     list(images_dir.glob('*.jpeg')) + \
                     list(images_dir.glob('*.png'))
        
        # 매칭되는 스크립트가 있는 이미지만 처리
        matched_pairs = []
        for image_path in image_files:
            script_path = scripts_dir / f"{image_path.stem}.json"
            if script_path.exists():
                matched_pairs.append({
                    'image': image_path,
                    'script': script_path,
                    'name': image_path.stem
                })
        
        return matched_pairs
    
    def process_file_pair(self, pair):
        """이미지+스크립트 페어 처리"""
        print(f"\n{'='*60}")
        print(f"🎬 처리 시작: {pair['name']}")
        print(f"{'='*60}")
        
        # 1. 스크립트 로드
        print("\n📄 1. 스크립트 로드 중...")
        with open(pair['script'], 'r', encoding='utf-8') as f:
            script_data = json.load(f)
        print(f"   ✓ 제목: {script_data.get('title', 'N/A')}")
        print(f"   ✓ 시간: {script_data.get('duration', 'N/A')}초")
        
        # 2. 이미지 분석 (Gemini)
        print("\n🔍 2. 이미지 분석 중 (Gemini AI)...")
        analysis_result = self.analyze_image_with_gemini(pair['image'], script_data)
        print(f"   ✓ 제품 감지: {'예' if analysis_result.get('is_product') else '아니오'}")
        
        # 3. 제품 리서치 (제품인 경우)
        research_result = None
        if analysis_result.get('is_product'):
            print("\n🔎 3. 제품 리서치 중...")
            research_result = self.research_product(analysis_result)
            if research_result.get('selling'):
                print(f"   ✓ 판매 중: {len(research_result.get('platforms', []))}개 플랫폼")
                print(f"   ✓ 가격대: {research_result.get('price_range', 'N/A')}")
        else:
            print("\n⏭️  3. 제품 리서치 건너뛰기 (일반 이미지)")
        
        # 4. 키워드 최적화
        print("\n🎯 4. 키워드 최적화 중 (Gemini AI)...")
        optimized = self.optimize_keywords(script_data, analysis_result, research_result)
        print(f"   ✓ 원본 제목: {script_data.get('title', 'N/A')}")
        print(f"   ✓ 최적화 제목: {optimized['title']}")
        print(f"   ✓ 해시태그: {len(optimized['hashtags'])}개")
        
        # 5. 썸네일 생성
        print("\n🖼️  5. 썸네일 생성 중...")
        thumbnail_path = self.create_thumbnail(pair['image'], optimized)
        print(f"   ✓ 저장: {thumbnail_path}")
        
        # 6. 비디오 생성 (D-ID)
        print("\n🎥 6. 비디오 생성 중 (D-ID API)...")
        print("   ⏳ 5-8분 소요됩니다. 잠시만 기다려주세요...")
        video_path = self.create_video_with_did(pair['image'], script_data['script_text'], 
                                                 script_data.get('voice_id', 'ko-KR-SunHiNeural'))
        print(f"   ✓ 비디오 생성 완료: {video_path}")
        
        # 7. 메타데이터 저장
        print("\n💾 7. 메타데이터 저장 중...")
        metadata_path = self.save_metadata(pair['name'], optimized, analysis_result, research_result)
        print(f"   ✓ 저장: {metadata_path}")
        
        # 8. YouTube 업로드 (선택사항)
        youtube_url = None
        if os.getenv('YOUTUBE_CLIENT_ID'):
            print("\n📤 8. YouTube 업로드 중...")
            youtube_url = self.upload_to_youtube(video_path, thumbnail_path, optimized)
            print(f"   ✓ 업로드 완료: {youtube_url}")
        else:
            print("\n⏭️  8. YouTube 업로드 건너뛰기 (API 키 없음)")
            print("   💡 비디오는 output/videos/ 폴더에 저장되었습니다.")
        
        # 9. 원본 파일 이동
        print("\n📦 9. 파일 정리 중...")
        self.move_to_completed(pair)
        print("   ✓ 원본 파일을 completed 폴더로 이동")
        
        print(f"\n{'='*60}")
        print("✅ 처리 완료!")
        print(f"{'='*60}")
        
        return {
            'name': pair['name'],
            'video': video_path,
            'thumbnail': thumbnail_path,
            'metadata': metadata_path,
            'youtube_url': youtube_url,
            'optimized': optimized
        }
    
    def analyze_image_with_gemini(self, image_path, script_data):
        """Gemini로 이미지 분석"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 이미지 로드
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 프롬프트 로드
            with open('prompts/prompts.json', 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            
            prompt = prompts['keyword_analysis']['prompt_template'].format(
                image_description="이미지 분석",
                category=script_data.get('category', 'general')
            )
            
            # API 호출
            response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': image_data}])
            
            # JSON 응답 파싱
            result_text = response.text
            # JSON 블록 추출
            if '```json' in result_text:
                json_str = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                json_str = result_text.split('```')[1].split('```')[0].strip()
            else:
                json_str = result_text.strip()
            
            result = json.loads(json_str)
            
            # 제품 여부 판단
            result['is_product'] = result.get('category') in ['tech', 'lifestyle'] and \
                                   any(keyword in result.get('main_topic', '').lower() 
                                       for keyword in ['제품', '기기', '아이템', 'product'])
            
            return result
            
        except Exception as e:
            print(f"   ⚠️  Gemini 분석 실패: {str(e)}")
            return {
                'main_topic': script_data.get('title', '주제'),
                'high_revenue_keywords': ['AI', '자동화', '돈버는법', '꿀팁', '2024'],
                'top_tier_keywords': ['1분만에', '꿀팁', '대박'],
                'category': script_data.get('category', 'general'),
                'is_product': False
            }
    
    def research_product(self, analysis_result):
        """제품 리서치 (간단한 버전)"""
        # 실제로는 Google Custom Search API를 사용
        # 여기서는 시뮬레이션
        print("   💡 실제 제품 리서치를 위해서는 Google Custom Search API가 필요합니다.")
        return {
            'selling': True,
            'platforms': ['쿠팡', '네이버쇼핑'],
            'price_range': '가격 정보 없음',
            'recommendation': '제품 리뷰 콘텐츠'
        }
    
    def optimize_keywords(self, script_data, analysis_result, research_result):
        """키워드 최적화"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 키워드 DB 로드
            with open('config/keywords.json', 'r', encoding='utf-8') as f:
                keywords_db = json.load(f)
            
            prompt = f"""다음 콘텐츠를 YouTube 숏폼에 최적화하세요:

원본 제목: {script_data.get('title')}
카테고리: {analysis_result.get('category')}
주요 주제: {analysis_result.get('main_topic')}
고수익 키워드: {', '.join(analysis_result.get('high_revenue_keywords', []))}

최적화 규칙:
1. 고수익 키워드 1-2개 포함
2. "꿀팁", "1분만에", "대박" 등 클릭 유도 키워드 사용
3. 60자 이내
4. 호기심 자극

JSON 형식으로 응답:
{{
  "title": "최적화된 제목",
  "hashtags": ["#해시태그1", "#해시태그2", ...15개],
  "description": "SEO 최적화된 설명"
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
            
            optimized = json.loads(json_str)
            
            return optimized
            
        except Exception as e:
            print(f"   ⚠️  최적화 실패, 기본값 사용: {str(e)}")
            return {
                'title': f"{script_data.get('title')} | 1분만에 보는 꿀팁 | 구독필수",
                'hashtags': ['#shorts', '#숏폼'] + analysis_result.get('high_revenue_keywords', [])[:5],
                'description': script_data.get('description', script_data.get('title'))
            }
    
    def create_thumbnail(self, image_path, optimized):
        """썸네일 생성 (간단한 버전)"""
        from PIL import Image, ImageDraw, ImageFont
        import shutil
        
        # 출력 경로
        output_dir = Path('output/thumbnails')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{image_path.stem}_thumbnail.png"
        
        # 일단 원본 이미지 복사 (나중에 텍스트 오버레이 추가 가능)
        shutil.copy(image_path, output_path)
        
        return str(output_path)
    
    def create_video_with_did(self, image_path, script_text, voice_id):
        """D-ID로 비디오 생성"""
        import requests
        
        api_key = os.getenv('DID_API_KEY')
        if not api_key:
            print("   ⚠️  D-ID API 키가 없습니다. 시뮬레이션 모드...")
            # 시뮬레이션: 이미지를 비디오로 복사
            output_dir = Path('output/videos')
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{image_path.stem}_final.mp4"
            
            import shutil
            shutil.copy(image_path, output_path.with_suffix('.jpg'))
            print("   💡 실제 비디오를 생성하려면 D-ID API 키가 필요합니다.")
            return str(output_path.with_suffix('.jpg'))
        
        try:
            # 1. 이미지 업로드 (실제로는 S3나 다른 호스팅 필요)
            print("   📤 이미지 업로드 중...")
            
            # 2. D-ID API 호출
            url = "https://api.d-id.com/talks"
            headers = {
                "Authorization": f"Basic {base64.b64encode(api_key.encode()).decode()}",
                "Content-Type": "application/json"
            }
            
            # 이미지를 base64로 인코딩
            with open(image_path, 'rb') as f:
                image_base64 = base64.b64encode(f.read()).decode()
            
            payload = {
                "source_url": f"data:image/jpeg;base64,{image_base64}",
                "script": {
                    "type": "text",
                    "input": script_text,
                    "provider": {
                        "type": "microsoft",
                        "voice_id": voice_id
                    }
                },
                "config": {
                    "stitch": True,
                    "result_format": "mp4"
                }
            }
            
            print("   🎬 비디오 생성 요청 중...")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            talk_id = response.json()['id']
            print(f"   ✓ Talk ID: {talk_id}")
            
            # 3. 결과 폴링
            print("   ⏳ 비디오 생성 대기 중...")
            max_wait = 300  # 5분
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                time.sleep(5)
                
                status_response = requests.get(
                    f"https://api.d-id.com/talks/{talk_id}",
                    headers=headers
                )
                status_data = status_response.json()
                status = status_data.get('status')
                
                print(f"   ⏳ 상태: {status}")
                
                if status == 'done':
                    video_url = status_data['result_url']
                    print("   ✓ 비디오 생성 완료!")
                    
                    # 비디오 다운로드
                    video_response = requests.get(video_url)
                    output_dir = Path('output/videos')
                    output_dir.mkdir(parents=True, exist_ok=True)
                    output_path = output_dir / f"{image_path.stem}_final.mp4"
                    
                    with open(output_path, 'wb') as f:
                        f.write(video_response.content)
                    
                    return str(output_path)
                
                elif status == 'error':
                    print(f"   ❌ 생성 실패: {status_data.get('error')}")
                    break
            
            print("   ⚠️  타임아웃: 비디오 생성에 시간이 너무 오래 걸립니다.")
            return None
            
        except Exception as e:
            print(f"   ❌ D-ID 오류: {str(e)}")
            return None
    
    def save_metadata(self, name, optimized, analysis_result, research_result):
        """메타데이터 저장"""
        output_dir = Path('output/optimized')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{name}_metadata.json"
        
        metadata = {
            'name': name,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'optimized': optimized,
            'analysis': analysis_result,
            'research': research_result
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return str(output_path)
    
    def upload_to_youtube(self, video_path, thumbnail_path, optimized):
        """YouTube 업로드 (시뮬레이션)"""
        print("   💡 실제 업로드를 위해서는 YouTube Data API 설정이 필요합니다.")
        print("   💡 비디오와 썸네일은 output/ 폴더에 저장되었습니다.")
        return "https://youtube.com/shorts/simulated"
    
    def move_to_completed(self, pair):
        """처리 완료된 파일 이동"""
        completed_dir = Path('input/completed')
        completed_dir.mkdir(parents=True, exist_ok=True)
        
        import shutil
        shutil.move(pair['image'], completed_dir / pair['image'].name)
        shutil.move(pair['script'], completed_dir / pair['script'].name)
    
    def run(self):
        """메인 실행"""
        print("\n" + "="*60)
        print("🚀 YouTube 숏폼 자동화 시스템")
        print("="*60)
        
        # 입력 파일 스캔
        print("\n📂 입력 파일 스캔 중...")
        pairs = self.scan_input_folder()
        
        if not pairs:
            print("\n❌ 처리할 파일이 없습니다.")
            print("\n사용 방법:")
            print("1. input/images/ 폴더에 이미지 업로드")
            print("2. input/scripts/ 폴더에 동일한 이름의 JSON 파일 생성")
            print("   예: my_video.jpg + my_video.json")
            return
        
        print(f"✓ {len(pairs)}개의 파일 쌍 발견")
        for pair in pairs:
            print(f"   - {pair['name']}")
        
        # 각 파일 처리
        results = []
        for pair in pairs:
            try:
                result = self.process_file_pair(pair)
                results.append(result)
            except Exception as e:
                print(f"\n❌ 오류 발생: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # 최종 요약
        print("\n" + "="*60)
        print("📊 처리 완료 요약")
        print("="*60)
        for result in results:
            print(f"\n✅ {result['name']}")
            print(f"   비디오: {result['video']}")
            print(f"   썸네일: {result['thumbnail']}")
            if result['youtube_url']:
                print(f"   YouTube: {result['youtube_url']}")
        
        print("\n" + "="*60)
        print("🎉 모든 처리 완료!")
        print("="*60)

if __name__ == '__main__':
    automation = YouTubeAutomation()
    automation.run()
