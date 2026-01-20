// 전역 변수
let analysisResult = null;
let selectedKeywords = new Set();
let selectedTitle = null;

// 주제 분석
async function analyzeTopic() {
    const topicInput = document.getElementById('topic-input');
    const topic = topicInput.value.trim();
    
    if (!topic) {
        alert('주제를 입력하세요');
        return;
    }
    
    // UI 업데이트
    document.getElementById('input-section').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('complete-section').style.display = 'none';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic: topic })
        });
        
        if (!response.ok) {
            throw new Error('분석 실패');
        }
        
        analysisResult = await response.json();
        
        // 결과 표시
        displayResults();
        
    } catch (error) {
        alert('오류가 발생했습니다: ' + error.message);
        document.getElementById('input-section').style.display = 'block';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// 결과 표시
function displayResults() {
    document.getElementById('results-section').style.display = 'block';
    
    // 1. 핵심 키워드
    document.getElementById('main-keyword').textContent = analysisResult.main_keyword;
    document.getElementById('core-needs').textContent = 
        '핵심 니즈: ' + analysisResult.core_needs.join(', ');
    
    // 2. 고수익 키워드
    const keywordsList = document.getElementById('keywords-list');
    keywordsList.innerHTML = '';
    
    let index = 0;
    
    // 고수익 키워드
    analysisResult.high_revenue_keywords.forEach((kw, i) => {
        const card = createKeywordCard(kw.keyword, kw.type, kw.competition, kw.cpc_potential, index);
        keywordsList.appendChild(card);
        index++;
    });
    
    // 롱테일 키워드
    analysisResult.longtail_keywords.forEach((kw, i) => {
        const card = createKeywordCard(kw, '롱테일', 'low', '중간', index);
        keywordsList.appendChild(card);
        index++;
    });
    
    // 3. 추천 제목
    const titlesList = document.getElementById('titles-list');
    titlesList.innerHTML = '';
    
    analysisResult.recommended_titles.forEach((title, i) => {
        const card = createTitleCard(title.title, title.hook, title.ctr_score, i);
        titlesList.appendChild(card);
    });
    
    // 4. 본문 구성 전략
    const strategy = analysisResult.content_strategy;
    document.getElementById('content-strategy').innerHTML = `
        <p><strong>서론:</strong> ${strategy.intro}</p>
        <p><strong>본론:</strong> ${strategy.body}</p>
        <p><strong>결론:</strong> ${strategy.conclusion}</p>
    `;
}

// 키워드 카드 생성
function createKeywordCard(keyword, type, competition, cpc, index) {
    const card = document.createElement('div');
    card.className = 'keyword-card';
    card.dataset.index = index;
    
    card.innerHTML = `
        <h3>${keyword}</h3>
        <div class="keyword-meta">
            <span class="badge badge-type">${type}</span>
            <span class="badge badge-competition">경쟁도: ${competition}</span>
            <span class="badge badge-cpc">CPC: ${cpc}</span>
        </div>
    `;
    
    card.onclick = function() {
        toggleKeywordSelection(this, index);
    };
    
    return card;
}

// 제목 카드 생성
function createTitleCard(title, hook, ctrScore, index) {
    const card = document.createElement('div');
    card.className = 'title-card';
    card.dataset.index = index;
    
    card.innerHTML = `
        <span class="ctr-score">${ctrScore}/100</span>
        <h3>${title}</h3>
        <div class="title-meta">
            <span>🎣 훅킹 요소: ${hook}</span>
        </div>
    `;
    
    card.onclick = function() {
        selectTitle(this, index);
    };
    
    return card;
}

// 키워드 선택 토글
function toggleKeywordSelection(card, index) {
    if (selectedKeywords.has(index)) {
        selectedKeywords.delete(index);
        card.classList.remove('selected');
    } else {
        selectedKeywords.add(index);
        card.classList.add('selected');
    }
    
    updateSelectionSummary();
}

// 제목 선택
function selectTitle(card, index) {
    // 기존 선택 해제
    document.querySelectorAll('.title-card').forEach(c => {
        c.classList.remove('selected');
    });
    
    // 새로운 선택
    card.classList.add('selected');
    selectedTitle = index;
    
    updateSelectionSummary();
}

// 선택 요약 업데이트
function updateSelectionSummary() {
    const summary = document.getElementById('selection-summary');
    
    if (selectedKeywords.size > 0 || selectedTitle !== null) {
        summary.style.display = 'block';
        
        // 선택된 키워드 표시
        const keywordsDisplay = document.getElementById('selected-keywords-display');
        keywordsDisplay.innerHTML = '<h3>선택된 키워드 (' + selectedKeywords.size + '개):</h3>';
        
        const keywordsContainer = document.createElement('div');
        
        // 모든 키워드 리스트 생성
        const allKeywords = [];
        analysisResult.high_revenue_keywords.forEach(kw => {
            allKeywords.push(kw.keyword);
        });
        allKeywords.push(...analysisResult.longtail_keywords);
        
        selectedKeywords.forEach(index => {
            const span = document.createElement('span');
            span.className = 'selected-item';
            span.textContent = '✓ ' + allKeywords[index];
            keywordsContainer.appendChild(span);
        });
        
        keywordsDisplay.appendChild(keywordsContainer);
        
        // 선택된 제목 표시
        if (selectedTitle !== null) {
            const titleDisplay = document.getElementById('selected-title-display');
            titleDisplay.innerHTML = '<h3>선택된 제목:</h3>';
            
            const span = document.createElement('span');
            span.className = 'selected-item';
            span.textContent = '✓ ' + analysisResult.recommended_titles[selectedTitle].title;
            titleDisplay.appendChild(span);
        }
    } else {
        summary.style.display = 'none';
    }
}

// 스크립트 생성
async function generateScript() {
    if (selectedKeywords.size === 0) {
        alert('최소 1개 이상의 키워드를 선택하세요');
        return;
    }
    
    if (selectedTitle === null) {
        alert('제목을 선택하세요');
        return;
    }
    
    // 로딩 표시
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = true;
    generateBtn.textContent = '⏳ 스크립트 생성 중...';
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keywords: Array.from(selectedKeywords),
                title: selectedTitle
            })
        });
        
        if (!response.ok) {
            throw new Error('스크립트 생성 실패');
        }
        
        const result = await response.json();
        
        // 완료 섹션 표시
        displayComplete(result);
        
    } catch (error) {
        alert('오류가 발생했습니다: ' + error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = '🎬 YouTube 숏폼 스크립트 자동 생성';
    }
}

