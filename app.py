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
    
    with st.form("project_submission_form"):
        topic_choice = st.selectbox(
            "Select your Hackathon Topic Area:",
            ["🌿 Environment", "🏥 Health", "📚 Education", "🐾 Animal Welfare", "🤖 Smart Cities"]
        )
        proj_name = st.text_input("Project / App Name:", placeholder="What are you calling your solution?")
        proj_desc = st.text_area("Description:", placeholder="Describe how your app solves a problem in 1 sentence...")
        
        submit_btn = st.form_submit_with_button_label("Send Data ⚡")
        
        if submit_btn:
            if not student_id:
                st.error("❌ Submission Failed! You must enter a Student ID or Team Name in the left sidebar first.")
            elif not proj_name or not proj_desc:
                st.error("❌ Submission Failed! Please fill out all form text fields before sending.")
            else:
                new_record = {
                    "team_name": student_id,
                    "user_name": student_id,
                    "topic": topic_choice,
                    "project_name": proj_name,
                    "desc": proj_desc
                }
                st.session_state.mock_db.insert(0, new_record)
                st.success(f"🎉 Success! Data packet uploaded smoothly under identifier: **{student_id}**")
                st.info("Head over to the next tab ('Data Viewer Dashboard') to check your record live!")

# ==========================================
# TAB 2: DATA VIEWER DASHBOARD (Module 2)
# ==========================================
with app_mode[1]:
    st.subheader("📊 Live Data Viewer Dashboard")
    st.write("This feed reads records directly out of our cloud tables. Look for your project below!")
    
    if len(st.session_state.mock_db) == 0:
        st.info("The database is currently clear. Go to the Form Submission tab to write an entry.")
    else:
        for idx, entry in enumerate(st.session_state.mock_db):
            with st.container():
                st.markdown(f"### 📦 Record #{idx+1}: {entry['project_name']}")
                st.markdown(f"**Submitted by:** `{entry['team_name']}` | **Official Track Tag:** **[{entry['topic']}]**")
                st.write(f"*Solution Narrative:* {entry['desc']}")
                st.markdown("---")

# ==========================================
# TAB 3: UI DESIGN & STATE (Module 3)
# ==========================================
with app_mode[2]:
    st.subheader("🎨 Understand Dynamic Application States")
    st.write("An app changes its look based on variables. Slide the controls below to see it change live.")
    
    accent_color = st.selectbox("Choose a UI Accent Color:", ["Default Blue", "Alert Red", "Success Green"])
    user_font_size = st.slider("Adjust Welcome Font Size:", min_value=16, max_value=32, value=20)
    
    st.markdown("---")
    if accent_color == "Default Blue":
        st.info(f"### <p style='font-size:{user_font_size}px;'>Welcome to your Dashboard</p>", unsafe_allow_html=True)
    elif accent_color == "Alert Red":
        st.error(f"### <p style='font-size:{user_font_size}px;'>🚨 CRITICAL SYSTEM NOTICE</p>", unsafe_allow_html=True)
    elif accent_color == "Success Green":
        st.success(f"### <p style='font-size:{user_font_size}px;'>✅ Application Online and Secure</p>", unsafe_allow_html=True)

# ==========================================
# TAB 4: DATA CHARTING (Module 4)
# ==========================================
with app_mode[3]:
    st.subheader("Data Analytics & Visualization")
    st.write("Most winning hackathon apps don't
