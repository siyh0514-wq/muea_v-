#!/usr/bin/env python3
"""
완전 자동 숏폼 비디오 생성기
이미지만 넣고 언어만 선택하면 고화질 영상 자동 생성!

사용법:
  python auto_video_creator.py --lang ko
  python auto_video_creator.py --lang zh
  python auto_video_creator.py --lang en
  python auto_video_creator.py --lang ja
  python auto_video_creator.py --lang th
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 다국어 키워드 선택기 import
from multilingual_selector import MultilingualKeywordSelector

class AutoVideoCreator:
    """완전 자동 비디오 생성기"""
    
    def __init__(self, language='ko', quality='high', ai_provider='gemini'):
        self.language = language
        self.quality = quality
        self.ai_provider = ai_provider.lower()
        self.selector = MultilingualKeywordSelector(language, ai_provider=self.ai_provider)
        self.load_configs()
        
    def load_configs(self):
        """설정 로드"""
        with open('config/did_integration.json', 'r', encoding='utf-8') as f:
            self.did_config = json.load(f)
        with open('config/languages.json', 'r', encoding='utf-8') as f:
            self.lang_config = json.load(f)
            
        self.current_lang = self.lang_config['supported_languages'][self.language]
        
    def auto_generate_from_image(self, image_path):
        """
        이미지에서 자동으로 비디오 생성
        
        Args:
            image_path: 이미지 파일 경로
        
        Returns:
            dict: 생성된 비디오 정보
        """
        print("\n" + "="*80)
        print(f"🎬 자동 숏폼 비디오 생성 시작 ({self.current_lang['name']})")
        print("="*80)
        
        # 1. 이미지 분석 (Gemini Vision)
        print("\n📸 1단계: 이미지 분석 중...")
        image_analysis = self.analyze_image_with_gemini(image_path)
        
        # 2. 키워드 자동 추출
        print("\n🔍 2단계: 고수익 키워드 자동 추출 중...")
        topic = image_analysis.get('detected_subject', '제품 리뷰')
        keyword_analysis = self.selector.analyze_topic(topic)
        
        # 3. 최적 키워드 자동 선택 (상위 3개)
        print("\n✨ 3단계: 최적 키워드 자동 선택...")
        all_keywords = []
        for kw in keyword_analysis['keywords'][:3]:
            all_keywords.append(kw['text'])
        
        # 4. 최적 제목 자동 선택 (CTR 점수 가장 높은 것)
        best_title = max(keyword_analysis['titles'], key=lambda x: x['ctr_score'])
        selected_title = best_title['text']
        
        print(f"   ✓ 선택된 키워드: {', '.join(all_keywords)}")
        print(f"   ✓ 선택된 제목: {selected_title} (CTR: {best_title['ctr_score']})")
        
        # 5. 스크립트 자동 생성 (여러 버전)
        print("\n📝 4단계: 다양한 버전 스크립트 생성 중...")
        versions = self.selector.generate_versions(
            topic, all_keywords, selected_title, num_versions=3
        )
        
        # 6. 고화질 비디오 생성
        print(f"\n🎥 5단계: {self.quality.upper()} 화질 비디오 생성 중...")
        videos = []
        for version in versions:
            video_path = self.create_high_quality_video(
                image_path, version, image_analysis
            )
            videos.append({
                'version_id': version['version_id'],
                'video_path': video_path,
                'title': version['title'],
                'script': version['script']
            })
            print(f"   ✓ {version['version_id']} 생성 완료: {video_path}")
        
        # 7. 결과 저장
        result = {
            'language': self.language,
            'quality': self.quality,
            'source_image': str(image_path),
            'topic': topic,
            'keywords': all_keywords,
            'title': selected_title,
            'videos': videos,
            'created_at': datetime.now().isoformat()
        }
        
        self.save_result(result)
        
        return result
    
    def analyze_image_with_gemini(self, image_path):
        """AI로 이미지 분석 (Gemini 또는 GPT-4o Vision)"""
        try:
            from PIL import Image
            
            # 언어별 프롬프트
            prompts = {
                'ko': "이 이미지를 분석하고 숏폼 쇼핑 채널용 정보를 JSON으로 제공하세요: detected_subject(제품명), is_product(제품 여부), description(상세 설명), suggested_category(카테고리), key_features(특징 3개)",
                'zh': "分析这张图片并提供短视频购物频道所需的JSON信息: detected_subject(产品名), is_product(是否产品), description(详细说明), suggested_category(类别), key_features(3个特点)",
                'en': "Analyze this image and provide JSON for short-form shopping channel: detected_subject(product name), is_product(boolean), description(details), suggested_category(category), key_features(3 features)",
                'ja': "この画像を分析してショート動画ショッピングチャンネル用JSON情報を提供: detected_subject(商品名), is_product(商品かどうか), description(詳細説明), suggested_category(カテゴリー), key_features(特徴3つ)",
                'th': "วิเคราะห์รูปภาพนี้และให้ข้อมูล JSON สำหรับช่องช้อปปิ้งวิดีโอสั้น: detected_subject(ชื่อสินค้า), is_product(เป็นสินค้าหรือไม่), description(คำอธิบาย), suggested_category(หมวดหมู่), key_features(3 คุณสมบัติ)"
            }
            prompt = prompts.get(self.language, prompts['ko'])
            
            if self.ai_provider == 'openai':
                # OpenAI GPT-4o Vision
                import openai
                import base64
                
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    print("   ⚠️  OpenAI API 키가 없습니다. 기본 분석 사용...")
                    return self._default_analysis(image_path)
                
                openai.api_key = api_key
                
                # 이미지를 base64로 인코딩
                with open(image_path, 'rb') as f:
                    image_base64 = base64.b64encode(f.read()).decode()
                
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )
                
                result_text = response.choices[0].message.content
                
            else:
                # Gemini Vision (기본)
                import google.generativeai as genai
                
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    print("   ⚠️  Gemini API 키가 없습니다. 기본 분석 사용...")
                    return self._default_analysis(image_path)
                
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                img = Image.open(image_path)
                response = model.generate_content([prompt, img])
                result_text = response.text
            
            # JSON 파싱
            import re
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                return json.loads(json_match.group())
            
            return {
                'detected_subject': image_path.stem,
                'is_product': True,
                'description': result_text[:200],
                'suggested_category': 'general'
            }
            
        except Exception as e:
            print(f"   ⚠️  분석 실패: {e}")
            return self._default_analysis(image_path)
    
    def _default_analysis(self, image_path):
        """기본 분석 결과"""
        return {
            'detected_subject': image_path.stem,
            'is_product': False,
            'description': '이미지 설명',
            'suggested_category': 'general'
        }
    
    def create_high_quality_video(self, image_path, version, image_analysis):
        """고화질 비디오 생성"""
        import requests
        import base64
        import time
        
        api_key = os.getenv('DID_API_KEY')
        if not api_key:
            print(f"      ⚠️  D-ID API 키가 없습니다. 시뮬레이션 모드...")
            # 시뮬레이션: 정보만 저장
            output_dir = Path('output/videos')
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{image_path.stem}_{version['version_id']}_HD.mp4"
            
            # 메타데이터만 저장
            with open(output_path.with_suffix('.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'version': version,
                    'quality': self.quality,
                    'resolution': '1920x1080',
                    'status': 'simulated'
                }, f, ensure_ascii=False, indent=2)
            
            print(f"      💡 실제 고화질 비디오를 생성하려면 D-ID API 키가 필요합니다.")
            return str(output_path)
        
        try:
            # D-ID API 호출
            url = "https://api.d-id.com/talks"
            headers = {
                "Authorization": f"Basic {base64.b64encode(api_key.encode()).decode()}",
                "Content-Type": "application/json"
            }
            
            # 이미지를 base64로 인코딩
            with open(image_path, 'rb') as f:
                image_base64 = base64.b64encode(f.read()).decode()
            
            # 화질 설정
            quality_settings = self.did_config['video_generation']['quality_options'][self.quality]
            
            payload = {
                "source_url": f"data:image/jpeg;base64,{image_base64}",
                "script": {
                    "type": "text",
                    "input": version['script'],
                    "provider": {
                        "type": "microsoft",
                        "voice_id": version['voice_id']
                    }
                },
                "config": {
                    "stitch": True,
                    "result_format": "mp4",
                    "fluent": True,
                    "driver_expressions": {
                        "expressions": [{"expression": "happy", "start_frame": 0}]
                    }
                },
                "driver_url": "bank://lively",
                "result_format": "mp4"
            }
            
            print(f"      📤 D-ID API 호출 중 ({quality_settings['description']})...")
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                talk_id = response.json()['id']
                print(f"      ⏳ 비디오 생성 중... (ID: {talk_id})")
                
                # 비디오 생성 완료 대기
                status_url = f"{url}/{talk_id}"
                max_attempts = 60  # 최대 5분
                for i in range(max_attempts):
                    time.sleep(5)
                    status_response = requests.get(status_url, headers=headers)
                    status_data = status_response.json()
                    
                    if status_data['status'] == 'done':
                        video_url = status_data['result_url']
                        
                        # 비디오 다운로드
                        output_dir = Path('output/videos')
                        output_dir.mkdir(parents=True, exist_ok=True)
                        output_path = output_dir / f"{image_path.stem}_{version['version_id']}_HD.mp4"
                        
                        video_response = requests.get(video_url)
                        with open(output_path, 'wb') as f:
                            f.write(video_response.content)
                        
                        print(f"      ✅ 고화질 비디오 생성 완료!")
                        return str(output_path)
                    
                    elif status_data['status'] == 'error':
                        print(f"      ❌ 오류 발생: {status_data.get('error')}")
                        break
                    
                    print(f"      ⏳ 진행 중... ({i+1}/{max_attempts})")
                
                print("      ⚠️  타임아웃")
            else:
                print(f"      ❌ API 오류: {response.status_code}")
                print(f"         {response.text}")
            
        except Exception as e:
            print(f"      ❌ 비디오 생성 실패: {e}")
        
        # 실패시 시뮬레이션 경로 반환
        output_dir = Path('output/videos')
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir / f"{image_path.stem}_{version['version_id']}_HD.mp4")
    
    def save_result(self, result):
        """결과 저장"""
        output_dir = Path('output/results')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"result_{result['language']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 결과 저장: {filepath}")
    
    def process_all_images(self):
        """input/images/ 폴더의 모든 이미지 처리"""
        image_dir = Path('input/images')
        if not image_dir.exists():
            print(f"❌ {image_dir} 폴더가 없습니다.")
            return []
        
        image_files = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png')) + list(image_dir.glob('*.jpeg'))
        
        if not image_files:
            print(f"❌ {image_dir}에 이미지 파일이 없습니다.")
            return []
        
        print(f"\n📂 {len(image_files)}개의 이미지 발견")
        
        results = []
        for i, image_path in enumerate(image_files, 1):
            print(f"\n{'='*80}")
            print(f"처리 중: [{i}/{len(image_files)}] {image_path.name}")
            print(f"{'='*80}")
            
            try:
                result = self.auto_generate_from_image(image_path)
                results.append(result)
                
                # 처리 완료된 이미지 이동
                completed_dir = Path('input/completed')
                completed_dir.mkdir(parents=True, exist_ok=True)
                import shutil
                shutil.move(str(image_path), str(completed_dir / image_path.name))
                print(f"\n✅ 완료! 이미지를 {completed_dir}로 이동")
                
            except Exception as e:
                print(f"\n❌ 오류: {e}")
                continue
        
        return results

def main():
    parser = argparse.ArgumentParser(description='완전 자동 숏폼 비디오 생성기')
    parser.add_argument('--lang', type=str, default='ko', 
                       choices=['ko', 'zh', 'en', 'ja', 'th'],
                       help='언어 선택 (ko=한국어, zh=中文, en=English, ja=日本語, th=ภาษาไทย)')
    parser.add_argument('--quality', type=str, default='high',
                       choices=['high', 'ultra'],
                       help='비디오 화질 (high=1080p, ultra=4K)')
    parser.add_argument('--ai', type=str, default='gemini',
                       choices=['gemini', 'openai', 'gpt'],
                       help='AI Provider (gemini=Gemini AI [저렴], openai/gpt=GPT-4o [고품질])')
    parser.add_argument('--image', type=str, help='특정 이미지 파일 경로 (선택사항)')
    
    args = parser.parse_args()
    
    # gpt -> openai로 변환
    ai_provider = 'openai' if args.ai in ['openai', 'gpt'] else 'gemini'
    
    print("\n" + "="*80)
    print("🎬 완전 자동 숏폼 비디오 생성기")
    print("="*80)
    print(f"언어: {args.lang}")
    print(f"화질: {args.quality.upper()}")
    print(f"AI: {ai_provider.upper()} {'(GPT-4o Vision)' if ai_provider == 'openai' else '(Gemini 1.5)'}")
    print("="*80)
    
    creator = AutoVideoCreator(language=args.lang, quality=args.quality, ai_provider=ai_provider)
    
    if args.image:
        # 특정 이미지만 처리
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"❌ 이미지 파일을 찾을 수 없습니다: {args.image}")
            return
        
        result = creator.auto_generate_from_image(image_path)
        
    else:
        # input/images/ 폴더의 모든 이미지 처리
        results = creator.process_all_images()
        
        if results:
            print("\n" + "="*80)
            print(f"🎉 완료! 총 {len(results)}개의 비디오 생성됨")
            print("="*80)
            for result in results:
                print(f"\n📁 {result['source_image']}")
                print(f"   제목: {result['title']}")
                print(f"   비디오: {len(result['videos'])}개 버전")

if __name__ == "__main__":
    main()
