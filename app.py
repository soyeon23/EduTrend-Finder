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
    fetch_multi_signal_data, apply_moving_average, normalize_data, calculate_correlation,
    generate_strategic_insights
)
from keyword_list import KEYWORDS
import random
import plotly.graph_objects as go
from datetime import datetime
import io

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

# Analysis options states
if 'show_moving_average' not in st.session_state:
    st.session_state.show_moving_average = True
if 'apply_normalization' not in st.session_state:
    st.session_state.apply_normalization = False
if 'ma_window' not in st.session_state:
    st.session_state.ma_window = 7

# Data update timestamp tracking
if 'last_data_update' not in st.session_state:
    st.session_state.last_data_update = None

# --------------------------------------------------------------------------
# SIDEBAR OPTIONS
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ 분석 옵션")
    st.markdown("---")

    st.markdown("**📈 이동 평균 (Moving Average)**")
    st.session_state.show_moving_average = st.checkbox(
        "이동 평균 표시",
        value=st.session_state.show_moving_average,
        help="차트에 7일 이동 평균선을 함께 표시합니다"
    )

    if st.session_state.show_moving_average:
        st.session_state.ma_window = st.slider(
            "이동 평균 기간 (일)",
            min_value=3,
            max_value=14,
            value=st.session_state.ma_window,
            help="이동 평균 계산에 사용할 일수"
        )

    st.markdown("---")

    st.markdown("**📊 데이터 정규화**")
    st.session_state.apply_normalization = st.checkbox(
        "Min-Max 정규화 (0-100)",
        value=st.session_state.apply_normalization,
        help="모든 키워드를 0-100 범위로 정규화하여 공정한 비교가 가능합니다"
    )

    if st.session_state.apply_normalization:
        st.markdown("""
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 0.75rem; margin-top: 0.5rem; font-size: 0.8rem; color: #1e40af;">
            <strong>ℹ️ 정규화 활성화됨</strong><br>
            각 키워드의 최솟값을 0, 최댓값을 100으로 변환하여 상대적 추세를 비교합니다.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("**📋 분석 정보**")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #64748b; line-height: 1.6;">
    • <strong>이동 평균</strong>: 단기 변동을 완화하여 추세 파악<br>
    • <strong>정규화</strong>: 키워드 간 상대적 비교 용이<br>
    • <strong>상관 계수</strong>: Web-YouTube 간 연관성 측정
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("**⚠️ 데이터 해석 유의사항**")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #94a3b8; line-height: 1.5;">
    Google Trends 데이터는 <strong>상대 지수</strong>입니다.<br>
    실제 검색량이 아닌 상대적 관심도(0-100)를 나타냅니다.
    </div>
    """, unsafe_allow_html=True)

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

    if web_df.empty or len(web_df.columns) < len(KEYWORDS) * 0.5:
        web_df = get_mock_data(KEYWORDS, timeframe)
        web_is_mock = True

    if youtube_df.empty or len(youtube_df.columns) < len(KEYWORDS) * 0.5:
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


