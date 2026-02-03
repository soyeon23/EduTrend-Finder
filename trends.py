import pandas as pd
from pytrends.request import TrendReq
import time
import random
from keyword_list import get_category
from concurrent.futures import ThreadPoolExecutor, as_completed

def create_pytrends():
    """새로운 PyTrends 인스턴스 생성 (스레드 안전)"""
    try:
        return TrendReq(hl='ko-KR', tz=540, timeout=(10, 25), retries=2, backoff_factor=0.1)
    except Exception:
        return None

# 기본 PyTrends 인스턴스 (연관 검색어 등 단일 스레드 작업용)
pytrends = create_pytrends()

def fetch_trend_data(keywords, timeframe='today 3-m', pytrends_instance=None):
    """
    Google Trends 데이터를 가져옵니다.
    MVP에서는 5개씩 나누어 요청를 보냅니다 (Rate Limit 방지).
    실패 시 Mock Data를 반환할 수도 있도록 처리합니다.
    """
    # 스레드 안전을 위해 인스턴스 사용 또는 새로 생성
    pt = pytrends_instance if pytrends_instance else pytrends
    if pt is None:
        pt = create_pytrends()
    if pt is None:
        return pd.DataFrame()

    all_data = pd.DataFrame()

    # 최대 5개씩 청크 분할
    chunk_size = 5
    keyword_chunks = [keywords[i:i + chunk_size] for i in range(0, len(keywords), chunk_size)]

    for chunk in keyword_chunks:
        try:
            # 최소 딜레이 (Rate Limit 방지)
            time.sleep(random.uniform(0.3, 0.6))
            pt.build_payload(chunk, cat=0, timeframe=timeframe, geo='KR')
            data = pt.interest_over_time()
            
            if not data.empty:
                # isPartial 컬럼 제거
                if 'isPartial' in data.columns:
                    data = data.drop(columns=['isPartial'])

                # 중복 컬럼 제거
                data = data.loc[:, ~data.columns.duplicated()]

                # 데이터 병합
                if all_data.empty:
                    all_data = data
                else:
                    # 기존 컬럼과 중복되지 않는 것만 추가
                    new_cols = [c for c in data.columns if c not in all_data.columns]
                    if new_cols:
                        all_data = pd.concat([all_data, data[new_cols]], axis=1)
        except Exception as e:
            print(f"Error fetching chunk {chunk}: {e}")
            # 에러 발생 시 해당 청크는 건너뛰거나 0으로 채움
            pass
            
    return all_data

def fetch_related_queries(keyword, timeframe='today 3-m'):
    """
    특정 키워드의 연관 검색어(Related Queries)를 가져옵니다.
    """
    try:
        # 최소 딜레이
        time.sleep(random.uniform(0.2, 0.4))
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='KR')
        related = pytrends.related_queries()
        
        if related and keyword in related:
            # top / rising 중 rising(급상승) 우선, 없으면 top
            rising_df = related[keyword]['rising']
            top_df = related[keyword]['top']
            
            queries = []
            if rising_df is not None and not rising_df.empty:
                queries.extend(rising_df['query'].head(5).tolist())
            
            if top_df is not None and not top_df.empty:
                queries.extend(top_df['query'].head(5).tolist())
                
            # 중복 제거 및 최대 10개
            return list(dict.fromkeys(queries))[:10]
            
    except Exception as e:
        print(f"Error fetching related queries for {keyword}: {e}")
        pass
        
    return get_mock_related_queries(keyword)

def get_mock_related_queries(keyword):
    """
    데모용 연관 검색어 반환
    """
    suffixes = ["강의", "입문", "자격증", "책", "무료", "사용법", "튜토리얼", "전망", "취업"]
    return [f"{keyword} {s}" for s in suffixes]

