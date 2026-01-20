#!/usr/bin/env python3
"""
웹 기반 키워드 선택 인터페이스
Flask 서버로 클릭 가능한 UI 제공
"""

import os
import json
import webbrowser
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from keyword_selector import KeywordSelector

app = Flask(__name__)
selector = KeywordSelector()

# 현재 분석 결과를 저장할 전역 변수
current_analysis = None
current_topic = None

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """주제 분석 API"""
    global current_analysis, current_topic
    
    data = request.json
    topic = data.get('topic', '')
    
    if not topic:
        return jsonify({'error': '주제를 입력하세요'}), 400
    
    current_topic = topic
    
    # AI 분석 수행
    print(f"🔍 '{topic}' 분석 중...")
    current_analysis = selector.analyze_topic(topic)
    
    return jsonify(current_analysis)

@app.route('/generate', methods=['POST'])
def generate_script():
    """선택된 키워드로 스크립트 생성 API"""
    global current_analysis, current_topic
    
    if not current_analysis:
        return jsonify({'error': '먼저 주제를 분석하세요'}), 400
    
    data = request.json
    selected_keyword_indices = data.get('keywords', [])
    selected_title_index = data.get('title', 0)
    
    # 키워드 추출
    all_keywords = []
    for kw in current_analysis['high_revenue_keywords']:
        all_keywords.append(kw['keyword'])
    all_keywords.extend(current_analysis['longtail_keywords'])
    
    selected_keywords = [all_keywords[i] for i in selected_keyword_indices if i < len(all_keywords)]
    
    # 제목 추출
    titles = current_analysis['recommended_titles']
    if selected_title_index < len(titles):
        selected_title = titles[selected_title_index]['title']
    else:
        selected_title = titles[0]['title']
    
    # 선택 결과
    selection_result = {
        'selected_keywords': selected_keywords,
        'selected_title': selected_title,
        'main_keyword': current_analysis['main_keyword'],
        'content_strategy': current_analysis['content_strategy'],
        'auto_generate': True
    }
    
    # 스크립트 생성
    print("\n🎬 YouTube 숏폼 스크립트 생성 중...")
    script_data = selector.generate_script_from_selection(selection_result)
    
    # 저장
    script_path = selector.save_script(script_data)
    
    return jsonify({
        'success': True,
        'script_path': script_path,
        'script_data': script_data
    })

def run_web_ui(port=5000, debug=False):
    """웹 UI 실행"""
    print("\n" + "="*80)
    print("🌐 웹 기반 키워드 선택 시스템")
    print("="*80)
    print(f"\n브라우저에서 http://localhost:{port} 을 열어주세요")
    print("자동으로 브라우저가 열립니다...\n")
    
    # 브라우저 자동 열기
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    run_web_ui()
