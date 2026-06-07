import streamlit as st
import math
import pandas as pd
import pydeck as pdk
import base64
from supabase import create_client, Client

# ==============================================================================
# 1. INITIALIZE SECURE CONNECTIONS & SESSION STATES
# ==============================================================================
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

MASTER_APP_PASSWORD = st.secrets["APP_PASSWORD"]

# Persistent operational tracking blocks
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "pending_requests" not in st.session_state:
    st.session_state.pending_requests = []
if "peer_connections" not in st.session_state:
    st.session_state.peer_connections = []
if "demo_mentor_id" not in st.session_state:
    st.session_state.demo_mentor_id = None
if "local_enrollments" not in st.session_state:
    st.session_state.local_enrollments = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "🌐 Global Hub Channel (All Connections)": [
            {"sender": "Dr. Carmel Borg", "text": "Welcome everyone! Looking forward to reviewing the structural proposal documentation later this week."}
        ],
        "👥 Peer Cohort Study Group Channel": [
            {"sender": "System", "text": "Peer cohort room created successfully. You can now coordinate study circles directly with your connected peers here."}
        ]
    }

# ==============================================================================
# AUTOMATED WORDPRESS SINGLE SIGN-ON (SSO) DETECTION ENGINE
# ==============================================================================
# Checks if '?st_token=' is inside the active address bar string
if not st.session_state.logged_in and "st_token" in st.query_params:
    try:
        encoded_token = st.query_params["st_token"]
        # Safe decoding from Base64 schema back into a standard email text string
        decoded_bytes = base64.b64decode(encoded_token.encode('utf-8'))
        auto_email = decoded_bytes.decode('utf-8').strip()
        
        if auto_email:
            st.session_state.logged_in = True
            st.session_state.user_email = auto_email
            # Clear the parameters clean so refreshing doesn't cause loop delays
            st.query_params.clear()
            st.toast(f"🔒 Authenticated securely via WordPress Sync Gateway!", icon="🔄")
    except Exception as token_err:
        st.sidebar.error(f"Autologin Pipeline Bypass Restrained: {token_err}")

# ==============================================================================
# 2. GEOSPATIAL GEOMETRY ENGINE & FRESH DATA EXTRACTION LOOP
# ==============================================================================
COUNTRY_COORDINATES = {
    "Malta": (35.9375, 14.3754),
    "Ireland": (53.4129, -8.2439),
    "UK": (55.3781, -3.4360),
    "United Kingdom": (55.3781, -3.4360)
}

GLOBAL_COURSE_CATALOG = []

try:
    mentors_query = supabase.table("mentors").select("*").execute()
    mentors_list = mentors_query.data if mentors_query.data else []
    
    students_query = supabase.table("students").select("*").execute()
    students_list = students_query.data if students_query.data else []
    
    enroll_query = supabase.table("course_enrollments").select("*").execute()
    db_enrollments = enroll_query.data if enroll_query.data else []
    
    courses_query = supabase.table("courses").select("*").execute()
    if courses_query.data:
        for c in courses_query.data:
            GLOBAL_COURSE_CATALOG.append({
                "id": str(c.get("id")),
                "title": str(c.get("title")),
                "slug": str(c.get("slug")),
                "desc": str(c.get("desc_text") or "No course description provided.")
            })
except Exception as e:
    st.error(f"Database Synchronizer Delay: {e}")
    mentors_list, students_list, db_enrollments = [], [], []

if not mentors_list:
    mentors_list = [
        {"id": "mock-mentor-1", "full_name": "Dr. Liam O'Connor", "org": "SOCIHACKS Network Expert", "country": "Ireland", "skills": "Advisory", "physical_address": "Cork, Ireland"},
        {"id": "mock-mentor-2", "full_name": "Dr. Joseph Aquilina", "org": "SOCIHACKS Network Expert", "country": "Malta", "skills": "General Advisory", "physical_address": "Msida, Malta"}
    ]
if not students_list:
    students_list = [
        {"id": "mock-student-1", "full_name": "Demo Student Account", "email": "youth.demo@socihacks.org", "country": "Malta", "mentor_id": None},
        {"id": "mock-student-2", "full_name": "Malik Al-Saeed (Peer)", "email": "malik.peer@socihacks.org", "country": "UK", "mentor_id": None}
    ]

malta_coords = COUNTRY_COORDINATES.get("Malta")

# ==============================================================================
# 3. INTERACTIVE INTERFACE VIEW CONTEXTS
# ==============================================================================
if not st.session_state.logged_in:
    st.title("🔗 PhD Matchmaking Lifecycle Router")
    st.subheader("Global Distribution of Active Infrastructure Networks")
    
    public_marker_points = []
    for m in mentors_list:
        m_country = m.get("country", "Malta")
        m_coords = COUNTRY_COORDINATES.get(m_country, malta_coords)
        public_marker_points.append({
            "name": m.get("full_name", "Expert Node"), "latitude": m_coords[0], "longitude": m_coords[1], "type": "Mentor"
        })

    if public_marker_points:
        df_public = pd.DataFrame(public_marker_points)
        public_layer = pdk.Layer(
            "ScatterplotLayer", data=df_public, get_position="[longitude, latitude]",
            get_color="[0, 128, 255, 200]", get_radius=60000, pickable=True
        )
        st.pydeck_chart(pdk.Deck(
            layers=[public_layer],
            initial_view_state=pdk.ViewState(latitude=48.5, longitude=2.5, zoom=3.0),
            tooltip={"text": "{name}"}
        ))

    st.markdown("---")
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown("### Sign In")
        email_input = st.text_input("Registered Email Address", key="login_email_field").strip()
        password_input = st.text_input("Account Password", type="password", key="login_pwd_field")
        
        if st.button("Unlock Environment Dashboard", use_container_width=True):
            if password_input == "DemoPassword123!" or password_input == MASTER_APP_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.rerun()
            else:
                st.error("Authentication Failure.")
    with col2:
        with st.container(border=True):
            st.markdown("#### 🎓 Assessment Sandbox Accounts")
            st.markdown("- **Youth Type:** `youth.demo@socihacks.org` \n- **Mentor Type:** `mentor.demo@socihacks.org` \n- **Universal Pwd:** `DemoPassword123!`")

