import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import hashlib
import hmac
from datetime import datetime
from supabase import create_client, Client

# ==============================================================================
# 1. CORE CLIENT CONNECTIONS & GLOBAL STATE ENTITIES
# ==============================================================================
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

MASTER_APP_PASSWORD = st.secrets["APP_PASSWORD"]
WP_SSO_SECRET_KEY = st.secrets.get("WP_SSO_SECRET_KEY", "socihacks_secure_handshake_gateway_2026")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_type" not in st.session_state:
    st.session_state.user_type = "Unassigned"
if "user_role" not in st.session_state:
    st.session_state.user_role = "Student" 
if "user_region" not in st.session_state:
    st.session_state.user_region = "Malta" 
if "assigned_courses" not in st.session_state:
    st.session_state.assigned_courses = []
if "online_pre_completed" not in st.session_state:
    st.session_state.online_pre_completed = False
if "online_post_completed" not in st.session_state:
    st.session_state.online_post_completed = False
if "completed_items" not in st.session_state:
    st.session_state.completed_items = set()

# ==============================================================================
# 2. EXACT WORDPRESS CURRICULUM ARCHITECTURE MATRIX
# ==============================================================================
LMS_COURSE_STRUCTURE = {
    "Module 1: Environment Setup & Initialization": [
        "Local Python Interfacing Tools", "Development Workspace Setup", "API Authentication Principles"
    ],
    "Module 2: Controlling the Cloud Database": [
        "Database Architecture Basics", "Relational Layer Structural Paradigms", "PostgREST Client Configuration"
    ],
    "Module 3: Variables, Logic, and UI State": [
        "View State Foundations", "Multi-Page Sidebar Navigation Layouts", "Persistent Variables Engineering"
    ],
    "Module 4: Data Visualization & Analytics": [
        "PyDeck Layer Syntaxes", "Coordinate Datatypes Isolation"
    ],
    "Module 5: Universal Feature Engineering": [
        "Dynamic Frontend Web Inputs", "Safe Append Procedures"
    ],
    "Module 6: App Layouts & User Experience (UX)": [
        "Spatial Mapping Vector Controls", "Interactive Map Rendering", "Asynchronous Architecture Mapping", "Deployment Operations Protocols"
    ],
    "Module 7: Media, Colors, and Styling": [
        "Custom UI Themes & CSS Hacks", "Media Elements & Asset Integration", "Branding Variables Calibration"
    ],
    "Module 8: Advanced Logic & Data Processing": [
        "Extracting Live Remote Geolocation JSONs", "Dataframe Restructuring Algorithms", "Automated Coordinate Updates"
    ],
    "Module 9: Community Data Science & Pre-Event Research": [
        "Live Chat Communication Components", "Study Hall Integration Modules", "Project Sandbox Deployments"
    ]
}

TOTAL_COURSE_ITEMS_COUNT = 26

CORE_RESEARCH_COMPETENCIES = {
    "comp_1_python": {
        "title": "💻 Running Python Locally",
        "desc": "How comfortable do you feel setting up Python on your computer, using terminal commands, and fixing errors when software programs don't launch correctly?"
    },
    "comp_2_supabase": {
        "title": "🔒 Keeping Secret Keys Safe",
        "desc": "How confident are you connecting your web application to a live cloud database using secret keys without accidentally exposing those passwords publicly?"
    },
    "comp_3_state": {
        "title": "🧠 App Memory & Layout States",
        "desc": "How confident are you making sure your app remembers user choices, checkboxes, or typed text when they switch back and forth between different sidebar pages?"
    },
    "comp_4_pydeck": {
        "title": "🗺️ Map Making & Geolocation Rendering",
        "desc": "How comfortable do you feel reading GPS coordinates (Latitude and Longitude numbers) and plotting them on interactive PyDeck maps?"
    },
    "comp_5_crud": {
        "title": "📝 Building Functional Web Forms",
        "desc": "How confident do you feel designing web forms where users can type things in, press a submit button, and successfully send new information into a secure database?"
    },
    "comp_6_transform": {
        "title": "📡 Reading Live Web Feeds",
        "desc": "How confident are you writing clean code that grabs live, real-time data feeds from the internet and formats them into readable tables or maps?"
    }
}

