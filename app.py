import streamlit as st
import joblib
import re
import docx
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import io
from PIL import Image
import base64

# Page configuration
st.set_page_config(
    page_title="🎯 HR Smart Recruiter Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 4s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        margin-bottom: 2rem;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .hero-feature {
        background: rgba(255,255,255,0.15);
        padding: 1rem 1.5rem;
        border-radius: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 500;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        color: #667eea;
        margin: 1rem 0;
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    .metric-change {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .section-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 3rem 0 2rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    .upload-area {
        background: linear-gradient(135deg, #f8faff 0%, #e8ecff 100%);
        border: 3px dashed #667eea;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .upload-area::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        animation: pulse 3s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .upload-area:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #e8ecff 0%, #d1d9ff 100%);
        transform: translateY(-5px);
    }
    
    .upload-icon {
        font-size: 4rem;
        color: #667eea;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .upload-text {
        font-size: 1.3rem;
        color: #475569;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    .upload-subtext {
        font-size: 1rem;
        color: #64748b;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .cv-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .cv-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    .cv-card:hover {
        transform: translateX(10px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
    }
    
    .cv-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .category-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .confidence-bar {
        background: linear-gradient(90deg, #e2e8f0, #cbd5e1);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: width 1s ease;
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #f8faff 0%, #e8ecff 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
    }
    
    .feature-item {
        padding: 0.8rem 0;
        color: #475569;
        font-weight: 500;
        border-bottom: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-item:last-child {
        border-bottom: none;
    }
    
    .feature-item::before {
        content: '✦';
        color: #667eea;
        font-weight: bold;
        margin-right: 0.8rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .analysis-section {
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-processing {
        background: rgba(251, 191, 36, 0.1);
        color: #d97706;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }
    
    .status-complete {
        background: rgba(34, 197, 94, 0.1);
        color: #16a34a;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.1);
        color: #dc2626;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .progress-container {
        background: #f1f5f9;
        border-radius: 50px;
        height: 12px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 50px;
        transition: width 0.5s ease;
    }
    
    .keyword-tag {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.2rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .chart-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin: 1rem 0;
    }
    
    .info-card {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #1e40af;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #92400e;
    }
    
    .success-card {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #065f46;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_cvs' not in st.session_state:
    st.session_state.processed_cvs = []
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Mock model loading (replace with actual model loading)
@st.cache_resource
def load_models():
    """Load pre-trained models"""
    try:
        # Mock models for demonstration - replace with actual loading
        class MockModel:
            def predict(self, X):
                categories = ['Data Science', 'Software Engineering', 'DevOps', 'Product Management', 
                            'Business Analysis', 'Digital Marketing', 'UI/UX Design', 'Quality Assurance']
                return [np.random.choice(categories)]
            
            def predict_proba(self, X):
                return [[np.random.random() for _ in range(8)]]
        
        class MockVectorizer:
            def transform(self, texts):
                return texts  # Mock transformation
        
        class MockEncoder:
            def inverse_transform(self, encoded):
                return encoded
        
        return MockModel(), MockVectorizer(), MockEncoder()
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

# Text cleaning function
def clean_text(text):
    """Clean and preprocess text"""
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'RT|cc', ' ', text)
    text = re.sub(r'#\S+', '', text)
    text = re.sub(r'@\S+', ' ', text)
    text = re.sub(r'[^\x00-\x7f]', r' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# File extraction functions
def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        return " ".join([p.text for p in doc.paragraphs])
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""

# Load models
model, vectorizer, encoder = load_models()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">🎯 HR Smart Recruiter Pro</div>
        <p style="color: #64748b; margin-bottom: 2rem;">Advanced AI-Powered Recruitment Platform</p>
        
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
            <h4 style="margin: 0 0 1rem 0;">🚀 Platform Features</h4>
            <ul class="feature-list" style="margin: 0; color: white;">
                <li class="feature-item" style="color: white; border-color: rgba(255,255,255,0.2);">Multi-format CV parsing</li>
                <li class="feature-item" style="color: white; border-color: rgba(255,255,255,0.2);">AI-powered categorization</li>
                <li class="feature-item" style="color: white; border-color: rgba(255,255,255,0.2);">Advanced analytics dashboard</li>
                <li class="feature-item" style="color: white; border-color: rgba(255,255,255,0.2);">Intelligent keyword search</li>
                <li class="feature-item" style="color: white; border-color: rgba(255,255,255,0.2);">Bulk processing capabilities</li>
                <li class="feature-item" style="color: white; border-color: rgba(255,255,255,0.2);">Export & reporting tools</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # System stats
    st.markdown("### 📊 System Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("CVs Processed", "12,847", "↗️ +234")
    with col2:
        st.metric("Active Users", "1,456", "↗️ +89")
    
    st.metric("Accuracy Rate", "94.7%", "↗️ +2.1%")
    st.metric("Processing Speed", "< 2s", "↗️ 15%")
    
    # Support information
    st.markdown("""
    <div class="info-card">
        <h4 style="margin: 0 0 0.5rem 0;">💡 Need Help?</h4>
        <p style="margin: 0; font-size: 0.9rem;">Contact our support team for assistance with bulk processing, custom integrations, or technical issues.</p>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">🎯 HR Smart Recruiter Pro</h1>
    <p class="hero-subtitle">Transform Your Recruitment Process with Advanced AI Technology</p>
    <div class="hero-features">
        <div class="hero-feature">📄 Multi-Format Support</div>
        <div class="hero-feature">🧠 AI Classification</div>
        <div class="hero-feature">📊 Advanced Analytics</div>
        <div class="hero-feature">⚡ Lightning Fast</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📁 CV Upload & Analysis",
    "📊 Analytics Dashboard", 
    "🔍 Advanced Search",
    "📈 Reporting & Insights",
    "⚙️ Settings & Tools"
])

# Tab 1: CV Upload & Analysis
with tab1:
    st.markdown('<h2 class="section-header">📁 CV Upload & Processing Center</h2>', unsafe_allow_html=True)
    
    # Upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="upload-area">
            <div class="upload-icon">📁</div>
            <div class="upload-text">Drop your CV files here</div>
            <div class="upload-subtext">Supports PDF, DOCX formats • Multiple files allowed • Max 200MB per file</div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Choose CV files",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            help="Upload multiple CV files for batch processing"
        )
    
    with col2:
        st.markdown("### 🎯 Processing Options")
        
        processing_mode = st.radio(
            "Select Processing Mode:",
            ["Quick Analysis", "Detailed Analysis", "Advanced Insights"]
        )
        
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.5,
            max_value=1.0,
            value=0.8,
            step=0.05,
            help="Minimum confidence level for category classification"
        )
        
        enable_keywords = st.checkbox("Extract Keywords", value=True)
        enable_skills = st.checkbox("Identify Skills", value=True)
        enable_experience = st.checkbox("Analyze Experience", value=True)

    if uploaded_files:
        st.markdown("---")
        st.markdown('<h3 class="section-header" style="font-size: 2rem; margin: 2rem 0 1rem 0;">🔄 Processing Results</h3>', unsafe_allow_html=True)
        
        # Process files
        results = []
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                progress_bar.progress((i + 1) / len(uploaded_files))
                
                # Extract text based on file type
                if file.type == "application/pdf":
                    text = extract_text_from_pdf(file)
                else:
                    text = extract_text_from_docx(file)
                
                if text.strip():
                    cleaned = clean_text(text)
                    
                    # Mock prediction (replace with actual model prediction)
                    if model:
                        vectorized = vectorizer.transform([cleaned])
                        prediction = model.predict(vectorized)
                        probabilities = model.predict_proba(vectorized)
                        confidence = np.max(probabilities)
                        category = prediction[0]
                    else:
                        category = "Software Engineering"
                        confidence = 0.85
                    
                    # Extract basic information
                    word_count = len(text.split())
                    char_count = len(text)
                    
                    results.append({
                        "File": file.name,
                        "Category": category,
                        "Confidence": confidence,
                        "Content": cleaned,
                        "Word_Count": word_count,
                        "Char_Count": char_count,
                        "Status": "Processed"
                    })
                else:
                    results.append({
                        "File": file.name,
                        "Category": "Error",
                        "Confidence": 0.0,
                        "Content": "",
                        "Word_Count": 0,
                        "Char_Count": 0,
                        "Status": "Failed"
                    })
                
                time.sleep(0.1)  # Simulate processing time
            
            status_text.text("✅ Processing Complete!")
            st.session_state.processed_cvs = results
        
        # Display results
        if results:
            df = pd.DataFrame(results)
            successful_results = df[df['Status'] == 'Processed']
            
            # Summary metrics
            st.markdown("### 📊 Processing Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(df)}</div>
                    <div class="metric-label">Total CVs</div>
                    <div class="metric-change" style="color: #10b981;">✅ Uploaded</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(successful_results)}</div>
                    <div class="metric-label">Successfully Processed</div>
                    <div class="metric-change" style="color: #10b981;">✅ Complete</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg_confidence = successful_results['Confidence'].mean() if not successful_results.empty else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_confidence:.1%}</div>
                    <div class="metric-label">Avg Confidence</div>
                    <div class="metric-change" style="color: #3b82f6;">📊 Accuracy</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                unique_categories = successful_results['Category'].nunique() if not successful_results.empty else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{unique_categories}</div>
                    <div class="metric-label">Categories Found</div>
                    <div class="metric-change" style="color: #8b5cf6;">🎯 Diversity</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed results
            st.markdown("### 📋 Detailed Analysis Results")
            
            for idx, row in successful_results.iterrows():
                with st.expander(f"📄 {row['File']} • {row['Category']} • {row['Confidence']:.1%} confidence"):
                    col_a, col_b = st.columns([2, 1])
                    
                    with col_a:
                        st.markdown(f"""
                        <div class="cv-card">
                            <div class="cv-title">
                                📄 {row['File']}
                                <span class="category-badge">{row['Category']}</span>
                            </div>
                            <div style="margin: 1rem 0;">
                                <strong>Confidence Level:</strong>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {row['Confidence']*100}%;"></div>
                                </div>
                                {row['Confidence']:.1%}
                            </div>
                            <div style="margin: 1rem 0;">
                                <strong>Content Preview:</strong><br>
                                <div style="background: #f8faff; color: #1e293b; padding: 1rem; border-radius: 10px; margin-top: 0.5rem; max-height: 200px; overflow-y: auto;">
                                    {row['Content'][:500]}{"..." if len(row['Content']) > 500 else ""}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        st.markdown("#### 📊 Document Stats")
                        st.metric("Word Count", f"{row['Word_Count']:,}")
                        st.metric("Character Count", f"{row['Char_Count']:,}")
                        
                        if enable_keywords:
                            # Mock keyword extraction
                            keywords = ["Python", "Machine Learning", "Data Analysis", "SQL", "React"]
                            st.markdown("#### 🔑 Key Skills")
                        for keyword in keywords:
                                st.markdown(f"<span class='keyword-tag'>{keyword}</span>", unsafe_allow_html=True)

                        if enable_experience:
                            st.markdown("#### 🧑‍💼 Experience Analysis")
                            st.info("Experience extraction model not integrated yet.")

                        if enable_skills:
                            st.markdown("#### 🛠️ Skills Analysis")
                            st.info("Skills extraction model not integrated yet.")

# Tab 2: Analytics Dashboard
with tab2:
    st.markdown('<h2 class="section-header">📊 Analytics Dashboard</h2>', unsafe_allow_html=True)
    if st.session_state.processed_cvs:
        df = pd.DataFrame(st.session_state.processed_cvs)
        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(df[df['Status'] == 'Processed'], x="Category", title="CVs by Category")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.scatter(df[df['Status'] == 'Processed'], x="Word_Count", y="Confidence", color="Category",
                             title="Confidence vs Word Count")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🔑 Keyword Cloud (Demo)")
        text_all = " ".join(df[df['Status'] == 'Processed']['Content'])
        if text_all.strip():
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_all)
            st.image(wordcloud.to_array(), use_container_width=True)
    else:
        st.warning("No processed CVs available. Please upload files in Tab 1.")

# Tab 3: Advanced Search
with tab3:
    st.markdown('<h2 class="section-header">🔍 Advanced Candidate Search</h2>', unsafe_allow_html=True)
    if st.session_state.processed_cvs:
        df = pd.DataFrame(st.session_state.processed_cvs)
        search_query = st.text_input("Enter a keyword or skill to search:")
        if search_query:
            results = df[df['Content'].str.contains(search_query, case=False, na=False)]
            if not results.empty:
                st.success(f"Found {len(results)} matching CV(s).")
                st.dataframe(results[["File", "Category", "Confidence", "Word_Count"]])
            else:
                st.error("No matching candidates found.")
    else:
        st.warning("No CV data available for searching. Please process CVs in Tab 1.")

# Tab 4: Reporting & Insights
with tab4:
    st.markdown('<h2 class="section-header">📈 Reporting & Insights</h2>', unsafe_allow_html=True)
    if st.session_state.processed_cvs:
        df = pd.DataFrame(st.session_state.processed_cvs)
        st.download_button(
            label="📥 Download Processed Results (CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"processed_cvs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        st.markdown("### 📊 Confidence Distribution")
        fig = px.histogram(df[df['Status'] == 'Processed'], x="Confidence", nbins=20)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No processed CVs to generate reports.")

# Tab 5: Settings & Tools
with tab5:
    st.markdown('<h2 class="section-header">⚙️ Settings & Tools</h2>', unsafe_allow_html=True)

    st.markdown("### 🎨 Theme Settings")
    theme = st.radio("Select Theme:", ["Light", "Dark", "Corporate"])

    st.markdown("### ⚡ System Utilities")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Clear Session State"):
            st.session_state.processed_cvs = []
            st.session_state.analysis_complete = False
            st.success("Session state cleared.")

    with col2:
        if st.button("Refresh Dashboard"):
            st.experimental_rerun()

    st.markdown("### ℹ️ About")
    st.info("HR Smart Recruiter Pro is an AI-powered recruitment platform designed to streamline CV analysis and candidate selection.")