def calculate_growth_metrics(df):
    """
    데이터프레임을 받아 성장률, 상태, 그리고 '추세 진단(Diagnosis)'을 계산합니다.
    """
    results = []
    
    if df.empty:
        return pd.DataFrame()

    n_rows = len(df)
    if n_rows < 10:
        early_period = df
        recent_period = df
    else:
        split_idx = int(n_rows * 0.3)
        early_period = df.iloc[:split_idx]
        recent_period = df.iloc[-split_idx:]
    
    # 4주(약 28일) 기준 윈도우 비교를 위한 인덱스 계산 (데이터가 일별이라고 가정)
    last_4w_idx = max(0, n_rows - 28)
    prev_4w_idx = max(0, n_rows - 56)
        
    for keyword in df.columns:
        # 1. 기본 통계
        series = df[keyword]
        # 중복 컬럼으로 인해 DataFrame이 반환되는 경우 처리
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]

        early_series = early_period[keyword]
        recent_series = recent_period[keyword]
        if isinstance(early_series, pd.DataFrame):
            early_series = early_series.iloc[:, 0]
        if isinstance(recent_series, pd.DataFrame):
            recent_series = recent_series.iloc[:, 0]

        early_mean = float(early_series.mean())
        recent_mean = float(recent_series.mean())
        total_mean = float(series.mean())
        std_dev = float(series.std())
        max_val = float(series.max())

        # NaN 처리
        if pd.isna(early_mean):
            early_mean = 0.0
        if pd.isna(recent_mean):
            recent_mean = 0.0
        if pd.isna(total_mean):
            total_mean = 0.0
        if pd.isna(std_dev):
            std_dev = 0.0

        # 2. 성장률 계산 (기존 로직 유지 + 보완)
        if early_mean < 1.0:
            if recent_mean > 5.0:
                growth_rate = 999.0 # Low base effect
            else:
                growth_rate = 0.0
        else:
            growth_rate = ((recent_mean - early_mean) / early_mean) * 100
            
        # 3. 상세 진단 지표 계산
        
        # A) 데이터 부족 여부 (0이 30% 이상이면 부족으로 간주)
        zero_ratio = (series == 0).sum() / n_rows
        is_insufficient = zero_ratio > 0.3
        
        # B) 변동성 (변동계수 CV = std / mean)
        cv = std_dev / total_mean if total_mean > 0 else 0
        volatility_label = "높음" if cv > 0.5 else ("보통" if cv > 0.2 else "낮음")
        
        # C) 스파이크 여부 (최대값이 평균+2std 보다 크거나, 최근 평균의 2.5배 이상)
        is_spike = (max_val > total_mean + 2 * std_dev) or (max_val > 2.5 * recent_mean)
        
        # D) 최근 추세 (최근 4주 vs 직전 4주)
        recent_4w_mean = series.iloc[last_4w_idx:].mean()
        prev_4w_mean = series.iloc[prev_4w_idx:last_4w_idx].mean() if prev_4w_idx < last_4w_idx else early_mean
        
        is_rising_short_term = recent_4w_mean > prev_4w_mean * 1.1 # 10% 이상 상승
        
        # 4. 최종 진단 라벨링 (Heuristics)
        diagnosis_type = "관찰 필요"
        diagnosis_reason = "특이 사항 없음"
        caution_label = "-"
        
        if is_insufficient:
            diagnosis_type = "⛔ 데이터 부족"
            diagnosis_reason = "검색 데이터의 30% 이상이 0으로 집계됨"
            caution_label = "데이터 부족"
        elif early_mean < 5 and growth_rate > 100:
            diagnosis_type = "⚠️ 저관심도 급등"
            diagnosis_reason = "초기 관심도가 낮아 성장률이 과장될 수 있음 (Base Effect)"
            caution_label = "저관심도 기반"
        elif is_spike and volatility_label == "높음":
            diagnosis_type = "⚠️ 일시 급등 (이슈성)"
            diagnosis_reason = "평균 대비 과도한 스파이크 발생, 변동성 큼"
            caution_label = "일시 급등 가능"
        elif growth_rate > 10 and is_rising_short_term and volatility_label != "높음":
            diagnosis_type = "✅ 지속 상승"
            diagnosis_reason = "최근 구간 평균 상승세가 뚜렷하며 변동성 안정적"
            caution_label = "지속 상승 유력"
        elif growth_rate < -5:
            diagnosis_type = "📉 하락세"
            diagnosis_reason = "최근 관심도가 초기 대비 감소함"
            caution_label = "하락 반전"
        elif growth_rate > 0:
            diagnosis_type = "📈 완만한 상승"
            diagnosis_reason = "급격하지 않으나 상승 흐름 유지 중"
            caution_label = "상승 흐름"
        else:
            diagnosis_type = "➖ 정체/안정"
            diagnosis_reason = "큰 변동 없이 관심도 유지 중"
            caution_label = "안정"

        # 5. Planning Insight & Action Recommendation (PM Logic)
        insight_target = "입문/기초 타겟 적합" if "기초" in keyword or "입문" in keyword else "실무/중급 타겟 고려"
        if "자격증" in keyword: insight_target = "취업/자격증 취득 목표 타겟"
        
        insight_position = "트렌드 리포트형 콘텐츠" if volatility_label == "높음" else "커리큘럼형/로드맵 콘텐츠"
        
        # Action Logic
        action_label = "이번 분기 기획 제외" # Default
        if diagnosis_type == "✅ 지속 상승":
            action_label = "🚀 신규 기획 검토"
            insight_risk = "수요 검증됨. 차별화된 심화 주제 발굴 필요."
        elif diagnosis_type == "➖ 정체/안정":
            if recent_mean > 40:
                action_label = "🔄 기존 과정 리뉴얼"
                insight_risk = "수요 안정적. 최신 트렌드 반영한 리뉴얼 권장."
            else:
                action_label = "➖ 현상 유지/보류"
                insight_risk = "큰 변동 없음. 리소스 투입 대비 성과 낮을 수 있음."
        elif "급등" in diagnosis_type or volatility_label == "높음":
            action_label = "🧪 단기 테스트 콘텐츠"
            insight_risk = "일시적 유행 가능성. 웨비나/특강으로 가볍게 수요 검증."
        elif diagnosis_type == "📉 하락세":
            action_label = "⛔ 이번 분기 기획 제외"
            insight_risk = "관심도 하락 중. 신규 진입 시 리스크 큼."
        elif is_insufficient:
             action_label = "⛔ 데이터 부족"
             insight_risk = "판단 근거 부족."

        results.append({
            '키워드': keyword,
            '성장률(%)': round(growth_rate, 1),
            '최근 관심도': round(recent_mean, 1),
            '상태': diagnosis_type.split(" ")[-1] if " " in diagnosis_type else diagnosis_type, 
            '진단유형': diagnosis_type,
            '진단근거': diagnosis_reason,
            '주의라벨': caution_label,
            '변동성': volatility_label,
            '추천액션': action_label, # New Column
            '기획_타겟': insight_target,
            '기획_포지션': insight_position,
            '기획_리스크': insight_risk,
            '카테고리': get_category(keyword)
        })
        
    return pd.DataFrame(results)

def get_mock_data(keywords, timeframe='today 3-m'):
    """
    PyTrends 연결 실패 시 사용할 데모용 Mock Data 생성
    """
    dates = pd.date_range(end=pd.Timestamp.now(), periods=90) # approx 3 months
    df = pd.DataFrame(index=dates)

    for kw in keywords:
        # 랜덤 추세 생성
        base = random.randint(10, 50)
        trend = random.choice([-0.1, 0, 0.2, 0.5]) # 하락, 정체, 상승, 급상승
        noise = [random.randint(-5, 5) for _ in range(90)]
        values = [max(0, min(100, base + (i * trend) + n)) for i, n in enumerate(noise)]
        df[kw] = values

    return df


# =============================================================================
# 다중 신호 데이터 수집 (YouTube Search 추가)
# =============================================================================

def fetch_youtube_trend_data(keywords, timeframe='today 3-m', pytrends_instance=None):
    """
    YouTube Search 트렌드 데이터를 가져옵니다.
    gprop='youtube'로 YouTube 검색 트렌드 수집.
    """
    # 스레드 안전을 위해 인스턴스 사용 또는 새로 생성
    pt = pytrends_instance if pytrends_instance else pytrends
    if pt is None:
        pt = create_pytrends()
    if pt is None:
        return pd.DataFrame()

    all_data = pd.DataFrame()
    chunk_size = 5
    keyword_chunks = [keywords[i:i + chunk_size] for i in range(0, len(keywords), chunk_size)]

    for chunk in keyword_chunks:
        try:
            # 최소 딜레이 (Rate Limit 방지)
            time.sleep(random.uniform(0.3, 0.6))
            pt.build_payload(chunk, cat=0, timeframe=timeframe, geo='KR', gprop='youtube')
            data = pt.interest_over_time()

            if not data.empty:
                if 'isPartial' in data.columns:
                    data = data.drop(columns=['isPartial'])

                # 중복 컬럼 제거
                data = data.loc[:, ~data.columns.duplicated()]

                if all_data.empty:
                    all_data = data
                else:
                    # 기존 컬럼과 중복되지 않는 것만 추가
                    new_cols = [c for c in data.columns if c not in all_data.columns]
                    if new_cols:
                        all_data = pd.concat([all_data, data[new_cols]], axis=1)
        except Exception as e:
            print(f"Error fetching YouTube chunk {chunk}: {e}")
            pass

    return all_data


