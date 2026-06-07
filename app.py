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
    st.write("Most winning hackathon apps don't just collect data—they show it beautifully.")
    st.write("Imagine your app is tracking user survey feedback. Adjust the metric scores below:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        score_a = st.number_input("Usability Score (1-10):", min_value=1, max_value=10, value=7)
    with col2:
        score_b = st.number_input("Design Rating (1-10):", min_value=1, max_value=10, value=6)
    with col3:
        score_c = st.number_input("Impact Score (1-10):", min_value=1, max_value=10, value=8)
        
    chart_data = {
        "Metric": ["Usability", "Design", "Impact"],
        "Score out of 10": [score_a, score_b, score_c]
    }
    st.bar_chart(data=chart_data, x="Metric", y="Score out of 10")

# ==========================================
# TAB 5: UNIVERSAL HACK-TOOLS (Module 5)
# ==========================================
with app_mode[4]:
    st.subheader("🧰 The Universal Hackathon Toolkit")
    st.write("Master these two features; they work for every single hackathon topic!")

    st.markdown("### 🔍 Feature 1: Real-Time Category Filtering")
    filter_choice = st.selectbox(
        "Simulate filtering a live database by topic:",
        ["Show All Topics", "🌿 Environment", "🏥 Health", "📚 Education", "🐾 Animal Welfare", "🤖 Smart Cities"]
    )
    
    st.write("---")
    for project in st.session_state.mock_db:
        if filter_choice == "Show All Topics" or filter_choice in project["topic"]:
            with st.container():
                st.markdown(f"**{project['project_name']}** ({project['topic']})")
                st.write(project["desc"])
                st.markdown("---")

    st.markdown("### 🚨 Feature 2: Condition Alerts & Flags")
    system_load = st.slider("Simulate an App System Metric (e.g., Battery level, Air Quality index, Wait Time):", 0, 100, 45)
    
    if system_load < 30:
        st.success(f"💚 Status Green ({system_load}%): Environment is completely stable and optimal.")
    elif 30 <= system_load <= 70:
        st.warning(f"⚠️ Status Yellow ({system_load}%): Moderate activity detected. Monitor closely.")
    else:
        st.error(f"🚨 Status Red ({system_load}%): CRITICAL LIMIT BREACHED! Dispatch immediate team.")

# ==========================================
# TAB 6: LAYOUT STUDIO (Module 6)
# ==========================================
with app_mode[5]:
    st.subheader("📐 The App Layout Studio")
    st.write("By default, Streamlit stacks everything vertically. Use these tools to arrange your app like a pro!")

    st.markdown("### 🗂️ Grid Layouts: Columns")
    col_layout = st.radio("Choose a column structure:", ["2 Equal Columns", "3 Equal Columns"])
    
    if col_layout == "2 Equal Columns":
        c1, c2 = st.columns(2)
        with c1:
            st.info("📦 **Column 1 Data Card**\n\nPerfect for displaying a primary metric or summary.")
        with c2:
            st.success("🎨 **Column 2 User Actions**\n\nPerfect for buttons, dropdowns, or forms.")
    elif col_layout == "3 Equal Columns":
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="🌿 Environment Score", value="92%", delta="↑ 4%")
        with c2:
            st.metric(label="🏥 Health App Pings", value="14", delta="-2")
        with c3:
            st.metric(label="🤖 Smart Grid Nodes", value="450", delta="Stable")

    st.markdown("---")
    st.markdown("### 🔽 Clean UI: Collapsible Expanders")
    
    with st.expander("❓ Click here to read the Hackathon Judging Criteria"):
        st.write("1. **Innovation (25%):** How unique is the solution?")
        st.write("2. **Technical Execution (25%):** Did you connect your frontend UI to the cloud database successfully?")
        st.write("3. **Design & Layout (25%):** Is the app clean, organized, and easy for a judge to navigate?")
        st.write("4. **Presentation (25%):** How well did you pitch your app concept?")
        st.caption("🔒 Verification Code: LAYOUT_MASTER_2026")

# ==========================================
# TAB 7: MEDIA & STYLING LAB (Module 7)
# ==========================================
with app_mode[6]:
    st.subheader("🎨 The Media & Styling Lab")
    st.write("Learn how to
