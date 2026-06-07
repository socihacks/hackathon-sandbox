import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Sandbox",
    page_icon="🚀",
    layout="wide"
)

if "mock_db" not in st.session_state:
    st.session_state.mock_db = [
        {"team_name": "Team-Alpha", "user_name": "Alex", "topic": "🌿 Environment", "project_name": "Eco-Bin Sensor", "desc": "Bin monitor."},
        {"team_name": "Team-Beta", "user_name": "Sam", "topic": "🏥 Health", "project_name": "Med-Remind Audio", "desc": "Pill alerts."},
        {"team_name": "Team-Gamma", "user_name": "Jordan", "topic": "📚 Education", "project_name": "SkillShare Portal", "desc": "Tutor app."},
        {"team_name": "Team-Delta", "user_name": "Taylor", "topic": "🐾 Animal Welfare", "project_name": "StraySafe Map", "desc": "Shelter map."},
        {"team_name": "Team-Epsilon", "user_name": "Morgan", "topic": "🤖 Smart Cities", "project_name": "GridPulse Monitor", "desc": "Grid tracker."}
    ]

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.header("🔐 Portal")
    student_id = st.text_input("Enter ID:", placeholder="e.g., Student_101")
    if student_id:
        st.success(f"🟢 Active: {student_id}")
    else:
        st.warning("⚠️ Enter ID.")

# ==========================================
# NAVIGATION TABS
# ==========================================
st.title("🚀 Sandbox App")

app_mode = st.tabs([
    "📝 Form Submission", 
    "📊 Data Dashboard", 
    "🎨 UI State", 
    "📈 Data Charting", 
    "🛠️ Hack-Tools", 
    "📐 Layout Studio", 
    "🎨 Media Lab", 
    "⚡ Advanced Logic",
    "📊 Data Science"
])

# TAB 1
with app_mode[0]:
    st.subheader("📝 Intake Form")
    with st.form("project_form"):
        topic_choice = st.selectbox("Track:", ["🌿 Environment", "🏥 Health", "📚 Education", "🐾 Animal Welfare", "🤖 Smart Cities"])
        proj_name = st.text_input("App Name:")
        proj_desc = st.text_area("Description:")
        
        submit_btn = st.form_submit_button("Send Data ⚡")
        
        if submit_btn:
            if not student_id:
                st.error("❌ Need ID")
            elif not proj_name or not proj_desc:
                st.error("❌ Fields empty")
            else:
                new_record = {"team_name": student_id, "user_name": student_id, "topic": topic_choice, "project_name": proj_name, "desc": proj_desc}
                st.session_state.mock_db.insert(0, new_record)
                st.success("🎉 Sent!")

# TAB 2
with app_mode[1]:
    st.subheader("📊 Live Feed")
    for idx, entry in enumerate(st.session_state.mock_db):
        with st.container():
            st.markdown(f"### 📦 #{idx+1}: {entry['project_name']}")
            st.write(f"By: {entry['team_name']} | Track: {entry['topic']}")
            st.write(f"Info: {entry['desc']}")
            st.markdown("---")

# TAB 3
with app_mode[2]:
    st.subheader("🎨 Dynamic UI States")
    accent_color = st.selectbox("Color:", ["Blue", "Red", "Green"])
    user_font_size = st.slider("Font Size:", 16, 32, 20)
    st.markdown("---")
    
    # FIXED: Replaced st.info/st.error/st.success with st.markdown to cleanly handle HTML font styling safely
    if accent_color == "Blue":
        st.markdown(f"<div style='background-color:#eff6ff; padding:15px; border-left:5px solid #3b82f6; border-radius:4px;'><p style='font-size:{user_font_size}px; color:#1e40af; margin:0; font-weight:bold;'>Dashboard Blue</p></div>", unsafe_allow_html=True)
    elif accent_color == "Red":
        st.markdown(f"<div style='background-color:#fef2f2; padding:15px; border-left:5px solid #ef4444; border-radius:4px;'><p style='font-size:{user_font_size}px; color:#991b1b; margin:0; font-weight:bold;'>Alert Red</p></div>", unsafe_allow_html=True)
    elif accent_color == "Green":
        st.markdown(f"<div style='background-color:#f0fdf4; padding:15px; border-left:5px solid #22c55e; border-radius:4px;'><p style='font-size:{user_font_size}px; color:#166534; margin:0; font-weight:bold;'>System Green</p></div>", unsafe_allow_html=True)