def fetch_multi_signal_data(keywords, timeframe='today 3-m'):
    """
    웹 검색과 YouTube 검색 트렌드를 병렬로 가져옵니다.
    각 스레드에서 별도의 PyTrends 인스턴스를 사용하여 경합 방지.
    Returns: dict with 'web' and 'youtube' DataFrames
    """
    results = {'web': pd.DataFrame(), 'youtube': pd.DataFrame()}

    def fetch_web():
        # 각 스레드에서 독립적인 인스턴스 생성
        pt = create_pytrends()
        return fetch_trend_data(keywords, timeframe, pytrends_instance=pt)

    def fetch_youtube():
        # 각 스레드에서 독립적인 인스턴스 생성
        pt = create_pytrends()
        return fetch_youtube_trend_data(keywords, timeframe, pytrends_instance=pt)

    # 병렬 실행
    with ThreadPoolExecutor(max_workers=2) as executor:
        web_future = executor.submit(fetch_web)
        youtube_future = executor.submit(fetch_youtube)

        results['web'] = web_future.result()
        results['youtube'] = youtube_future.result()

    return results


def get_mock_youtube_data(keywords):
    """
    YouTube 트렌드 데모용 Mock Data 생성.
    웹 검색과 다른 패턴을 시뮬레이션합니다.
    """
    dates = pd.date_range(end=pd.Timestamp.now(), periods=90)
    df = pd.DataFrame(index=dates)

    for kw in keywords:
        # YouTube는 웹과 다른 패턴 (영상 콘텐츠 특성 반영)
        base = random.randint(5, 40)
        # YouTube는 급등/급락이 더 빈번한 경향
        trend = random.choice([-0.2, 0, 0.3, 0.8])
        noise = [random.randint(-8, 8) for _ in range(90)]
        values = [max(0, min(100, base + (i * trend) + n)) for i, n in enumerate(noise)]
        df[kw] = values

    return df


