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

# Persistent operational tracking blocks for class module
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "local_submissions" not in st.session_state:
    st.session_state.local_submissions = {}
if "completed_lectures" not in st.session_state:
    st.session_state.completed_lectures = set()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "📢 Class Announcements": [
            {"sender": "Professor Borg", "text": "Welcome to the training dashboard! Reminder: The submission channel for Module 2 Project Architecture closes tonight at midnight PST."}
        ],
        "💬 Live Study Hall Q&A": [
            {"sender": "System", "text": "Welcome to the real-time interaction hub. Post your code blockers or project questions here."}
        ]
    }

# ==============================================================================
# AUTOMATED WORDPRESS SINGLE SIGN-ON (SSO) DETECTION ENGINE
# ==============================================================================
if not st.session_state.logged_in and "st_token" in st.query_params:
    try:
        encoded_token = st.query_params["st_token"]
        decoded_bytes = base64.b64decode(encoded_token.encode('utf-8'))
        auto_email = decoded_bytes.decode('utf-8').strip()
        
        if auto_email:
            st.session_state.logged_in = True
            st.session_state.user_email = auto_email
            st.query_params.clear()
            st.toast(f"🔒 Securely Synced to Virtual Classroom Hub!", icon="🎓")
    except Exception as token_err:
        st.sidebar.error(f"Autologin Pipeline Bypass Restrained: {token_err}")

# ==============================================================================
# 2. CLASSROOM SCHEDULING & CURRICULUM DATA MODEL
# ==============================================================================
CLASS_MODULES = [
    {
        "id": "mod_1",
        "title": "Module 1: Streamlit Foundation & State Variables",
        "date": "Live Now (Self-Paced)",
        "zoom_link": "https://zoom.us/mock-link-socihacks-1",
        "assignment_prompt": "Build a multi-page routing menu using st.sidebar and st.radio. Capture a text state across screens.",
        "resources": ["💡 Streamlit Component Docs", "📁 Starter Repository Asset Pack"]
    },
    {
        "id": "mod_2",
        "title": "Module 2: Supabase Relational Integrations & Auth",
        "date": "Live Stream: June 10, 2026 @ 4:00 PM PST",
        "zoom_link": "https://zoom.us/mock-link-socihacks-2",
        "assignment_prompt": "Construct an input submission form that creates row entries inside a live Supabase collection table securely.",
        "resources": ["🔌 Supabase Quickstart Guide", "🔒 Database Security Policy Templates"]
    },
    {
        "id": "mod_3",
        "title": "Module 3: Geospatial Map Layers & Interactive Portals",
        "date": "Live Stream: June 15, 2026 @ 4:00 PM PST",
        "zoom_link": "https://zoom.us/mock-link-socihacks-3",
        "assignment_prompt": "Render an interactive PyDeck Scatterplot mapping layer using coordinate sets extracted directly from an active API feed.",
        "resources": ["📍 PyDeck Spatial Layer Reference", "🗺️ GeoJSON Sample Coordinates"]
    }
]

GLOBAL_COURSE_CATALOG = []
try:
    courses_query = supabase.table("courses").select("*").execute()
    if courses_query.data:
        for c in courses_query.data:
            GLOBAL_COURSE_CATALOG.append({
                "id": str(c.get("id")),
                "title": str(c.get("title")),
                "slug": str(c.get("slug")),
                "desc": str(c.get("desc_text") or "No description provided.")
            })
except Exception:
    pass

# ==============================================================================
# 3. INTERACTIVE INTERFACE VIEW CONTEXTS
# ==============================================================================
if not st.session_state.logged_in:
    st.title("🎓 SOCIHACKS Virtual Classroom Environment")
    st.subheader("Welcome to the Interactive Hackathon Training Portal")
    st.markdown("Please log into your main dashboard on **socihacks.com** to launch this app or type your developer testing credentials below.")
    
    st.markdown("---")
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown("### Classroom Portal Login")
        email_input = st.text_input("Student Registration Email", key="class_email_field").strip()
        password_input = st.text_input("Access Pin Code / Password", type="password", key="class_pwd_field")
        
        if st.button("Access Live Classroom Materials", use_container_width=True):
            if password_input == "DemoPassword123!" or password_input == MASTER_APP_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.rerun()
            else:
                st.error("Authentication check failed. Try again or login via WordPress.")
    with col2:
        with st.container(border=True):
            st.markdown("#### 🧪 Developer Testing Node")
            st.markdown("- **Sandbox User:** `youth.demo@socihacks.org` \n- **Universal Access Key:** `DemoPassword123!`")

