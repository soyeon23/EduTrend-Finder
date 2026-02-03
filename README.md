# EduTrend Finder 📊

교육 콘텐츠 기획자를 위한 교육 트렌드 탐색 및 의사결정 지원 대시보드입니다.
Google Trends 데이터를 기반으로 최근 교육 키워드의 관심도 변화를 추적합니다.

## 🚀 실행 방법

### 1. 환경 설정 및 설치
Python 3.8 이상이 필요합니다.

```bash
# 가상환경 생성 (권장)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 앱 실행
```bash
streamlit run app.py
```
브라우저가 자동으로 열리며 대시보드를 확인할 수 있습니다.

## 🤝 팀원과 공유하는 법 (내 PC 부팅 시)
본인(호스트)의 PC에서 앱을 실행한 상태로 두어야 타인이 접속할 수 있습니다.

1. **앱 실행 시 터미널(콘솔) 화면 확인**:
   앱이 실행되면 아래와 같은 주소가 나타납니다.
   ```
   Local URL: http://localhost:8501
   Network URL: http://192.168.0.15:8501   <-- (이 주소!)
   ```
2. **네트워크 주소 공유**:
   `Network URL`에 해당하는 주소(예: `http://192.168.x.x:8501`)를 복사해서 팀원에게 전달하세요.
3. **접속 조건**:
   - 팀원과 본인이 **같은 와이파이(공유기)** 내에 있어야 합니다.
   - 본인의 **Windows 방화벽**이 연결을 차단하지 않아야 합니다. (접속 불가 시 '방화벽 설정 > 앱 허용'에서 python 확인)

## ⚠️ 주의사항 (Disclaimer)
- **Google Trends API 제한**: 너무 잦은 새로고침 시 Google Trends의 요청 제한(Rate Limit)이 발생할 수 있습니다. 이 경우 앱은 자동으로 **데모 모드(Mock Data)**로 전환되어 동작합니다.
- **데이터 해석**: 제공되는 데이터는 '상대적 검색 관심도(0~100)'입니다. 절대적인 검색량이 아니며, 실제 매출이나 수강생 수와 직결되지 않습니다. 기획 아이디어 발굴을 위한 선행 지표로만 활용하세요.

## 📂 주요 기능
1. **메인 대시보드**: 급상승 TOP 키워드, 카테고리별 필터링
2. **상세 분석**: 특정 키워드의 3/6/12개월 추이 그래프 및 인사이트
3. **키워드 비교**: 여러 키워드 간의 관심도 상대 비교
4. **리포트**: 분석 데이터 CSV 다운로드

## 🛠 기술 스택
- **Language**: Python
- **Web Framework**: Streamlit
- **Visualization**: Plotly Express
- **Data Fetching**: PyTrends (Google Trends Unofficial API)