def analyze_cross_signals(web_metrics, youtube_df, keywords):
    """
    웹 검색과 YouTube 검색 신호를 교차 분석하여
    '학습 의도 신호 강도'를 판단합니다.

    목적: 정확한 예측이 아닌, 판단 보완을 위한 신호 교차 확인

    Returns: DataFrame with cross-signal analysis
    """
    results = []

    if youtube_df.empty:
        youtube_df = get_mock_youtube_data(keywords)

    # YouTube 성장률 계산
    n_rows = len(youtube_df) if not youtube_df.empty else 0

    for kw in keywords:
        web_row = web_metrics[web_metrics['키워드'] == kw]
        if web_row.empty:
            continue

        web_growth = web_row.iloc[0]['성장률(%)']
        web_recent = web_row.iloc[0]['최근 관심도']
        web_volatility = web_row.iloc[0]['변동성']

        # YouTube 지표 계산
        if kw in youtube_df.columns and n_rows >= 10:
            yt_series = youtube_df[kw]
            # 중복 컬럼으로 인해 DataFrame이 반환되는 경우 처리
            if isinstance(yt_series, pd.DataFrame):
                yt_series = yt_series.iloc[:, 0]

            split_idx = int(n_rows * 0.3)
            yt_early = float(yt_series.iloc[:split_idx].mean())
            yt_recent = float(yt_series.iloc[-split_idx:].mean())

            # NaN 체크
            if pd.isna(yt_early) or yt_early < 1.0:
                yt_growth = 999.0 if (not pd.isna(yt_recent) and yt_recent > 5.0) else 0.0
            else:
                yt_growth = ((yt_recent - yt_early) / yt_early) * 100
        else:
            # Mock 또는 데이터 없음
            yt_growth = web_growth * random.uniform(0.5, 1.5)
            yt_recent = web_recent * random.uniform(0.3, 1.2)

        # === 교차 신호 해석 ===
        signal_pattern = ""
        signal_interpretation = ""
        signal_strength = "보통"  # 낮음, 보통, 높음

        # 패턴 1: 웹 안정 + YouTube 급상승 → 영상 학습 수요 증가 신호
        if abs(web_growth) < 15 and yt_growth > 30:
            signal_pattern = "영상 전환 신호"
            signal_interpretation = "웹 검색은 안정적이나 YouTube 검색 급상승. 영상/강의 형태 수요 증가 가능성."
            signal_strength = "높음"

        # 패턴 2: 웹 + YouTube 모두 상승 → 강한 학습 수요 신호
        elif web_growth > 10 and yt_growth > 10:
            signal_pattern = "복합 상승 신호"
            signal_interpretation = "웹과 YouTube 모두 상승세. 다양한 형태의 학습 탐색이 활발함."
            signal_strength = "높음"

        # 패턴 3: 웹 상승 + YouTube 정체/하락 → 정보 탐색 단계
        elif web_growth > 15 and yt_growth < 5:
            signal_pattern = "정보 탐색 단계"
            signal_interpretation = "웹 검색 증가 중이나 영상 탐색은 미미. 아직 학습 단계 진입 전일 수 있음."
            signal_strength = "보통"

        # 패턴 4: 웹 하락 + YouTube 상승 → 학습 채널 이동
        elif web_growth < -5 and yt_growth > 10:
            signal_pattern = "채널 이동 신호"
            signal_interpretation = "웹 검색 감소, YouTube 검색 증가. 학습 채널이 영상으로 이동 중일 수 있음."
            signal_strength = "보통"

        # 패턴 5: 둘 다 하락 → 관심 감소
        elif web_growth < -5 and yt_growth < -5:
            signal_pattern = "관심 감소 신호"
            signal_interpretation = "웹과 YouTube 모두 하락세. 전반적인 관심 감소 추세."
            signal_strength = "낮음"

        # 패턴 6: 둘 다 정체 → 안정적 수요
        elif abs(web_growth) < 10 and abs(yt_growth) < 10:
            signal_pattern = "안정 유지"
            signal_interpretation = "웹과 YouTube 모두 큰 변동 없음. 기존 관심도 유지 중."
            signal_strength = "보통"

        else:
            signal_pattern = "혼합 신호"
            signal_interpretation = "명확한 패턴 없음. 추가 관찰 필요."
            signal_strength = "낮음"

        results.append({
            '키워드': kw,
            '웹_성장률': round(web_growth, 1),
            'YouTube_성장률': round(yt_growth, 1),
            '웹_관심도': round(web_recent, 1),
            '신호_패턴': signal_pattern,
            '신호_해석': signal_interpretation,
            '신호_강도': signal_strength,
            '웹_변동성': web_volatility
        })

    return pd.DataFrame(results)


# =============================================================================
# 데이터 한계 명시 텍스트 (UX용)
# =============================================================================

DATA_LIMITATIONS = {
    'main_notice': """
        이 데이터는 '정답'이 아닌 '판단을 돕는 신호(Signal)'입니다.
    """,

    'limitations': [
        {
            'title': '상대 지수',
            'desc': 'Google Trends는 실제 검색량이 아닌 상대적 관심도(0-100)입니다. 키워드 간 절대 크기 비교는 제한됩니다.'
        },
        {
            'title': '학습 의도 구분 한계',
            'desc': '검색 증가가 반드시 교육 수요 증가를 의미하지 않습니다. 일반 관심과 학습 의도는 구분되지 않습니다.'
        },
        {
            'title': '지속성 판단',
            'desc': '단기 이슈성 급등과 중·장기 학습 수요를 완벽히 구분하기 어렵습니다.'
        }
    ],

    'cross_signal_purpose': """
        YouTube 검색 데이터는 '정확한 수요 예측'이 아닌,
        서로 다른 플랫폼에서 동일 키워드 관심이 반복되는지 확인하여
        단일 지표의 한계를 보완하기 위한 용도입니다.
    """,

    'positioning': "EduTrend Finder DataSource : Web · YouTube · Google Trends"
}
