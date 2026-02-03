import streamlit as st

st.set_page_config(
    page_title="EduTrend Finder",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from trends import (
    fetch_trend_data, calculate_growth_metrics, get_mock_data, fetch_related_queries,
    fetch_youtube_trend_data, get_mock_youtube_data, analyze_cross_signals, DATA_LIMITATIONS,
    fetch_multi_signal_data
)
from keyword_list import KEYWORDS
import random

# Clean, Minimal SaaS Style CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1a1a1a;
    }

    .block-container {
        padding-top: 3rem !important;
    }

    /* ===== HEADER ===== */
    .app-header {
        background: #ffffff;
        padding: 1rem 0;
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    /* ===== HERO ===== */
    .hero-container {
        padding: 6rem 1rem;
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
        border-radius: 30px; 
        margin-bottom: 4rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        color: white;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('https://www.transparenttextures.com/patterns/cubes.png');
        opacity: 0.05;
        pointer-events: none;
    }
    .hero-title {
        font-size: clamp(2.5rem, 8vw, 4.5rem);
        font-weight: 900;
        color: #ffffff;
        margin: 0 auto 1.5rem auto;
        letter-spacing: -0.05em;
        line-height: 1.1;
        text-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
    }
    .hero-subtitle-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 2rem auto;
    }
    .hero-subtitle {
        display: inline-flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(4px);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
    }
    .hero-subtitle-text {
        font-size: 1rem;
        color: #e0e7ff;
        font-weight: 500;
        text-align: center;
    }
    .hero-data-source {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: rgba(255, 255, 255, 0.25);
        padding: 0.4rem 0.9rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.95rem;
        color: white;
    }

    /* Home Navigation Cards */
    .home-nav-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 0.5rem;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .home-nav-card:hover {
        border-color: #6366f1;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
        transform: translateY(-4px);
    }
    .home-nav-card .stButton {
        margin-top: 0.5rem;
    }
    .home-nav-card button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 1.5rem !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .home-nav-card button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    .home-card-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    .home-card-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .home-card-desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    .use-cases {
        display: flex;
        gap: 2rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 3rem;
    }
    .use-case-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.25rem;
        padding: 2.5rem 2rem;
        background: rgba(255, 255, 255, 0.98);
        border: none;
        border-radius: 20px;
        width: 320px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .use-case-item:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
    }
    .use-case-icon {
        width: 56px;
        height: 56px;
        background: #fdf2f8;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .use-case-text {
        font-size: 1.15rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1.5;
        text-align: center;
    }

    /* ===== SECTION HEADERS ===== */
    .section-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #a3a3a3;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 2rem 0 1rem 0;
    }
    .section-heading {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a1a;
        margin: 0 0 0.25rem 0;
    }
    .section-desc {
        font-size: 0.9rem;
        color: #737373;
        margin: 0 0 1.25rem 0;
    }

    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 1.25rem;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #737373;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    .metric-value-highlight {
        color: #6366f1;
    }

    /* ===== KEYWORD STYLES ===== */
    .keyword-growth {
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 4px;
        margin-right: 1rem;
    }
    .growth-up {
        background: #dcfce7;
        color: #166534;
    }
    .growth-down {
        background: #fee2e2;
        color: #991b1b;
    }
    .growth-flat {
        background: #f5f5f5;
        color: #525252;
    }
    .keyword-action {
        font-size: 0.8rem;
        color: #737373;
        padding: 0.2rem 0.5rem;
        background: #f5f5f5;
        border-radius: 4px;
    }

    /* ===== TAG CHIPS ===== */
    .tag-chip {
        display: inline-block;
        background: #f5f5f5;
        color: #525252;
        padding: 0.35rem 0.7rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
        border: 1px solid #e5e5e5;
        background: white;
        color: #1a1a1a;
        transition: all 0.15s;
    }
    .stButton > button:hover {
        border-color: #d4d4d4;
        background: #fafafa;
    }

    /* ===== NOTICE BOX ===== */
    .notice-box {
        background: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 6px;
        padding: 1rem 1.25rem;
        margin: 1.5rem 0;
        font-size: 0.85rem;
        color: #525252;
    }
    .notice-box strong {
        color: #1a1a1a;
    }

    /* ===== COMING SOON ===== */
    .coming-soon-card {
        background: #fafafa;
        border: 1px dashed #d4d4d4;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
    }
    .coming-soon-badge {
        display: inline-block;
        background: #e5e5e5;
        color: #737373;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .coming-soon-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #525252;
        margin-bottom: 0.25rem;
    }
    .coming-soon-desc {
        font-size: 0.85rem;
        color: #a3a3a3;
    }

    /* ===== NAV CARDS (Robust Streamlit-Native Overlay) ===== */
    .nav-card-wrapper {
        position: relative !important;
        height: 320px !important;
        width: 100% !important;
        margin-bottom: 2rem;
    }

    /* Force the button to be on top and fill everything inside the wrapper */
    .nav-card-wrapper .stButton {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 320px !important;
        z-index: 1000 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Target specific buttons inside wrappers */
    .nav-card-wrapper .stButton button {
        width: 100% !important;
        height: 320px !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
        border-radius: 20px !important;
        cursor: pointer !important;
    }
    
    .nav-card-wrapper .stButton button:hover {
        background: rgba(99, 102, 241, 0.05) !important;
    }

    /* Header Logo Styles */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 14px;
        position: relative;
        z-index: 1;
        pointer-events: none;
    }
    .logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 9px;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    .logo-text {
        color: #000000;
        font-weight: 850;
        font-size: 1.7rem;
        letter-spacing: -0.04em;
        white-space: nowrap;
        line-height: 1;
        margin-top: 1px;
    }
    
    .logo-wrapper {
        position: relative;
        height: 48px;
        display: flex;
        align-items: center;
    }
    
    .logo-wrapper .stButton {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 10 !important;
        margin: 0 !important;
    }
    
    .logo-wrapper .stButton button {
        width: 100% !important;
        height: 100% !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
    }

    .home-sim-card {
        text-align: center;
        background: #ffffff;
        border: 1px solid #f0f0f0;
        border-radius: 20px;
        height: 320px;
        width: 100%;
        padding: 3rem 1.5rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.03);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        pointer-events: none; /* Let clicks pass to the button overlay */
        background-color: white !important;
    }

    /* Visual tilt/hover on the card sparked by the wrapper hover */
    .nav-card-wrapper:hover .home-sim-card {
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.12) !important;
        border-color: #6366f1 !important;
    }

    /* ===== FOOTER ===== */
    .app-footer {
        text-align: center;
        padding: 2rem 0;
        color: #a3a3a3;
        font-size: 0.8rem;
        border-top: 1px solid #f0f0f0;
        margin-top: 3rem;
    }

    /* ===== SIMULATOR CTA ===== */
    .simulator-cta {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 2rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    .simulator-cta-text {
        flex: 1;
    }
    .simulator-cta-title {
        font-size: 1rem;
        font-weight: 600;
        color: #0369a1;
        margin-bottom: 0.25rem;
    }
    .simulator-cta-desc {
        font-size: 0.85rem;
        color: #0c4a6e;
    }

    /* ===== SIMULATOR CARDS ===== */
    .sim-card {
        background: white;
        border: 2px solid #e5e5e5;
        border-radius: 12px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        height: 100%;
    }
    .sim-card:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }
    .sim-card.selected {
        border-color: #6366f1;
        background: #f5f3ff;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    .sim-card-keyword {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.75rem;
    }
    .sim-card-growth {
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sim-card-growth.positive {
        color: #16a34a;
    }
    .sim-card-growth.negative {
        color: #dc2626;
    }
    .sim-card-growth.neutral {
        color: #737373;
    }
    .sim-card-trend {
        font-size: 0.85rem;
        color: #737373;
        padding: 0.3rem 0.6rem;
        background: #f5f5f5;
        border-radius: 4px;
        display: inline-block;
    }
    .sim-card-check {
        position: absolute;
        top: 1rem;
        right: 1rem;
        width: 24px;
        height: 24px;
        background: #6366f1;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.8rem;
    }

    /* ===== SIMULATOR REPORT ===== */
    .sim-report {
        background: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
    }
    .sim-report-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e5e5e5;
    }
    .sim-report-section {
        margin-bottom: 1.5rem;
    }
    .sim-report-section-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6366f1;
        margin-bottom: 0.5rem;
    }
    .sim-report-text {
        font-size: 0.95rem;
        color: #374151;
        line-height: 1.7;
    }
    .sim-report-risk {
        background: #fffbeb;
        border: 1px solid #fcd34d;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .sim-report-risk-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #92400e;
        margin-bottom: 0.5rem;
    }
    .sim-report-risk-text {
        font-size: 0.9rem;
        color: #78350f;
    }

    /* ===== STEP INDICATOR ===== */
    .step-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 2rem;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .step-number {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .step-number.active {
        background: #6366f1;
        color: white;
    }
    .step-number.completed {
        background: #dcfce7;
        color: #166534;
    }
    .step-number.inactive {
        background: #f5f5f5;
        color: #a3a3a3;
    }
    .step-label {
        font-size: 0.85rem;
        color: #737373;
    }
    .step-label.active {
        color: #1a1a1a;
        font-weight: 500;
    }
    .step-divider {
        width: 40px;
        height: 1px;
        background: #e5e5e5;
    }

    /* ===== DATA LIMITATIONS ===== */
    .data-limits-banner {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fcd34d;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1.5rem 0;
    }
    .data-limits-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #92400e;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .data-limits-text {
        font-size: 0.85rem;
        color: #78350f;
        line-height: 1.6;
    }
    .data-limits-list {
        margin: 0.75rem 0 0 0;
        padding-left: 1.25rem;
    }
    .data-limits-list li {
        font-size: 0.8rem;
        color: #92400e;
        margin-bottom: 0.35rem;
    }

    /* ===== CROSS SIGNAL VIEW ===== */
    .signal-compare-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .signal-compare-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .signal-compare-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #334155;
    }
    .signal-badge {
        font-size: 0.75rem;
        font-weight: 500;
        padding: 0.25rem 0.6rem;
        border-radius: 4px;
    }
    .signal-badge.high {
        background: #dcfce7;
        color: #166534;
    }
    .signal-badge.medium {
        background: #fef3c7;
        color: #92400e;
    }
    .signal-badge.low {
        background: #f1f5f9;
        color: #64748b;
    }
    .signal-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
    }
    .signal-label {
        font-size: 0.85rem;
        color: #64748b;
    }
    .signal-value {
        font-size: 0.9rem;
        font-weight: 600;
        color: #1e293b;
    }
    .signal-value.positive { color: #16a34a; }
    .signal-value.negative { color: #dc2626; }
    .signal-interpretation {
        background: #f1f5f9;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-top: 0.75rem;
        font-size: 0.85rem;
        color: #475569;
        line-height: 1.5;
    }
    .signal-pattern-tag {
        display: inline-block;
        background: #e0e7ff;
        color: #4338ca;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin-right: 0.5rem;
    }

    /* ===== SERVICE POSITIONING ===== */
    .positioning-notice {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        font-size: 0.8rem;
        color: #64748b;
        text-align: center;
    }

    /* ===== DATA SOURCE TABS ===== */
    .data-source-tabs {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #e5e5e5;
        padding-bottom: 0.5rem;
    }
    .data-source-tab {
        padding: 0.5rem 1rem;
        border-radius: 6px 6px 0 0;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        border: none;
        background: transparent;
        color: #737373;
    }
    .data-source-tab.active {
        background: #6366f1;
        color: white;
    }
    .data-source-tab:hover:not(.active) {
        background: #f5f5f5;
    }

    /* ===== YOUTUBE SPECIFIC ===== */
    .youtube-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #fee2e2;
        color: #dc2626;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .web-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #dbeafe;
        color: #2563eb;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ===== DEMO MODE BANNER ===== */
    .demo-mode-banner {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .demo-mode-icon {
        font-size: 1.2rem;
    }
    .demo-mode-text {
        font-size: 0.85rem;
        color: #92400e;
    }
    .demo-mode-text strong {
        color: #78350f;
    }

    /* ===== DUAL SOURCE CARD ===== */
    .dual-source-card {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .dual-source-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .dual-source-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    .dual-source-row {
        display: flex;
        gap: 1.5rem;
    }
    .source-item {
        flex: 1;
        padding: 1rem;
        background: #fafafa;
        border-radius: 8px;
    }
    .source-item-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8rem;
        color: #737373;
        margin-bottom: 0.5rem;
    }
    .source-item-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    .source-item-value.positive { color: #16a34a; }
    .source-item-value.negative { color: #dc2626; }
    .source-item-value.neutral { color: #737373; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 2. STATE MANAGEMENT & NAVIGATION
# --------------------------------------------------------------------------
# 2. SESSION STATE
# --------------------------------------------------------------------------
CURRENT_V = "v2_landing"

# Page & Version check
if 'app_version' not in st.session_state or st.session_state.app_version != CURRENT_V:
    st.session_state.page = 'home'
    st.session_state.app_version = CURRENT_V

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_keyword' not in st.session_state:
    st.session_state.selected_keyword = None
if 'shortlist' not in st.session_state:
    st.session_state.shortlist = set()
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Period state
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = "3개월"

# Simulator states
if 'sim_step' not in st.session_state:
    st.session_state.sim_step = 1
if 'sim_selected' not in st.session_state:
    st.session_state.sim_selected = set()
if 'sim_candidates' not in st.session_state:
    st.session_state.sim_candidates = []
if 'sim_from_keyword' not in st.session_state:
    st.session_state.sim_from_keyword = None

def navigate_to(page, keyword=None):
    st.session_state.page = page
    if keyword:
        st.session_state.selected_keyword = keyword
    st.rerun()

def start_simulator(from_keyword=None):
    st.session_state.page = 'simulator'
    st.session_state.sim_step = 1
    st.session_state.sim_selected = set()
    st.session_state.sim_from_keyword = from_keyword
    st.session_state.sim_candidates = []
    st.rerun()

# --------------------------------------------------------------------------
# 3. DATA LOADING (CACHED)
# --------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_all_data(timeframe='today 3-m'):
    """웹 + YouTube 데이터를 병렬로 로드. (df, metrics, youtube_df, web_is_mock, youtube_is_mock) 반환"""
    # 병렬 로딩
    result = fetch_multi_signal_data(KEYWORDS, timeframe)

    web_df = result['web']
    youtube_df = result['youtube']

    web_is_mock = False
    youtube_is_mock = False

    if web_df.empty:
        web_df = get_mock_data(KEYWORDS, timeframe)
        web_is_mock = True

    if youtube_df.empty:
        youtube_df = get_mock_youtube_data(KEYWORDS)
        youtube_is_mock = True

    metrics = calculate_growth_metrics(web_df)
    return web_df, metrics, youtube_df, web_is_mock, youtube_is_mock

@st.cache_data(ttl=3600)
def load_data(timeframe='today 3-m'):
    """웹 검색 트렌드 데이터 로드. (df, metrics, is_mock) 반환"""
    df = fetch_trend_data(KEYWORDS, timeframe)
    is_mock = False
    if df.empty:
        df = get_mock_data(KEYWORDS, timeframe)
        is_mock = True
    metrics = calculate_growth_metrics(df)
    return df, metrics, is_mock

@st.cache_data(ttl=3600)
def load_related(keyword):
    return fetch_related_queries(keyword)

@st.cache_data(ttl=3600)
def load_youtube_data(timeframe='today 3-m'):
    """YouTube 검색 트렌드 데이터 로드. (df, is_mock) 반환"""
    df = fetch_youtube_trend_data(KEYWORDS, timeframe)
    is_mock = False
    if df.empty:
        df = get_mock_youtube_data(KEYWORDS)
        is_mock = True
    return df, is_mock

@st.cache_data(ttl=3600)
def load_cross_signals(timeframe='today 3-m'):
    """웹 + YouTube 교차 신호 분석 데이터 로드"""
    df, metrics, youtube_df, _, _ = load_all_data(timeframe)
    cross_signals = analyze_cross_signals(metrics, youtube_df, KEYWORDS)
    return cross_signals

timeframe_map = {
    "3개월": "today 3-m",
    "6개월": "today 6-m",
    "12개월": "today 12-m"
}

# --------------------------------------------------------------------------
# 4. COMPONENTS
# --------------------------------------------------------------------------
def render_header():
    # Using vertical_alignment="center" to solve the "not aligned" issue
    col1, col2, col3 = st.columns([2.5, 5, 1], vertical_alignment="center")
    with col1:
        st.markdown('<div class="logo-btn-wrapper">', unsafe_allow_html=True)
        if st.button("📊 EduTrend Finder", key="logo_home", help="홈으로 이동"):
            navigate_to('home')
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <style>
            /* Logo button style - 강조 */
            .logo-btn-wrapper button,
            .logo-btn-wrapper button p,
            .logo-btn-wrapper [data-testid="stButton"] button {
                background: none !important;
                border: none !important;
                box-shadow: none !important;
                font-size: 1.5rem !important;
                font-weight: 900 !important;
                color: #111827 !important;
                padding: 0.5rem 0 !important;
                cursor: pointer !important;
                letter-spacing: -0.03em !important;
                white-space: nowrap !important;
                text-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
            }
            .logo-btn-wrapper button:hover,
            .logo-btn-wrapper [data-testid="stButton"] button:hover {
                color: #6366f1 !important;
            }

            /* Reset button style for nav */
            div[data-testid="stColumn"] button {
                border: none !important;
                background: none !important;
                box-shadow: none !important;
                transition: all 0.2s !important;
            }

            /* Nav items style */
            .nav-item button, .nav-item-active button {
                color: #4b5563 !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                padding: 0.75rem 1.2rem !important; /* Wider tap area */
                width: 100% !important;
            }
            
            .nav-item button:hover, .nav-item-active button:hover {
                color: #6366f1 !important;
            }
            
            .nav-item-active button {
                color: #6366f1 !important;
                border-bottom: 2px solid #6366f1 !important;
                border-radius: 0 !important;
            }

            /* Regular header button (refresh) */
            div.header-btn button {
                background: #6366f1 !important;
                color: white !important;
                border: none !important;
                padding: 0.6rem 1.2rem !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                font-size: 0.85rem !important;
                box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2) !important;
            }
            div.header-btn button:hover {
                background: #4f46e5 !important;
                box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3) !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    with col2:
        # Equal spacing for nav items
        nc1, nc2, nc3, nc4 = st.columns([1, 1, 1, 1], vertical_alignment="center")
        with nc1:
            active_class = "nav-item-active" if st.session_state.page in ['dashboard', 'detail'] else "nav-item"
            st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)
            if st.button("트렌드 대시보드", key="nav_dash"):
                navigate_to('dashboard')
            st.markdown('</div>', unsafe_allow_html=True)
        with nc2:
            active_class = "nav-item-active" if st.session_state.page == 'compare' else "nav-item"
            st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)
            if st.button("키워드 비교 분석", key="nav_comp"):
                navigate_to('compare')
            st.markdown('</div>', unsafe_allow_html=True)
        with nc3:
            active_class = "nav-item-active" if st.session_state.page == 'report' else "nav-item"
            st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)
            if st.button("인사이트 리포트", key="nav_rep"):
                navigate_to('report')
            st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="header-btn">', unsafe_allow_html=True)
        if st.button("새로고침", key="header_refresh"):
            st.cache_data.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def get_growth_class(growth):
    if growth > 10:
        return "growth-up"
    elif growth < -5:
        return "growth-down"
    return "growth-flat"

def get_growth_sign(growth):
    return "+" if growth > 0 else ""

def format_growth_rate(growth):
    """성장률 포맷팅 (999% = Low Base Effect → N/A 표시)"""
    if growth >= 999:
        return "N/A"
    sign = "+" if growth > 0 else ""
    return f"{sign}{growth:.1f}%"

def is_low_base_effect(growth):
    """Low Base Effect 여부 확인"""
    return growth >= 999

def get_trend_label(growth):
    if growth > 20:
        return "급상승"
    elif growth > 10:
        return "상승"
    elif growth > 0:
        return "완만한 상승"
    elif growth > -5:
        return "정체"
    else:
        return "하락"

def render_simulator_cta():
    st.markdown("""
    <div class="simulator-cta">
        <div class="simulator-cta-text">
            <div class="simulator-cta-title">이 데이터로 강의 주제 선택해보기</div>
            <div class="simulator-cta-desc">트렌드 데이터를 기반으로 기획 판단을 체험해보세요</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("시뮬레이션 시작 →", key="sim_cta_main", use_container_width=False):
        start_simulator()

def render_keyword_simulator_cta(keyword):
    st.markdown(f"""
    <div class="simulator-cta" style="margin-top: 2rem;">
        <div class="simulator-cta-text">
            <div class="simulator-cta-title">이 키워드, 강의로 만들 가치 있을까?</div>
            <div class="simulator-cta-desc">'{keyword}'를 포함한 후보들과 비교하며 기획 판단을 체험해보세요</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("시뮬레이션 시작 →", key="sim_cta_detail", use_container_width=False):
        start_simulator(from_keyword=keyword)


def render_data_limitations_banner(collapsible=False):
    """데이터 한계 명시 배너"""
    if collapsible:
        # 접을 수 있는 형태로 상단에 표시
        with st.expander("⚠️ 데이터 해석 안내 (클릭하여 펼치기)", expanded=False):
            st.markdown(f"""
            <div class="data-limits-banner" style="margin: 0;">
                <div class="data-limits-title" style="margin-bottom: 0.75rem;">
                    {DATA_LIMITATIONS['main_notice'].strip()}
                </div>
                <ul class="data-limits-list">
                    <li><strong>{DATA_LIMITATIONS['limitations'][0]['title']}:</strong> {DATA_LIMITATIONS['limitations'][0]['desc']}</li>
                    <li><strong>{DATA_LIMITATIONS['limitations'][1]['title']}:</strong> {DATA_LIMITATIONS['limitations'][1]['desc']}</li>
                    <li><strong>{DATA_LIMITATIONS['limitations'][2]['title']}:</strong> {DATA_LIMITATIONS['limitations'][2]['desc']}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="data-limits-banner">
            <div class="data-limits-title">
                <span>⚠️</span> {DATA_LIMITATIONS['main_notice'].strip()}
            </div>
            <ul class="data-limits-list">
                <li><strong>{DATA_LIMITATIONS['limitations'][0]['title']}:</strong> {DATA_LIMITATIONS['limitations'][0]['desc']}</li>
                <li><strong>{DATA_LIMITATIONS['limitations'][1]['title']}:</strong> {DATA_LIMITATIONS['limitations'][1]['desc']}</li>
                <li><strong>{DATA_LIMITATIONS['limitations'][2]['title']}:</strong> {DATA_LIMITATIONS['limitations'][2]['desc']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def render_service_positioning():
    """서비스 포지셔닝 명시"""
    st.markdown(f"""
    <div class="positioning-notice">
        {DATA_LIMITATIONS['positioning']}
    </div>
    """, unsafe_allow_html=True)


def render_demo_mode_banner(web_is_mock=False, youtube_is_mock=False):
    """데모 모드 배너 표시"""
    if not web_is_mock and not youtube_is_mock:
        return

    sources = []
    if web_is_mock:
        sources.append("웹 검색")
    if youtube_is_mock:
        sources.append("YouTube")

    source_text = " · ".join(sources)

    st.markdown(f"""
    <div class="demo-mode-banner">
        <span class="demo-mode-icon">🔄</span>
        <div class="demo-mode-text">
            <strong>데모 모드</strong> · {source_text} 데이터는 현재 실시간 연결이 불가하여 시뮬레이션 데이터로 표시됩니다.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_cross_signal_view(keyword, cross_signals):
    """특정 키워드의 교차 신호 분석 뷰"""
    signal_row = cross_signals[cross_signals['키워드'] == keyword]
    if signal_row.empty:
        return

    row = signal_row.iloc[0]
    web_growth = row['웹_성장률']
    yt_growth = row['YouTube_성장률']
    pattern = row['신호_패턴']
    interpretation = row['신호_해석']
    strength = row['신호_강도']

    strength_class = "high" if strength == "높음" else "medium" if strength == "보통" else "low"
    web_class = "positive" if web_growth > 0 else "negative"
    yt_class = "positive" if yt_growth > 0 else "negative"

    st.markdown(f"""
    <div class="signal-compare-card">
        <div class="signal-compare-header">
            <span class="signal-compare-title">다중 신호 교차 확인</span>
            <span class="signal-badge {strength_class}">신호 강도: {strength}</span>
        </div>
        <div class="signal-row">
            <span class="signal-label">웹 검색 성장률</span>
            <span class="signal-value {web_class}">{'+' if web_growth > 0 else ''}{web_growth:.1f}%</span>
        </div>
        <div class="signal-row">
            <span class="signal-label">YouTube 검색 성장률</span>
            <span class="signal-value {yt_class}">{'+' if yt_growth > 0 else ''}{yt_growth:.1f}%</span>
        </div>
        <div class="signal-interpretation">
            <span class="signal-pattern-tag">{pattern}</span>
            {interpretation}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="notice-box" style="font-size: 0.8rem; color: #64748b;">
        <strong>교차 신호 목적:</strong> {DATA_LIMITATIONS['cross_signal_purpose'].strip()}
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# 5. PAGES
# --------------------------------------------------------------------------

def page_home():
    # Hero Section (Aggressive Dark Gradient)
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">EduTrend Finder</h1>
        <div class="hero-subtitle-wrapper">
            <div class="hero-subtitle">
                <span class="hero-data-source">🌐 Web</span>
                <span class="hero-data-source">▶️ YouTube</span>
                <span class="hero-data-source">📊 Google Trends</span>
            </div>
            <div class="hero-subtitle-text">기반 교육 키워드 성장률 분석 도구</div>
        </div>
        <div class="use-cases">
            <div class="use-case-item">
                <div class="use-case-icon">💡</div>
                <div class="use-case-text">지금 강의로 만들면<br>반응이 있을 주제일까요?</div>
            </div>
            <div class="use-case-item">
                <div class="use-case-icon">📈</div>
                <div class="use-case-text">유행이 아닌,<br>실제로 성장 중인 키워드일까요?</div>
            </div>
            <div class="use-case-item">
                <div class="use-case-icon">🎯</div>
                <div class="use-case-text">여러 후보 중<br>어떤 주제를 우선해야 할까요?</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h3 class="section-heading" style="text-align: center; font-size: 1.5rem; margin-bottom: 1rem; font-weight: 800;">탐색 시작하기</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
        <div class="home-nav-card">
            <div>
                <div class="home-card-icon">📊</div>
                <div class="home-card-title">트렌드 대시보드</div>
                <div class="home-card-desc">실시간 급상승 키워드와<br>핵심 성장 지표 확인</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("바로가기 →", key="nav_dash_main", use_container_width=True):
            navigate_to('dashboard')
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="home-nav-card">
            <div>
                <div class="home-card-icon">⚖️</div>
                <div class="home-card-title">키워드 비교 분석</div>
                <div class="home-card-desc">최대 5개 키워드 간<br>관심도 추이 교차 비교</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("바로가기 →", key="nav_comp_main", use_container_width=True):
            navigate_to('compare')
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="home-nav-card">
            <div>
                <div class="home-card-icon">📋</div>
                <div class="home-card-title">인사이트 리포트</div>
                <div class="home-card-desc">심층 분석 결과와<br>신규 기획 추천</div>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("바로가기 →", key="nav_rep_main", use_container_width=True):
            navigate_to('report')
        st.markdown('</div>', unsafe_allow_html=True)



def page_dashboard():
    st.markdown('<h2 class="section-heading">트렌드 대시보드</h2>', unsafe_allow_html=True)
    st.markdown("""
    <p class="section-desc">
        <span class="web-badge">🌐 Web</span>
        <span class="youtube-badge" style="margin-left: 0.5rem;">▶️ YouTube</span>
        <span style="margin-left: 0.5rem;">Google Trends 기반 교육 키워드 성장률 데이터</span>
    </p>
    """, unsafe_allow_html=True)

    # Controls
    col1, col2, col3 = st.columns([1, 2, 3])
    with col1:
        period = st.selectbox("기간", list(timeframe_map.keys()), label_visibility="collapsed")
    with col2:
        search_q = st.text_input("search", placeholder="키워드 검색...",
                                 label_visibility="collapsed", value=st.session_state.search_query)
        if search_q != st.session_state.search_query:
            st.session_state.search_query = search_q

    # Store period in session for other pages
    st.session_state.selected_period = period

    # Load Data (Web + YouTube 병렬 로딩)
    with st.spinner("데이터 로드 중..."):
        df, metrics, youtube_df, web_is_mock, youtube_is_mock = load_all_data(timeframe_map[period])

    # Demo mode banner if using mock data
    render_demo_mode_banner(web_is_mock, youtube_is_mock)

    # 데이터 한계 안내 (접을 수 있는 형태로 상단에 표시)
    render_data_limitations_banner(collapsible=True)

    if '추천액션' not in metrics.columns:
        st.cache_data.clear()
        st.rerun()

    if search_q:
        render_search_results(search_q, df, metrics, web_is_mock, youtube_is_mock)
        return

    # Metrics Summary
    top_kw = metrics.sort_values('성장률(%)', ascending=False).head(20)
    top_growth = top_kw.iloc[0]['성장률(%)'] if len(top_kw) > 0 else 0
    top_growth_display = format_growth_rate(top_growth)
    new_count = len(metrics[metrics['추천액션'].str.contains("신규 기획")])
    test_count = len(metrics[metrics['추천액션'].str.contains("테스트")])
    total_count = len(metrics)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Top 성장률 (웹)</div>
            <div class="metric-value metric-value-highlight">{top_growth_display}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">신규 기획 추천</div>
            <div class="metric-value">{new_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">테스트 권장</div>
            <div class="metric-value">{test_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">모니터링 키워드</div>
            <div class="metric-value">{total_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Top Keywords Section
    st.markdown('<p class="section-title">급상승 키워드</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">성장률 TOP 20</h3>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-desc">{period} 기준 · 성장률 = 최근 30% 구간 평균 / 초기 30% 구간 평균</p>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    for idx, (_, row) in enumerate(top_kw.iterrows()):
        target = col_l if idx < 10 else col_r
        rank = idx + 1
        growth = row['성장률(%)']
        g_class = get_growth_class(growth) if not is_low_base_effect(growth) else "growth-flat"
        growth_display = format_growth_rate(growth)
        action = row['추천액션'].replace("🚀 ", "").replace("🧪 ", "").replace("🔄 ", "").replace("⛔ ", "").replace("➖ ", "")

        with target:
            cols = st.columns([0.4, 2.5, 1.2, 1.5])
            with cols[0]:
                st.markdown(f"<span style='color:#a3a3a3; font-weight:600;'>{rank}</span>", unsafe_allow_html=True)
            with cols[1]:
                if st.button(row['키워드'], key=f"kw_{rank}", use_container_width=True):
                    navigate_to('detail', row['키워드'])
            with cols[2]:
                st.markdown(f"<span class='keyword-growth {g_class}'>{growth_display}</span>", unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f"<span class='keyword-action'>{action}</span>", unsafe_allow_html=True)

    # === Simulator CTA (급상승 키워드 바로 아래) ===
    render_simulator_cta()

    st.markdown("<br>", unsafe_allow_html=True)

    # Shortlist
    if st.session_state.shortlist:
        with st.expander(f"기획 후보 ({len(st.session_state.shortlist)})", expanded=False):
            st.write(", ".join(list(st.session_state.shortlist)))
            c1, c2 = st.columns(2)
            with c1:
                if st.button("비교 분석"):
                    navigate_to('compare')
            with c2:
                if st.button("초기화"):
                    st.session_state.shortlist = set()
                    st.rerun()

    # Full Table
    st.markdown('<p class="section-title">전체 데이터</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">키워드 상세</h3>', unsafe_allow_html=True)

    cats = ["전체"] + list(metrics['카테고리'].unique())
    cat = st.radio("카테고리", cats, horizontal=True, label_visibility="collapsed")

    filtered = metrics.copy()
    if cat != "전체":
        filtered = filtered[filtered['카테고리'] == cat]

    filtered['선택'] = filtered['키워드'].apply(lambda x: x in st.session_state.shortlist)
    display_df = filtered.sort_values('성장률(%)', ascending=False)

    edited = st.data_editor(
        display_df,
        column_order=("선택", "키워드", "성장률(%)", "최근 관심도", "추천액션", "진단유형", "카테고리"),
        column_config={
            "선택": st.column_config.CheckboxColumn("선택"),
            "성장률(%)": st.column_config.NumberColumn("성장률", format="%.1f%%"),
            "최근 관심도": st.column_config.ProgressColumn("관심도", min_value=0, max_value=100),
        },
        hide_index=True,
        use_container_width=True,
        height=350,
        disabled=("키워드", "성장률(%)", "최근 관심도", "추천액션", "진단유형", "카테고리")
    )

    for _, row in edited.iterrows():
        kw = row['키워드']
        if row['선택']:
            st.session_state.shortlist.add(kw)
        elif kw in st.session_state.shortlist:
            st.session_state.shortlist.remove(kw)

    # 서비스 포지셔닝 명시 (하단 고정)
    render_service_positioning()


def render_search_results(query, df, metrics, web_is_mock=False, youtube_is_mock=False):
    render_demo_mode_banner(web_is_mock, youtube_is_mock)
    filtered = metrics[metrics['키워드'].str.contains(query, case=False)]

    if filtered.empty:
        st.info(f"'{query}'에 대한 결과가 없습니다.")
        if st.button("← 돌아가기"):
            st.session_state.search_query = ""
            st.rerun()
        return

    st.markdown(f'<p class="section-title">검색 결과</p>', unsafe_allow_html=True)
    st.markdown(f'<h3 class="section-heading">"{query}"</h3>', unsafe_allow_html=True)

    for _, row in filtered.iterrows():
        kw = row['키워드']
        growth = row['성장률(%)']

        st.markdown("---")
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.markdown(f"### {kw}")
        with c2:
            g_class = get_growth_class(growth)
            g_sign = get_growth_sign(growth)
            st.markdown(f"<span class='keyword-growth {g_class}' style='font-size:1.2rem;'>{g_sign}{growth:.1f}%</span>", unsafe_allow_html=True)
        with c3:
            if st.button("상세 →", key=f"s_{kw}"):
                navigate_to('detail', kw)

        if kw in df.columns:
            import plotly.express as px
            fig = px.line(df, y=kw)
            fig.update_layout(height=200, margin=dict(l=0,r=0,t=10,b=0), xaxis_title="", yaxis_title="")
            fig.update_traces(line_color='#6366f1')
            st.plotly_chart(fig, use_container_width=True)

        mc = st.columns(4)
        mc[0].metric("관심도", f"{row['최근 관심도']:.0f}")
        mc[1].metric("진단", row['진단유형'].split()[-1])
        mc[2].metric("변동성", row['변동성'])
        mc[3].metric("액션", row['추천액션'].split()[-1])

    st.markdown("---")
    if st.button("← 전체 목록"):
        st.session_state.search_query = ""
        st.rerun()


def page_detail():
    if not st.session_state.selected_keyword:
        st.warning("키워드를 선택하세요.")
        if st.button("돌아가기"):
            navigate_to('dashboard')
        return

    kw = st.session_state.selected_keyword

    c1, c2, c3 = st.columns([1, 4, 2])
    with c1:
        if st.button("← 목록"):
            navigate_to('dashboard')
    with c2:
        st.markdown(f"## {kw}")
    with c3:
        in_list = kw in st.session_state.shortlist
        if st.button("후보에서 제거" if in_list else "후보에 추가"):
            if in_list:
                st.session_state.shortlist.remove(kw)
            else:
                st.session_state.shortlist.add(kw)
            st.rerun()

    # Use period from session state if available
    period = st.session_state.get('selected_period', '3개월')
    timeframe = timeframe_map.get(period, 'today 3-m')

    with st.spinner(""):
        df, metrics, youtube_df, web_is_mock, youtube_is_mock = load_all_data(timeframe)

    # Demo mode banner
    render_demo_mode_banner(web_is_mock, youtube_is_mock)

    if kw not in df.columns:
        st.warning("데이터 없음")
        return

    row = metrics[metrics['키워드'] == kw].iloc[0]
    growth = row['성장률(%)']
    growth_display = format_growth_rate(growth)

    st.markdown('<p class="section-title">핵심 지표</p>', unsafe_allow_html=True)

    mc = st.columns(4)
    mc[0].metric("웹 성장률", growth_display)
    mc[1].metric("평균 관심도", f"{row['최근 관심도']:.0f}")
    mc[2].metric("진단", row['진단유형'].split()[-1])
    mc[3].metric("변동성", row['변동성'])

    # Action
    st.markdown(f"""
    <div class="notice-box">
        <strong>기획 판단:</strong> {row['추천액션']}<br>
        <span style="color:#737373;">{row['진단근거']}</span>
    </div>
    """, unsafe_allow_html=True)

    # === YouTube Cross-Signal Analysis ===
    st.markdown('<p class="section-title">데이터 신뢰성 보완 (다중 신호)</p>', unsafe_allow_html=True)
    cross_signals = load_cross_signals(timeframe)
    render_cross_signal_view(kw, cross_signals)

    # Charts - Web and YouTube side by side
    st.markdown('<p class="section-title">트렌드</p>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        import plotly.express as px
        st.markdown('<h3 class="section-heading"><span class="web-badge">🌐 Web</span> 검색 관심도</h3>', unsafe_allow_html=True)
        fig_web = px.line(df, y=kw)
        fig_web.update_layout(height=250, xaxis_title="", yaxis_title="관심도 (0-100)", margin=dict(t=10))
        fig_web.update_traces(line_color='#2563eb', line_width=2)
        st.plotly_chart(fig_web, use_container_width=True)

    with chart_col2:
        st.markdown('<h3 class="section-heading"><span class="youtube-badge">▶️ YouTube</span> 검색 관심도</h3>', unsafe_allow_html=True)
        if kw in youtube_df.columns:
            import plotly.express as px
            fig_yt = px.line(youtube_df, y=kw)
            fig_yt.update_layout(height=250, xaxis_title="", yaxis_title="관심도 (0-100)", margin=dict(t=10))
            fig_yt.update_traces(line_color='#dc2626', line_width=2)
            st.plotly_chart(fig_yt, use_container_width=True)
        else:
            st.info("YouTube 데이터 없음")

    st.markdown('<p class="section-title">연관 키워드</p>', unsafe_allow_html=True)
    related = load_related(kw)
    chips = "".join([f"<span class='tag-chip'>{r}</span>" for r in related])
    st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p class="section-title">기획 참고</p>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown(f"**타겟**<br><span style='color:#737373;'>{row['기획_타겟']}</span>", unsafe_allow_html=True)
    with i2:
        st.markdown(f"**포지셔닝**<br><span style='color:#737373;'>{row['기획_포지션']}</span>", unsafe_allow_html=True)
    with i3:
        st.markdown(f"**리스크**<br><span style='color:#737373;'>{row['기획_리스크']}</span>", unsafe_allow_html=True)

    # === Simulator CTA (키워드 상세 하단) ===
    render_keyword_simulator_cta(kw)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p class="section-title">추가 분석</p>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    with cs1:
        st.markdown("""
        <div class="coming-soon-card">
            <span class="coming-soon-badge">P1</span>
            <div class="coming-soon-title">플랫폼별 비교</div>
            <div class="coming-soon-desc">Udemy, 인프런 등 강의 현황</div>
        </div>
        """, unsafe_allow_html=True)
    with cs2:
        st.markdown("""
        <div class="coming-soon-card">
            <span class="coming-soon-badge">P2</span>
            <div class="coming-soon-title">경쟁 강도</div>
            <div class="coming-soon-desc">시장 포화도 분석</div>
        </div>
        """, unsafe_allow_html=True)


def page_compare():
    st.markdown('<p class="section-title">비교 분석</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">키워드 비교</h3>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">여러 키워드의 트렌드를 비교하여 우선순위를 판단하세요.</p>', unsafe_allow_html=True)

    # Period selector
    col1, col2 = st.columns([1, 4])
    with col1:
        period = st.selectbox("기간", list(timeframe_map.keys()), label_visibility="collapsed",
                              index=list(timeframe_map.keys()).index(st.session_state.get('selected_period', '3개월')))

    with st.spinner(""):
        df, metrics, youtube_df, web_is_mock, youtube_is_mock = load_all_data(timeframe_map[period])

    # Demo mode banner
    render_demo_mode_banner(web_is_mock, youtube_is_mock)

    default = list(metrics['키워드'].unique())[:2]
    if st.session_state.shortlist:
        sl = list(st.session_state.shortlist)
        if len(sl) <= 5:
            default = sl

    selected = st.multiselect("키워드 선택 (최대 5개)", list(metrics['키워드'].unique()), default=default)

    if selected:
        # Data source tabs
        data_source = st.radio("데이터 소스", ["웹 검색", "YouTube 검색", "둘 다 비교"],
                               horizontal=True, label_visibility="collapsed")

        if data_source == "웹 검색":
            import plotly.express as px
            fig = px.line(df[selected])
            fig.update_layout(height=350, xaxis_title="", yaxis_title="관심도 (웹)")
            st.plotly_chart(fig, use_container_width=True)
        elif data_source == "YouTube 검색":
            available = [k for k in selected if k in youtube_df.columns]
            if available:
                import plotly.express as px
                fig = px.line(youtube_df[available])
                fig.update_layout(height=350, xaxis_title="", yaxis_title="관심도 (YouTube)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("선택한 키워드의 YouTube 데이터가 없습니다.")
        else:
            # Side by side comparison
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<span class="web-badge">🌐 Web</span>', unsafe_allow_html=True)
                import plotly.express as px
                fig_web = px.line(df[selected])
                fig_web.update_layout(height=280, xaxis_title="", yaxis_title="관심도", margin=dict(t=10))
                st.plotly_chart(fig_web, use_container_width=True)
            with c2:
                st.markdown('<span class="youtube-badge">▶️ YouTube</span>', unsafe_allow_html=True)
                available = [k for k in selected if k in youtube_df.columns]
                if available:
                    import plotly.express as px
                    fig_yt = px.line(youtube_df[available])
                    fig_yt.update_layout(height=280, xaxis_title="", yaxis_title="관심도", margin=dict(t=10))
                    st.plotly_chart(fig_yt, use_container_width=True)
                else:
                    st.info("YouTube 데이터 없음")

        comp = metrics[metrics['키워드'].isin(selected)]
        st.dataframe(
            comp.sort_values('성장률(%)', ascending=False),
            column_order=("키워드", "성장률(%)", "최근 관심도", "진단유형", "추천액션"),
            hide_index=True,
            use_container_width=True
        )


def page_report():
    st.markdown('<p class="section-title">리포트</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">트렌드 분석 결과</h3>', unsafe_allow_html=True)
    st.markdown("""
    <p class="section-desc">
        <span class="web-badge">🌐 Web</span>
        <span class="youtube-badge" style="margin-left: 0.5rem;">▶️ YouTube</span>
        <span style="margin-left: 0.5rem;">데이터 기반 종합 분석</span>
    </p>
    """, unsafe_allow_html=True)

    # Period selector
    period = st.selectbox("기간", list(timeframe_map.keys()), label_visibility="collapsed",
                          index=list(timeframe_map.keys()).index(st.session_state.get('selected_period', '3개월')))

    with st.spinner(""):
        df, metrics, youtube_df, web_is_mock, youtube_is_mock = load_all_data(timeframe_map[period])
        cross_signals = load_cross_signals(timeframe_map[period])

    # Demo mode banner
    render_demo_mode_banner(web_is_mock, youtube_is_mock)

    new_list = metrics[metrics['추천액션'].str.contains('신규')]['키워드'].tolist()
    test_list = metrics[metrics['추천액션'].str.contains('테스트')]['키워드'].tolist()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**신규 기획 추천**")
        if new_list:
            st.write(", ".join(new_list[:5]))
        else:
            st.write("없음")
    with c2:
        st.markdown("**테스트 권장**")
        if test_list:
            st.write(", ".join(test_list[:5]))
        else:
            st.write("없음")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Top 5 성장률 (웹 검색)**")

    top5 = metrics.sort_values('성장률(%)', ascending=False).head(5)
    for i, (_, r) in enumerate(top5.iterrows()):
        g = r['성장률(%)']
        g_display = format_growth_rate(g)
        st.markdown(f"{i+1}. **{r['키워드']}** · {g_display} · {r['추천액션']}")

    # Cross-signal insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**다중 신호 인사이트**")

    high_signal = cross_signals[cross_signals['신호_강도'] == '높음']
    if not high_signal.empty:
        st.markdown("🔥 **신호 강도 높음** (웹 + YouTube 동반 상승)")
        for _, sig in high_signal.head(3).iterrows():
            st.markdown(f"- {sig['키워드']}: {sig['신호_패턴']} · 웹 {format_growth_rate(sig['웹_성장률'])} / YouTube {format_growth_rate(sig['YouTube_성장률'])}")
    else:
        st.markdown("현재 신호 강도가 높은 키워드가 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">다운로드</p>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "분석 결과 CSV",
            metrics.to_csv(index=False).encode('utf-8-sig'),
            "edutrend_analysis.csv",
            use_container_width=True
        )
    with d2:
        st.download_button(
            "원본 데이터 CSV",
            df.to_csv().encode('utf-8-sig'),
            "edutrend_raw.csv",
            use_container_width=True
        )


# --------------------------------------------------------------------------
# 6. SIMULATOR PAGE
# --------------------------------------------------------------------------
def page_simulator():
    # Header
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("← 대시보드"):
            st.session_state.sim_step = 1
            st.session_state.sim_selected = set()
            navigate_to('dashboard')

    # Load Data
    with st.spinner(""):
        df, metrics, _ = load_data("today 3-m")

    # Generate candidates if needed
    if not st.session_state.sim_candidates:
        sorted_metrics = metrics.sort_values('성장률(%)', ascending=False)
        candidates = []

        # If from keyword detail, include that keyword
        if st.session_state.sim_from_keyword and st.session_state.sim_from_keyword in sorted_metrics['키워드'].values:
            kw_row = sorted_metrics[sorted_metrics['키워드'] == st.session_state.sim_from_keyword].iloc[0]
            candidates.append(kw_row)

        # Add top keywords
        for _, row in sorted_metrics.iterrows():
            if len(candidates) >= 5:
                break
            if row['키워드'] not in [c['키워드'] for c in candidates]:
                candidates.append(row)

        # Shuffle for variety (but keep order somewhat meaningful)
        if len(candidates) > 3:
            mid = candidates[1:-1]
            random.shuffle(mid)
            candidates = [candidates[0]] + mid + [candidates[-1]]

        st.session_state.sim_candidates = candidates

    candidates = st.session_state.sim_candidates

    # Step Indicator
    step = st.session_state.sim_step
    st.markdown(f"""
    <div class="step-indicator">
        <div class="step-item">
            <div class="step-number {'completed' if step > 1 else 'active' if step == 1 else 'inactive'}">{'✓' if step > 1 else '1'}</div>
            <span class="step-label {'active' if step == 1 else ''}">소개</span>
        </div>
        <div class="step-divider"></div>
        <div class="step-item">
            <div class="step-number {'completed' if step > 2 else 'active' if step == 2 else 'inactive'}">{'✓' if step > 2 else '2'}</div>
            <span class="step-label {'active' if step == 2 else ''}">주제 선택</span>
        </div>
        <div class="step-divider"></div>
        <div class="step-item">
            <div class="step-number {'active' if step == 3 else 'inactive'}">3</div>
            <span class="step-label {'active' if step == 3 else ''}">결과 리포트</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # STEP 1: Introduction
    if step == 1:
        st.markdown('<h2 class="section-heading">강의 주제 선택 시뮬레이션</h2>', unsafe_allow_html=True)
        st.markdown("""
        <p class="section-desc" style="font-size: 1rem; line-height: 1.8; max-width: 600px;">
            트렌드 데이터를 기반으로, 제한된 선택 안에서 다음 강의 주제를 선택해보세요.<br><br>
            5개의 교육 키워드 후보 중 <strong>최대 2개</strong>를 선택하고,<br>
            선택에 대한 기획 판단 리포트를 확인할 수 있습니다.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("시작하기 →", use_container_width=False):
            st.session_state.sim_step = 2
            st.rerun()

    # STEP 2: Selection
    elif step == 2:
        st.markdown('<h2 class="section-heading">강의 주제 후보</h2>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">최대 2개의 키워드를 선택하세요. 선택 후 결과 리포트를 생성합니다.</p>', unsafe_allow_html=True)

        selected = st.session_state.sim_selected

        # Warning if over limit
        if len(selected) >= 2:
            st.info("최대 2개까지만 선택할 수 있습니다. 다른 키워드를 선택하려면 먼저 선택을 해제하세요.")

        # Candidate Cards
        cols = st.columns(5)
        for idx, cand in enumerate(candidates):
            kw = cand['키워드']
            growth = cand['성장률(%)']
            trend = get_trend_label(growth)
            is_selected = kw in selected

            growth_class = "positive" if growth > 10 else "negative" if growth < -5 else "neutral"
            g_sign = "+" if growth > 0 else ""

            with cols[idx]:
                card_class = "selected" if is_selected else ""
                st.markdown(f"""<div class="sim-card {card_class}" style="position: relative;">
{'<div class="sim-card-check">✓</div>' if is_selected else ''}
<div class="sim-card-keyword">{kw}</div>
<div class="sim-card-growth {growth_class}">{g_sign}{growth:.1f}%</div>
<div class="sim-card-trend">{trend}</div>
</div>""", unsafe_allow_html=True)

                # Toggle button
                btn_label = "선택 해제" if is_selected else "선택"
                btn_disabled = len(selected) >= 2 and not is_selected

                if st.button(btn_label, key=f"sim_sel_{idx}", disabled=btn_disabled, use_container_width=True):
                    if is_selected:
                        st.session_state.sim_selected.remove(kw)
                    else:
                        st.session_state.sim_selected.add(kw)
                    st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Selection summary
        if selected:
            st.markdown(f"**선택된 키워드:** {', '.join(selected)}")

        # Submit button
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
        with col_btn2:
            if st.button("결과 확인 →", disabled=len(selected) == 0, use_container_width=True):
                st.session_state.sim_step = 3
                st.rerun()

    # STEP 3: Report
    elif step == 3:
        st.markdown('<h2 class="section-heading">기획 판단 리포트</h2>', unsafe_allow_html=True)

        selected = list(st.session_state.sim_selected)
        selected_data = [c for c in candidates if c['키워드'] in selected]

        # Generate Report
        st.markdown('<div class="sim-report">', unsafe_allow_html=True)
        st.markdown('<div class="sim-report-title">선택 결과 요약</div>', unsafe_allow_html=True)

        # Selected keywords summary
        st.markdown('<div class="sim-report-section">', unsafe_allow_html=True)
        st.markdown('<div class="sim-report-section-title">선택한 키워드</div>', unsafe_allow_html=True)

        for data in selected_data:
            kw = data['키워드']
            growth = data['성장률(%)']
            g_sign = "+" if growth > 0 else ""
            st.markdown(f"• **{kw}** — 성장률 {g_sign}{growth:.1f}%")

        st.markdown('</div>', unsafe_allow_html=True)

        # Judgment rationale
        st.markdown('<div class="sim-report-section">', unsafe_allow_html=True)
        st.markdown('<div class="sim-report-section-title">판단 근거</div>', unsafe_allow_html=True)

        avg_growth = sum(d['성장률(%)'] for d in selected_data) / len(selected_data)

        rationale_parts = []

        if avg_growth > 20:
            rationale_parts.append(f"선택한 키워드는 평균 {avg_growth:.1f}%의 높은 성장률을 보이고 있어 시장 관심이 급증하는 주제입니다.")
        elif avg_growth > 10:
            rationale_parts.append(f"선택한 키워드는 평균 {avg_growth:.1f}%의 안정적인 성장률을 보이며, 지속적인 관심이 확인됩니다.")
        elif avg_growth > 0:
            rationale_parts.append(f"선택한 키워드는 평균 {avg_growth:.1f}%의 완만한 성장세를 보이고 있습니다.")
        else:
            rationale_parts.append(f"선택한 키워드는 현재 성장률이 {avg_growth:.1f}%로 정체 또는 하락 추세입니다.")

        # Check for education-related terms
        edu_terms = ['교육', '강의', '입문', '기초', '자격증', '튜토리얼']
        has_edu_context = any(any(term in str(d['키워드']) for term in edu_terms) for d in selected_data)

        if has_edu_context:
            rationale_parts.append("키워드에 교육/학습 의도가 포함되어 있어 강의 콘텐츠로의 전환 가능성이 높습니다.")
        else:
            rationale_parts.append("일반 검색 키워드로, 교육 콘텐츠 수요로 직접 연결되는지는 추가 검증이 필요합니다.")

        st.markdown(f'<p class="sim-report-text">{" ".join(rationale_parts)}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Risk comment
        st.markdown('<div class="sim-report-risk">', unsafe_allow_html=True)
        st.markdown('<div class="sim-report-risk-title">리스크 & 고려사항</div>', unsafe_allow_html=True)

        risks = []
        for data in selected_data:
            if data['변동성'] == '높음':
                risks.append(f"'{data['키워드']}'는 변동성이 높아 일시적 트렌드일 가능성이 있습니다.")
            if data['성장률(%)'] > 50:
                risks.append(f"'{data['키워드']}'의 급격한 성장은 단기 이슈에 의한 것일 수 있어 지속성 검토가 필요합니다.")

        if not risks:
            risks.append("선택한 키워드는 비교적 안정적인 지표를 보이나, 실제 교육 수요와의 연관성은 별도 검증이 권장됩니다.")

        st.markdown(f'<p class="sim-report-risk-text">{" ".join(risks)}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("다시 선택하기", use_container_width=True):
                st.session_state.sim_step = 2
                st.session_state.sim_selected = set()
                st.rerun()
        with col2:
            if st.button("대시보드로", use_container_width=True):
                st.session_state.sim_step = 1
                st.session_state.sim_selected = set()
                st.session_state.sim_candidates = []
                navigate_to('dashboard')


# --------------------------------------------------------------------------
# MAIN ROUTER
# --------------------------------------------------------------------------
render_header()
st.markdown("<div style='height: 1px; background: #e5e5e5; margin: 1rem 0 2rem 0;'></div>", unsafe_allow_html=True)

if st.session_state.page == 'home':
    page_home()
elif st.session_state.page == 'dashboard':
    page_dashboard()
elif st.session_state.page == 'detail':
    page_detail()
elif st.session_state.page == 'compare':
    page_compare()
elif st.session_state.page == 'report':
    page_report()
elif st.session_state.page == 'simulator':
    page_simulator()

st.markdown("""
<div class="app-footer">
    EduTrend Finder DataSource : Web · YouTube · Google Trends
</div>
""", unsafe_allow_html=True)