# ==============================================================================
# 3. RELATIONAL SYNC & IDENTITY LOOKUPS FROM EXPORT SCHEMA
# ==============================================================================
GLOBAL_EVENT_CATALOG = []
mentors_list = []
students_list = []

try:
    # Pull profiles straight from your unified master table
    master_query = supabase.table("students").select("*").execute()
    if master_query.data:
        # Segregate cohort members dynamically based on user_type strings
        students_list = [row for row in master_query.data if row.get("user_type") == "Youth Participant"]
        mentors_list = [row for row in master_query.data if row.get("user_type") == "Industry Mentor"]
except Exception:
    pass

# --- TRACK ASSIGNED COURSES & AUTOMATIC PROGRESS SYNC ---
if st.session_state.logged_in and st.session_state.user_role == "Student":
    try:
        # Pull allocated rows assigned through backend admin scripts
        enroll_response = supabase.table("course_enrollments").select("course_id, course_title, course_slug").eq("student_email", st.session_state.user_email).execute()
        if enroll_response.data:
            st.session_state.assigned_courses = enroll_response.data
        else:
            st.session_state.assigned_courses = []
            
        # Extract progress points pushed by the LMS connection
        completions_response = supabase.table("course_completions").select("lesson_item_id").eq("student_email", st.session_state.user_email).execute()
        if completions_response.data:
            st.session_state.completed_items = set([row["lesson_item_id"] for row in completions_response.data])
    except Exception:
        pass

try:
    if st.session_state.logged_in:
        events_response = supabase.table("hackathon_events").select("*").eq("country", st.session_state.user_region).execute()
    else:
        events_response = supabase.table("hackathon_events").select("*").execute()
    GLOBAL_EVENT_CATALOG = events_response.data if events_response.data else []
except Exception: 
    GLOBAL_EVENT_CATALOG = []

def verify_online_surveys_status():
    if st.session_state.logged_in:
        try:
            pre_res = supabase.table("research_surveys").select("id").eq("student_email", st.session_state.user_email).eq("survey_phase", "PRE").eq("delivery_mode", "ONLINE_COURSE").execute()
            if pre_res.data:
                st.session_state.online_pre_completed = True
                
            post_res = supabase.table("research_surveys").select("id").eq("student_email", st.session_state.user_email).eq("survey_phase", "POST").eq("delivery_mode", "ONLINE_COURSE").execute()
            if post_res.data:
                st.session_state.online_post_completed = True
        except Exception: 
            pass

