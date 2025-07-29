import streamlit as st
import base64
from datetime import datetime
import json
import uuid

# Page config
st.set_page_config(
    page_title="OCT Analysis System",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-area {
        border: 2px dashed #3b82f6;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8fafc;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .confidence-high { color: #10b981; }
    .confidence-medium { color: #f59e0b; }
    .confidence-low { color: #ef4444; }
    .cnv-detected { background: #fef2f2; border-left: 4px solid #ef4444; }
    .normal-result { background: #f0fdf4; border-left: 4px solid #10b981; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>👁️ OCT Analysis System</h1>
        <p>AI-Powered CNV Detection System</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### เข้าสู่ระบบ")
        username = st.text_input("Username", placeholder="doctor")
        password = st.text_input("Password", type="password", placeholder="123456")
        
        if st.button("เข้าสู่ระบบ", use_container_width=True):
            if username == "doctor" and password == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials. Use username: doctor, password: 123456")
        
        st.info("Demo: username: **doctor**, password: **123456**")

def analyze_image(image_data):
    """Simulate AI analysis"""
    import random
    import time
    
    # Simulate processing time
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f'Analyzing... {i+1}%')
        time.sleep(0.02)
    
    # Generate random results
    confidence = 70 + random.random() * 30
    has_detection = random.random() > 0.3
    
    diseases = [
        'Choroidal Neovascularization (CNV)',
        'Diabetic Macular Edema',
        'Age-related Macular Degeneration',
        'Macular Hole',
        'Epiretinal Membrane'
    ]
    
    detected_disease = diseases[random.randint(0, len(diseases)-1)] if has_detection else None
    
    result = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.now(),
        'has_detection': has_detection,
        'confidence': confidence,
        'detected_disease': detected_disease,
        'risk_level': 'High Risk' if (has_detection and confidence > 85) else 'Medium Risk' if has_detection else 'Low Risk',
        'image_data': image_data
    }
    
    progress_bar.empty()
    status_text.empty()
    
    return result

def dashboard_page():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard</h1>
        <p>ภาพรวมการวิเคราะห์และสถิติ</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    total_analyses = len(st.session_state.analysis_history)
    cnv_detected = sum(1 for a in st.session_state.analysis_history if a.get('has_detection', False))
    normal_results = total_analyses - cnv_detected
    avg_confidence = sum(a.get('confidence', 0) for a in st.session_state.analysis_history) / max(total_analyses, 1)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Analyses", total_analyses, delta=None)
    with col2:
        st.metric("CNV Detected", cnv_detected, delta=None)
    with col3:
        st.metric("Normal Results", normal_results, delta=None)
    with col4:
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%", delta=None)
    
    # Recent analyses
    st.markdown("### Recent Analyses")
    if st.session_state.analysis_history:
        for analysis in st.session_state.analysis_history[:5]:
            result_class = "cnv-detected" if analysis.get('has_detection') else "normal-result"
            st.markdown(f"""
            <div class="result-card {result_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>Analysis {analysis['id'][:8]}</strong><br>
                        <small>{analysis['timestamp'].strftime('%Y-%m-%d %H:%M')}</small>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-weight: bold;">
                            {'⚠️ CNV Detected' if analysis.get('has_detection') else '✅ Normal'}
                        </span><br>
                        <small>{analysis.get('confidence', 0):.1f}% confidence</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No analyses yet. Start by uploading an OCT image.")

def upload_page():
    st.markdown("""
    <div class="main-header">
        <h1>📁 Upload OCT Image</h1>
        <p>Upload your OCT B-Scan image for AI analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an OCT image file",
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        help="Upload OCT B-Scan images in common formats"
    )
    
    if uploaded_file is not None:
        # Display image
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded OCT Image", use_column_width=True)
        
        with col2:
            st.markdown("### Image Information")
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size} bytes")
            st.write(f"**Type:** {uploaded_file.type}")
        
        if st.button("🔍 Start Analysis", use_container_width=True, type="primary"):
            # Convert image to base64 for storage
            image_data = base64.b64encode(uploaded_file.read()).decode()
            
            # Analyze image
            with st.spinner("Analyzing image..."):
                result = analyze_image(image_data)
                st.session_state.current_analysis = result
                st.session_state.analysis_history.insert(0, result)
            
            # Show results
            show_results(result)

def show_results(result):
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Main result
    if result['has_detection']:
        st.markdown(f"""
        <div class="result-card cnv-detected">
            <h3>⚠️ CNV DETECTED</h3>
            <p><strong>Disease:</strong> {result['detected_disease']}</p>
            <p><strong>Risk Level:</strong> {result['risk_level']}</p>
            <p><strong>Confidence:</strong> {result['confidence']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-card normal-result">
            <h3>✅ NORMAL RESULT</h3>
            <p><strong>Status:</strong> No abnormalities detected</p>
            <p><strong>Risk Level:</strong> {result['risk_level']}</p>
            <p><strong>Confidence:</strong> {result['confidence']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Confidence visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Confidence Score")
        confidence_class = "confidence-high" if result['confidence'] > 90 else "confidence-medium" if result['confidence'] > 70 else "confidence-low"
        st.markdown(f"<h2 class='{confidence_class}'>{result['confidence']:.1f}%</h2>", unsafe_allow_html=True)
        
        # Progress bar
        st.progress(result['confidence'] / 100)
    
    with col2:
        st.markdown("### Recommendations")
        if result['has_detection']:
            if result['confidence'] > 85:
                st.error("🚨 Urgent referral to retina specialist recommended")
            st.warning("💉 Anti-VEGF injection may be indicated")
            st.info("📊 Report generated for physician review")
        else:
            st.success("✅ Continue routine eye examinations")
    
    # Download report button
    if st.button("📄 Download Report", use_container_width=True):
        report_data = generate_report(result)
        st.download_button(
            label="Download Analysis Report",
            data=report_data,
            file_name=f"OCT_Analysis_Report_{result['id'][:8]}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

def generate_report(result):
    report = f"""
OCT ANALYSIS REPORT
==================

Analysis ID: {result['id']}
Analysis Date: {result['timestamp'].strftime('%Y-%m-%d')}
Analysis Time: {result['timestamp'].strftime('%H:%M:%S')}

ANALYSIS RESULTS:
- Status: {'CNV DETECTED' if result['has_detection'] else 'NORMAL'}
- Confidence: {result['confidence']:.1f}%
- Risk Level: {result['risk_level']}
{f"- Detected Disease: {result['detected_disease']}" if result.get('detected_disease') else ''}

SUMMARY:
{result['detected_disease'] + ' detected' if result['has_detection'] else 'No abnormalities detected'} with {result['confidence']:.1f}% confidence.

RECOMMENDATIONS:
{('- Urgent referral to retina specialist' if result['confidence'] > 85 else '- Further evaluation recommended') if result['has_detection'] else '- Continue routine examinations'}

Generated by OCT Analysis System
    """.strip()
    
    return report

def history_page():
    st.markdown("""
    <div class="main-header">
        <h1>📋 Patient History</h1>
        <p>ประวัติการวิเคราะห์ทั้งหมด</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.analysis_history:
        st.info("No analysis history found. Start analyzing OCT images to see history here.")
        return
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        filter_option = st.selectbox(
            "Filter by Result",
            ["All Results", "CNV Detected", "Normal"]
        )
    
    with col2:
        sort_option = st.selectbox(
            "Sort by",
            ["Newest First", "Oldest First", "Highest Confidence"]
        )
    
    with col3:
        if st.button("🗑️ Clear History"):
            st.session_state.analysis_history = []
            st.rerun()
    
    # Apply filters
    filtered_history = st.session_state.analysis_history.copy()
    
    if filter_option == "CNV Detected":
        filtered_history = [a for a in filtered_history if a.get('has_detection', False)]
    elif filter_option == "Normal":
        filtered_history = [a for a in filtered_history if not a.get('has_detection', False)]
    
    # Apply sorting
    if sort_option == "Oldest First":
        filtered_history.reverse()
    elif sort_option == "Highest Confidence":
        filtered_history.sort(key=lambda x: x.get('confidence', 0), reverse=True)
    
    # Display history
    for analysis in filtered_history:
        result_class = "cnv-detected" if analysis.get('has_detection') else "normal-result"
        st.markdown(f"""
        <div class="result-card {result_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>Analysis {analysis['id'][:8]}</strong><br>
                    <small>{analysis['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small><br>
                    {f"<small><strong>Disease:</strong> {analysis.get('detected_disease', 'N/A')}</small>" if analysis.get('has_detection') else ''}
                </div>
                <div style="text-align: right;">
                    <span style="font-weight: bold;">
                        {'⚠️ CNV Detected' if analysis.get('has_detection') else '✅ Normal'}
                    </span><br>
                    <small>{analysis.get('confidence', 0):.1f}% confidence</small><br>
                    <small><strong>Risk:</strong> {analysis.get('risk_level', 'N/A')}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "Choose a page:",
            ["📊 Dashboard", "📁 Upload", "📋 History", "🚪 Logout"]
        )
        
        if page == "🚪 Logout":
            st.session_state.logged_in = False
            st.rerun()
    
    # Main content
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "📁 Upload":
        upload_page()
    elif page == "📋 History":
        history_page()

if __name__ == "__main__":
    main()
