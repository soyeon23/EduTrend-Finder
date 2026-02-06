import markdown
from weasyprint import HTML, CSS
from pathlib import Path

# 파일 경로 설정
md_file = Path(r"c:\Users\ssy49\Desktop\EduTrend- Finder\EduTrend_Finder_제안서.md")
pdf_file = Path(r"c:\Users\ssy49\Desktop\EduTrend- Finder\EduTrend_Finder_제안서.pdf")

# Markdown 파일 읽기
md_content = md_file.read_text(encoding='utf-8')

# Markdown을 HTML로 변환
html_content = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'nl2br']
)

# CSS 스타일 정의 (A4 3페이지 최적화)
css_style = """
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
}

@font-face {
    font-family: 'Pretendard';
    src: local('Pretendard'), local('Malgun Gothic'), local('맑은 고딕');
}

body {
    font-family: 'Pretendard', 'Malgun Gothic', '맑은 고딕', sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #1a1a1a;
}

h1 {
    font-size: 18pt;
    font-weight: 700;
    color: #1e3a5f;
    text-align: center;
    margin-bottom: 5px;
    padding-bottom: 10px;
    border-bottom: 2px solid #4f46e5;
}

h2 {
    font-size: 14pt;
    font-weight: 600;
    color: #1e3a5f;
    margin-top: 15px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid #e5e7eb;
}

h3 {
    font-size: 11pt;
    font-weight: 600;
    color: #374151;
    margin-top: 12px;
    margin-bottom: 6px;
}

p {
    margin: 6px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9pt;
}

th, td {
    border: 1px solid #d1d5db;
    padding: 6px 8px;
    text-align: left;
}

th {
    background-color: #f3f4f6;
    font-weight: 600;
    color: #1f2937;
}

tr:nth-child(even) {
    background-color: #f9fafb;
}

code, pre {
    font-family: 'D2Coding', 'Consolas', monospace;
    font-size: 8pt;
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 4px;
}

pre {
    padding: 10px;
    overflow-x: auto;
    white-space: pre;
    line-height: 1.3;
}

hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 15px 0;
}

strong {
    font-weight: 600;
    color: #1f2937;
}

blockquote {
    border-left: 3px solid #4f46e5;
    padding-left: 12px;
    margin: 10px 0;
    color: #4b5563;
    font-style: italic;
}

ul, ol {
    margin: 6px 0;
    padding-left: 20px;
}

li {
    margin: 3px 0;
}

/* 페이지 나눔 방지 */
table, pre, blockquote {
    page-break-inside: avoid;
}

h2, h3 {
    page-break-after: avoid;
}
"""

# 완전한 HTML 문서 생성
full_html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>EduTrend Finder 제안서</title>
</head>
<body>
{html_content}
</body>
</html>
"""

# PDF 생성
print("PDF 변환 중...")
HTML(string=full_html).write_pdf(
    pdf_file,
    stylesheets=[CSS(string=css_style)]
)

print(f"PDF 생성 완료: {pdf_file}")