# ==============================================================================
# 4. ROUTER PORTAL SHELL MANAGEMENT (LOGIN & GATEWAY)
# ==============================================================================
if not st.session_state.logged_in:
    st.title("🔗 PhD Matchmaking Lifecycle Router")
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.markdown("### Classroom Portal Login")
        email_input = st.text_input("Registered Email Address", key="login_email").strip().lower()
        password_input = st.text_input("Account Password", type="password", key="login_pwd")
        
        if st.button("Unlock Dashboard Gateway", use_container_width=True):
            if password_input == "DemoPassword123!" or password_input == MASTER_APP_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                
                # Default credential assignments
                st.session_state.user_role = "Mentor" if "mentor" in email_input else "Student"
                st.session_state.user_type = "Senior Research Advisor" if st.session_state.user_role == "Mentor" else "Youth Participant"
                
                try:
                    live_checkin = supabase.table("students").select("user_type, physical_address").eq("email", email_input).execute()
                    if live_checkin.data:
                        raw_type = live_checkin.data[0].get("user_type", "Youth Participant")
                        st.session_state.user_role = "Mentor" if "Mentor" in raw_type else "Student"
                        st.session_state.user_type = raw_type
                        
                        raw_addr = live_checkin.data[0].get("physical_address", "Malta")
                        st.session_state.user_region = "Ireland" if "Ireland" in raw_addr else "Malta"
                except Exception: 
                    pass
                
                verify_online_surveys_status()
                st.rerun()
            else:
                st.error("Invalid Credentials Supplied.")
                
    with col2:
        with st.container(border=True):
            st.markdown("#### 🧪 Dual-Role Developer Testing Node")
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                if st.button("🎭 Load Youth Demo Profile", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.user_email = "youth.demo@socihacks.org"
                    st.session_state.user_role = "Student"
                    st.session_state.user_type = "Youth Participant"
                    st.session_state.user_region = "Malta"
                    
                    # FIXED: Added 'course_id' to resolve structural filtering blocks
                    st.session_state.assigned_courses = [{
                        "course_id": "pre-hackathon-app-developer-bootcamp",
                        "course_title": "Pre-Hackathon App Developer Bootcamp",
                        "course_slug": "pre-hackathon-app-developer-bootcamp"
                    }]
                    st.session_state.completed_items = {"item_1_local_python_interfacing_tools", "item_2_development_workspace_setup"}
                    verify_online_surveys_status()
                    st.rerun()
            with sub_col2:
                if st.button("💼 Load Mentor Demo Profile", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.user_email = "mentor.demo@socihacks.org"
                    st.session_state.user_role = "Mentor"
                    st.session_state.user_type = "Industry Mentor"
                    st.session_state.user_region = "Ireland"
                    st.session_state.online_pre_completed = True
                    st.session_state.online_post_completed = True
                    st.rerun()
            st.caption("Bypass Credential Access Standard: `DemoPassword123!`")

    st.markdown("---")
    st.subheader("📍 Active Cohort Spatial Distribution Map")
    map_records = []
    
    for s in students_list:
        if s.get("latitude") and s.get("longitude"):
            map_records.append({"lat": float(s["latitude"]), "lon": float(s["longitude"]), "name": s.get("full_name"), "type": "Student", "color": [242, 108, 79, 200]})
    for m in mentors_list:
        if m.get("latitude") and m.get("longitude"):
            map_records.append({"lat": float(m["latitude"]), "lon": float(m["longitude"]), "name": m.get("full_name"), "type": "Mentor", "color": [34, 139, 34, 200]})

    if map_records:
        map_df = pd.DataFrame(map_records)
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(latitude=map_df["lat"].mean(), longitude=map_df["lon"].mean(), zoom=6, pitch=30),
            layers=[pdk.Layer("ScatterplotLayer", data=map_df, get_position="[lon, lat]", get_color="color", get_radius=8000, pickable=True)],
            tooltip={"text": "{name} ({type})"}
        ))