else:
    current_user_email = st.session_state.user_email
    matched_student = next((s for s in students_list if s.get("email") == current_user_email), None)
    matched_mentor = next((m for m in mentors_list if m.get("email") == current_user_email), None)
    
    if current_user_email == "youth.demo@socihacks.org" and not matched_student:
        matched_student = {"id": "mock-student-1", "full_name": "Demo Student Account", "country": "Malta", "mentor_id": st.session_state.demo_mentor_id}
    elif current_user_email == "mentor.demo@socihacks.org" and not matched_mentor:
        matched_mentor = {"id": "mock-mentor-1", "full_name": "Demo Mentor Account", "country": "Ireland"}

    if matched_student and st.session_state.demo_mentor_id:
        matched_student["mentor_id"] = st.session_state.demo_mentor_id

    user_enrolled_ids = [e.get("course_id") for e in db_enrollments if e.get("student_email") == current_user_email]
    if current_user_email == "youth.demo@socihacks.org":
        user_enrolled_ids = list(set(user_enrolled_ids + st.session_state.local_enrollments))

    # ==============================================================================
    # 4. SIDEBAR PANEL DISPLAY
    # ==============================================================================
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/network.png", width=45)
        st.markdown(f"**Logged In As:**\n`{current_user_email}`")
        st.markdown("---")
        
        try:
            badges_query = supabase.table("user_badges").select("*").eq("student_email", current_user_email).execute()
            user_badges = badges_query.data if badges_query.data else []
        except Exception:
            user_badges = []

        if current_user_email == "youth.demo@socihacks.org" and not user_badges:
            user_badges = [
                {"badge_name": "SOCIHACKS Scholar", "badge_icon_url": "https://img.icons8.com/fluency/48/medal.png"},
                {"badge_name": "Data Explorer", "badge_icon_url": "https://img.icons8.com/fluency/48/trophy.png"}
            ]

        if user_badges:
            st.markdown("🏅 **Your Unlocked Badges**")
            num_cols = max(1, min(len(user_badges), 4))
            badge_cols = st.columns(num_cols)
            
            for idx, badge in enumerate(user_badges):
                col_target = badge_cols[idx % num_cols]
                with col_target:
                    b_name = str(badge.get("badge_name") or "Unlocked Achievement")
                    b_icon = str(badge.get("badge_icon_url") or "https://img.icons8.com/fluency/48/medal.png")
                    st.markdown(
                        f'<div title="{b_name}" style="display: flex; justify-content: center;">'
                        f'<img src="{b_icon}" width="35" style="cursor: pointer;">'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
            st.markdown("---")

        menu_selection = st.radio(
            "Navigation Menu",
            ["🔗 Network Matchmaking Router", "📚 LMS Course Gateway", "📍 Regional Connection Node Map", "💬 Internal Group Chats"]
        )
        st.markdown("---")
        if st.button("Terminate Session Gateway", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.demo_mentor_id = None
            st.session_state.pending_requests = []
            st.session_state.peer_connections = []
            st.session_state.local_enrollments = []
            st.rerun()

    # --- FEATURE 1: ROUTER WITH PEER DISCOVERY ---
    if menu_selection == "🔗 Network Matchmaking Router":
        st.title("🔗 PhD Matchmaking Lifecycle Router")
        tab1, tab2 = st.tabs(["🏛️ Expert Mentors", "👥 Peer Network Hub"])
        
        with tab1:
            if matched_student:
                st.subheader("Available Industry Mentors")
                assigned_mentor_id = matched_student.get("mentor_id")
                
                for mentor in mentors_list:
                    m_id = mentor.get("id", "expert-node")
                    m_name = mentor.get('full_name', 'Expert Advisor')
                    with st.container(border=True):
                        st.markdown(f"### 🏅 {m_name}")
                        st.markdown(f"💡 **Expertise:** {mentor.get('skills', 'Advisory')}")
                        
                        if m_id == assigned_mentor_id:
                            st.button("🔒 Connected to Your Account", key=f"disabled_{m_id}", disabled=True, use_container_width=True)
                        elif m_id in st.session_state.pending_requests:
                            st.button("⏳ Connection Request Pending", key=f"pending_{m_id}", disabled=True, use_container_width=True)
                        else:
                            if st.button(f"Send Connection Proposal Request", key=f"btn_{m_id}", use_container_width=True):
                                st.session_state.pending_requests.append(m_id)
                                st.toast(f"Proposal dispatch confirmation sent to {m_name}!", icon="🚀")
                                st.flush_cmd = True 
                                st.rerun()
                                
            elif matched_mentor:
                st.subheader("Assigned Youth Nodes")
                for student in students_list:
                    with st.container(border=True):
                        st.markdown(f"### 👤 Student Node: {student.get('full_name')}")
                        st.caption(f"Origin Region: {student.get('country')}")

        with
        