else:
    current_user_email = st.session_state.user_email

    # ==============================================================================
    # 4. CLASSROOM NAVIGATION SIDEBAR
    # ==============================================================================
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/education.png", width=45)
        st.markdown(f"**Student Account Node:**\n`{current_user_email}`")
        st.markdown("---")
        
        # Progress Tracker Logic
        total_modules = len(CLASS_MODULES)
        completed_count = len(st.session_state.completed_lectures)
        progress_percentage = completed_count / total_modules if total_modules > 0 else 0.0
        
        st.markdown(f"**Course Completion Progression:** `{int(progress_percentage * 100)}%`")
        st.progress(progress_percentage)
        st.markdown("---")

        menu_selection = st.radio(
            "Class Navigation System",
            ["📺 Live Virtual Lecture Stream", "📥 Course Resource Center", "📝 Assignment Lab Dropbox", "💬 Live Study Hall Rooms"]
        )
        st.markdown("---")
        if st.button("Disconnect from Classroom Terminal", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.local_submissions = {}
            st.session_state.completed_lectures = set()
            st.rerun()

    # --- TRACK 1: LIVE VIRTUAL LECTURE STREAM ---
    if menu_selection == "📺 Live Virtual Lecture Stream":
        st.title("📺 Live Interactive Lecture Stream")
        st.markdown("Access active live lecture coordinates, synchronize timestamps, and track your ongoing class status blocks here.")
        
        for mod in CLASS_MODULES:
            m_id = mod["id"]
            with st.container(border=True):
                col_info, col_action = st.columns([3, 1])
                with col_info:
                    st.markdown(f"### {mod['title']}")
                    st.caption(f"🗓️ Scheduled Session Time: **{mod['date']}**")
                with col_action:
                    st.write("")
                    st.link_button("🔗 Join Zoom Stream", mod["zoom_link"], use_container_width=True)
                
                # Completion confirmation checker
                is_checked = m_id in st.session_state.completed_lectures
                if st.checkbox("Mark module lesson complete", value=is_checked, key=f"check_{m_id}"):
                    if m_id not in st.session_state.completed_lectures:
                        st.session_state.completed_lectures.add(m_id)
                        st.rerun()
                else:
                    if m_id in st.session_state.completed_lectures:
                        st.session_state.completed_lectures.remove(m_id)
                        st.rerun()

    # --- TRACK 2: COURSE RESOURCE CENTER ---
    elif menu_selection == "📥 Course Resource Center":
        st.title("📥 Material Distribution Repository")
        st.markdown("Download active project code templates, architecture briefs, and structural assets directly.")
        
        for mod in CLASS_MODULES:
            with st.container(border=True):
                st.markdown(f"#### 📁 Documentation Pack: {mod['title']}")
                for res in mod["resources"]:
                    st.markdown(f"- **Download / View:** [{res}](https://github.com/socihacks/hackathon-sandbox)")
        
        if GLOBAL_COURSE_CATALOG:
            st.markdown("---")
            st.subheader("🔗 Synced Main System Catalog Paths")
            for crs in GLOBAL_COURSE_CATALOG:
                with st.container(border=True):
                    st.markdown(f"**{crs['title']}**")
                    email_bytes = current_user_email.encode('utf-8')
                    secure_token = base64.b64encode(email_bytes).decode('utf-8')
                    wp_target_url = f"https://www.socihacks.com/courses/{crs['slug']}?st_token={secure_token}"
                    st.link_button("🌐 Open LMS Core Page", wp_target_url)

    # --- TRACK 3: ASSIGNMENT LAB DROPBOX ---
    elif menu_selection == "📝 Assignment Lab Dropbox":
        st.title("📝 Sandbox Code Submission Hub")
        st.markdown("Submit production repository deployment links or testing scripts here to check off grading verification points.")
        
        selected_mod = st.selectbox("Select Target Assignment Scope:", [m["title"] for m in CLASS_MODULES])
        curr_mod = next(m for m in CLASS_MODULES if m["title"] == selected_mod)
        
        with st.container(border=True):
            st.markdown(f"### {curr_mod['title']}")
            st.info(f"📋 **Project Prompt:** {curr_mod['assignment_prompt']}")
            
            sub_key = curr_mod["id"]
            existing_sub = st.session_state.local_submissions.get(sub_key, "")
            
            repo_link = st.text_input("Enter your live deployed app link / GitHub repo link:", value=existing_sub, key=f"input_{sub_key}")
            
            if st.button("Transmit Project Source Link", key=f"submit_btn_{sub_key}"):
                if repo_link.strip() != "":
                    st.session_state.local_submissions[sub_key] = repo_link
                    st.success("🎯 Submission link captured securely and cached for evaluation review!")
                else:
                    st.warning("Please enter a valid URL link before transmitting.")

    # --- TRACK 4: LIVE STUDY HALL ROOMS ---
    elif menu_selection == "💬 Live Study Hall Rooms":
        st.title("💬 Secure Student Group Rooms")
        
        selected_channel = st.selectbox("Choose active discussion node:", list(st.session_state.chat_history.keys()))
        
        chat_container = st.container(height=360)
        with chat_container:
            for message in st.session_state.chat_history[selected_channel]:
                with st.chat_message("user" if message["sender"] != "System" else "assistant"):
                    st.markdown(f"**{message['sender']}**: {message['text']}")

        if user_msg := st.chat_input("Broadcast chat text data to room peers..."):
            st.session_state.chat_history[selected_channel].append({"sender": current_user_email, "text": user_msg})
            st.toast("Message distributed successfully!")
            st.rerun()
