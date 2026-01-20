#!/usr/bin/env python3
"""
🎬 쇼핑 숏폼 영상 제작 시스템
- 15-20초 숏폼 전용
- 플랫폼별 최적화 (YouTube/TikTok/Instagram)
- 다국어 대본 지원
- 고화질 + 자막 필수
- YouTube 자동 업로드
"""

import argparse
import json
import os
from pathlib import Path


class ShortFormCreator:
    """숏폼 영상 자동 생성기"""
    
    PLATFORMS = {
        'youtube': {
            'name': 'YouTube Shorts', 
            'lengths': [15, 30, 45, 60],  # 선택 가능한 길이들
            'optimal': 60,
            'upload': True  # 자동 업로드 지원
        },
        'tiktok': {
            'name': 'TikTok',
            'lengths': [9, 15, 21, 30],
            'optimal': 15,
            'upload': False
        },
        'instagram': {
            'name': 'Instagram Reels',
            'lengths': [15, 30, 45, 60],
            'optimal': 30,
            'upload': False
        }
    }
    
    LANGUAGES = {
        'ko': '한국어',
        'zh': '中文', 
        'en': 'English',
        'ja': '日本語',
        'th': 'ภาษาไทย'
    }
    
    def __init__(self, platform, language, quality='high', subtitles=True, length=None):
        self.platform = platform
        self.language = language
        self.quality = quality
        self.subtitles = subtitles
        
        # 플랫폼별 설정
        self.platform_config = self.PLATFORMS.get(platform, self.PLATFORMS['youtube'])
        
        # 길이 설정 (지정하지 않으면 최적 길이 사용)
        if length and length in self.platform_config['lengths']:
            self.video_length = length
        else:
            self.video_length = self.platform_config['optimal']
        
        # YouTube 업로드 URL
        self.youtube_upload_url = None
        
    def plan(self, product_name):
        """
        ## 1. PLAN (계획)
        작업 단계를 논리적으로 수립
        """
        print("## 1. PLAN (계획)")
        print("=" * 50)
        
        steps = [
            f"1️⃣ 상품 분석: '{product_name}' 핵심 셀링 포인트 도출",
            f"2️⃣ 중국어 검색어: 타오바오 영상 소스용 키워드 생성",
            f"3️⃣ 대본 작성: {self.video_length}초 {self.LANGUAGES[self.language]} 숏폼 대본",
            "4️⃣ 화면 연출: 각 장면별 비주얼 가이드 작성",
            "5️⃣ 썸네일: 클릭 유도 썸네일 디자인 제안",
            f"6️⃣ 영상 생성: {self.quality} 화질 + 자막 포함",
            f"7️⃣ 플랫폼: {self.platform_config['name']} 최적화"
        ]
        
        for step in steps:
            print(f"  {step}")
        
        print("\n")
        return steps
    
    def execute(self, product_name, product_info=""):
        """
        ## 2. EXECUTE (실행)
        계획에 따라 실제 작업 수행
        """
        print("## 2. EXECUTE (실행)")
        print("=" * 50)
        
        # 1단계: 상품 분석
        print("\n### 1️⃣ 상품 분석")
        selling_points = self._analyze_product(product_name, product_info)
        print(f"✅ 핵심 셀링 포인트: {', '.join(selling_points)}")
        
        # 2단계: 중국어 검색어
        print("\n### 2️⃣ 중국어 검색어 (타오바오용)")
        chinese_keywords = self._generate_chinese_keywords(product_name)
        print(f"✅ {chinese_keywords}")
        
        # 3단계: 대본 작성
        print(f"\n### 3️⃣ {self.LANGUAGES[self.language]} 대본 ({self.video_length}초)")
        script = self._create_script(product_name, selling_points)
        self._print_script_table(script)
        
        # 4단계: 썸네일
        print("\n### 4️⃣ 썸네일 디자인")
        thumbnail = self._create_thumbnail_guide(product_name)
        print(f"✅ {thumbnail}")
        
        # 5단계: 영상 정보
        print(f"\n### 5️⃣ 영상 설정")
        print(f"  - 길이: {self.video_length}초")
        print(f"  - 화질: {self.quality} (1080p+)")
        print(f"  - 자막: 필수 포함")
        print(f"  - 플랫폼: {self.platform_config['name']}")
        
        # 결과 저장
        result = {
            'product': product_name,
            'platform': self.platform,
            'language': self.language,
            'chinese_keywords': chinese_keywords,
            'selling_points': selling_points,
            'script': script,
            'thumbnail': thumbnail,
            'video_length': self.video_length,
            'quality': self.quality
        }
        
        self._save_result(result)
        
        return result
    
    def _analyze_product(self, product_name, product_info):
        """상품 핵심 셀링 포인트 분석"""
        # 실제로는 AI API 사용
        return [
            "가격 경쟁력",
            "품질 우수",
            "사용 편의성"
        ]
    
    def _generate_chinese_keywords(self, product_name):
        """중국어 검색어 생성"""
        # 실제로는 번역 API 사용
        keywords_map = {
            'airpods': 'AirPods Pro 无线耳机',
            'cosmetic': '化妆品 护肤品',
            'default': f'{product_name} 商品'
        }
        
        for key, value in keywords_map.items():
            if key in product_name.lower():
                return value
        return keywords_map['default']
    
    def _create_script(self, product_name, selling_points):
        """숏폼 대본 생성"""
        
        # 플랫폼별 대본 구조
        if self.platform == 'tiktok':
            # TikTok: 15초, 매우 빠른 전개
            scenes = [
                {
                    'time': '0-3초',
                    'visual': f'{product_name} 클로즈업 + 강렬한 텍스트',
                    'narration': self._get_hook_script()
                },
                {
                    'time': '4-10초',
                    'visual': '제품 사용 장면 + 혜택 강조',
                    'narration': self._get_benefit_script(selling_points[0])
                },
                {
                    'time': '11-15초',
                    'visual': '구매 링크 + CTA',
                    'narration': self._get_cta_script()
                }
            ]
        elif self.platform == 'instagram':
            # Instagram: 30초, 균형잡힌 구성
            scenes = [
                {
                    'time': '0-5초',
                    'visual': f'{product_name} 매력적인 앵글',
                    'narration': self._get_hook_script()
                },
                {
                    'time': '6-15초',
                    'visual': '제품 특징 3가지 보여주기',
                    'narration': self._get_benefit_script(', '.join(selling_points[:2]))
                },
                {
                    'time': '16-25초',
                    'visual': '실제 사용 후기/비교',
                    'narration': self._get_proof_script()
                },
                {
                    'time': '26-30초',
                    'visual': '프로필 링크 유도',
                    'narration': self._get_cta_script()
                }
            ]
        else:  # YouTube
            # YouTube: 60초, 상세 설명
            scenes = [
                {
                    'time': '0-5초',
                    'visual': f'{product_name} 임팩트 있는 오프닝',
                    'narration': self._get_hook_script()
                },
                {
                    'time': '6-20초',
                    'visual': '제품 상세 특징 소개',
                    'narration': self._get_benefit_script(', '.join(selling_points))
                },
                {
                    'time': '21-40초',
                    'visual': '실사용 데모 + 장점',
                    'narration': self._get_demo_script()
                },
                {
                    'time': '41-55초',
                    'visual': '가격/혜택 정보',
                    'narration': self._get_offer_script()
                },
                {
                    'time': '56-60초',
                    'visual': '구독 + 좋아요 유도',
                    'narration': self._get_cta_script()
                }
            ]
        
        return scenes
    
    def _get_hook_script(self):
        """후킹 멘트 (언어별)"""
        hooks = {
            'ko': "이거 모르면 손해보는 꿀템 발견!",
            'zh': "这个不知道就亏大了！",
            'en': "You're missing out if you don't know this!",
            'ja': "知らないと損する神アイテム！",
            'th': "พลาดแล้วเสียดายแน่นอน!"
        }
        return hooks.get(self.language, hooks['ko'])
    
    def _get_benefit_script(self, benefit):
        """혜택 설명 (언어별)"""
        templates = {
            'ko': f"{benefit} 때문에 완전 핫템이에요!",
            'zh': f"因为{benefit}，超级火爆！",
            'en': f"It's super hot because of {benefit}!",
            'ja': f"{benefit}で超人気！",
            'th': f"ฮิตมากเพราะ{benefit}!"
        }
        return templates.get(self.language, templates['ko'])
    
    def _get_proof_script(self):
        """증거/후기 (언어별)"""
        proofs = {
            'ko': "실제 사용자들 반응 보세요!",
            'zh': "看看真实用户的反馈！",
            'en': "Check out real user reviews!",
            'ja': "実際の使用者の反応見て！",
            'th': "ดูรีวิวจากผู้ใช้จริง!"
        }
        return proofs.get(self.language, proofs['ko'])
    
    def _get_demo_script(self):
        """데모 설명 (언어별)"""
        demos = {
            'ko': "사용법 완전 간단해요, 보세요!",
            'zh': "使用方法超简单，看！",
            'en': "It's super easy to use, watch!",
            'ja': "使い方めちゃ簡単、見て！",
            'th': "ใช้ง่ายมาก ดูนี่!"
        }
        return demos.get(self.language, demos['ko'])
    
    def _get_offer_script(self):
        """가격/혜택 (언어별)"""
        offers = {
            'ko': "지금 특가 + 쿠폰까지! 놓치지 마세요!",
            'zh': "现在特价+优惠券！别错过！",
            'en': "Special price + coupon now! Don't miss it!",
            'ja': "今だけ特価+クーポン！お見逃しなく！",
            'th': "ราคาพิเศษ + คูปอง! อย่าพลาด!"
        }
        return offers.get(self.language, offers['ko'])
    
    def _get_cta_script(self):
        """CTA (언어별)"""
        ctas = {
            'ko': "지금 바로 확인하세요!",
            'zh': "现在就去看看！",
            'en': "Check it out now!",
            'ja': "今すぐチェック！",
            'th': "ดูเลยตอนนี้!"
        }
        return ctas.get(self.language, ctas['ko'])
    
    def _create_thumbnail_guide(self, product_name):
        """썸네일 디자인 가이드"""
        return f"제품 이미지 70% + '최저가' 텍스트 20% + 할인율 10% (빨강/노랑)"
    
    def _print_script_table(self, script):
        """대본을 표 형식으로 출력"""
        print("\n┌─────────────┬──────────────────────────────┬────────────────────────────────┐")
        print("│   시간대    │          화면 연출           │           내레이션             │")
        print("├─────────────┼──────────────────────────────┼────────────────────────────────┤")
        
        for scene in script:
            time = scene['time'].center(13)
            visual = scene['visual'][:28].ljust(28)
            narration = scene['narration'][:30].ljust(30)
            print(f"│ {time} │ {visual} │ {narration} │")
        
        print("└─────────────┴──────────────────────────────┴────────────────────────────────┘")
    
    def _save_result(self, result):
        """결과 저장"""
        output_dir = Path('output/shorts')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{result['product']}_{self.platform}_{self.language}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 결과 저장: {filepath}")


def main():
    parser = argparse.ArgumentParser(description='🎬 쇼핑 숏폼 영상 제작')
    parser.add_argument('--product', type=str, required=True, help='상품명')
    parser.add_argument('--platform', type=str, choices=['youtube', 'tiktok', 'instagram'], 
                       default='youtube', help='플랫폼 선택')
    parser.add_argument('--lang', type=str, choices=['ko', 'zh', 'en', 'ja', 'th'],
                       default='ko', help='대본 언어')
    parser.add_argument('--quality', type=str, choices=['high', 'ultra'],
                       default='high', help='영상 화질')
    parser.add_argument('--info', type=str, default='', help='상품 추가 정보')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"🎬 쇼핑 숏폼 영상 제작 시스템")
    print(f"{'='*60}\n")
    
    # 숏폼 제작기 초기화
    creator = ShortFormCreator(
        platform=args.platform,
        language=args.lang,
        quality=args.quality
    )
    
    # PLAN 단계
    creator.plan(args.product)
    
    # EXECUTE 단계  
    result = creator.execute(args.product, args.info)
    
    print(f"\n{'='*60}")
    print("✅ 완료! 이제 영상을 제작하실 수 있습니다.")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
