"""
GMU COLLEGE FAQ ASSISTANT
A semantic search-based FAQ system for university students
Custom built with modular architecture and original functionality
"""

import streamlit as st
from database_manager import FAQDatabase, AnalyticsManager
from search_engine import SemanticSearch

# ============= PAGE CONFIGURATION =============
st.set_page_config(
    page_title="GMU College - FAQ Assistant", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ============= THEME MANAGEMENT =============
with st.sidebar:
    theme_mode = st.radio("🌓 Theme:", ["☀️ Light", "🌙 Dark"], index=0)
    st.divider()

is_light = "☀️" in theme_mode

# Apply CSS - FIXED FOR VISIBILITY
if is_light:
    st.markdown("""
    <style>
    * { background-color: #ffffff !important; color: #000000 !important; }
    body, .main, .stApp { background-color: #ffffff !important; color: #000000 !important; }
    .main-title { font-size: 4.5em !important; font-weight: bold !important; text-align: center !important; color: #0066cc !important; background-color: #ffffff !important; }
    .section-header { font-size: 3em !important; font-weight: bold !important; color: #000000 !important; background-color: #ffffff !important; border-bottom: 4px solid #0066cc !important; padding-bottom: 0.5em !important; }
    .facility-box { background-color: #e7f3ff !important; padding: 2em !important; border-radius: 12px !important; border-left: 6px solid #0066cc !important; color: #000000 !important; }
    h1, h2, h3, h4, h5, h6, p, div, span { color: #000000 !important; background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    * { color: #ffffff !important; }
    body, .main, .stApp { background-color: #1a1a1a !important; color: #ffffff !important; }
    .main-title { font-size: 4.5em !important; font-weight: bold !important; text-align: center !important; color: #4da6ff !important; background-color: transparent !important; }
    .section-header { font-size: 3em !important; font-weight: bold !important; color: #ffffff !important; background-color: transparent !important; border-bottom: 4px solid #4da6ff !important; padding-bottom: 0.5em !important; }
    .facility-box { background-color: #2d2d2d !important; padding: 2em !important; border-radius: 12px !important; border-left: 6px solid #4da6ff !important; color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6, p, div, span { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# ============= SESSION STATE =============
if 'faq_db' not in st.session_state:
    st.session_state.faq_db = FAQDatabase()
    st.session_state.analytics = AnalyticsManager.load_analytics()
    st.session_state.search_engine = SemanticSearch(st.session_state.faq_db.get_questions_list())

# ============= NAVIGATION =============
with st.sidebar:
    st.markdown('<h2 style="font-size: 2.2em; font-weight: bold;">🏫 NAVIGATION</h2>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Section:", 
        ["🏠 Home", "❓ FAQ Bot", "🏢 Hostel", "🎓 College", "📋 Academics", "💰 Finance", "📊 Analytics", "🎓 Learning"],
        label_visibility="collapsed")

# ============= HOME PAGE =============
if page == "🏠 Home":
    st.markdown('<h1 class="main-title">🎓 STUDENT INFORMATION PORTAL</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc;">🎓 GMU COLLEGE</h2>
        Premier educational institution providing quality education.<br/><br/>
        📍 Campus: <b>PB ROAD DAVANGERE</b><br/>
        📞 Phone: <b>1-800-GMU-HELP</b><br/>
        📧 Email: <b>info@gmucollege.edu</b>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #dc3545;">🏢 GMU HOSTEL</h2>
        Comfortable on-campus living with excellent facilities.<br/><br/>
        🛏️ Total: <b>2000 beds</b><br/>
        👨‍🎓 Boys: <b>1200 beds</b><br/>
        👩‍🎓 Girls: <b>800 beds</b>
        </div>
        """, unsafe_allow_html=True)

# ============= FAQ BOT PAGE =============
elif page == "❓ FAQ Bot":
    st.markdown('<h2 class="section-header">❓ Ask Your Questions</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        user_query = st.text_input("Type question:", placeholder="e.g., What are room types?")
    with col2:
        search_btn = st.button("🔍 Search")
    
    if user_query and search_btn:
        # Record query
        AnalyticsManager.record_query(st.session_state.analytics, user_query)
        
        # Search
        results = st.session_state.search_engine.search(user_query, top_k=3)
        answers = st.session_state.faq_db.get_answers_list()
        
        st.markdown("---")
        st.markdown('<h3 style="font-size: 2em; color: #0066cc;">📌 TOP ANSWERS</h3>', unsafe_allow_html=True)
        
        for idx, result in enumerate(results, 1):
            confidence = result['similarity']
            color = "#28a745" if confidence >= 0.7 else ("#ffc107" if confidence >= 0.5 else "#dc3545")
            emoji = "✅" if confidence >= 0.7 else ("⚠️" if confidence >= 0.5 else "❌")
            
            AnalyticsManager.record_confidence(st.session_state.analytics, confidence)
            
            st.markdown(f"""
            <div class="facility-box" style="border-left: 6px solid {color};">
            <h3 style="color: {color};">{emoji} ANSWER #{idx}</h3>
            <p><b>Confidence: {result['confidence_percent']:.1f}%</b></p>
            <p>{answers[result['index']]}</p>
            <hr style="margin: 15px 0;">
            <p style="font-size: 0.9em;"><b>Related:</b> {result['question']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feedback
        st.markdown("---")
        st.markdown('<h3 style="color: #0066cc;">👍 Helpful?</h3>', unsafe_allow_html=True)
        fb_col1, fb_col2, fb_col3 = st.columns(3)
        
        with fb_col1:
            if st.button("👍 Yes", key="fb1"):
                AnalyticsManager.record_feedback(st.session_state.analytics, user_query, "helpful")
                AnalyticsManager.save_analytics(st.session_state.analytics)
                st.success("✅ Thank you!")
        
        with fb_col2:
            if st.button("🤔 Somewhat", key="fb2"):
                AnalyticsManager.record_feedback(st.session_state.analytics, user_query, "somewhat")
                AnalyticsManager.save_analytics(st.session_state.analytics)
                st.info("ℹ️ We'll improve!")
        
        with fb_col3:
            if st.button("👎 No", key="fb3"):
                AnalyticsManager.record_feedback(st.session_state.analytics, user_query, "not_helpful")
                AnalyticsManager.save_analytics(st.session_state.analytics)
                st.warning("⚠️ Use Learning section")
    
    # All FAQs
    with st.expander("📚 View All FAQs"):
        faqs = st.session_state.faq_db.get_all_faqs()
        for i, (q, a) in enumerate(faqs.items(), 1):
            st.markdown(f'**❓ {i}. {q}**')
            st.markdown(a)
            st.markdown("---")

# ============= HOSTEL PAGE =============
elif page == "🏢 Hostel":
    st.markdown('<h2 class="section-header">🏢 GMU HOSTEL</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="facility-box" style="text-align: center;">
        <div style="font-size: 2.5em;">🏗️</div>
        <h3>TOTAL</h3>
        <p style="font-size: 2em; font-weight: bold;">2000</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="facility-box" style="text-align: center;">
        <div style="font-size: 2.5em;">👨‍🎓</div>
        <h3>BOYS</h3>
        <p style="font-size: 2em; font-weight: bold;">1200</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="facility-box" style="text-align: center;">
        <div style="font-size: 2.5em;">👩‍🎓</div>
        <h3>GIRLS</h3>
        <p style="font-size: 2em; font-weight: bold;">800</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="facility-box">
    <h3>Room Types:</h3>
    <b>Single:</b> $3,000/Sem - AC, Bath, WiFi, Wardrobe<br/>
    <b>Double:</b> $2,000/Sem - AC, Bath, WiFi, Wardrobes<br/>
    <b>Triple:</b> $1,500/Sem - AC, Bath, WiFi, Wardrobes
    </div>
    """, unsafe_allow_html=True)

# ============= COLLEGE PAGE =============
elif page == "🎓 College":
    st.markdown('<h2 class="section-header">🎓 GMU COLLEGE</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    metrics = [("25+ Yrs", "🎓", "Experience"), ("5000+", "👥", "Students"), ("50+", "📚", "Programs"), ("98%", "🌍", "Placement")]
    
    for metric, col in zip(metrics, [col1, col2, col3, col4]):
        with col:
            st.markdown(f"""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2.5em;">{metric[1]}</div>
            <p style="font-size: 1.8em; font-weight: bold;">{metric[0]}</p>
            <p>{metric[2]}</p>
            </div>
            """, unsafe_allow_html=True)

# ============= ACADEMICS PAGE =============
elif page == "📋 Academics":
    st.markdown('<h2 class="section-header">📋 ACADEMIC CALENDAR</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="facility-box">
    <b>Semester Duration:</b> 6 months<br/>
    <b>Total Semesters:</b> 8 (4 years)<br/>
    <b>Internal Assessment:</b> 3 tests (30%)<br/>
    <b>Final Exam:</b> (60%)<br/>
    <b>Minimum Pass:</b> 40%<br/>
    <b>Min Attendance:</b> 75%
    </div>
    """, unsafe_allow_html=True)

# ============= FINANCE PAGE =============
elif page == "💰 Finance":
    st.markdown('<h2 class="section-header">💰 FEES</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="facility-box" style="text-align: center;">
        <h3>UG</h3>
        <p style="font-size: 2em; font-weight: bold;">₹3,000</p>
        <p>Per Semester</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="facility-box" style="text-align: center;">
        <h3>PG</h3>
        <p style="font-size: 2em; font-weight: bold;">₹4,000</p>
        <p>Per Semester</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="facility-box" style="text-align: center;">
        <h3>INTL</h3>
        <p style="font-size: 2em; font-weight: bold;">₹6,000+</p>
        <p>Per Semester</p>
        </div>
        """, unsafe_allow_html=True)

# ============= ANALYTICS PAGE =============
elif page == "📊 Analytics":
    st.markdown('<h2 class="section-header">📊 ANALYTICS</h2>', unsafe_allow_html=True)
    
    analytics = st.session_state.analytics
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center;">
        <h3>❓</h3>
        <p style="font-size: 2em; font-weight: bold;">{analytics['total_queries']}</p>
        <p>Queries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center;">
        <h3>✅</h3>
        <p style="font-size: 2em; font-weight: bold;">{analytics['high_confidence']}</p>
        <p>High Conf</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center;">
        <h3>⚠️</h3>
        <p style="font-size: 2em; font-weight: bold;">{analytics['low_confidence']}</p>
        <p>Low Conf</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center;">
        <h3>📚</h3>
        <p style="font-size: 2em; font-weight: bold;">{analytics['learned_answers']}</p>
        <p>Learned</p>
        </div>
        """, unsafe_allow_html=True)

# ============= LEARNING PAGE =============
elif page == "🎓 Learning":
    st.markdown('<h2 class="section-header">🎓 ADD QUESTIONS</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4>❓ NEW QUESTION</h4>', unsafe_allow_html=True)
        new_q = st.text_area("Question:", height=100, key="new_q")
    
    with col2:
        st.markdown('<h4>✍️ ANSWER</h4>', unsafe_allow_html=True)
        new_a = st.text_area("Answer:", height=100, key="new_a")
    
    st.markdown("---")
    
    col_s, col_c = st.columns(2)
    
    with col_s:
        if st.button("📤 SUBMIT"):
            if new_q and new_a:
                st.session_state.faq_db.add_faq(new_q, new_a)
                st.session_state.search_engine.retrain(st.session_state.faq_db.get_questions_list())
                AnalyticsManager.add_learned_answer(st.session_state.analytics)
                AnalyticsManager.save_analytics(st.session_state.analytics)
                st.success("✅ Added!")
                st.balloons()
            else:
                st.error("⚠️ Fill both fields!")
    
    with col_c:
        if st.button("🗑️ CLEAR"):
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"<h3>Total FAQs: {st.session_state.faq_db.get_faq_count()}</h3>", unsafe_allow_html=True)

# Save analytics
AnalyticsManager.save_analytics(st.session_state.analytics)
