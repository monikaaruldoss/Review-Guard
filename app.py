"""
ReviewGuard - Fake Product Review Detection Application
A comprehensive machine learning application for detecting fake product reviews
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import joblib
from io import BytesIO

# Import modules
from modules import upload, cleaning, manipulation, analysis, visualization
from modules import preprocessing, feature_extraction, model_training, prediction

# Page configuration
st.set_page_config(
    page_title="ReviewGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Exo+2:wght@500;600;700&family=JetBrains+Mono:wght@400;700&family=Manrope:wght@400;600;700;800&family=Montserrat:wght@500;600;700&family=Orbitron:wght@600;700&family=Sora:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --bg-a: #07142e;
        --bg-b: #0a4d68;
        --bg-c: #15aabf;
        --accent-1: #ff6b6b;
        --accent-2: #ffd166;
        --accent-3: #2ec4b6;
        --text-main: #e8f7ff;
        --text-soft: #bcd4e6;
        --glass: rgba(255, 255, 255, 0.08);
        --glass-strong: rgba(255, 255, 255, 0.14);
        --border-glow: rgba(255, 209, 102, 0.35);
        --dur-page: 20s;
        --dur-aurora: 24s;
        --dur-orb: 14s;
    }

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }

    /* Dynamic gradient canvas */
    .stApp {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(1200px 700px at -10% -15%, rgba(255, 107, 107, 0.35), transparent 55%),
            radial-gradient(900px 600px at 110% 0%, rgba(255, 209, 102, 0.28), transparent 60%),
            radial-gradient(1000px 700px at 50% 120%, rgba(46, 196, 182, 0.30), transparent 58%),
            linear-gradient(140deg, var(--bg-a) 0%, var(--bg-b) 45%, var(--bg-c) 100%);
        background-size: 130% 130%;
        animation: pageGradientShift var(--dur-page) ease-in-out infinite;
    }

    .stApp::before,
    .stApp::after {
        content: "";
        position: fixed;
        z-index: 0;
        pointer-events: none;
        will-change: transform, background-position;
    }

    .stApp::before {
        inset: -30% -20% -25% -20%;
        opacity: 0.42;
        mix-blend-mode: soft-light;
        background:
            radial-gradient(60% 46% at 18% 16%, rgba(255, 209, 102, 0.35), transparent 60%),
            radial-gradient(52% 46% at 80% 22%, rgba(255, 107, 107, 0.34), transparent 58%),
            radial-gradient(56% 50% at 48% 86%, rgba(46, 196, 182, 0.34), transparent 62%),
            repeating-linear-gradient(
                130deg,
                rgba(255, 255, 255, 0.035) 0px,
                rgba(255, 255, 255, 0.035) 2px,
                transparent 2px,
                transparent 20px
            );
        background-size: 120% 120%, 130% 130%, 125% 125%, 220px 220px;
        animation: auroraShift var(--dur-aurora) linear infinite;
    }

    .stApp::after {
        width: 34vax;
        height: 34vmax;
        right: -10vmax;
        bottom: -12vmax;
        border-radius: 50%;
        filter: blur(10px);
        opacity: 0.35;
        mix-blend-mode: screen;
        background: radial-gradient(circle at 60% 40%, rgba(46, 196, 182, 0.85), rgba(21, 170, 191, 0.08) 70%);
        animation: ambientDriftTwo var(--dur-orb) ease-in-out infinite alternate;
    }

    @keyframes pageGradientShift {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    @keyframes ambientDriftOne {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(5vmax, 3vmax) scale(1.06); }
        100% { transform: translate(9vmax, 6vmax) scale(1.1); }
    }

    @keyframes auroraShift {
        0% {
            transform: translate3d(0, 0, 0) scale(1);
            background-position: 0% 0%, 0% 0%, 0% 0%, 0 0;
        }
        50% {
            transform: translate3d(-2.5%, 2%, 0) scale(1.04);
            background-position: 62% 48%, 45% 60%, 58% 42%, 180px 120px;
        }
        100% {
            transform: translate3d(2.5%, -2%, 0) scale(1.02);
            background-position: 100% 100%, 100% 100%, 100% 100%, 360px 260px;
        }
    }

    @keyframes ambientDriftTwo {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-6vmax, -3vmax) scale(1.05); }
        100% { transform: translate(-10vmax, -6vmax) scale(1.1); }
    }

    /* Ensure app content stays above animated background layers */
    .stApp > header,
    .stApp > div,
    section[data-testid="stSidebar"] {
        position: relative;
        z-index: 1;
    }

    .main-title {
        position: relative;
        text-align: center;
        color: #ffffff;
        font-family: 'Cinzel', serif;
        font-size: clamp(2.2rem, 4.6vw, 3.6rem);
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 0.25em;
        text-shadow: 0 0 22px rgba(255, 209, 102, 0.55), 0 0 40px rgba(46, 196, 182, 0.28);
        animation: titleReveal 900ms ease-out;
    }

    .main-title::after {
        content: "";
        display: block;
        width: min(280px, 60%);
        height: 4px;
        margin: 0.45rem auto 0;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(255, 107, 107, 0.2), rgba(255, 209, 102, 0.95), rgba(46, 196, 182, 0.2));
        animation: titleBeam 3.2s ease-in-out infinite;
    }

    .subtitle {
        text-align: center;
        color: var(--text-soft);
        font-family: 'JetBrains Mono', monospace;
        font-size: clamp(0.95rem, 1.4vw, 1.15rem);
        margin-bottom: 1.4em;
        opacity: 0.95;
        animation: subtitleFloat 1400ms ease-out;
    }

    @keyframes titleReveal {
        0% { transform: translateY(-8px) scale(0.98); opacity: 0; }
        100% { transform: translateY(0) scale(1); opacity: 1; }
    }

    @keyframes subtitleFloat {
        0% { transform: translateY(10px); opacity: 0; }
        100% { transform: translateY(0); opacity: 0.95; }
    }

    @keyframes titleBeam {
        0%, 100% { transform: scaleX(0.88); opacity: 0.65; }
        50% { transform: scaleX(1); opacity: 1; }
    }

    /* Glass cards for key containers */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMarkdownContainer"]),
    div[data-testid="stExpander"] {
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }

    /* Sidebar removed from UI */
    section[data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] {
        font-family: 'Montserrat', sans-serif;
        background: linear-gradient(180deg, rgba(6, 24, 44, 0.80), rgba(13, 39, 65, 0.78));
        border-right: 1px solid rgba(255, 255, 255, 0.16);
    }

    section[data-testid="stSidebar"] * {
        color: #e9fbff !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        position: sticky;
        top: 0;
        margin-top: -0.2rem;
        z-index: 20;
        display: flex;
        gap: 0.4rem;
        padding: 0.42rem;
        border-radius: 14px;
        background: rgba(7, 24, 40, 0.60);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }

    .stTabs [data-baseweb="tab-list"]::before {
        display: none;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Exo 2', sans-serif;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.28rem;
        border-radius: 10px;
        border: 1px solid transparent;
        background: rgba(255, 255, 255, 0.03);
        color: #e5f4ff;
        font-weight: 700;
        font-size: 0.94rem;
        min-height: 2.45rem;
        padding: 0.35rem 0.8rem;
        letter-spacing: 0.012em;
        box-shadow: none;
        transition: transform 180ms ease, background-color 180ms ease, border-color 180ms ease, color 180ms ease;
    }

    .stTabs [data-baseweb="tab"]::before {
        font-size: 0.92rem;
        font-weight: 700;
        line-height: 1;
        opacity: 0.9;
    }

    .stTabs [data-baseweb="tab"]:nth-child(1)::before { content: "•"; }
    .stTabs [data-baseweb="tab"]:nth-child(2)::before { content: "•"; }
    .stTabs [data-baseweb="tab"]:nth-child(3)::before { content: "•"; }
    .stTabs [data-baseweb="tab"]:nth-child(4)::before { content: "•"; }
    .stTabs [data-baseweb="tab"]:nth-child(5)::before { content: "•"; }
    .stTabs [data-baseweb="tab"]:nth-child(6)::before { content: "•"; }
    .stTabs [data-baseweb="tab"]:nth-child(7)::before { content: "•"; }

    .stTabs [data-baseweb="tab"]::after {
        display: none;
    }

    .stTabs [aria-selected="true"] {
        border: 1px solid rgba(255, 255, 255, 0.42);
        background: linear-gradient(135deg, rgba(255, 119, 119, 0.82), rgba(72, 192, 176, 0.82));
        color: #ffffff !important;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.28), 0 0 14px rgba(255, 209, 102, 0.30);
        transform: translateY(-1px);
        animation: activeTabPulse 2.2s ease-in-out infinite;
    }

    .stTabs [data-baseweb="tab"]:hover {
        border-color: rgba(255, 255, 255, 0.26);
        background: rgba(255, 255, 255, 0.09);
        transform: translateY(-1px);
    }

    .stTabs [data-baseweb="tab"]:hover::after,
    .stTabs [aria-selected="true"]::after {
        display: none;
    }

    @keyframes activeTabPulse {
        0%, 100% { box-shadow: 0 8px 18px rgba(0, 0, 0, 0.28), 0 0 0 rgba(255, 209, 102, 0.0); }
        50% { box-shadow: 0 10px 22px rgba(0, 0, 0, 0.32), 0 0 16px rgba(255, 209, 102, 0.42); }
    }

    @keyframes tabsSheen {
        0%, 100% { opacity: 0; }
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        font-family: 'Exo 2', sans-serif;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.20);
        border-radius: 12px;
        font-weight: 800;
        letter-spacing: 0.02em;
        color: #ffffff;
        background: linear-gradient(130deg, rgba(255, 107, 107, 0.85), rgba(46, 196, 182, 0.85));
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25);
        transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
    }

    .stButton > button::before,
    .stDownloadButton > button::before {
        content: "";
        position: absolute;
        inset: 0;
        transform: translateX(-120%) skewX(-22deg);
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.36), transparent);
        transition: transform 560ms ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        filter: saturate(1.1);
        box-shadow: 0 12px 22px rgba(0, 0, 0, 0.30);
    }

    .stButton > button:hover::before,
    .stDownloadButton > button:hover::before {
        transform: translateX(120%) skewX(-22deg);
    }

    /* Inputs and data surfaces */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput input,
    .stDataFrame,
    .stPlotlyChart,
    .stMetric {
        background: var(--glass) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 12px !important;
        font-family: 'Manrope', sans-serif !important;
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border-color: rgba(255, 209, 102, 0.7) !important;
        box-shadow: 0 0 0 2px rgba(255, 209, 102, 0.24);
    }

    .stDataFrame, .stPlotlyChart {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.22);
    }

    .stDataFrame:hover, .stPlotlyChart:hover, .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.28);
        border-color: rgba(255, 209, 102, 0.4) !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid var(--border-glow);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
    }

    /* Headings in content area */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-main);
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 0.01em;
    }

    .stMarkdown p, .stMarkdown li, .stMarkdown span, label {
        font-family: 'Sora', sans-serif;
        color: #e6f5ff;
    }

    .stMetric label, .stMetric div {
        font-family: 'JetBrains Mono', monospace !important;
    }

    [data-testid="stFileUploader"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700;
        letter-spacing: 0.01em;
    }

    /* Progressively reveal content blocks */
    div[data-testid="stVerticalBlock"] > div {
        animation: fadeLift 460ms ease both;
    }

    div[data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 70ms; }
    div[data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 120ms; }
    div[data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 170ms; }
    div[data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: 220ms; }

    @keyframes fadeLift {
        0% { opacity: 0; transform: translateY(6px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 768px) {
        .main-title {
            letter-spacing: 0.04em;
        }

        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto;
        }

        .stApp::before,
        .stApp::after {
            opacity: 0.28;
        }

        .stApp::before {
            inset: -40% -35% -35% -35%;
        }

        .stApp::after {
            width: 48vmax;
            height: 48vmax;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        .stApp,
        .stApp::before,
        .stApp::after,
        .main-title,
        .subtitle,
        .stTabs [aria-selected="true"],
        div[data-testid="stVerticalBlock"] > div {
            animation: none !important;
        }

        .stButton > button::before,
        .stDownloadButton > button::before {
            display: none;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'vectorizer' not in st.session_state:
    st.session_state.vectorizer = None
if 'model_metrics' not in st.session_state:
    st.session_state.model_metrics = None
if 'motion_speed' not in st.session_state:
    st.session_state.motion_speed = "Medium"
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "Dark"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'model_algo' not in st.session_state:
    st.session_state.model_algo = "logistic_regression"
if 'model_test_size' not in st.session_state:
    st.session_state.model_test_size = 0.2
if 'model_max_features' not in st.session_state:
    st.session_state.model_max_features = 100

# Top controls (replaces sidebar)
st.markdown("### Control Panel")
ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.1, 1.1, 1.4, 2.0])

with ctrl_col1:
    st.session_state.dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    st.session_state.theme_mode = "Dark" if st.session_state.dark_mode else "Light"

with ctrl_col2:
    st.session_state.motion_speed = st.selectbox(
        "Background Motion",
        ["Slow", "Medium", "Fast"],
        index=["Slow", "Medium", "Fast"].index(st.session_state.motion_speed),
        help="Controls moving background speed."
    )

with ctrl_col3:
    if st.session_state.df is not None:
        st.success(f"Loaded: {len(st.session_state.df)} rows")
    else:
        st.warning("Dataset not loaded")

with ctrl_col4:
    st.write("**Quick Status**")
    status_items = []
    status_items.append("Dataset" if st.session_state.df is not None else "Dataset needed")
    status_items.append("Cleaned" if st.session_state.df_cleaned is not None else "Raw")
    status_items.append("Model ready" if st.session_state.model is not None else "Model not trained")
    st.caption(" • ".join(status_items))

with st.expander("Export & Model Files", expanded=False):
    export_col1, export_col2 = st.columns(2)

    with export_col1:
        if st.session_state.df_processed is not None:
            csv = st.session_state.df_processed.to_csv(index=False)
            st.download_button(
                label="Download Results CSV",
                data=csv,
                file_name="predictions_results.csv",
                mime="text/csv"
            )
        else:
            st.caption("Run processing/prediction to enable CSV export.")

    with export_col2:
        if st.session_state.model is not None:
            model_data = pickle.dumps({
                'model': st.session_state.model,
                'vectorizer': st.session_state.vectorizer
            })

            st.download_button(
                label="Download Trained Model",
                data=model_data,
                file_name="fake_review_model.pkl",
                mime="application/octet-stream"
            )
        else:
            st.caption("Train a model to enable model export.")

st.markdown("---")

# Motion speed overrides for animated background
motion_speed_map = {
    "Slow": {"page": "34s", "aurora": "40s", "orb": "24s"},
    "Medium": {"page": "20s", "aurora": "24s", "orb": "14s"},
    "Fast": {"page": "12s", "aurora": "14s", "orb": "9s"}
}
selected_speed = motion_speed_map.get(st.session_state.motion_speed, motion_speed_map["Medium"])

theme_map = {
    "Dark": {
        "bg_a": "#07142e",
        "bg_b": "#0a4d68",
        "bg_c": "#15aabf",
        "text_main": "#e8f7ff",
        "text_soft": "#bcd4e6",
        "glass": "rgba(255, 255, 255, 0.08)",
        "glass_strong": "rgba(255, 255, 255, 0.14)",
        "border_glow": "rgba(255, 209, 102, 0.35)",
        "content_text": "#e6f5ff",
        "tab_bg": "rgba(7, 24, 40, 0.60)",
        "tab_text": "#e5f4ff"
    },
    "Light": {
        "bg_a": "#f6fbff",
        "bg_b": "#dbeafe",
        "bg_c": "#bfdbfe",
        "text_main": "#0b2a47",
        "text_soft": "#33597a",
        "glass": "rgba(255, 255, 255, 0.72)",
        "glass_strong": "rgba(255, 255, 255, 0.86)",
        "border_glow": "rgba(37, 99, 235, 0.28)",
        "content_text": "#17324d",
        "tab_bg": "rgba(255, 255, 255, 0.74)",
        "tab_text": "#12314f"
    }
}
selected_theme = theme_map.get(st.session_state.theme_mode, theme_map["Dark"])

st.markdown(f"""
<style>
    :root {{
        --bg-a: {selected_theme['bg_a']};
        --bg-b: {selected_theme['bg_b']};
        --bg-c: {selected_theme['bg_c']};
        --text-main: {selected_theme['text_main']};
        --text-soft: {selected_theme['text_soft']};
        --glass: {selected_theme['glass']};
        --glass-strong: {selected_theme['glass_strong']};
        --border-glow: {selected_theme['border_glow']};
        --dur-page: {selected_speed['page']};
        --dur-aurora: {selected_speed['aurora']};
        --dur-orb: {selected_speed['orb']};
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: {selected_theme['tab_bg']} !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: {selected_theme['tab_text']} !important;
    }}

    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span,
    label,
    .stText,
    .stCaption,
    .stSubheader,
    .stHeader {{
        color: {selected_theme['content_text']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Home",
    "Dataset Upload",
    "Data Cleaning",
    "Data Manipulation",
    "Data Analysis",
    "Data Visualization",
    "Fake Review Detection"
])

# ============================================================================
# TAB 1: HOME
# ============================================================================
with tab1:
    st.markdown('<p class="main-title">🛡️ ReviewGuard</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Fake Product Review Detection System</p>', unsafe_allow_html=True)
    st.header("Welcome to ReviewGuard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What This App Does
        ReviewGuard analyzes product reviews and predicts whether they are **genuine** or **fake** using NLP and machine learning.

        ### Quick Workflow
        1. Upload your CSV dataset
        2. Clean and inspect your data
        3. Visualize patterns
        4. Train model and predict fake reviews

        ### Core Features
        - Data cleaning and preprocessing
        - Interactive analysis and charts
        - Fake review prediction with exportable results
        """)
    
    with col2:
        st.markdown("""
        ### ✅ Required Before You Start
        
        This analysis works only with **user-uploaded data**.
        
        **Steps:**
        1. Prepare your CSV file
        2. Go to **Dataset Upload** tab
        3. Upload your CSV file
        4. Follow workflow tabs in order
        5. Download results
        """)
        
        st.warning("""
        **⚠️ IMPORTANT:** 
        All analysis, cleaning, and machine learning 
        operations work on YOUR uploaded dataset. 
        No sample data is auto-loaded.
        """)
        
        st.markdown("""
        ### Dataset Format
        
        Your CSV should contain:
        - `review_text` - The review content
        - `rating` - Product rating
        - `product_id` - Product identifier
        - `review_date` - Date of review
        - `label` - 0/1 or genuine/fake
        """)
    
    st.markdown("---")
    
    st.subheader("Technology Stack")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        **Data Processing**
        - 🐼 Pandas
        - 🔢 NumPy
        """)
    
    with col2:
        st.markdown("""
        **Machine Learning**
        - 🤖 Scikit-learn
        - 📊 Model Selection
        """)
    
    with col3:
        st.markdown("""
        **NLP & Text**
        - 📝 NLTK
        - 🔤 Preprocessing
        """)
    
    with col4:
        st.markdown("""
        **Visualization**
        - 📈 Plotly
        - 🎨 Matplotlib
        """)

# ============================================================================
# TAB 2: DATASET UPLOAD
# ============================================================================
with tab2:
    st.header("📁 Dataset Upload")
    st.markdown("Upload a CSV file containing product reviews to get started.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Option 1: Your Dataset")
        uploaded_df = upload.upload_dataset()
        
        if uploaded_df is not None:
            st.session_state.df = uploaded_df
            st.success("✅ Dataset loaded successfully!")
    
    with col2:
        st.subheader("Dataset Requirements")
        st.markdown("""
        **Your CSV must contain:**
        - `review_text` - Review content
        - `rating` - Product rating (1-5)
        - `label` - 0 (genuine) or 1 (fake)
        
        **Optional columns:**
        - `product_id`
        - `review_date`
        
        **Example:**
        | review_text | rating | label |
        |---|---|---|
        | Great product! | 5 | 0 |
        | Amazing! Worth it! | 5 | 1 |
        | Poor quality | 2 | 0 |
        """)

# ============================================================================
# TAB 3: DATA CLEANING
# ============================================================================
with tab3:
    st.header("🧹 Data Cleaning")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first (Tab 2)")
    else:
        df_working = st.session_state.df.copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Step 1: Handle Missing Values")
            
            if st.checkbox("Check missing values"):
                missing_report = cleaning.check_missing_values(df_working)
            
            if st.checkbox("Fill missing values"):
                fill_method = st.selectbox("Select fill method:", ["mean", "median", "mode"])
                if st.button("Apply filling"):
                    df_working = cleaning.fill_missing_values(df_working, method=fill_method)
        
        with col2:
            st.subheader("Step 2: Remove Duplicates")
            
            if st.checkbox("Remove duplicate rows"):
                if st.button("Remove duplicates"):
                    df_working = cleaning.remove_duplicates(df_working)
        
        st.markdown("---")
        
        st.subheader("Step 3: Text Cleaning")
        
        review_cols = [col for col in df_working.columns if 'review' in col.lower()]
        
        if review_cols:
            text_column = st.selectbox("Select text column:", review_cols)
            
            col1, col2 = st.columns(2)
            with col1:
                remove_stopwords_flag = st.checkbox("Remove stopwords", value=True)
            with col2:
                lemmatize_flag = st.checkbox("Lemmatize text", value=True)
            
            if st.button("Apply text cleaning"):
                df_working = cleaning.apply_text_cleaning(
                    df_working, text_column,
                    remove_stopwords_flag=remove_stopwords_flag,
                    lemmatize=lemmatize_flag
                )
        
        st.markdown("---")
        
        st.subheader("Cleaned Data Preview")
        st.dataframe(df_working.head(10), use_container_width=True)
        
        # Save cleaned data
        if st.button("💾 Save Cleaned Dataset"):
            st.session_state.df_cleaned = df_working
            st.success("✅ Cleaned dataset saved to session!")

# ============================================================================
# TAB 4: DATA MANIPULATION
# ============================================================================
with tab4:
    st.header("🛠️ Data Manipulation")
    
    if st.session_state.df_cleaned is None:
        if st.session_state.df is None:
            st.warning("⚠️ Please upload a dataset first (Tab 2)")
        else:
            st.info("ℹ️ Using original dataset (not cleaned yet)")
            df_working = st.session_state.df.copy()
    else:
        df_working = st.session_state.df_cleaned.copy()
    
    if st.session_state.df is not None or st.session_state.df_cleaned is not None:
        df_manipulated = manipulation.data_manipulation_interface(df_working)
        
        st.markdown("---")
        st.subheader("Manipulated Data Preview")
        st.dataframe(df_manipulated.head(10), use_container_width=True)
        
        # Save manipulated data
        if st.button("💾 Save Manipulated Dataset"):
            st.session_state.df_processed = df_manipulated
            st.success("✅ Manipulated dataset saved!")

# ============================================================================
# TAB 5: DATA ANALYSIS
# ============================================================================
with tab5:
    st.header("📊 Data Analysis")
    
    if st.session_state.df is None:
        st.error("🚫 DATA UPLOAD REQUIRED")
        st.markdown("""
        ### Please upload your dataset first!
        
        This tab performs cleaning operations on **your uploaded data**.
        
        **To proceed:**
        1. Go to the **📁 Dataset Upload** tab
        2. Upload your CSV file with product reviews
        3. Return to this tab to clean your data
        
        **Required columns in your CSV:**
        - `review_text` - The review content
        - `rating` - Product rating
        - `label` - 0 (genuine) or 1 (fake)
        """)
        st.stop()
    else:
        df_working = st.session_state.df_cleaned if st.session_state.df_cleaned is not None else st.session_state.df
        
        analysis.analysis_interface(df_working)

# ============================================================================
# TAB 6: DATA VISUALIZATION
# ============================================================================
with tab6:
    st.header("📈 Data Visualization")
    
    if st.session_state.df is None:
        st.error("🚫 DATA UPLOAD REQUIRED")
        st.markdown("""
        ### Please upload your dataset first!
        
        This tab performs visualization on **your uploaded data**.
        
        **To proceed:**
        1. Go to the **📁 Dataset Upload** tab
        2. Upload your CSV file with product reviews
        3. Return to this tab to visualize your data
        
        **Required columns in your CSV:**
        - `review_text` - The review content
        - `rating` - Product rating
        - `label` - 0 (genuine) or 1 (fake)
        """)
        st.stop()
    else:
        df_working = st.session_state.df_cleaned if st.session_state.df_cleaned is not None else st.session_state.df
        
        visualization.visualization_interface(df_working)

# ============================================================================
# TAB 7: FAKE REVIEW DETECTION
# ============================================================================
with tab7:
    st.header("🤖 Fake Review Detection")
    
    if st.session_state.df is None:
        st.error("🚫 DATA UPLOAD REQUIRED")
        st.markdown("""
        ### Please upload your dataset first!
        
        This tab performs analysis and visualization on **your uploaded data**.
        
        **To proceed:**
        1. Go to the **📁 Dataset Upload** tab
        2. Upload your CSV file with product reviews
        3. Return to this tab to visualize your data
        
        **Required columns in your CSV:**
        - `review_text` - The review content
        - `rating` - Product rating
        - `label` - 0 (genuine) or 1 (fake)
        """)
        st.stop()
    else:
        df_working = st.session_state.df_cleaned if st.session_state.df_cleaned is not None else st.session_state.df
        
        st.subheader("Machine Learning Workflow")
        
        # Check for required columns
        label_cols = [col for col in df_working.columns if 'label' in col.lower() or 'fake' in col.lower()]
        review_cols = [col for col in df_working.columns if 'review' in col.lower()]
        
        if not label_cols or not review_cols:
            st.error("⚠️ Dataset must contain 'label' and 'review_text' columns for model training")
        else:
            label_col = label_cols[0]
            text_col = review_cols[0]

            st.subheader("Model Configuration")
            cfg_col1, cfg_col2, cfg_col3 = st.columns(3)

            with cfg_col1:
                algorithm = st.selectbox(
                    "Select algorithm:",
                    ["logistic_regression", "naive_bayes", "random_forest"],
                    index=["logistic_regression", "naive_bayes", "random_forest"].index(st.session_state.model_algo)
                )
                st.session_state.model_algo = algorithm

            with cfg_col2:
                test_size = st.slider("Test set size:", 0.1, 0.5, float(st.session_state.model_test_size), step=0.05)
                st.session_state.model_test_size = test_size

            with cfg_col3:
                max_features = st.slider("Max TF-IDF features:", 50, 500, int(st.session_state.model_max_features), step=10)
                st.session_state.model_max_features = max_features
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Step 1️⃣: Preprocessing")
                st.write("Text preprocessing and feature extraction...")
                
                if st.button("Start Preprocessing"):
                    with st.spinner("Preprocessing in progress..."):
                        preprocessing.download_nltk_resources()
                        
                        # Create a copy for preprocessing
                        df_train = df_working.copy()
                        
                        # Preprocess text
                        df_train[text_col] = df_train[text_col].apply(
                            preprocessing.preprocess_text
                        )
                        
                        # Extract features
                        X_features, tfidf_matrix, feature_cols = feature_extraction.prepare_features_for_model(
                            df_train, text_col, max_features=max_features
                        )
                        
                        st.session_state.X_features = X_features
                        st.session_state.tfidf_matrix = tfidf_matrix
                        st.session_state.feature_cols = feature_cols
                        st.session_state.y_labels = df_train[label_col].values
                        st.session_state.df_train = df_train
                        
                        st.success("✅ Preprocessing completed!")
                        st.info(f"Features extracted: {len(feature_cols)} features")
            
            with col2:
                st.subheader("Step 2️⃣: Model Training")
                st.write("Train and evaluate the model...")
                
                if st.button("Train Model"):
                    if not hasattr(st.session_state, 'X_features'):
                        st.error("❌ Please complete preprocessing first!")
                    else:
                        with st.spinner("Training model..."):
                            # Split data
                            from sklearn.model_selection import train_test_split
                            
                            X_train, X_test, y_train, y_test = train_test_split(
                                st.session_state.X_features,
                                st.session_state.y_labels,
                                test_size=test_size,
                                random_state=42
                            )
                            
                            # Train model
                            model, metrics, predictions = model_training.train_and_evaluate(
                                X_train, X_test, y_train, y_test, algorithm=algorithm
                            )
                            
                            st.session_state.model = model
                            st.session_state.model_metrics = metrics
                            st.session_state.X_test = X_test
                            st.session_state.y_test = y_test
                            
                            st.success("✅ Model trained successfully!")
            
            st.markdown("---")
            
            # Display metrics
            if st.session_state.model is not None and st.session_state.model_metrics is not None:
                st.subheader("Step 3️⃣: Model Evaluation")
                
                model_training.display_metrics(st.session_state.model_metrics)
                
                st.markdown("---")
                
                # Make predictions
                st.subheader("Step 4️⃣: Make Predictions")
                
                if st.button("Generate Predictions"):
                    with st.spinner("Generating predictions..."):
                        # Make predictions on all data
                        df_predictions = st.session_state.df_train.copy()
                        
                        predictions_values, probabilities = prediction.predict_batch(
                            st.session_state.model,
                            st.session_state.X_features
                        )
                        
                        df_predictions['prediction'] = predictions_values
                        
                        if probabilities is not None:
                            df_predictions['prediction_confidence'] = np.max(probabilities, axis=1)
                        
                        st.session_state.df_processed = df_predictions
                        
                        st.success("✅ Predictions completed!")
                        
                        # Display prediction report
                        report = prediction.generate_prediction_report(df_predictions)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Reviews", report['total_reviews'])
                        with col2:
                            st.metric("Fake Reviews", report['fake_reviews'])
                        with col3:
                            st.metric("Genuine Reviews", report['genuine_reviews'])
                        
                        st.write("**Prediction Results Preview:**")
                        display_cols = [col for col in df_predictions.columns 
                                      if col in ['review_text', 'rating', 'prediction', 'prediction_confidence']]
                        st.dataframe(df_predictions[display_cols].head(20), use_container_width=True)
                
                st.markdown("---")
                
                # Single review prediction
                st.subheader("⭐ Predict Single Review")
                
                single_review = st.text_area("Enter a product review:")
                
                if st.button("Predict Review"):
                    if single_review.strip():
                        # Preprocess the review
                        processed_review = preprocessing.preprocess_text(single_review)
                        
                        # Create TF-IDF features
                        if hasattr(st.session_state, 'tfidf_matrix'):
                            # For single prediction, we need to fit a new vectorizer on current text
                            from sklearn.feature_extraction.text import TfidfVectorizer
                            
                            # Get all training texts for vectorizer
                            all_texts = st.session_state.df_train[text_col].values
                            temp_vectorizer = TfidfVectorizer(
                                max_features=max_features,
                                ngram_range=(1, 2),
                                min_df=2,
                                max_df=0.9
                            )
                            temp_vectorizer.fit(all_texts)
                            
                            # Transform the single review
                            review_features = temp_vectorizer.transform([processed_review])
                            
                            # Predict
                            pred = st.session_state.model.predict(review_features)[0]
                            
                            try:
                                prob = st.session_state.model.predict_proba(review_features)[0]
                                confidence = np.max(prob)
                            except:
                                confidence = None
                            
                            result = "🚨 FAKE REVIEW" if pred == 1 else "✅ GENUINE REVIEW"
                            
                            st.success(result)
                            if confidence:
                                st.metric("Confidence", f"{confidence:.2%}")
                    else:
                        st.warning("Please enter a review text!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📦 Version")
    st.text("ReviewGuard v1.0")

with col2:
    st.markdown("### 📧 Support")
    st.text("For issues or feedback, contact support")

with col3:
    st.markdown("### 📜 License")
    st.text("Open Source License")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 ReviewGuard - Fake Product Review Detection System</p>", 
            unsafe_allow_html=True)