// 완료 화면 표시
function displayComplete(result) {
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('complete-section').style.display = 'block';
    
    const scriptData = result.script_data;
    
    document.getElementById('script-result').innerHTML = `
        <h4>📁 저장 위치</h4>
        <p><strong>${result.script_path}</strong></p>
        
        <h4>📝 생성된 제목</h4>
        <p>${scriptData.title}</p>
        
        <h4>🎬 대본</h4>
        <p>${scriptData.script_text}</p>
        
        <h4>⏱️ 예상 시간</h4>
        <p>${scriptData.duration}초</p>
        
        <h4>#️⃣ 해시태그</h4>
        <p>${scriptData.hashtags.join(' ')}</p>
        
        <h4>📌 다음 단계</h4>
        <p>1. 이미지를 준비하세요 (제품 사진 또는 관련 이미지)</p>
        <p>2. <code>input/images/</code> 폴더에 이미지를 저장하세요</p>
        <p>3. <code>python main.py</code> 실행하여 자동 비디오 생성</p>
    `;
}

// 초기화
function resetForm() {
    document.getElementById('input-section').style.display = 'block';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('complete-section').style.display = 'none';
    document.getElementById('topic-input').value = '';
    
    selectedKeywords.clear();
    selectedTitle = null;
    analysisResult = null;
}

// Enter 키 이벤트
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('topic-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            analyzeTopic();
        }
    });
});
