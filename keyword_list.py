# 초기 키워드 리스트 (MVP용)

KEYWORDS = [
    # AI / Data
    "ChatGPT 교육",
    "프롬프트 엔지니어링",
    "생성형 AI",
    "데이터 분석 기초",
    "머신러닝 입문",
    "파이썬 크롤링",
    "SQL 자격증",
    "AI 윤리",
    
    # Development
    "웹 풀스택 개발",
    "리액트 강의",
    "Next.js 튜토리얼",
    "스프링 부트",
    "DevOps 입문",
    "클린 코드",
    
    # No-Code / Productivity
    "노션 활용법",
    "재피어 자동화",
    "피그마 강의",
    "노코드 툴",
    "업무 자동화",
    
    # Marketing / Business
    "디지털 마케팅",
    "SEO 최적화",
    "콘텐츠 마케팅",
    "그로스 해킹",
    "GA4 자격증",
    
    # Soft Skills / Others
    "리더십 교육",
    "디자인 씽킹",
    "문제 해결 능력",
    "직무 멘토링"
]

def get_category(keyword):
    """
    단순 키워드 기반 카테고리 분류
    """
    k = keyword.lower()
    if any(x in k for x in ['ai', 'gpt', '러닝', '분석', 'sql', '파이썬']):
        return 'AI/데이터'
    if any(x in k for x in ['개발', '리액트', 'next', '스프링', '코드', 'devops']):
        return '개발'
    if any(x in k for x in ['노션', '재피어', '피그마', '자동화', '노코드']):
        return '노코드/생산성'
    if any(x in k for x in ['마케팅', 'seo', 'ga4', '그로스']):
        return '마케팅'
    return '기타'