def render_normalization_notice():
    """
    정규화 상태 안내 문구를 렌더링합니다.
    정규화가 활성화된 경우에만 표시됩니다.
    """
    if st.session_state.apply_normalization:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                    border: 1px solid #93c5fd;
                    border-radius: 8px;
                    padding: 0.75rem 1rem;
                    margin-bottom: 1rem;
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;">
            <span style="font-size: 1.2rem;">ℹ️</span>
            <div>
                <div style="font-size: 0.9rem; font-weight: 600; color: #1e40af; margin-bottom: 0.2rem;">
                    현재 차트는 모든 키워드를 0–100 기준으로 정규화하여 비교하고 있습니다.
                </div>
                <div style="font-size: 0.8rem; color: #3b82f6;">
                    키워드 간 상대적 추세 비교 목적 · 실제 검색량 비교가 아님
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_data_footer():
    """
    데이터 출처 및 업데이트 시점을 표시하는 Footer를 렌더링합니다.
    """
    # 업데이트 시점 가져오기
    last_update = st.session_state.get('last_data_update')
    if last_update:
        update_str = last_update.strftime("%Y-%m-%d %H:%M")
    else:
        update_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    st.markdown(f"""
    <div style="text-align: center;
                padding: 1.5rem 0;
                color: #94a3b8;
                font-size: 0.75rem;
                border-top: 1px solid #f0f0f0;
                margin-top: 2rem;
                line-height: 1.8;">
        <div style="margin-bottom: 0.3rem;">
            <strong>Data Source:</strong> Google Trends (Web Search · YouTube Search)
        </div>
        <div>
            <strong>Last Updated:</strong> {update_str} (KST)
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_trend_chart(df, keyword, color='#6366f1', title=None, show_ma=True, normalize=False):
    """
    트렌드 차트를 생성합니다 (원본 + 이동평균 동시 표시 가능).

    Args:
        df: 원본 데이터프레임
        keyword: 차트에 표시할 키워드
        color: 메인 색상
        title: 차트 제목
        show_ma: 이동평균 표시 여부
        normalize: 정규화 적용 여부
    """
    if keyword not in df.columns:
        return None

    # 데이터 준비
    chart_df = df[[keyword]].copy()

    # 정규화 적용
    if normalize:
        chart_df = normalize_data(chart_df)

    fig = go.Figure()

    # 원본 데이터 라인
    fig.add_trace(go.Scatter(
        x=chart_df.index,
        y=chart_df[keyword],
        mode='lines',
        name='원본',
        line=dict(color=color, width=1.5),
        opacity=0.5 if show_ma else 1.0
    ))

    # 이동 평균 라인
    if show_ma and st.session_state.show_moving_average:
        ma_df = apply_moving_average(chart_df, window=st.session_state.ma_window)
        fig.add_trace(go.Scatter(
            x=ma_df.index,
            y=ma_df[keyword],
            mode='lines',
            name=f'{st.session_state.ma_window}일 이동평균',
            line=dict(color=color, width=2.5)
        ))

    fig.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=30 if title else 10, b=0),
        xaxis_title="",
        yaxis_title="관심도 (0-100)" if normalize else "관심도",
        title=title,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )

    return fig


def generate_report_html(metrics, strategic_insights, cross_signals, period):
    """
    HTML 형식의 전략 리포트를 생성합니다.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = strategic_insights['summary']
    priority_kws = strategic_insights['priority_keywords']
    market_stages = strategic_insights['market_stages']
    trend_classifications = strategic_insights['trend_classifications']
    correlations = strategic_insights['correlations']

    # 시장 단계별 분류
    stage_groups = {'🌱 도입기': [], '📈 성장기': [], '🏔️ 성숙기': [], '📉 쇠퇴기': [], '🔄 전환기': []}
    for kw, stage_info in market_stages.items():
        stage_groups[stage_info['stage']].append(kw)

    # 트렌드 분류
    sustainable = [kw for kw, tc in trend_classifications.items() if tc['type'] in ['지속 성장', '완만한 성장', '안정적 유지']]
    temporary = [kw for kw, tc in trend_classifications.items() if tc['type'] in ['일시적 급등', '급등 후 하락']]

    # 상관관계 분류
    high_corr = [(k, v) for k, v in correlations.items() if v is not None and v > 0.6]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EduTrend Finder - Strategic Insight Report</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif; color: #1a1a1a; line-height: 1.6; padding: 40px; max-width: 1000px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #6366f1; }}
            .header h1 {{ font-size: 2rem; color: #1e1b4b; margin-bottom: 10px; }}
            .header .subtitle {{ color: #64748b; font-size: 0.9rem; }}
            .header .date {{ color: #94a3b8; font-size: 0.85rem; margin-top: 5px; }}
            .section {{ margin-bottom: 30px; }}
            .section-title {{ font-size: 1.2rem; font-weight: 700; color: #4f46e5; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 1px solid #e5e7eb; }}
            .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }}
            .metric-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; text-align: center; }}
            .metric-box .label {{ font-size: 0.8rem; color: #64748b; margin-bottom: 5px; }}
            .metric-box .value {{ font-size: 1.5rem; font-weight: 700; color: #1e1b4b; }}
            .metric-box .value.highlight {{ color: #6366f1; }}
            .priority-item {{ background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 15px; margin-bottom: 10px; }}
            .priority-item .name {{ font-weight: 700; font-size: 1.1rem; color: #166534; }}
            .priority-item .reason {{ font-size: 0.85rem; color: #64748b; }}
            .priority-item .stats {{ display: flex; gap: 20px; margin-top: 10px; font-size: 0.9rem; }}
            .stage-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }}
            .stage-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; text-align: center; }}
            .stage-box .count {{ font-size: 1.5rem; font-weight: 700; color: #4f46e5; }}
            .stage-box .label {{ font-size: 0.8rem; color: #64748b; }}
            .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .list-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; }}
            .list-box h4 {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 10px; }}
            .list-box ul {{ list-style: none; padding: 0; }}
            .list-box li {{ padding: 5px 0; font-size: 0.9rem; border-bottom: 1px solid #f1f5f9; }}
            .list-box li:last-child {{ border-bottom: none; }}
            .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #94a3b8; font-size: 0.8rem; }}
            @media print {{ body {{ padding: 20px; }} .section {{ page-break-inside: avoid; }} }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 EduTrend Finder</h1>
            <div class="subtitle">Strategic Insight Report</div>
            <div class="date">분석 기간: {period} | 생성일: {report_date}</div>
        </div>

        <div class="section">
            <div class="section-title">📋 요약 메트릭</div>
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="label">분석 키워드</div>
                    <div class="value">{summary['total_keywords']}</div>
                </div>
                <div class="metric-box">
                    <div class="label">성장기 키워드</div>
                    <div class="value highlight">{summary['growth_stage_count']}</div>
                </div>
                <div class="metric-box">
                    <div class="label">안정 트렌드</div>
                    <div class="value">{summary['stable_trend_count']}</div>
                </div>
                <div class="metric-box">
                    <div class="label">우선 추천</div>
                    <div class="value highlight">{summary['priority_count']}</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🎯 우선순위 키워드</div>
            {''.join([f'''
            <div class="priority-item">
                <div class="name">{idx+1}. {pk['keyword']}</div>
                <div class="reason">{pk['reason']}</div>
                <div class="stats">
                    <span>🌐 Web: {'+' if pk['web_growth'] > 0 else ''}{pk['web_growth']:.1f}%</span>
                    <span>▶️ YouTube: {'+' if pk['youtube_growth'] > 0 else ''}{pk['youtube_growth']:.1f}%</span>
                    <span>신뢰도: {pk['confidence']}%</span>
                </div>
            </div>
            ''' for idx, pk in enumerate(priority_kws[:5])]) if priority_kws else '<p style="color: #64748b;">우선 추천 조건을 만족하는 키워드 없음</p>'}
        </div>

        <div class="section">
            <div class="section-title">📊 시장 단계별 분류</div>
            <div class="stage-grid">
                <div class="stage-box">
                    <div class="count">{len(stage_groups['🌱 도입기'])}</div>
                    <div class="label">🌱 도입기</div>
                </div>
                <div class="stage-box">
                    <div class="count">{len(stage_groups['📈 성장기'])}</div>
                    <div class="label">📈 성장기</div>
                </div>
                <div class="stage-box">
                    <div class="count">{len(stage_groups['🏔️ 성숙기'])}</div>
                    <div class="label">🏔️ 성숙기</div>
                </div>
                <div class="stage-box">
                    <div class="count">{len(stage_groups['📉 쇠퇴기'])}</div>
                    <div class="label">📉 쇠퇴기</div>
                </div>
                <div class="stage-box">
                    <div class="count">{len(stage_groups['🔄 전환기'])}</div>
                    <div class="label">🔄 전환기</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📈 트렌드 분류</div>
            <div class="two-col">
                <div class="list-box">
                    <h4>✅ 지속 성장 ({len(sustainable)}개)</h4>
                    <ul>
                        {''.join([f'<li>{kw}</li>' for kw in sustainable[:7]]) if sustainable else '<li>해당 없음</li>'}
                        {f'<li style="color: #94a3b8;">... 외 {len(sustainable)-7}개</li>' if len(sustainable) > 7 else ''}
                    </ul>
                </div>
                <div class="list-box">
                    <h4>⚠️ 일시적 급등 ({len(temporary)}개)</h4>
                    <ul>
                        {''.join([f'<li>{kw}</li>' for kw in temporary[:7]]) if temporary else '<li>해당 없음</li>'}
                        {f'<li style="color: #94a3b8;">... 외 {len(temporary)-7}개</li>' if len(temporary) > 7 else ''}
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🔗 Web-YouTube 높은 상관관계</div>
            <div class="list-box">
                <ul>
                    {''.join([f'<li><strong>{kw}</strong>: {corr:.3f}</li>' for kw, corr in sorted(high_corr, key=lambda x: x[1], reverse=True)[:10]]) if high_corr else '<li>높은 상관관계 키워드 없음</li>'}
                </ul>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📋 전체 키워드 분석 결과</div>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
                <thead>
                    <tr style="background: #f1f5f9;">
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #e2e8f0;">키워드</th>
                        <th style="padding: 10px; text-align: right; border-bottom: 2px solid #e2e8f0;">성장률</th>
                        <th style="padding: 10px; text-align: right; border-bottom: 2px solid #e2e8f0;">관심도</th>
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #e2e8f0;">진단</th>
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #e2e8f0;">추천액션</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #f1f5f9;">{row['키워드']}</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #f1f5f9; color: {'#16a34a' if row['성장률(%)'] > 0 else '#dc2626'};">{'+' if row['성장률(%)'] > 0 else ''}{row['성장률(%)']:.1f}%</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #f1f5f9;">{row['최근 관심도']:.0f}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #f1f5f9;">{row['진단유형']}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #f1f5f9;">{row['추천액션']}</td>
                    </tr>
                    ''' for _, row in metrics.sort_values('성장률(%)', ascending=False).iterrows()])}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>EduTrend Finder | DataSource: Web · YouTube · Google Trends</p>
            <p>이 데이터는 '정답'이 아닌 '판단을 돕는 신호(Signal)'입니다.</p>
        </div>
    </body>
    </html>
    """
    return html_content


def create_multi_keyword_chart(df, keywords, title=None, show_ma=True, normalize=False):
    """
    여러 키워드를 한 차트에 표시합니다.

    Args:
        df: 원본 데이터프레임
        keywords: 표시할 키워드 리스트
        title: 차트 제목
        show_ma: 이동평균만 표시할지 여부
        normalize: 정규화 적용 여부
    """
    available = [k for k in keywords if k in df.columns]
    if not available:
        return None

    # 데이터 준비
    chart_df = df[available].copy()

    # 정규화 적용
    if normalize:
        chart_df = normalize_data(chart_df)

    fig = go.Figure()

    colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

    for idx, keyword in enumerate(available):
        color = colors[idx % len(colors)]

        if show_ma and st.session_state.show_moving_average:
            # 이동평균만 표시
            ma_df = apply_moving_average(chart_df[[keyword]], window=st.session_state.ma_window)
            fig.add_trace(go.Scatter(
                x=ma_df.index,
                y=ma_df[keyword],
                mode='lines',
                name=keyword,
                line=dict(color=color, width=2)
            ))
        else:
            # 원본 표시
            fig.add_trace(go.Scatter(
                x=chart_df.index,
                y=chart_df[keyword],
                mode='lines',
                name=keyword,
                line=dict(color=color, width=1.5)
            ))

    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=30 if title else 10, b=0),
        xaxis_title="",
        yaxis_title="관심도 (0-100)" if normalize else "관심도",
        title=title,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )

    return fig


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
        if st.button("바로가기 →", key="nav_comp_main", width='stretch'):
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
        if st.button("바로가기 →", key="nav_rep_main", width='stretch'):
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
    with st.spinner("🔍 40개 이상의 교육 키워드 트렌드를 정밀하게 분석 중입니다... (약 5~10초 소요)"):
        df, metrics, youtube_df, web_is_mock, youtube_is_mock = load_all_data(timeframe_map[period])
        # 데이터 업데이트 시점 기록
        st.session_state.last_data_update = datetime.now()

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
                if st.button(row['키워드'], key=f"kw_{rank}", width='stretch'):
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
        width='stretch',
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

    # 데이터 출처 및 업데이트 시점 Footer
    render_data_footer()


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
            st.plotly_chart(fig, width='stretch')

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
        st.session_state.last_data_update = datetime.now()

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

    # 정규화 안내 문구 (활성화 시에만 표시)
    render_normalization_notice()

    # 이동 평균 옵션 표시
    if st.session_state.show_moving_average:
        st.markdown(f"<p style='font-size: 0.85rem; color: #6366f1;'>📈 {st.session_state.ma_window}일 이동평균 적용됨</p>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<h3 class="section-heading"><span class="web-badge">🌐 Web</span> 검색 관심도</h3>', unsafe_allow_html=True)
        fig_web = create_trend_chart(
            df, kw, color='#2563eb',
            show_ma=st.session_state.show_moving_average,
            normalize=st.session_state.apply_normalization
        )
        if fig_web:
            st.plotly_chart(fig_web, width='stretch')

    with chart_col2:
        st.markdown('<h3 class="section-heading"><span class="youtube-badge">▶️ YouTube</span> 검색 관심도</h3>', unsafe_allow_html=True)
        if kw in youtube_df.columns:
            fig_yt = create_trend_chart(
                youtube_df, kw, color='#dc2626',
                show_ma=st.session_state.show_moving_average,
                normalize=st.session_state.apply_normalization
            )
            if fig_yt:
                st.plotly_chart(fig_yt, width='stretch')
        else:
            st.info("YouTube 데이터 없음")

    # Web-YouTube 상관관계 표시
    correlations = calculate_correlation(df, youtube_df, [kw])
    if kw in correlations and correlations[kw] is not None:
        corr_val = correlations[kw]
        corr_label = "강한 양의 상관" if corr_val > 0.7 else "보통 양의 상관" if corr_val > 0.4 else "약한 상관" if corr_val > 0.1 else "거의 무관"
        corr_color = "#16a34a" if corr_val > 0.5 else "#f59e0b" if corr_val > 0.2 else "#64748b"
        st.markdown(f"""
        <div class="notice-box" style="display: flex; align-items: center; gap: 1rem;">
            <div>
                <strong>Web ↔ YouTube 상관 계수:</strong>
                <span style="font-size: 1.2rem; font-weight: 700; color: {corr_color}; margin-left: 0.5rem;">{corr_val:.3f}</span>
                <span style="font-size: 0.85rem; color: #64748b; margin-left: 0.5rem;">({corr_label})</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

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

    # 데이터 출처 및 업데이트 시점 Footer
    render_data_footer()


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
        st.session_state.last_data_update = datetime.now()

    # Demo mode banner
    render_demo_mode_banner(web_is_mock, youtube_is_mock)

    default = list(metrics['키워드'].unique())[:2]
    if st.session_state.shortlist:
        sl = list(st.session_state.shortlist)
        if len(sl) <= 5:
            default = sl

    selected = st.multiselect("키워드 선택 (최대 5개)", list(metrics['키워드'].unique()), default=default)

    if selected:
        # 정규화 안내 문구 (활성화 시에만 표시)
        render_normalization_notice()

        # 이동 평균 옵션 표시
        if st.session_state.show_moving_average:
            st.markdown(f"<p style='font-size: 0.85rem; color: #6366f1;'>📈 {st.session_state.ma_window}일 이동평균 적용됨</p>", unsafe_allow_html=True)

        # Data source tabs
        data_source = st.radio("데이터 소스", ["웹 검색", "YouTube 검색", "둘 다 비교"],
                               horizontal=True, label_visibility="collapsed")

        if data_source == "웹 검색":
            fig = create_multi_keyword_chart(
                df, selected,
                show_ma=st.session_state.show_moving_average,
                normalize=st.session_state.apply_normalization
            )
            if fig:
                st.plotly_chart(fig, width='stretch')
        elif data_source == "YouTube 검색":
            available = [k for k in selected if k in youtube_df.columns]
            if available:
                fig = create_multi_keyword_chart(
                    youtube_df, available,
                    show_ma=st.session_state.show_moving_average,
                    normalize=st.session_state.apply_normalization
                )
                if fig:
                    st.plotly_chart(fig, width='stretch')
            else:
                st.info("선택한 키워드의 YouTube 데이터가 없습니다.")
        else:
            # Side by side comparison
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<span class="web-badge">🌐 Web</span>', unsafe_allow_html=True)
                fig_web = create_multi_keyword_chart(
                    df, selected,
                    show_ma=st.session_state.show_moving_average,
                    normalize=st.session_state.apply_normalization
                )
                if fig_web:
                    fig_web.update_layout(height=280)
                    st.plotly_chart(fig_web, width='stretch')
            with c2:
                st.markdown('<span class="youtube-badge">▶️ YouTube</span>', unsafe_allow_html=True)
                available = [k for k in selected if k in youtube_df.columns]
                if available:
                    fig_yt = create_multi_keyword_chart(
                        youtube_df, available,
                        show_ma=st.session_state.show_moving_average,
                        normalize=st.session_state.apply_normalization
                    )
                    if fig_yt:
                        fig_yt.update_layout(height=280)
                        st.plotly_chart(fig_yt, width='stretch')
                else:
                    st.info("YouTube 데이터 없음")

        # 상관계수 테이블 추가
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Web ↔ YouTube 상관 계수**")
        correlations = calculate_correlation(df, youtube_df, selected)
        corr_data = []
        for kw in selected:
            corr_val = correlations.get(kw)
            if corr_val is not None:
                corr_label = "강함" if corr_val > 0.7 else "보통" if corr_val > 0.4 else "약함"
                corr_data.append({'키워드': kw, '상관계수': corr_val, '강도': corr_label})
            else:
                corr_data.append({'키워드': kw, '상관계수': None, '강도': '-'})

        import pandas as pd
        corr_df = pd.DataFrame(corr_data)
        st.dataframe(corr_df, hide_index=True, width='stretch')

        st.markdown("<br>", unsafe_allow_html=True)

        comp = metrics[metrics['키워드'].isin(selected)]
        st.dataframe(
            comp.sort_values('성장률(%)', ascending=False),
            column_order=("키워드", "성장률(%)", "최근 관심도", "진단유형", "추천액션"),
            hide_index=True,
            width='stretch'
        )

    # 데이터 출처 및 업데이트 시점 Footer
    render_data_footer()


def page_report():
    st.markdown('<p class="section-title">리포트</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">Strategic Insight Report</h3>', unsafe_allow_html=True)
    st.markdown("""
    <p class="section-desc">
        <span class="web-badge">🌐 Web</span>
        <span class="youtube-badge" style="margin-left: 0.5rem;">▶️ YouTube</span>
        <span style="margin-left: 0.5rem;">데이터 기반 전략적 인사이트</span>
    </p>
    """, unsafe_allow_html=True)

    # Period selector
    period = st.selectbox("기간", list(timeframe_map.keys()), label_visibility="collapsed",
                          index=list(timeframe_map.keys()).index(st.session_state.get('selected_period', '3개월')))

    with st.spinner("데이터 분석 중..."):
        df, metrics, youtube_df, web_is_mock, youtube_is_mock = load_all_data(timeframe_map[period])
        cross_signals = load_cross_signals(timeframe_map[period])
        # 전략적 인사이트 생성
        strategic_insights = generate_strategic_insights(df, youtube_df, metrics, list(metrics['키워드']))
        st.session_state.last_data_update = datetime.now()

    # Demo mode banner
    render_demo_mode_banner(web_is_mock, youtube_is_mock)

    # ============================================
    # 1. 요약 메트릭 카드
    # ============================================
    st.markdown('<p class="section-title">요약</p>', unsafe_allow_html=True)

    summary = strategic_insights['summary']
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">분석 키워드</div>
            <div class="metric-value">{summary['total_keywords']}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">성장기 키워드</div>
            <div class="metric-value metric-value-highlight">{summary['growth_stage_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">안정 트렌드</div>
            <div class="metric-value">{summary['stable_trend_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">우선 추천</div>
            <div class="metric-value metric-value-highlight">{summary['priority_count']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================
    # 2. 우선순위 키워드 추천
    # ============================================
    st.markdown('<p class="section-title">우선순위 키워드</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">🎯 기획 추천 키워드</h3>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">성장기 시장 + 지속 성장 트렌드를 보이는 키워드</p>', unsafe_allow_html=True)

    priority_kws = strategic_insights['priority_keywords']
    if priority_kws:
        for idx, pk in enumerate(priority_kws[:5]):
            confidence_bar = "🟢" * (pk['confidence'] // 20) + "⚪" * (5 - pk['confidence'] // 20)
            st.markdown(f"""
            <div class="dual-source-card">
                <div class="dual-source-header">
                    <span class="dual-source-title">{idx + 1}. {pk['keyword']}</span>
                    <span style="font-size: 0.85rem; color: #6366f1;">{pk['reason']}</span>
                </div>
                <div class="dual-source-row">
                    <div class="source-item">
                        <div class="source-item-label"><span class="web-badge">🌐 Web</span> 성장률</div>
                        <div class="source-item-value {'positive' if pk['web_growth'] > 0 else 'negative'}">{'+' if pk['web_growth'] > 0 else ''}{pk['web_growth']:.1f}%</div>
                    </div>
                    <div class="source-item">
                        <div class="source-item-label"><span class="youtube-badge">▶️ YT</span> 성장률</div>
                        <div class="source-item-value {'positive' if pk['youtube_growth'] > 0 else 'negative'}">{'+' if pk['youtube_growth'] > 0 else ''}{pk['youtube_growth']:.1f}%</div>
                    </div>
                    <div class="source-item">
                        <div class="source-item-label">신뢰도</div>
                        <div class="source-item-value">{confidence_bar} {pk['confidence']}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("현재 우선 추천 조건을 만족하는 키워드가 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================
    # 3. 시장 단계별 분류
    # ============================================
    st.markdown('<p class="section-title">시장 단계 분석</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">📊 키워드별 시장 단계</h3>', unsafe_allow_html=True)

    market_stages = strategic_insights['market_stages']
    stage_groups = {'🌱 도입기': [], '📈 성장기': [], '🏔️ 성숙기': [], '📉 쇠퇴기': [], '🔄 전환기': []}

    for kw, stage_info in market_stages.items():
        stage_groups[stage_info['stage']].append(kw)

    stage_cols = st.columns(5)
    stage_labels = ['🌱 도입기', '📈 성장기', '🏔️ 성숙기', '📉 쇠퇴기', '🔄 전환기']

    for idx, stage in enumerate(stage_labels):
        with stage_cols[idx]:
            st.markdown(f"**{stage}**")
            st.markdown(f"<span style='font-size: 1.5rem; font-weight: 700;'>{len(stage_groups[stage])}</span>", unsafe_allow_html=True)
            if stage_groups[stage]:
                for kw in stage_groups[stage][:3]:
                    st.markdown(f"<span class='tag-chip'>{kw}</span>", unsafe_allow_html=True)
                if len(stage_groups[stage]) > 3:
                    st.markdown(f"<span style='color: #64748b; font-size: 0.8rem;'>외 {len(stage_groups[stage]) - 3}개</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================
    # 4. 트렌드 분류 (지속 성장 vs 일시적 급등)
    # ============================================
    st.markdown('<p class="section-title">트렌드 분류</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">📈 지속 성장 vs 일시적 급등</h3>', unsafe_allow_html=True)

    trend_classifications = strategic_insights['trend_classifications']
    sustainable = []
    temporary = []
    other = []

    for kw, tc in trend_classifications.items():
        if tc['type'] in ['지속 성장', '완만한 성장', '안정적 유지']:
            sustainable.append({'keyword': kw, **tc})
        elif tc['type'] in ['일시적 급등', '급등 후 하락']:
            temporary.append({'keyword': kw, **tc})
        else:
            other.append({'keyword': kw, **tc})

    tc1, tc2 = st.columns(2)
    with tc1:
        st.markdown("**✅ 지속 성장 키워드**")
        st.markdown("<p style='font-size: 0.85rem; color: #64748b;'>안정적인 상승 추세 유지</p>", unsafe_allow_html=True)
        if sustainable:
            for item in sustainable[:5]:
                st.markdown(f"- **{item['keyword']}**: {item['reason']} (신뢰도 {item['confidence']}%)")
        else:
            st.write("해당 없음")

    with tc2:
        st.markdown("**⚠️ 일시적 급등 키워드**")
        st.markdown("<p style='font-size: 0.85rem; color: #64748b;'>변동성 높음, 주의 필요</p>", unsafe_allow_html=True)
        if temporary:
            for item in temporary[:5]:
                st.markdown(f"- **{item['keyword']}**: {item['reason']} (신뢰도 {item['confidence']}%)")
        else:
            st.write("해당 없음")

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================
    # 5. 상관관계 분석
    # ============================================
    st.markdown('<p class="section-title">Web-YouTube 상관관계</p>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-heading">🔗 플랫폼 간 연관성</h3>', unsafe_allow_html=True)

    correlations = strategic_insights['correlations']
    high_corr = [(k, v) for k, v in correlations.items() if v is not None and v > 0.6]
    low_corr = [(k, v) for k, v in correlations.items() if v is not None and v < 0.3]

    corr1, corr2 = st.columns(2)
    with corr1:
        st.markdown("**🔥 높은 상관관계** (>0.6)")
        if high_corr:
            for kw, corr in sorted(high_corr, key=lambda x: x[1], reverse=True)[:5]:
                st.markdown(f"- {kw}: **{corr:.3f}**")
        else:
            st.write("해당 없음")
    with corr2:
        st.markdown("**📊 낮은 상관관계** (<0.3)")
        if low_corr:
            for kw, corr in sorted(low_corr, key=lambda x: x[1])[:5]:
                st.markdown(f"- {kw}: **{corr:.3f}**")
        else:
            st.write("해당 없음")

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================
    # 6. 기존 요약 정보
    # ============================================
    st.markdown('<p class="section-title">추가 분석</p>', unsafe_allow_html=True)

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

    # ============================================
    # 7. 다운로드 섹션
    # ============================================
    st.markdown('<p class="section-title">다운로드</p>', unsafe_allow_html=True)

    # HTML 리포트 생성
    report_html = generate_report_html(metrics, strategic_insights, cross_signals, period)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.download_button(
            "📊 분석 결과 CSV",
            metrics.to_csv(index=False).encode('utf-8-sig'),
            "edutrend_analysis.csv",
            width='stretch'
        )
    with d2:
        st.download_button(
            "📈 원본 데이터 CSV",
            df.to_csv().encode('utf-8-sig'),
            "edutrend_raw.csv",
            width='stretch'
        )
    with d3:
        st.download_button(
            "📄 리포트 다운로드 (HTML)",
            report_html.encode('utf-8'),
            f"edutrend_report_{datetime.now().strftime('%Y%m%d')}.html",
            mime="text/html",
            width='stretch',
            help="HTML 파일을 다운로드 후 브라우저에서 열어 PDF로 인쇄할 수 있습니다"
        )

    st.markdown("""
    <div class="notice-box" style="margin-top: 1rem; font-size: 0.85rem;">
        <strong>💡 PDF 저장 방법:</strong> HTML 리포트를 다운로드한 후, 브라우저에서 열고 <code>Ctrl+P</code> (또는 <code>Cmd+P</code>)를 눌러 PDF로 인쇄하세요.
    </div>
    """, unsafe_allow_html=True)

    # 데이터 출처 및 업데이트 시점 Footer
    render_data_footer()


# --------------------------------------------------------------------------
# 6. SIMULATOR PAGE
# --------------------------------------------------------------------------
def page_simulator():
    # Header
    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("← 대시보드", width='stretch'):
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

        # 데이터 준비
        avg_growth = sum(d['성장률(%)'] for d in selected_data) / len(selected_data) if selected_data else 0

        # 선택한 키워드 HTML 생성
        keywords_html = ""
        for data in selected_data:
            kw = data['키워드']
            growth = data['성장률(%)']
            g_sign = "+" if growth > 0 else ""
            keywords_html += f"<div style='margin-bottom: 0.5rem;'>• <strong>{kw}</strong> — 성장률 {g_sign}{growth:.1f}%</div>"

        # 판단 근거 생성
        rationale_parts = []
        if avg_growth > 20:
            rationale_parts.append(f"선택한 키워드는 평균 {avg_growth:.1f}%의 높은 성장률을 보이고 있어 시장 관심이 급증하는 주제입니다.")
        elif avg_growth > 10:
            rationale_parts.append(f"선택한 키워드는 평균 {avg_growth:.1f}%의 안정적인 성장률을 보이며, 지속적인 관심이 확인됩니다.")
        elif avg_growth > 0:
            rationale_parts.append(f"선택한 키워드는 평균 {avg_growth:.1f}%의 완만한 성장세를 보이고 있습니다.")
        else:
            rationale_parts.append(f"선택한 키워드는 현재 성장률이 {avg_growth:.1f}%로 정체 또는 하락 추세입니다.")

        edu_terms = ['교육', '강의', '입문', '기초', '자격증', '튜토리얼']
        has_edu_context = any(any(term in str(d['키워드']) for term in edu_terms) for d in selected_data)

        if has_edu_context:
            rationale_parts.append("키워드에 교육/학습 의도가 포함되어 있어 강의 콘텐츠로의 전환 가능성이 높습니다.")
        else:
            rationale_parts.append("일반 검색 키워드로, 교육 콘텐츠 수요로 직접 연결되는지는 추가 검증이 필요합니다.")

        rationale_text = " ".join(rationale_parts)

        # 리스크 생성
        risks = []
        for data in selected_data:
            if data['변동성'] == '높음':
                risks.append(f"'{data['키워드']}'는 변동성이 높아 일시적 트렌드일 가능성이 있습니다.")
            if data['성장률(%)'] > 50:
                risks.append(f"'{data['키워드']}'의 급격한 성장은 단기 이슈에 의한 것일 수 있어 지속성 검토가 필요합니다.")

        if not risks:
            risks.append("선택한 키워드는 비교적 안정적인 지표를 보이나, 실제 교육 수요와의 연관성은 별도 검증이 권장됩니다.")

        risks_text = " ".join(risks)

        # 전체 리포트 HTML (인라인 스타일로 렌더링 보장)
        report_html = f"""
<div style="background: #fafafa; border: 1px solid #e5e5e5; border-radius: 12px; padding: 2rem; margin-top: 1rem;">
    <div style="font-size: 1.25rem; font-weight: 700; color: #1a1a1a; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid #e5e5e5;">
        선택 결과 요약
    </div>
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.9rem; font-weight: 600; color: #6366f1; margin-bottom: 0.5rem;">선택한 키워드</div>
        {keywords_html}
    </div>
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 0.9rem; font-weight: 600; color: #6366f1; margin-bottom: 0.5rem;">판단 근거</div>
        <p style="font-size: 0.95rem; color: #374151; line-height: 1.7; margin: 0;">{rationale_text}</p>
    </div>
    <div style="background: #fffbeb; border: 1px solid #fcd34d; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
        <div style="font-size: 0.85rem; font-weight: 600; color: #92400e; margin-bottom: 0.5rem;">리스크 & 고려사항</div>
        <p style="font-size: 0.9rem; color: #78350f; margin: 0; line-height: 1.6;">{risks_text}</p>
    </div>
</div>
"""
        st.markdown(report_html, unsafe_allow_html=True)

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

# 글로벌 Footer (데이터 출처 및 업데이트 시점)
last_update = st.session_state.get('last_data_update')
update_str = last_update.strftime("%Y-%m-%d %H:%M") if last_update else datetime.now().strftime("%Y-%m-%d %H:%M")

st.markdown(f"""
<div class="app-footer">
    <div style="margin-bottom: 0.3rem;">
        <strong>Data Source:</strong> Google Trends (Web Search · YouTube Search)
    </div>
    <div style="font-size: 0.7rem; color: #b0b0b0;">
        Last Updated: {update_str} (KST)
    </div>
</div>
""", unsafe_allow_html=True)
