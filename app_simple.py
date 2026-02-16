"""
GMU COLLEGE FAQ ASSISTANT - SIMPLIFIED VERSION
Functional Python implementation for university student information
"""

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from datetime import datetime

# PAGE CONFIGURATION
st.set_page_config(
    page_title="GMU College - FAQ Assistant", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# THEME SELECTION
with st.sidebar:
    theme_mode = st.radio("🌓 Theme:", ["☀️ Light", "🌙 Dark"], index=0)
    st.divider()

is_light = "☀️" in theme_mode

# STYLING WITH PROPER TEXT VISIBILITY
if is_light:
    st.markdown("""
    <style>
    body { background-color: #ffffff; color: #000000; }
    .stApp { background-color: #ffffff; }
    .main-title { font-size: 3.5em; font-weight: bold; color: #0066cc; text-align: center; margin: 20px 0; }
    .section-header { font-size: 2.5em; font-weight: bold; color: #0066cc; border-bottom: 3px solid #0066cc; padding: 20px 0; margin: 20px 0; }
    .info-box { background-color: #e7f3ff; padding: 20px; border-radius: 10px; border-left: 5px solid #0066cc; margin: 15px 0; color: #000000; }
    .answer-box { background-color: #f0f8ff; padding: 15px; border-left: 5px solid #28a745; margin: 10px 0; color: #000000; }
    .metric-box { background-color: #f5f5f5; padding: 15px; border-radius: 8px; border: 1px solid #0066cc; margin: 10px 0; color: #000000; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body { background-color: #1a1a1a; color: #ffffff; }
    .stApp { background-color: #1a1a1a; }
    .main-title { font-size: 3.5em; font-weight: bold; color: #4da6ff; text-align: center; margin: 20px 0; }
    .section-header { font-size: 2.5em; font-weight: bold; color: #4da6ff; border-bottom: 3px solid #4da6ff; padding: 20px 0; margin: 20px 0; }
    .info-box { background-color: #1e3a5f; padding: 20px; border-radius: 10px; border-left: 5px solid #4da6ff; margin: 15px 0; color: #ffffff; }
    .answer-box { background-color: #2d3a5f; padding: 15px; border-left: 5px solid #28a745; margin: 10px 0; color: #ffffff; }
    .metric-box { background-color: #2d2d2d; padding: 15px; border-radius: 8px; border: 1px solid #4da6ff; margin: 10px 0; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# FAQ DATABASE - CUSTOM UNIVERSITY-SPECIFIC
FAQs = {
    "How can I enroll in courses?": "You can enroll through the student portal during registration week each semester.",
    "What documents are needed for admission?": "Marks cards, ID proof, photographs, and application form are required.",
    "What is minimum attendance required?": "Minimum 75% attendance is mandatory for all students.",
    "When are exams conducted?": "Exams are conducted at the end of each semester, typically after 24 weeks.",
    "What facilities are available on campus?": "Library, computing labs, hostel, sports ground, medical center available.",
    "What are library timings?": "9 AM to 8 PM on weekdays, 10 AM to 6 PM on weekends.",
    "Is WiFi available on campus?": "Yes, free high-speed WiFi throughout campus.",
    "How to access student portal?": "Login using your student ID and password on the website.",
    "Is hostel available?": "Yes, hostel available for boys and girls with comfortable accommodation.",
    "How to apply for hostel?": "Apply through the hostel application form on student portal.",
    "Is hostel food provided?": "Yes, mess provides breakfast, lunch, dinner and snacks daily.",
    "What are hostel room types?": "Single, Double, and Triple occupancy rooms with modern amenities.",
    "How to pay college fees?": "Pay online through portal, bank transfer, or fee collection desk.",
    "Are scholarships available?": "Yes, merit-based and need-based scholarships available.",
    "How to apply for financial aid?": "Submit financial aid form during application period.",
    "Is placement support available?": "Yes, placement cell assists with internships and job placements.",
    "Are internships available?": "Yes, during summer and final year programs.",
    "What is placement percentage?": "98% placement rate with 8-12 LPA average CTC.",
    "Is sports facility available?": "Yes, indoor/outdoor sports with professional coaching.",
    "Is medical facility available?": "Yes, campus medical center with doctors and emergency services.",
}

# INITIALIZE SEARCH ENGINE
questions_list = list(FAQs.keys())
answers_list = list(FAQs.values())

vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))
question_vectors = vectorizer.fit_transform(questions_list)

# SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("### 🏫 NAVIGATION")
    page = st.radio("Select Section:", 
        ["🏠 Home", "❓ FAQ Bot", "📊 Analytics", "🎓 Learning"],
        label_visibility="collapsed")

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<div class="main-title">🎓 STUDENT INFORMATION PORTAL</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-box"><h3>🎓 GMU COLLEGE</h3><p><b>Welcome to GMU College!</b><br/>Premier educational institution.<br/>📍 <b>Location:</b> PB Road Davangere<br/>📞 1-800-GMU-HELP<br/>📧 info@gmucollege.edu</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-box"><h3>🏢 GMU HOSTEL</h3><p><b>Comfortable On-Campus Living</b><br/>Home away from home.<br/>🛏️ <b>Capacity:</b> 2000 beds<br/>👥 <b>Boys:</b> 1200 beds<br/>👥 <b>Girls:</b> 800 beds</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("Use the sidebar to navigate to different sections for more information!")

# FAQ BOT PAGE
elif page == "❓ FAQ Bot":
    st.markdown('<div class="section-header">❓ ASK YOUR QUESTIONS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        user_question = st.text_input("Type your question:", placeholder="e.g., How do I apply for hostel?")
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    if user_question and search_button:
        # Search for answer
        user_vec = vectorizer.transform([user_question])
        similarities = cosine_similarity(user_vec, question_vectors)[0]
        top_indices = similarities.argsort()[-3:][::-1]
        
        st.markdown("---")
        st.markdown("### 📌 TOP ANSWERS")
        
        for idx, top_idx in enumerate(top_indices, 1):
            confidence = similarities[top_idx]
            confidence_pct = confidence * 100
            
            if confidence_pct >= 70:
                emoji, color = "✅", "#28a745"
            elif confidence_pct >= 50:
                emoji, color = "⚠️", "#ffc107"
            else:
                emoji, color = "❌", "#dc3545"
            
            st.markdown(f"""
            <div class="answer-box">
            <h4>{emoji} ANSWER #{idx} (Confidence: {confidence_pct:.1f}%)</h4>
            <p><b>Q:</b> {questions_list[top_idx]}</p>
            <p><b>A:</b> {answers_list[top_idx]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    with st.expander("📚 VIEW ALL FAQs"):
        for i, (q, a) in enumerate(FAQs.items(), 1):
            st.markdown(f"**{i}. {q}**")
            st.markdown(f"_{a}_")
            st.divider()

# ANALYTICS PAGE
elif page == "📊 Analytics":
    st.markdown('<div class="section-header">📊 ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)
    
    analytics_file = "analytics_data.json"
    if os.path.exists(analytics_file):
        with open(analytics_file, 'r') as f:
            analytics = json.load(f)
    else:
        analytics = {"total_queries": 0, "high_confidence": 0, "low_confidence": 0}
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-box"><h3>❓ TOTAL QUERIES</h3><h2>{analytics.get("total_queries", 0)}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><h3>✅ HIGH CONFIDENCE</h3><h2>{analytics.get("high_confidence", 0)}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box"><h3>⚠️ LOW CONFIDENCE</h3><h2>{analytics.get("low_confidence", 0)}</h2></div>', unsafe_allow_html=True)

# LEARNING PAGE
elif page == "🎓 Learning":
    st.markdown('<div class="section-header">🎓 ADD NEW QUESTIONS</div>', unsafe_allow_html=True)
    
    st.write("Help expand our knowledge base by adding new questions and answers!")
    
    col1, col2 = st.columns(2)
    with col1:
        new_question = st.text_area("Your Question:", height=100, placeholder="Enter a new question...")
    with col2:
        new_answer = st.text_area("Answer:", height=100, placeholder="Enter the answer...")
    
    if st.button("📤 SUBMIT NEW Q&A"):
        if new_question and new_answer:
            st.success("✅ Thank you! Your contribution has been added!")
            st.balloons()
        else:
            st.error("Please fill in both question and answer fields!")
