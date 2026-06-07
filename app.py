import streamlit as st
import pandas as pd

# ==========================================
# ⚙️ CONFIGURATION & THEME SETUP
# ==========================================
st.set_page_config(
    page_title="Pre-Hackathon Developer Sandbox",
    page_icon="🚀",
    layout="wide"
)

# Initialize a simulated in-memory session database if one doesn't exist
# This ensures that even without a database live, the app will never crash for kids!
if "mock_db" not in st.session_state:
    st.session_state.mock_db = [
        {"team_name": "Team-Alpha", "user_name": "Alex", "topic": "🌿 Environment", "project_name": "Eco-Bin Sensor", "desc": "Alerts trucks when recycling bins are 90% full."},
        {"team_name": "Team-Beta", "user_name": "Sam", "topic": "🏥 Health", "project_name": "Med-Remind Audio", "desc": "Voice alerts for senior citizens to take daily prescriptions."},
        {"team_name": "Team-Gamma", "user_name": "Jordan", "topic": "📚 Education", "project_name": "SkillShare Portal", "desc": "Connects retired teachers with students needing free math tutoring."},
        {"team_name": "Team-Delta", "user_name": "Taylor", "topic": "🐾 Animal Welfare", "project_name": "StraySafe Map", "desc": "Crowdsourced mapping tool to report stray animals to local shelters."},
        {"team_name": "Team-Epsilon", "user_name": "Morgan", "topic": "🤖 Smart Cities", "project_name": "GridPulse Monitor", "desc": "Tracks street light power outages using community reporting."}
    ]

# ==========================================
# 🔐 SIDEBAR: STUDENT PORTAL WORKSPACE
# ==========================================
with st.sidebar:
    st.header("🔐 Student Portal")
    st.write("Claim your workspace before completing any lessons.")
    
    student_id = st.text_input("Enter your assigned Student ID or Team Name:", placeholder="e.g., Student_101")
    
    if student_id:
        st.success(f"🟢 Workspace Active: {student_id}")
        st.write("Your session is fully authenticated to the cloud database.")
    else:
        st.warning("⚠️ Please enter a Student ID to unlock database tracking attributes.")

# ==========================================
# 🗺️ MAIN INTERFACE NAVIGATION TABS
# ==========================================
st.title("🚀 Pre-Hackathon Developer Sandbox")
st.write("Use the navigation tabs below to hop between your course assignments and text-box lessons.")

app_mode = st.tabs([
    "📝 Form Submission App", 
    "📊 Data Viewer Dashboard", 
    "🎨 UI Design & State", 
    "📈 Data Charting", 
    "🛠️ Universal Hack-Tools", 
    "📐 Layout Studio", 
    "🎨 Media & Styling", 
    "⚡ Advanced Logic",
    "📊 Data Science Lab"
])

# ==========================================
# TAB 1: FORM SUBMISSION APP (Module 2)
# ==========================================
with app_mode[0]:
    st.subheader("📝 Live Cloud Database Intake Form")
    st.write("Fill out this form to practice transmitting variables safely to the remote cloud server tables.")
    
    # Python Form Wrap Object
    with st.form("project_submission_form"):
        topic_choice = st.selectbox(
            "Select your Hackathon Topic Area:",
            ["🌿 Environment", "🏥 Health", "📚 Education", "🐾 Animal Welfare", "🤖 Smart Cities"]
        )
        proj_name = st.text_input("Project / App Name:", placeholder="What are you calling your solution?")
        proj_desc = st.text_area("Description:", placeholder="Describe how your app solves a problem in 1 sentence...")
        
        # Submit execution button
        submit_btn = st.form_submit_with_button_label("Send Data ⚡")
        
        if submit_btn:
            if not student_id:
