import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import json
import os
import pickle

st.set_page_config(
    page_title="GMU College - FAQ Assistant", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Dark/Light Mode Toggle in Sidebar
with st.sidebar:
    theme_mode = st.radio("🌓 Theme Mode:", ["☀️ Light Mode", "🌙 Dark Mode"], index=0, horizontal=False)
    st.divider()

# Custom CSS for better styling based on theme
if "☀️" in theme_mode:
    # Light Mode - Better visibility
    st.markdown("""
    <style>
        :root {
            --primary-color: #0066cc;
            --secondary-color: #dc3545;
            --text-color: #000000;
            --bg-color: #ffffff;
            --box-bg: #f8f9fa;
            --border-color: #e0e0e0;
        }
        body, .main {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .main-title {
            font-size: 4.5em !important;
            font-weight: bold;
            text-align: center;
            color: #0066cc;
            margin-bottom: 0.5em;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .hostel-title {
            font-size: 3.5em !important;
            font-weight: bold;
            color: #dc3545;
            text-align: center;
            margin: 1em 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .college-title {
            font-size: 3.5em !important;
            font-weight: bold;
            color: #0066cc;
            text-align: center;
            margin: 1em 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .section-header {
            font-size: 3em !important;
            font-weight: bold;
            color: #0066cc;
            margin: 1em 0 0.5em 0;
            border-bottom: 4px solid #0066cc;
            padding-bottom: 0.5em;
        }
        .facility-box {
            background-color: #e7f3ff;
            padding: 2em;
            border-radius: 12px;
            margin: 1em 0;
            border-left: 6px solid #0066cc;
            color: #000000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            font-size: 1.3em !important;
        }
        .meal-box {
            background-color: #fffacd;
            padding: 1.8em;
            border-radius: 12px;
            margin: 0.8em 0;
            border-left: 6px solid #ff9800;
            color: #000000;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            font-size: 1.2em !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #f8f9fa;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f0f0f0;
            border: 2px solid #0066cc;
            color: #000000;
            font-size: 1.2em !important;
        }
        input, textarea, select {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #0066cc !important;
            font-size: 1.2em !important;
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #0066cc;
            font-size: 1.3em !important;
        }
        /* Tab styling - BIGGER AND BOLD */
        .stTabs [role="tab"] {
            font-size: 1.6em !important;
            font-weight: bold !important;
            padding: 15px 25px !important;
            min-width: 140px !important;
            text-align: center !important;
        }
        .stTabs [role="tabpanel"] {
            font-size: 1.3em !important;
        }
        /* Headings - BOLD and BIG */
        h1, h2, h3, h4, h5, h6 {
            font-weight: bold !important;
        }
        /* Text styling */
        p, span, div {
            font-weight: 500 !important;
        }
        /* Sidebar radio buttons - BIGGER AND BOLD */
        .stRadio > label {
            font-size: 1.5em !important;
            font-weight: bold !important;
        }
        .stRadio [role="radio"] {
            width: 20px !important;
            height: 20px !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # Dark Mode - High contrast for visibility
    st.markdown("""
    <style>
        :root {
            --primary-color: #4da6ff;
            --secondary-color: #ff6b6b;
            --text-color: #ffffff;
            --bg-color: #1a1a1a;
            --box-bg: #2d2d2d;
            --border-color: #404040;
        }
        body, .main {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
        }
        .main-title {
            font-size: 4.5em !important;
            font-weight: bold;
            text-align: center;
            color: #4da6ff;
            margin-bottom: 0.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .hostel-title {
            font-size: 3.5em !important;
            font-weight: bold;
            color: #ff6b6b;
            text-align: center;
            margin: 1em 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .college-title {
            font-size: 3.5em !important;
            font-weight: bold;
            color: #4da6ff;
            text-align: center;
            margin: 1em 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .section-header {
            font-size: 3em !important;
            font-weight: bold;
            color: #4da6ff;
            margin: 1em 0 0.5em 0;
            border-bottom: 4px solid #4da6ff;
            padding-bottom: 0.5em;
        }
        .facility-box {
            background-color: #1e3a5f;
            padding: 2em;
            border-radius: 12px;
            margin: 1em 0;
            border-left: 6px solid #4da6ff;
            color: #ffffff;
            box-shadow: 0 2px 12px rgba(0,0,0,0.5);
            font-size: 1.3em !important;
        }
        .meal-box {
            background-color: #3d3a1a;
            padding: 1.8em;
            border-radius: 12px;
            margin: 0.8em 0;
            border-left: 6px solid #ffb84d;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.5);
            font-size: 1.2em !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #2d2d2d;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #3d3d3d;
            border: 2px solid #4da6ff;
            color: #ffffff;
            font-size: 1.2em !important;
        }
        input, textarea, select {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border: 2px solid #4da6ff !important;
            font-size: 1.2em !important;
        }
        .stMetric {
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #4da6ff;
            color: #ffffff;
            font-size: 1.3em !important;
        }
        /* Tab styling - BIGGER AND BOLD */
        .stTabs [role="tab"] {
            font-size: 1.6em !important;
            font-weight: bold !important;
            padding: 15px 25px !important;
            min-width: 140px !important;
            text-align: center !important;
            color: #ffffff !important;
        }
        .stTabs [role="tabpanel"] {
            font-size: 1.3em !important;
        }
        /* Headings - BOLD and BIG */
        h1, h2, h3, h4, h5, h6 {
            font-weight: bold !important;
        }
        /* Text styling */
        p, span, div {
            font-weight: 500 !important;
        }
        /* Sidebar radio buttons - BIGGER AND BOLD */
        .stRadio > label {
            font-size: 1.5em !important;
            font-weight: bold !important;
            color: #ffffff !important;
        }
        .stRadio [role="radio"] {
            width: 20px !important;
            height: 20px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Weekly Meal Schedule for GMU Hostel
WEEKLY_MEAL_SCHEDULE = {
    "Monday": {
        "Breakfast": "Idli, Dosa, Sambhar, Chutney, Fresh Juice",
        "Lunch": "Rice, Dal Fry, Chicken Curry, Salad, Pickle",
        "Dinner": "Roti, Paneer Masala, Steamed Vegetables",
        "Snacks": "Milk, Cookies, Banana"
    },
    "Tuesday": {
        "Breakfast": "Poha, Jalebi, Tea, Bread, Butter",
        "Lunch": "Biryani, Raita, Mixed Vegetables, Pappad",
        "Dinner": "Chapati, Fish Curry, Green Vegetables",
        "Snacks": "Tea, Samosa, Orange"
    },
    "Wednesday": {
        "Breakfast": "Oats, Eggs, Whole Wheat Bread, Orange Juice",
        "Lunch": "Pulao, Rajma, Seasonal Vegetables, Pickle",
        "Dinner": "Parantha, Chole Masala, Yogurt",
        "Snacks": "Milk, Biscuits, Apple"
    },
    "Thursday": {
        "Breakfast": "Upma, Coconut Chutney, Vada, Milk, Banana",
        "Lunch": "Rice, Sambar, Fish/Paneer, Salad, Pickle",
        "Dinner": "Naan, Butter Chicken, Steamed Broccoli",
        "Snacks": "Tea, Cake, Mango"
    },
    "Friday": {
        "Breakfast": "Cornflakes with Milk, Toast, Jam, Orange Juice",
        "Lunch": "Basmati Rice, Lentil Dal, Mutton Curry, Vegetables",
        "Dinner": "Tawa Bread, Paneer Tikka, Mixed Vegetables",
        "Snacks": "Milk, Donut, Strawberry"
    },
    "Saturday": {
        "Breakfast": "Puri, Potato Curry, Sweet, Tea, Milk",
        "Lunch": "Chicken Biryani, Cucumber Salad, Pickle, Pappad",
        "Dinner": "Roti, Lamb Keema, Peas and Carrots",
        "Snacks": "Cold Milk, Pastry, Grapes"
    },
    "Sunday": {
        "Breakfast": "Pancakes, Syrup, Eggs, Fresh Fruit",
        "Lunch": "Special Rice Variety, Prawns Curry, Salad, Dessert",
        "Dinner": "Tandoori Naan, Paneer Butter Masala, Mushrooms",
        "Snacks": "Tea, Cookies, Watermelon"
    }
}

# Comprehensive FAQ Database
faqs = {
"How can I enroll in courses?": "You can enroll through the student portal during registration week.",
"What facilities are available on campus?": "Library, labs, hostel, sports ground, medical center.",
"How to apply for financial aid?": "Submit financial aid form on university website.",
"What is the academic calendar?": "Semester starts in August and January.",
"Is hostel available?": "Yes hostel is available for boys and girls.",
"How to contact administration?": "Email admin@university.edu or visit office.",

"What is minimum attendance required?": "Minimum 75 percent attendance is mandatory.",
"Are scholarships available?": "Yes merit-based and need-based scholarships are provided.",
"What are library timings?": "Library is open from 9 AM to 8 PM.",
"Is placement support available?": "Yes placement and training cell helps students.",

"Is WiFi available on campus?": "Yes free WiFi is available.",
"What documents needed for admission?": "Marks cards, ID proof and photographs are required.",
"How to pay college fees?": "Fees can be paid online through portal or bank.",
"When are exams conducted?": "Exams are conducted at end of each semester.",

"Is medical facility available?": "Yes campus has medical center.",
"Is sports facility available?": "Yes various indoor and outdoor sports available.",
"What courses are offered?": "Engineering, Data Science, Business and Arts.",
"Is transportation provided?": "Yes buses are provided for students.",

"How to access student portal?": "Login using student ID and password.",
"How to apply for hostel?": "Apply through hostel application form online.",

"What is exam passing criteria?": "Minimum 40 percent is required to pass.",
"Are internships available?": "Yes students get internship opportunities.",
"Is there counseling support?": "Yes counseling services are provided.",

"What are college working hours?": "College works from 9 AM to 4 PM.",
"Is canteen available?": "Yes campus has canteen facility.",

"How to get ID card?": "ID card is issued during admission.",
"Is attendance tracked online?": "Yes attendance is available in portal.",

"How to apply for certificates?": "Apply through admin office or portal.",
"Is online class available?": "Yes some courses offer online classes.",

"What is semester duration?": "Each semester is about 6 months.",
"How many semesters are there?": "Usually 8 semesters for engineering.",

"Is library membership required?": "Yes students must register in library.",
"Can parents meet teachers?": "Yes during parent-teacher meetings.",

"How to submit assignments?": "Assignments are submitted online or in class.",
"Are workshops conducted?": "Yes regular workshops are conducted.",

"Is there research facility?": "Yes labs support research work.",
"How to change course?": "Apply through academic office.",

"Is hostel food provided?": "Yes mess facility is available.",
"What languages are taught?": "English and regional languages are taught.",

"How to contact support desk?": "Visit help desk or email support."
}


questions = list(faqs.keys())
answers = list(faqs.values())

vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))
X = vectorizer.fit_transform(questions)

# Store FAQ data in session state for updates
if 'faqs_db' not in st.session_state:
    st.session_state.faqs_db = faqs.copy()
    st.session_state.questions_list = questions.copy()
    st.session_state.answers_list = answers.copy()
    st.session_state.vectorizer = vectorizer
    st.session_state.X = X

def retrain_bot():
    """Retrain the bot with updated FAQs"""
    st.session_state.questions_list = list(st.session_state.faqs_db.keys())
    st.session_state.answers_list = list(st.session_state.faqs_db.values())
    st.session_state.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))
    st.session_state.X = st.session_state.vectorizer.fit_transform(st.session_state.questions_list)

def get_answer(user_question):
    """Get answers with improved matching"""
    if len(st.session_state.questions_list) == 0:
        return [], 0
    
    user_vec = st.session_state.vectorizer.transform([user_question])
    similarity = cosine_similarity(user_vec, st.session_state.X)
    
    # Get top 3 answers with confidence scores
    top_indices = similarity[0].argsort()[-3:][::-1]
    
    results = []
    for idx in top_indices:
        confidence = similarity[0][idx]
        results.append({
            'answer': st.session_state.answers_list[idx],
            'confidence': confidence,
            'question': st.session_state.questions_list[idx]
        })
    
    return results

# Initialize or load analytics data
ANALYTICS_FILE = "analytics_data.json"

def load_analytics():
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    return {
        "total_queries": 0,
        "high_confidence": 0,
        "low_confidence": 0,
        "learned_answers": 0,
        "top_questions": {},
        "user_feedback": []
    }

def save_analytics(analytics_data):
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(analytics_data, f, indent=4)

# Load analytics data at startup
analytics_data = load_analytics()

# Sidebar Navigation
with st.sidebar:
    st.markdown('<h2 style="font-size: 2.2em; font-weight: bold; color: #0066cc;">🏫 NAVIGATION</h2>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Select Section:", 
        ["🏠 Home", "❓ FAQ Bot", "🏢 GMU Hostel", "🎓 GMU College", "📋 Academics", "💰 Finance", "📊 Analytics", "🎓 Learning"],
        label_visibility="collapsed")

# Main Page
if page == "🏠 Home":
    st.markdown('<h1 class="main-title">🎓 STUDENT INFORMATION PORTAL</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h3 class="college-title">🎓 GMU COLLEGE</h3>', unsafe_allow_html=True)
        st.info("""
        **Welcome to GMU College!**
        
        Your premier educational institution providing quality education and world-class facilities.
        
        📍 Campus Location: **PB ROAD DAVANGERE**
        📞 Phone: 1-800-GMU-HELP
        📧 Email: info@gmucollege.edu
        """)
    
    with col2:
        st.markdown('<h3 class="hostel-title">🏢 GMU HOSTEL</h3>', unsafe_allow_html=True)
        st.success("""
        **Comfortable On-Campus Living**
        
        Your home away from home with excellent facilities and caring management.
        
        🛏️ Total Capacity: 2000 beds
        👥 Boys Hostel: 1200 beds
        👥 Girls Hostel: 800 beds
        """)
    
    st.markdown("---")
    st.write("Use the sidebar to navigate to different sections for more information!")

elif page == "❓ FAQ Bot":
    st.markdown('<h2 class="section-header">❓ Ask Your Questions</h2>', unsafe_allow_html=True)
    st.write("")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input("Type your question here:", placeholder="e.g., What are hostel room types?", key="faq_input")
    
    with col2:
        search_button = st.button("🔍 Search", key="search_btn")
    
    if user_input and search_button:
        results = get_answer(user_input)
        
        # Update analytics
        analytics_data["total_queries"] += 1
        if user_input not in analytics_data["top_questions"]:
            analytics_data["top_questions"][user_input] = 0
        analytics_data["top_questions"][user_input] += 1
        
        st.markdown("---")
        st.markdown(f'<h3 style="font-size: 2em; color: #0066cc;">📌 TOP ANSWERS FOR YOUR QUESTION</h3>', unsafe_allow_html=True)
        st.markdown("")
        
        for idx, result in enumerate(results, 1):
            confidence_pct = result['confidence'] * 100
            
            # Update confidence analytics
            if confidence_pct >= 50:
                analytics_data["high_confidence"] += 1
            else:
                analytics_data["low_confidence"] += 1
            
            # Color based on confidence
            if confidence_pct >= 70:
                color = "#28a745"
                emoji = "✅"
            elif confidence_pct >= 50:
                color = "#ffc107"
                emoji = "⚠️"
            else:
                color = "#dc3545"
                emoji = "❌"
            
            st.markdown(f"""
            <div class="facility-box" style="border-left: 6px solid {color};">
            <h3 style="font-size: 1.8em; margin-top: 0; color: {color};">{emoji} ANSWER #{idx}</h3>
            <p style="font-size: 1.4em; font-weight: bold; color: #0066cc;">Confidence Score: {confidence_pct:.1f}%</p>
            <p style="font-size: 1.3em; color: #333; line-height: 1.8;">{result['answer']}</p>
            <hr style="margin: 15px 0;">
            <p style="font-size: 1.1em; color: #666; margin: 0;"><b>Related to:</b> {result['question']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
        
        # Feedback section
        st.markdown("---")
        st.markdown(f'<h3 style="font-size: 1.8em; color: #0066cc;">👍 Was This Helpful?</h3>', unsafe_allow_html=True)
        feedback_col1, feedback_col2, feedback_col3 = st.columns(3)
        
        with feedback_col1:
            if st.button("👍 Yes, Very Helpful", key="helpful_yes"):
                analytics_data["user_feedback"].append({"query": user_input, "rating": "helpful"})
                save_analytics(analytics_data)
                st.success("✅ Thank you for your feedback!")
        
        with feedback_col2:
            if st.button("🤔 Somewhat Helpful", key="helpful_maybe"):
                analytics_data["user_feedback"].append({"query": user_input, "rating": "somewhat"})
                save_analytics(analytics_data)
                st.info("ℹ️ We'll improve this!")
        
        with feedback_col3:
            if st.button("👎 Not Helpful", key="helpful_no"):
                analytics_data["user_feedback"].append({"query": user_input, "rating": "not_helpful"})
                save_analytics(analytics_data)
                st.warning("⚠️ Please use the Learning section to add your answer.")
    
    st.markdown("---")
    with st.expander("📚 View All FAQs", expanded=False):
        st.markdown("---")
        for i, (q, a) in enumerate(faqs.items(), 1):
            st.markdown(f'<h4 style="font-size: 1.6em; color: #0066cc;">❓ {i}. {q}</h4>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 1.3em;">{a}</p>', unsafe_allow_html=True)
            st.markdown("---")

elif page == "🏢 GMU Hostel":
    st.markdown('<h3 class="hostel-title">🏢 GMU HOSTEL</h3>', unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "🛏️ Rooms & Pricing", "🍽️ Meal Schedule", "📋 Rules & Facilities"])
    
    with tab1:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">🏢 Hostel Overview - Your Second Home</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Impressive Visual Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="facility-box" style="text-align: center; padding: 2em;">
            <div style="font-size: 3em; margin-bottom: 10px;">🏗️</div>
            <h3 style="margin: 10px 0; color: inherit;">TOTAL CAPACITY</h3>
            <div style="font-size: 2.5em; font-weight: bold; color: #0066cc; margin: 15px 0;">2000</div>
            <p style="margin: 5px 0; font-size: 0.9em;">Available Beds</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="facility-box" style="text-align: center; padding: 2em;">
            <div style="font-size: 3em; margin-bottom: 10px;">👨‍🎓</div>
            <h3 style="margin: 10px 0; color: inherit;">BOYS HOSTEL</h3>
            <div style="font-size: 2.5em; font-weight: bold; color: #0066cc; margin: 15px 0;">1200</div>
            <p style="margin: 5px 0; font-size: 0.9em;">Beds for Boys</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="facility-box" style="text-align: center; padding: 2em;">
            <div style="font-size: 3em; margin-bottom: 10px;">👩‍🎓</div>
            <h3 style="margin: 10px 0; color: inherit;">GIRLS HOSTEL</h3>
            <div style="font-size: 2.5em; font-weight: bold; color: #dc3545; margin: 15px 0;">800</div>
            <p style="margin: 5px 0; font-size: 0.9em;">Beds for Girls</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Hostel Features Section
        st.markdown('<h2 style="font-size: 2.5em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">✨ Why Choose GMU Hostel?</h2>', unsafe_allow_html=True)
        
        feat_col1, feat_col2 = st.columns(2)
        
        with feat_col1:
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2.5em; margin-bottom: 10px;">🛏️</div>
            <b>Comfortable Rooms</b><br/>
            Single, Double & Triple occupancy options with AC, attached bathrooms & WiFi
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2.5em; margin-bottom: 10px;">🍽️</div>
            <b>Delicious Meals</b><br/>
            Nutritious breakfast, lunch, dinner & snacks included in fees
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2.5em; margin-bottom: 10px;">🧺</div>
            <b>Laundry Service</b><br/>
            Free laundry twice weekly & iron service available
            </div>
            """, unsafe_allow_html=True)
        
        with feat_col2:
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2.5em; margin-bottom: 10px;">🔒</div>
            <b>24/7 Security</b><br/>
            CCTV surveillance, biometric gates & security personnel round the clock
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2.5em; margin-bottom: 10px;">📡</div>
            <b>High-Speed WiFi</b><br/>
            24/7 internet access in all rooms & common areas
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2.5em; margin-bottom: 10px;">🎉</div>
            <b>Social Events</b><br/>
            Monthly festivals, sports, cultural programs & community activities
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Key Statistics
        st.markdown('<h2 style="font-size: 2.5em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">📊 Hostel Statistics</h2>', unsafe_allow_html=True)
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">⭐</div>
            <div style="font-size: 1.5em; font-weight: bold;">5 Stars</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Student Rating</p>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">🏆</div>
            <div style="font-size: 1.5em; font-weight: bold;">95%</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Occupancy Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col3:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">👥</div>
            <div style="font-size: 1.5em; font-weight: bold;">2000+</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Happy Residents</p>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col4:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">🎓</div>
            <div style="font-size: 1.5em; font-weight: bold;">10+ Yrs</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Experience</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">🛏️ Room Types & Pricing</h2>', unsafe_allow_html=True)
        
        room_data = {
            "Room Type": ["Single Occupancy", "Double Occupancy", "Triple Occupancy"],
            "Price/Semester": ["$3,000", "$2,000", "$1,500"],
            "Features": [
                "AC • Attached Bath • WiFi • Wardrobe • Study Table",
                "AC • Attached Bath • WiFi • Wardrobes • Study Tables",
                "AC • Attached Bath • WiFi • Wardrobes • Study Tables"
            ]
        }
        
        for i, room_type in enumerate(room_data["Room Type"]):
            st.markdown(f"""
            <div class="facility-box">
            <b>{room_type}</b><br/>
            Price: {room_data['Price/Semester'][i]}<br/>
            Features: {room_data['Features'][i]}
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">📅 Weekly Meal Schedule</h2>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.4em; font-weight: bold;">*All meals included in hostel fees*</p>', unsafe_allow_html=True)
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day in days:
            with st.expander(f"📆 {day}"):
                meals = WEEKLY_MEAL_SCHEDULE[day]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="meal-box">
                    <b>🌅 Breakfast</b><br/>
                    {meals['Breakfast']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="meal-box">
                    <b>🍽️ Lunch</b><br/>
                    {meals['Lunch']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="meal-box">
                    <b>🌙 Dinner</b><br/>
                    {meals['Dinner']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="meal-box">
                    <b>☕ Snacks</b><br/>
                    {meals['Snacks']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">🏢 Hostel Rules & Facilities</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="facility-box">
            <b>📋 Rules</b><br/>
            ✓ Check-in by 11 PM<br/>
            ✓ Quiet hours 11 PM - 7 AM<br/>
            ✓ No smoking/alcohol<br/>
            ✓ Visitor hours 10 AM - 8 PM<br/>
            ✓ Monthly room inspection<br/>
            ✓ Respect communal property
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="facility-box">
            <b>⭐ Facilities</b><br/>
            ✓ Free WiFi 24/7<br/>
            ✓ Free Laundry (2x/week)<br/>
            ✓ 24/7 Security & CCTV<br/>
            ✓ Common Kitchen<br/>
            ✓ Recreation Room<br/>
            ✓ Biometric Access Gates
            </div>
            """, unsafe_allow_html=True)

elif page == "🎓 GMU College":
    st.markdown('<h3 class="college-title">🎓 GMU COLLEGE</h3>', unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📍 About", "💰 Fee Structure", "🎯 Academic Programs", "🏢 Internships", "🏛️ Events & Facilities"])
    
    with tab1:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">🎓 About GMU College</h2>', unsafe_allow_html=True)
        
        # Key Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">🎓</div>
            <div style="font-size: 1.5em; font-weight: bold;">25+ Yrs</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Excellence</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">👥</div>
            <div style="font-size: 1.5em; font-weight: bold;">5000+</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Students</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">📚</div>
            <div style="font-size: 1.5em; font-weight: bold;">50+</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Programs</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2em;">🌍</div>
            <div style="font-size: 1.5em; font-weight: bold;">98%</div>
            <p style="font-size: 0.9em; margin: 5px 0;">Placement</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        **GMU COLLEGE** - India's premier technical and management institute
        
        **📍 Address:** **PB ROAD DAVANGERE**
        
        We are committed to providing quality education and holistic development of students with state-of-the-art infrastructure and industry-aligned curriculum.
        
        **Our Mission:** Empower students through quality education for excellence in their chosen fields
        
        **Our Vision:** Create global leaders and innovators
        """)
    
    with tab2:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">💰 Complete Fee Structure</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Engineering Programs
        st.markdown("### 🔧 ENGINEERING (4 Years)")
        
        eng_col1, eng_col2 = st.columns(2)
        
        with eng_col1:
            st.markdown("""
            <div class="facility-box">
            <b>Computer Science & IT</b><br/>
            <div style="font-size: 1.2em; font-weight: bold; color: #0066cc; margin: 10px 0;">₹8,00,000</div>
            Per 4 Years<br/>
            <hr style="margin: 10px 0;">
            • Semester Fee: ₹2,00,000<br/>
            • Donation (One-time): ₹4,00,000<br/>
            • Hostel (4 years): ₹4,00,000<br/>
            <hr style="margin: 10px 0;">
            <b>Year-wise Breakdown:</b><br/>
            Year 1: ₹2,50,000<br/>
            Year 2: ₹2,00,000<br/>
            Year 3: ₹1,75,000<br/>
            Year 4: ₹1,75,000
            </div>
            """, unsafe_allow_html=True)
        
        with eng_col2:
            st.markdown("""
            <div class="facility-box">
            <b>Mechanical Engineering</b><br/>
            <div style="font-size: 1.2em; font-weight: bold; color: #0066cc; margin: 10px 0;">₹6,50,000</div>
            Per 4 Years<br/>
            <hr style="margin: 10px 0;">
            • Semester Fee: ₹1,50,000<br/>
            • Donation (One-time): ₹3,00,000<br/>
            • Hostel (4 years): ₹3,50,000<br/>
            <hr style="margin: 10px 0;">
            <b>Year-wise Breakdown:</b><br/>
            Year 1: ₹2,00,000<br/>
            Year 2: ₹1,50,000<br/>
            Year 3: ₹1,50,000<br/>
            Year 4: ₹1,50,000
            </div>
            """, unsafe_allow_html=True)
        
        eng_col3, eng_col4 = st.columns(2)
        
        with eng_col3:
            st.markdown("""
            <div class="facility-box">
            <b>Electrical Engineering</b><br/>
            <div style="font-size: 1.2em; font-weight: bold; color: #0066cc; margin: 10px 0;">₹6,50,000</div>
            Per 4 Years<br/>
            <hr style="margin: 10px 0;">
            • Semester Fee: ₹1,50,000<br/>
            • Donation (One-time): ₹3,00,000<br/>
            • Hostel (4 years): ₹3,50,000<br/>
            <hr style="margin: 10px 0;">
            <b>Year-wise Breakdown:</b><br/>
            Year 1: ₹2,00,000<br/>
            Year 2: ₹1,50,000<br/>
            Year 3: ₹1,50,000<br/>
            Year 4: ₹1,50,000
            </div>
            """, unsafe_allow_html=True)
        
        with eng_col4:
            st.markdown("""
            <div class="facility-box">
            <b>Civil Engineering</b><br/>
            <div style="font-size: 1.2em; font-weight: bold; color: #0066cc; margin: 10px 0;">₹5,50,000</div>
            Per 4 Years<br/>
            <hr style="margin: 10px 0;">
            • Semester Fee: ₹1,25,000<br/>
            • Donation (One-time): ₹2,50,000<br/>
            • Hostel (4 years): ₹3,00,000<br/>
            <hr style="margin: 10px 0;">
            <b>Year-wise Breakdown:</b><br/>
            Year 1: ₹1,75,000<br/>
            Year 2: ₹1,25,000<br/>
            Year 3: ₹1,25,000<br/>
            Year 4: ₹1,25,000
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Other Programs
        st.markdown("### 📊 Other Programs")
        
        other_col1, other_col2 = st.columns(2)
        
        with other_col1:
            st.markdown("""
            <div class="facility-box">
            <b>Bachelor of Business Admin (BBA)</b><br/>
            <div style="font-size: 1.1em; font-weight: bold; color: #0066cc; margin: 10px 0;">₹4,00,000 (3 Years)</div>
            • Annual Fee: ₹1,00,000<br/>
            • Donation: ₹1,00,000<br/>
            • Hostel: ₹1,00,000<br/>
            </div>
            """, unsafe_allow_html=True)
        
        with other_col2:
            st.markdown("""
            <div class="facility-box">
            <b>Master's Programs (MBA/M.Tech)</b><br/>
            <div style="font-size: 1.1em; font-weight: bold; color: #0066cc; margin: 10px 0;">₹6,00,000 (2 Years)</div>
            • Annual Fee: ₹1,50,000<br/>
            • Donation: ₹1,50,000<br/>
            • Hostel: ₹1,50,000<br/>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">🎯 Academic Programs & Details</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 📚 Program Structure")
        
        prog_col1, prog_col2 = st.columns(2)
        
        with prog_col1:
            st.markdown("""
            <div class="facility-box">
            <b>📅 Semester Duration</b><br/>
            • 6 Months per Semester<br/>
            • 4 Semesters per Year<br/>
            • Total 8 Semesters (4 Years)<br/>
            <hr style="margin: 10px 0;">
            <b>📖 Curriculum</b><br/>
            • Theory: 70%<br/>
            • Practical/Lab: 30%<br/>
            • Industrial Visits & Workshops
            </div>
            """, unsafe_allow_html=True)
        
        with prog_col2:
            st.markdown("""
            <div class="facility-box">
            <b>🎓 Learning Outcomes</b><br/>
            ✓ Industry-Ready Skills<br/>
            ✓ Hands-on Experience<br/>
            ✓ International Standards<br/>
            <hr style="margin: 10px 0;">
            <b>📊 Assessment</b><br/>
            • Continuous Assessment: 40%<br/>
            • Semester Exams: 60%<br/>
            • Project Work & Thesis
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🏆 Featured Programs")
        
        st.markdown("""
        <div class="facility-box">
        <b>🔧 COMPUTER SCIENCE & IT</b><br/>
        Focus: AI/ML, Cloud Computing, Web Development, Cybersecurity<br/>
        Special Features: Industry partnerships, Internship guarantee, Tech conferences
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="facility-box">
        <b>⚙️ MECHANICAL ENGINEERING</b><br/>
        Focus: Automation, Robotics, Design, Manufacturing<br/>
        Special Features: State-of-the-art labs, Industry collaborations, Research projects
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="facility-box">
        <b>⚡ ELECTRICAL ENGINEERING</b><br/>
        Focus: Power Systems, Electronics, Renewable Energy<br/>
        Special Features: Advanced labs, Real-world projects, Energy research
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">🏢 Internship & Placement Programs</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        int_col1, int_col2 = st.columns(2)
        
        with int_col1:
            st.markdown("""
            <div class="facility-box">
            <b>🎯 Summer Internship</b><br/>
            <div style="font-size: 1.1em; font-weight: bold; color: #0066cc; margin: 10px 0;">2-3 Months (After Year 2)</div>
            • Top companies: TCS, Infosys, Google<br/>
            • Average Stipend: ₹15,000/month<br/>
            • 85% placement rate<br/>
            • Mentorship Program<br/>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <b>💼 Winter Internship</b><br/>
            <div style="font-size: 1.1em; font-weight: bold; color: #0066cc; margin: 10px 0;">1-2 Months (Dec-Jan)</div>
            • Leading organizations<br/>
            • Average Stipend: ₹12,000/month<br/>
            • Flexible schedule<br/>
            • Skill development focus<br/>
            </div>
            """, unsafe_allow_html=True)
        
        with int_col2:
            st.markdown("""
            <div class="facility-box">
            <b>🚀 Final Year Project</b><br/>
            <div style="font-size: 1.1em; font-weight: bold; color: #0066cc; margin: 10px 0;">6 Months (Year 4)</div>
            • Industry-based projects<br/>
            • Company mentorship<br/>
            • Publication opportunities<br/>
            • Pre-placement exposure<br/>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <b>📊 Placement Drive</b><br/>
            <div style="font-size: 1.1em; font-weight: bold; color: #0066cc; margin: 10px 0;">Annual Recruitment</div>
            • 100+ companies visit<br/>
            • Average CTC: ₹8-12 LPA<br/>
            • 98% placement rate<br/>
            • Top placements: ₹20+ LPA<br/>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🤝 Top Recruiting Companies")
        
        companies = [
            "🔵 Google", "🔴 Microsoft", "🟡 Amazon", "🟢 Apple",
            "🟣 Meta", "🔷 Goldman Sachs", "🟠 Accenture", "🔶 TCS",
            "🔵 Infosys", "🟢 Wipro", "🟡 Cognizant", "🔴 IBM"
        ]
        
        cols = st.columns(6)
        for idx, company in enumerate(companies):
            with cols[idx % 6]:
                st.markdown(f"""
                <div class="facility-box" style="text-align: center; padding: 1em;">
                <b>{company}</b>
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">🎉 Academic Events & Facilities</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 🎪 Annual Academic Events")
        
        event_col1, event_col2 = st.columns(2)
        
        with event_col1:
            st.markdown("""
            <div class="facility-box">
            <b>📅 TECHFEST (March)</b><br/>
            <div style="font-size: 0.95em; margin: 10px 0;">
            • 3-day technical festival<br/>
            • 5000+ participants<br/>
            • 30+ technical competitions<br/>
            • National level participation<br/>
            • Prize pool: ₹5 lakhs
            </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <b>🎓 CONVOCATION (May)</b><br/>
            <div style="font-size: 0.95em; margin: 10px 0;">
            • Graduation ceremony<br/>
            • 1000+ graduands<br/>
            • Chief Guest: Industry leaders<br/>
            • Campus parade & celebrations<br/>
            • Family participation
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        with event_col2:
            st.markdown("""
            <div class="facility-box">
            <b>🔬 RESEARCH SYMPOSIUM (July)</b><br/>
            <div style="font-size: 0.95em; margin: 10px 0;">
            • Student research showcase<br/>
            • 200+ research papers<br/>
            • Faculty presentations<br/>
            • Industry collaboration<br/>
            • Publication opportunities
            </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <b>🎨 CULTURAL FEST (Sept)</b><br/>
            <div style="font-size: 0.95em; margin: 10px 0;">
            • 2-day cultural celebration<br/>
            • 50+ cultural events<br/>
            • Prize pool: ₹3 lakhs<br/>
            • National performances<br/>
            • Alumni participation
            </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🏛️ Campus Facilities")
        
        fac_col1, fac_col2 = st.columns(2)
        
        with fac_col1:
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2em; margin-bottom: 10px;">📚</div>
            <b>Central Library</b><br/>
            500K+ books | 50+ journals | Digital resources
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2em; margin-bottom: 10px;">💻</div>
            <b>Computing Labs</b><br/>
            20+ labs | 500+ systems | Latest software
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2em; margin-bottom: 10px;">🔬</div>
            <b>Research Facilities</b><br/>
            Advanced labs | Equipment | Industry partnerships
            </div>
            """, unsafe_allow_html=True)
        
        with fac_col2:
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2em; margin-bottom: 10px;">🏃</div>
            <b>Sports Complex</b><br/>
            Gym, Pool, Courts | Sports coaching
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2em; margin-bottom: 10px;">🎓</div>
            <b>Auditorium</b><br/>
            2000 capacity | State-of-the-art AV
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="facility-box">
            <div style="font-size: 2em; margin-bottom: 10px;">🍽️</div>
            <b>Dining & Recreation</b><br/>
            Cafeteria, Lounge | Student spaces
            </div>
            """, unsafe_allow_html=True)

elif page == "📋 Academics":
    st.markdown('<h2 class="section-header">📋 ACADEMIC CALENDAR & SCHEDULE</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Semester tabs
    tab_sem1, tab_sem2, tab_sem3, tab_sem4, tab_sem5, tab_sem6, tab_sem7, tab_sem8 = st.tabs(
        ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6", "Sem 7", "Sem 8 (Final)"]
    )
    
    # Semester 1 - Fall 2025
    with tab_sem1:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">📚 SEMESTER 1 - FALL 2025</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #0066cc; margin-bottom: 15px;">📅 Duration: August 25 - December 19 (24 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Aug 25: Classes Begin<br/>
        🔹 Sep 2-3: Orientation & Campus Tour<br/>
        🔹 Sep 15: Independence Day (Holiday)<br/>
        🔹 Oct 2: Gandhi Jayanti (Holiday)<br/>
        🔹 Oct 15-20: IA-1 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Nov 2-8: Diwali Break (5 Days)<br/>
        🔹 Nov 15-20: IA-2 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Dec 1-7: IA-3 (Internal Assessment) - Final Internal Test<br/>
        🔹 Dec 10-19: SEMESTER-1 FINAL EXAMS
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Programming Fundamentals<br/>
        📝 Subject 2: Mathematics I<br/>
        📝 Subject 3: Physics Basics<br/>
        📝 Subject 4: Communication Skills
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 30% | Attendance: 10% | Semester Exam: 60%
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Semester 2 - Spring 2026
    with tab_sem2:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">📚 SEMESTER 2 - SPRING 2026</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #0066cc; margin-bottom: 15px;">📅 Duration: January 12 - May 8 (24 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Jan 12: Classes Begin<br/>
        🔹 Jan 26: Republic Day (Holiday)<br/>
        🔹 Feb 1-8: IA-1 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Mar 8-15: Holi Break (7 Days)<br/>
        🔹 Mar 20-27: IA-2 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Apr 10-15: Good Friday & Easter Break<br/>
        🔹 Apr 25-May 2: IA-3 (Internal Assessment) - Final Internal Test<br/>
        🔹 May 5-8: SEMESTER-2 FINAL EXAMS
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Advanced Programming<br/>
        📝 Subject 2: Mathematics II<br/>
        📝 Subject 3: Chemistry Basics<br/>
        📝 Subject 4: Professional Development
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 30% | Attendance: 10% | Semester Exam: 60%
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Semester 3
    with tab_sem3:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">📚 SEMESTER 3 - FALL 2026</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #0066cc; margin-bottom: 15px;">📅 Duration: August 22 - December 18 (24 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Aug 22: Classes Begin<br/>
        🔹 Sep 15: Independence Day (Holiday)<br/>
        🔹 Oct 5-12: IA-1 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Oct 15: Dussehra (Holiday)<br/>
        🔹 Nov 5-12: IA-2 (Internal Assessment)<br/>
        🔹 Nov 8: Diwali (Holiday)<br/>
        🔹 Dec 1-8: IA-3 (Internal Assessment) - Final Internal Test<br/>
        🔹 Dec 10-18: SEMESTER-3 FINAL EXAMS
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Data Structures<br/>
        📝 Subject 2: Discrete Mathematics<br/>
        📝 Subject 3: Digital Logic<br/>
        📝 Subject 4: Technical Writing
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 30% | Attendance: 10% | Semester Exam: 60%
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Semester 4
    with tab_sem4:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">📚 SEMESTER 4 - SPRING 2027</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #0066cc; margin-bottom: 15px;">📅 Duration: January 11 - May 7 (24 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Jan 11: Classes Begin<br/>
        🔹 Jan 26: Republic Day (Holiday)<br/>
        🔹 Feb 10-17: IA-1 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Mar 10-17: Holi Break & IA-2 (Internal Assessment)<br/>
        🔹 Apr 5-12: IA-3 (Internal Assessment) - Final Internal Test<br/>
        🔹 Apr 28-May 7: SEMESTER-4 FINAL EXAMS
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Database Management<br/>
        📝 Subject 2: Web Technologies<br/>
        📝 Subject 3: Software Engineering<br/>
        📝 Subject 4: Embedded Systems
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 30% | Attendance: 10% | Semester Exam: 60%
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Semester 5
    with tab_sem5:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">📚 SEMESTER 5 - FALL 2027</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #0066cc; margin-bottom: 15px;">📅 Duration: August 21 - December 17 (24 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Aug 21: Classes Begin<br/>
        🔹 Sep 15: Independence Day (Holiday)<br/>
        🔹 Oct 3-10: IA-1 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Nov 1-8: IA-2 (Internal Assessment) & Diwali Break<br/>
        🔹 Dec 1-8: IA-3 (Internal Assessment) - Final Internal Test<br/>
        🔹 Dec 10-17: SEMESTER-5 FINAL EXAMS<br/>
        🔹 Dec 20: INTERNSHIP BEGINS
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Operating Systems<br/>
        📝 Subject 2: Networking Fundamentals<br/>
        📝 Subject 3: Compiler Design<br/>
        📝 Subject 4: Artificial Intelligence
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 30% | Attendance: 10% | Semester Exam: 60%
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Semester 6
    with tab_sem6:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #dc3545; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">🎯 SEMESTER 6 - FINAL SEMESTER (SPRING 2028)</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #dc3545; margin-bottom: 15px;">📅 Duration: January 9 - May 5 (24 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #dc3545; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Jan 9: INTERNSHIP ENDS & Classes Begin<br/>
        🔹 Jan 26: Republic Day (Holiday)<br/>
        🔹 Feb 8-15: IA-1 (Internal Assessment) - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Mar 5-12: Holi Break & IA-2 (Internal Assessment)<br/>
        🔹 Apr 8-15: IA-3 (Internal Assessment) - Final Internal Test<br/>
        🔹 Apr 28-May 5: SEMESTER-6 FINAL EXAMS (LAST EXAMS)<br/>
        🔹 May 15: PROJECT PRESENTATION & VIVA<br/>
        🔹 May 25: CONVOCATION CEREMONY
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #dc3545; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Cloud Computing<br/>
        📝 Subject 2: Machine Learning<br/>
        📝 Subject 3: Cybersecurity<br/>
        📝 Subject 4: Capstone Project
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #dc3545; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 30% | Attendance: 10% | Semester Exam: 60%<br/>
        + Project & Viva: 20% (Additional)
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Semester 7 & 8 - Optional
    with tab_sem7:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">📚 SEMESTER 7 - FALL 2028</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #0066cc; margin-bottom: 15px;">📅 Duration: August 26 - December 22 (24 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Aug 26: Classes Begin<br/>
        🔹 Oct 5-12: IA-1 - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Nov 5-12: IA-2<br/>
        🔹 Dec 1-8: IA-3 - Final Internal Test<br/>
        🔹 Dec 10-22: SEMESTER-7 FINAL EXAMS
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Advanced Algorithms<br/>
        📝 Subject 2: Distributed Systems<br/>
        📝 Subject 3: Mobile Development<br/>
        📝 Subject 4: Research Methods
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 30% | Attendance: 10% | Semester Exam: 60%
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab_sem8:
        st.markdown("""
        <div class="facility-box">
        <h2 style="color: #0066cc; font-size: 2.2em; font-weight: bold; margin-bottom: 20px;">📚 SEMESTER 8 - FINAL SEMESTER (SPRING 2029)</h2>
        <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
        <div style="font-size: 1.3em; font-weight: bold; color: #0066cc; margin-bottom: 15px;">📅 Duration: January 9 - April 30 (18 Weeks)</div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📌 IMPORTANT DATES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🔹 Jan 9: Classes Begin<br/>
        🔹 Feb 15-22: IA-1 - Subjects: Subject 1, Subject 2, Subject 3, Subject 4<br/>
        🔹 Mar 15-22: IA-2<br/>
        🔹 Apr 1-8: IA-3 - Final Internal Test<br/>
        🔹 Apr 15-30: SEMESTER-8 FINAL EXAMS & PROJECT VIVA
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">📖 SUBJECTS:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        📝 Subject 1: Advanced Project Management<br/>
        📝 Subject 2: Cloud Computing<br/>
        📝 Subject 3: Cyber Security<br/>
        📝 Subject 4: Professional Ethics & Internship
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🎓 GRADING SYSTEM:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        IA (3 Tests): 25% | Project: 25% | Viva: 10% | Semester Exam: 40%
        </div><br/>
        
        <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">🏆 POST-EXAM ACTIVITIES:</div>
        <div style="font-weight: normal; margin-left: 10px;">
        🎯 Placement Drive: May-June<br/>
        🎯 Graduation Ceremony: June 2029<br/>
        🎯 Final Semester Result: May 31, 2029
        </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Summary Information
    st.markdown("""
    <div class="facility-box">
    <h3 style="font-size: 2.2em; color: #0066cc; margin-bottom: 15px; font-weight: bold;">📊 IA (INTERNAL ASSESSMENT) SYSTEM</h3>
    <div style="font-size: 1.2em; line-height: 2; font-weight: normal;">
    <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">Each Semester has 3 Internal Assessment Tests:</div>
    <div style="font-weight: normal; margin-left: 10px;">
    🔹 <b>IA-1:</b> Month 1 (40% of semester)<br/>
    🔹 <b>IA-2:</b> Month 2-3 (Middle of semester)<br/>
    🔹 <b>IA-3:</b> Month 5-6 (Final month before exams)
    </div><br/>
    
    <div style="font-weight: normal;">
    🔹 <b>Subjects per Semester:</b> 4 Different Subjects<br/>
    🔹 <b>Test Duration:</b> 1 hour each<br/>
    🔹 <b>IA Weightage:</b> 30% of total marks<br/>
    🔹 <b>Final Semester:</b> IA + Project Presentation (Total 50%)
    </div><br/>
    
    <div style="font-size: 1.15em; font-weight: bold; color: #0066cc; margin-bottom: 10px;">HOLIDAYS & FUNCTIONS:</div>
    <div style="font-weight: normal; margin-left: 10px;">
    • Independence Day (Sep 15)<br/>
    • Dussehra/Diwali (Oct-Nov)<br/>
    • Republic Day (Jan 26)<br/>
    • Holi (Mar)<br/>
    • Cultural & Sports Events (Throughout Year)
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "💰 Finance":
    st.markdown('<h2 class="section-header">💰 FINANCIAL INFORMATION</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Large Finance Boxes
    fin_col1, fin_col2, fin_col3 = st.columns(3)
    
    with fin_col1:
        st.markdown("""
        <div class="facility-box" style="text-align: center; padding: 2.5em;">
        <div style="font-size: 2.5em; margin-bottom: 15px;">👨‍🎓</div>
        <h3 style="font-size: 1.5em; margin: 15px 0; color: #0066cc;">UNDERGRADUATE</h3>
        <div style="font-size: 2.2em; font-weight: bold; color: #0066cc; margin: 20px 0;">₹3,000</div>
        <p style="font-size: 1.1em; margin: 5px 0;">Per Semester</p>
        <p style="font-size: 0.95em; margin-top: 15px; line-height: 1.6;">
        4-Year Program<br/>
        Engineering & Sciences<br/>
        Full Facilities Access
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with fin_col2:
        st.markdown("""
        <div class="facility-box" style="text-align: center; padding: 2.5em;">
        <div style="font-size: 2.5em; margin-bottom: 15px;">🎓</div>
        <h3 style="font-size: 1.5em; margin: 15px 0; color: #0066cc;">POSTGRADUATE</h3>
        <div style="font-size: 2.2em; font-weight: bold; color: #0066cc; margin: 20px 0;">₹4,000</div>
        <p style="font-size: 1.1em; margin: 5px 0;">Per Semester</p>
        <p style="font-size: 0.95em; margin-top: 15px; line-height: 1.6;">
        2-Year Program<br/>
        MBA & M.Tech<br/>
        Advanced Facilities
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with fin_col3:
        st.markdown("""
        <div class="facility-box" style="text-align: center; padding: 2.5em;">
        <div style="font-size: 2.5em; margin-bottom: 15px;">🌍</div>
        <h3 style="font-size: 1.5em; margin: 15px 0; color: #0066cc;">INTERNATIONAL</h3>
        <div style="font-size: 2.2em; font-weight: bold; color: #0066cc; margin: 20px 0;">₹6,000+</div>
        <p style="font-size: 1.1em; margin: 5px 0;">Per Semester</p>
        <p style="font-size: 0.95em; margin-top: 15px; line-height: 1.6;">
        All Programs<br/>
        International Students<br/>
        Premium Services
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hostel Fees - Large
    st.markdown("""
    <div class="facility-box">
    <h2 style="font-size: 1.8em; color: #0066cc; margin-bottom: 20px;">🏢 HOSTEL FEES (Included in Total Package)</h2>
    <div style="font-size: 1.3em; line-height: 2;">
    🛏️ <b>Single Room:</b> <span style="color: #0066cc; font-size: 1.2em;">₹3,000</span>/Semester<br/>
    🛏️ <b>Double Room:</b> <span style="color: #0066cc; font-size: 1.2em;">₹2,000</span>/Semester<br/>
    🛏️ <b>Triple Room:</b> <span style="color: #0066cc; font-size: 1.2em;">₹1,500</span>/Semester<br/><br/>
    
    <b style="font-size: 1.15em;">✅ INCLUDED IN HOSTEL FEES:</b><br/>
    ✓ All Meals (Breakfast, Lunch, Dinner, Snacks)<br/>
    ✓ WiFi 24/7 High-Speed Internet<br/>
    ✓ Utilities (Water, Electricity)<br/>
    ✓ Laundry Service (2x per week)<br/>
    ✓ 24/7 Security & CCTV<br/>
    ✓ Maintenance & Cleaning
    </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "📊 Analytics":
    st.markdown('<h2 class="section-header">📊 ANALYTICS DASHBOARD</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load latest analytics
    analytics_data = load_analytics()
    
    # Key Metrics
    st.markdown('<h3 style="font-size: 2.5em; color: #0066cc; margin-bottom: 20px;">📈 KEY METRICS</h3>', unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center; padding: 2em;">
        <div style="font-size: 3em; margin-bottom: 15px;">❓</div>
        <h3 style="font-size: 2em; margin: 0; color: #0066cc;">TOTAL QUERIES</h3>
        <div style="font-size: 3em; font-weight: bold; color: #0066cc; margin: 15px 0;">{analytics_data['total_queries']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center; padding: 2em;">
        <div style="font-size: 3em; margin-bottom: 15px;">✅</div>
        <h3 style="font-size: 2em; margin: 0; color: #28a745;">HIGH CONFIDENCE</h3>
        <div style="font-size: 3em; font-weight: bold; color: #28a745; margin: 15px 0;">{analytics_data['high_confidence']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center; padding: 2em;">
        <div style="font-size: 3em; margin-bottom: 15px;">⚠️</div>
        <h3 style="font-size: 2em; margin: 0; color: #ffc107;">LOW CONFIDENCE</h3>
        <div style="font-size: 3em; font-weight: bold; color: #ffc107; margin: 15px 0;">{analytics_data['low_confidence']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center; padding: 2em;">
        <div style="font-size: 3em; margin-bottom: 15px;">📚</div>
        <h3 style="font-size: 2em; margin: 0; color: #0066cc;">LEARNED ANSWERS</h3>
        <div style="font-size: 3em; font-weight: bold; color: #0066cc; margin: 15px 0;">{analytics_data['learned_answers']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top Questions
    if analytics_data['top_questions']:
        st.markdown('<h3 style="font-size: 2.5em; color: #0066cc; margin-bottom: 20px;">🔝 TOP ASKED QUESTIONS</h3>', unsafe_allow_html=True)
        
        sorted_questions = sorted(analytics_data['top_questions'].items(), key=lambda x: x[1], reverse=True)
        
        for idx, (question, count) in enumerate(sorted_questions[:10], 1):
            st.markdown(f"""
            <div class="facility-box">
            <h4 style="font-size: 1.8em; margin-top: 0; color: #0066cc;">#{idx}. {question}</h4>
            <p style="font-size: 1.5em; margin: 0;"><b>Asked {count} times</b></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📊 No queries recorded yet. Start asking questions to see analytics!")
    
    st.markdown("---")
    
    # User Feedback Summary
    if analytics_data['user_feedback']:
        st.markdown('<h3 style="font-size: 2.5em; color: #0066cc; margin-bottom: 20px;">👍 USER FEEDBACK SUMMARY</h3>', unsafe_allow_html=True)
        
        helpful = sum(1 for f in analytics_data['user_feedback'] if f['rating'] == 'helpful')
        somewhat = sum(1 for f in analytics_data['user_feedback'] if f['rating'] == 'somewhat')
        not_helpful = sum(1 for f in analytics_data['user_feedback'] if f['rating'] == 'not_helpful')
        
        feedback_col1, feedback_col2, feedback_col3 = st.columns(3)
        
        with feedback_col1:
            st.markdown(f"""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2.5em;">👍</div>
            <h4 style="font-size: 1.8em; color: #28a745;">Helpful</h4>
            <p style="font-size: 2em; font-weight: bold; color: #28a745;">{helpful}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feedback_col2:
            st.markdown(f"""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2.5em;">🤔</div>
            <h4 style="font-size: 1.8em; color: #ffc107;">Somewhat</h4>
            <p style="font-size: 2em; font-weight: bold; color: #ffc107;">{somewhat}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feedback_col3:
            st.markdown(f"""
            <div class="facility-box" style="text-align: center;">
            <div style="font-size: 2.5em;">👎</div>
            <h4 style="font-size: 1.8em; color: #dc3545;">Not Helpful</h4>
            <p style="font-size: 2em; font-weight: bold; color: #dc3545;">{not_helpful}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "🎓 Learning":
    st.markdown('<h2 class="section-header">🎓 LEARNING - ADD QUESTIONS</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # SECTION 1: STUDENT QUESTIONS AT TOP
    st.markdown('<h3 style="font-size: 2.4em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">👨‍🎓 ADD YOUR QUESTIONS HERE</h3>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 1.5em; font-weight: bold; color: #666; margin-bottom: 30px;">💡 Students asking questions help expand our knowledge base. Submit your AI-related questions below!</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h4 style="font-size: 1.8em; color: #0066cc; font-weight: bold;">❓ NEW AI QUESTION</h4>', unsafe_allow_html=True)
        new_question = st.text_area("Enter your AI-related question:", height=100, key="new_q", placeholder="e.g., What is Generative AI?")
    
    with col2:
        st.markdown('<h4 style="font-size: 1.8em; color: #0066cc; font-weight: bold;">✍️ ANSWER</h4>', unsafe_allow_html=True)
        new_answer = st.text_area("Enter the detailed answer:", height=100, key="new_a", placeholder="e.g., Generative AI refers to...")
    
    st.markdown("---")
    
    col_submit, col_clear = st.columns(2)
    
    with col_submit:
        if st.button("📤 SUBMIT NEW Q&A", key="submit_qa"):
            if new_question and new_answer:
                # Add to FAQ dictionary
                faqs[new_question] = new_answer
                
                # Update analytics
                analytics_data["learned_answers"] += 1
                save_analytics(analytics_data)
                
                st.success("✅ AI Question & Answer successfully added!")
                st.balloons()
            else:
                st.error("⚠️ Please fill in both question and answer fields!")
    
    with col_clear:
        if st.button("🗑️ CLEAR FIELDS", key="clear_fields"):
            st.rerun()
    
    st.markdown("---")
    st.markdown('<h3 style="font-size: 2em; font-weight: bold; color: #0066cc; margin-bottom: 20px;">✨ CONTRIBUTION STATS</h3>', unsafe_allow_html=True)
    
    analytics_data = load_analytics()
    
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center;">
        <div style="font-size: 2.5em;">📚</div>
        <h4 style="font-size: 1.8em; color: #0066cc;">TOTAL QUESTIONS</h4>
        <p style="font-size: 2.5em; font-weight: bold; color: #0066cc;">{len(faqs)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
        <div class="facility-box" style="text-align: center;">
        <div style="font-size: 2.5em;">🎓</div>
        <h4 style="font-size: 1.8em; color: #0066cc;">NEW CONTRIBUTIONS</h4>
        <p style="font-size: 2.5em; font-weight: bold; color: #0066cc;">{analytics_data["learned_answers"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("---")
    
    # SECTION 2: PREFERRED QUESTIONS AT BOTTOM
    st.markdown('<h2 style="font-size: 2.8em; font-weight: bold; color: #0066cc; margin-top: 40px; margin-bottom: 20px;">⭐ TOP 15 PREFERRED AI QUESTIONS</h2>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 1.5em; font-weight: bold; color: #666; margin-bottom: 30px;">🔝 These are the most preferred and frequently asked questions by students</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top 15 AI-Related Preferred Questions
    preferred_questions = {
        "What is Artificial Intelligence?": "Artificial Intelligence (AI) is the simulation of human intelligence processes by computers. It involves learning from experience, recognizing patterns, and performing tasks that typically require human intelligence.",
        "What is Machine Learning?": "Machine Learning is a subset of AI where systems learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data and make predictions.",
        "What is Deep Learning?": "Deep Learning is a subset of Machine Learning based on artificial neural networks with multiple layers. It's used for complex tasks like image recognition, natural language processing, and speech recognition.",
        "What are Neural Networks?": "Neural Networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information and are fundamental to deep learning.",
        "What is Natural Language Processing (NLP)?": "NLP is a branch of AI that focuses on enabling computers to understand, interpret, and generate human language in a meaningful way.",
        "What is Computer Vision?": "Computer Vision is an AI field that enables machines to interpret and understand visual information from images and videos, similar to human vision.",
        "What is Supervised Learning?": "Supervised Learning is a machine learning approach where models are trained on labeled data. The algorithm learns to map inputs to known outputs.",
        "What is Unsupervised Learning?": "Unsupervised Learning involves training models on unlabeled data. The algorithm discovers hidden patterns and structures in the data without predefined outputs.",
        "What is Reinforcement Learning?": "Reinforcement Learning is a machine learning paradigm where an agent learns through interaction with an environment, receiving rewards or penalties for actions.",
        "What is Data Science?": "Data Science combines statistics, programming, and domain expertise to extract meaningful insights from data. It's closely related to AI and machine learning applications.",
        "What are AI Applications in Real World?": "AI is used in recommendation systems, autonomous vehicles, medical diagnosis, chatbots, fraud detection, image recognition, and many other real-world applications.",
        "How does AI impact Education?": "AI in education enables personalized learning, adaptive tutoring systems, automated grading, student performance analysis, and intelligent educational content delivery.",
        "What is Transfer Learning in AI?": "Transfer Learning is a machine learning technique where a model trained on one task is adapted for another task, saving time and improving performance with limited data.",
        "What are AI Ethics and Concerns?": "AI ethics addresses concerns like bias in algorithms, privacy, job displacement, transparency, accountability, and ensuring AI systems are fair and responsible.",
        "What is the Future of AI?": "The future of AI includes advanced autonomous systems, quantum computing integration, improved AI safety, more human-AI collaboration, and AI applications in healthcare, climate change, and scientific research."
    }
    
    # Display all 15 questions
    for idx, (question, answer) in enumerate(preferred_questions.items(), 1):
        st.markdown(f"""
        <div class="facility-box" style="border-left: 6px solid #0066cc; margin-bottom: 20px;">
        <h3 style="font-size: 2em; font-weight: bold; color: #0066cc; margin-top: 0; margin-bottom: 15px;">
        ❓ #{idx}. {question}
        </h3>
        <p style="font-size: 1.4em; line-height: 1.8; color: #333; margin: 0;">
        {answer}
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("🚀 Keep learning and contributing to make our AI knowledge base more comprehensive!")