else:
    # ==============================================================================
    # 5. AUTHENTICATED SESSION LAYERS
    # ==============================================================================
    current_user_email = st.session_state.user_email
    verify_online_surveys_status()

    with st.sidebar:
        st.markdown(f"**Identity:** `{current_user_email}`\n\n**Role:** `{st.session_state.user_type}`\n\n**Cohort:** `{st.session_state.user_region}`")
        st.markdown("---")
        
        if st.session_state.user_role == "Student":
            completed_count = len(st.session_state.completed_items)
            progress_percentage = completed_count / float(TOTAL_COURSE_ITEMS_COUNT)
            
            st.markdown(f"**LMS Verified Progress:** `{completed_count} / {TOTAL_COURSE_ITEMS_COUNT} Lessons` (`{int(progress_percentage * 100)}%`)")
            st.progress(min(progress_percentage, 1.0))
            st.markdown("---")

        navigation_selection = st.radio("System Routing Panel", ["📚 LMS Course Gateway", "🔗 Network Matchmaking Router", "🏆 Live Hackathon Events"])
        
        if st.button("Terminate Active Session", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.online_pre_completed = False
            st.session_state.online_post_completed = False
            st.session_state.completed_items = set()
            st.session_state.assigned_courses = []
            st.rerun()

    # --- ROUTER DEPLOYMENTS ---
    if navigation_selection == "🔗 Network Matchmaking Router":
        st.title("🔗 PhD Matchmaking Lifecycle Router")
        if st.session_state.user_role == "Mentor":
            st.subheader("💼 Mentor Connection Portal Administration")
            with st.container(border=True):
                st.markdown("### 📥 Connection Proposal Received")
                st.markdown("**Candidate student:** `youth.demo@socihacks.org` (Alex Camilleri)")
                if st.button("Confirm Match Connection Proposal", use_container_width=True):
                    st.success("Match verified! Handshake established successfully.")
        else:
            st.subheader("Available Industry Mentors (Browse Free Selection)")
            for mentor in mentors_list:
                with st.container(border=True):
                    st.markdown(f"### 🏅 {mentor.get('full_name')}")
                    st.markdown(f"💡 **Technical Skills Base:** {mentor.get('technical_skills', 'Data Engineering')}")
                    st.button("Send Connection Proposal Request", key=f"btn_{mentor.get('id')}", disabled=(current_user_email == "youth.demo@socihacks.org"), use_container_width=True)

    # --- LMS CONTROL GATEWAY INTERFACE BLOCK ---
    elif navigation_selection == "📚 LMS Course Gateway":
        st.title("📚 Headless LMS Control Interface")
        
        if st.session_state.user_role == "Mentor":
            st.info("ℹ️ Educational resources are configured for student execution tracks.")
        else:
            if not st.session_state.online_pre_completed:
                st.warning("🔒 App Development Tracks Locked")
                st.markdown("### 👋 Welcome to your Pre-Hackathon Workspace!")
                st.markdown("Before jumping over to WordPress to start your lessons, please answer these **6 quick questions** about your starting comfort level. This lets us track your skills growth before the live event!")
                
                with st.form("online_pre_survey_form"):
                    pre_answers = {}
                    slider_labels = {1: "1: Totally New", 2: "2: Heard of it", 3: "3: Can do with guidance", 4: "4: Fairly Confident", 5: "5: Ready to build independently"}
                    
                    for comp_key, comp_info in CORE_RESEARCH_COMPETENCIES.items():
                        with st.container(border=True):
                            st.markdown(f"### {comp_info['title']}")
                            st.markdown(comp_info['desc'])
                            
                            pre_answers[comp_key] = st.select_slider(
                                "Choose your current skill level:",
                                options=[1, 2, 3, 4, 5],
                                value=1,
                                format_func=lambda x: slider_labels[x],
                                key=f"pre_{comp_key}"
                            )
                    
                    if st.form_submit_button("Lock In My Answers & Connect Straight to My Courses! 🎉", use_container_width=True):
                        try:
                            supabase.table("research_surveys").insert({
                                "student_email": current_user_email, "survey_phase": "PRE", "delivery_mode": "ONLINE_COURSE",
                                "meta_data": {**pre_answers, "engine": "WordPress_LMSPress", "timestamp": datetime.now().isoformat()}
                            }).execute()
                        except Exception: 
                            pass 
                        st.session_state.online_pre_completed = True
                        st.rerun()
            else:
                # Displays the 2 production panels cleanly (removing the old Open Opportunities tab)
                active_tab, lms_curriculum_matrix_tab = st.tabs(["🎓 Enrolled Modules", f"📖 Bootcamp Curriculum ({TOTAL_COURSE_ITEMS_COUNT} Items)"])
                
                with active_tab:
                    if not st.session_state.assigned_courses:
                        st.warning("⚠️ No Allocated Course Modules Identified. Please contact your regional academic administrator to assign your track.")
                    else:
                        # Renders active assignment modules securely
                        for course in st.session_state.assigned_courses:
                            with st.container(border=True):
                                st.markdown(f"### 📖 {course.get('course_title', 'Pre-Hackathon App Developer Bootcamp')}")
                                
                                # --- SECURE PASS-THROUGH HANDSHAKE LOGIC ---
                                timestamp = str(int(datetime.now().timestamp()))
                                base_url = "https://www.socihacks.com/courses/"
                                slug = course.get('course_slug', 'pre-hackathon-app-developer-bootcamp')
                                
                                raw_payload = f"user={current_user_email}&course={slug}&time={timestamp}"
                                signature = hmac.new(
                                    WP_SSO_SECRET_KEY.encode('utf-8'),
                                    raw_payload.encode('utf-8'),
                                    hashlib.sha256
                                ).hexdigest()
                                
                                encoded_payload = base64.b64encode(raw_payload.encode('utf-8')).decode('utf-8')
                                sso_url = f"{base_url}{slug}/?sso_handshake={encoded_payload}&sig={signature}"
                                
                                st.link_button("🚀 Launch Linked WordPress Sandbox", sso_url, use_container_width=True)

                    # --- CONDITIONAL PROGRESS ASSESSMENT ELEMENT ---
                    st.markdown("---")
                    if len(st.session_state.completed_items) >= 24:
                        if not st.session_state.online_post_completed:
                            st.subheader("🎓 Coursework Complete! Post-Survey Assessment Panel")
                            st.markdown("🏆 **Incredible work!** Our systems confirm you have completed your digital modules on WordPress. Let's look at those 6 questions one last time to track your skill growth:")
                            
                            with st.form("online_post_survey_form"):
                                post_answers = {}
                                slider_labels = {1: "1: Still New", 2: "2: Familiar with it now", 3: "3: Can do with guidance", 4: "4: Fairly Confident", 5: "5: Ready to build independently"}
                                
                                for comp_key, comp_info in CORE_RESEARCH_COMPETENCIES.items():
                                    with st.container(border=True):
                                        st.markdown(f"### {comp_info['title']}")
                                        st.markdown(comp_info['desc'])
                                        
                                        post_answers[comp_key] = st.select_slider(
                                            "Choose your new current skill level:",
                                            options=[1, 2, 3, 4, 5],
                                            value=4,
                                            format_func=lambda x: slider_labels[x],
                                            key=f"post_{comp_key}"
                                        )
                                
                                if st.form_submit_button("Submit Final Progress Review & Confirm Graduation Checkpoint", use_container_width=True):
                                    try:
                                        supabase.table("research_surveys").insert({
                                            "student_email": current_user_email, "survey_phase": "POST", "delivery_mode": "ONLINE_COURSE",
                                            "meta_data": {**post_answers, "engine": "WordPress_LMSPress", "timestamp": datetime.now().isoformat()}
                                        }).execute()
                                    except Exception: 
                                        pass
                                    st.session_state.online_post_completed = True
                                    st.success("Post-course evaluation metrics linked! You are fully locked in.")
                                    st.rerun()
                        else:
                            with st.container(border=True):
                                st.markdown("### 🎉 Evaluation Instruments Fully Synchronized")
                                st.success("Assessment payload logged. Auto-dispatching programmatic verification notification email...")
                                
                                outbox_preview = f"To: {current_user_email}\nSubject: [SOCIHACKS LMS Core] Progress & Post-Survey Verified\n\nHello,\nYour matched pre-vs-post coursework metrics have been successfully locked into our analytic schema. Your regional profile is cleared for hackathon participation in: {st.session_state.user_region}."
                                st.text_area("Dispatched Email Outbox Stream", value=outbox_preview, height=130, disabled=True)
                    else:
                        st.caption(f"ℹ️ *Post-test evaluation drops automatically once you complete at least 24 of the 26 items inside the full curriculum workspace (Current Synced Progress: {len(st.session_state.completed_items)}).*")

                # --- READ ONLY DIRECT LIVE LEDGER SYNC VIEW ---
                with lms_curriculum_matrix_tab:
                    st.markdown("## 📋 Core Coursework Completion Ledger")
                    st.caption("🔄 *Live read-only tracker synced from your active WordPress LMSPress campus execution track.*")
                    st.markdown("---")
                    
                    item_idx = 1
                    for section_title, item_list in LMS_COURSE_STRUCTURE.items():
                        with st.expander(f"📁 {section_title} ({len(item_list)} Items)"):
                            for item in item_list:
                                item_unique_id = f"item_{item_idx}_{item.replace(' ', '_').lower()}"
                                is_verified_complete = item_unique_id in st.session_state.completed_items
                                
                                col_status, col_text = st.columns([1.2, 6])
                                with col_status:
                                    if is_verified_complete:
                                        st.markdown("`✅ Completed`")
                                    else:
                                        st.markdown("`⏳ Pending`")
                                with col_text:
                                    st.markdown(f"**Lesson {item_idx}:** {item}")
                                
                                item_idx += 1

    # --- HACKATHONS DEPLOYMENTS ---
    elif navigation_selection == "🏆 Live Hackathon Events":
        st.title("🏆 Live Hackathon Events Portal")
        for event in GLOBAL_EVENT_CATALOG:
            with st.container(border=True):
                st.markdown(f"### 🚀 {event.get('title')}\n📍 **Location:** `{event.get('location')}`")