# TAB 4
with app_mode[3]:
    st.subheader("📈 Charting Lab")
    col1, col2, col3 = st.columns(3)
    with col1:
        score_a = st.number_input("Usability (1-10):", 1, 10, 7)
    with col2:
        score_b = st.number_input("Design (1-10):", 1, 10, 6)
    with col3:
        score_c = st.number_input("Impact (1-10):", 1, 10, 8)
    chart_data = {"Metric": ["Usability", "Design", "Impact"], "Score": [score_a, score_b, score_c]}
    st.bar_chart(data=chart_data, x="Metric", y="Score")

# TAB 5
with app_mode[4]:
    st.subheader("🧰 Toolkit")
    filter_choice = st.selectbox("Filter Database:", ["All", "🌿 Environment", "🏥 Health", "📚 Education", "🐾 Animal Welfare", "🤖 Smart Cities"])
    for project in st.session_state.mock_db:
        if filter_choice == "All" or filter_choice in project["topic"]:
            st.write(f"**{project['project_name']}** ({project['topic']})")
    st.markdown("---")
    system_load = st.slider("System Metric Level:", 0, 100, 45)
    if system_load < 30:
        st.success(f"💚 Safe ({system_load}%)")
    elif system_load <= 70:
        st.warning(f"⚠️ Warning ({system_load}%)")
    else:
        st.error(f"🚨 Critical ({system_load}%)")

# TAB 6
with app_mode[5]:
    st.subheader("📐 Layout Studio")
    col_layout = st.radio("Columns:", ["2 Columns", "3 Columns"])
    if col_layout == "2 Columns":
        c1, c2 = st.columns(2)
        c1.info("Column 1")
        c2.success("Column 2")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", "92%")
        c2.metric("Pings", "14")
        c3.metric("Nodes", "450")
    with st.expander("❓ View Details"):
        st.write("Details text container.")
        st.caption("🔒 Code: LAYOUT_MASTER_2026")

# TAB 7
with app_mode[6]:
    st.subheader("🎨 Styling Media Lab")
    st.markdown("**Bold** text and *italics* sample.")
    st.info("Info box visual.")
    st.success("Success box visual.")
    graphic_choice = st.selectbox("Image Select:", ["Environment", "Health"])
    if graphic_choice == "Environment":
        img_url = "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=500"
    else:
        img_url = "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=500"
    st.image(img_url, use_container_width=True)
    st.caption(f"🔒 Asset: {graphic_choice.upper()}_OK")

# TAB 8
with app_mode[7]:
    st.subheader("⚡ Advanced Logic")
    scale_factor = st.slider("Scale Target:", 1, 1000, 250)
    severity = st.radio("Severity Level multiplier:", [1, 2, 3])
    total_impact_score = scale_factor * severity
    st.metric(label="Calculated Impact Metric Score:", value=total_impact_score)
    st.caption(f"🔒 Hash: CALC_SCORE_{total_impact_score}")

# TAB 9
with app_mode[8]:
    st.subheader("📊 Data Science Challenge")
    data_choice = st.radio("Choose the Actionable Option:", ["Option A: Vague text details.", "Option B: Max limit = 150, Spike = 40%"])
    if "Option A" in data_choice:
        st.error("❌ Try again.")
    else:
        st.success("✅ Good Data Science!")
        st.caption("🔒 Certification Code: METRIC_SCOUT_2026")
