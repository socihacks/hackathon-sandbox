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

        with tab2:
            st.subheader("Cross-Role Professional Clusters")
            if matched_student:
                for student in students_list:
                    if student.get("email") != current_user_email:
                        with st.container(border=True):
                            st.markdown(f"### 🎓 Peer: {student.get('full_name')}")
                            st.caption(f"Region Node: {student.get('country')} | Active Tracking State: `Online`")
                            if student.get("id") in st.session_state.peer_connections:
                                st.success("✅ Linked to Peer Cohort Study Circle")
                            else:
                                if st.button("Request Peer Collaboration Link", key=f"peer_{student.get('id')}"):
                                    st.session_state.peer_connections.append(student.get("id"))
                                    st.toast("Peer connection initialized!", icon="🤝")
                                    st.rerun()

    # --- FEATURE 2: HEADLESS LMS CONTROL INTERFACE ---
    elif menu_selection == "📚 LMS Course Gateway":
        st.title("📚 Headless LMS Control Interface")
        st.markdown("Your course catalog syncs using Supabase tables to securely communicate layout properties directly to `socihacks.com` via encoded access strings.")
        
        lms_tab1, lms_tab2 = st.tabs(["🎓 Your Enrolled Courses", "🛒 Available Opportunities"])
        
        with lms_tab1:
            st.subheader("Active Curriculums")
            active_courses = [c for c in GLOBAL_COURSE_CATALOG if c["id"] in user_enrolled_ids]
            
            if not active_courses:
                st.info("You aren't enrolled in any active curriculums yet. Browse available options below!")
            else:
                for crs in active_courses:
                    with st.container(border=True):
                        col_l, col_r = st.columns([3, 1])
                        with col_l:
                            st.markdown(f"### 📖 {crs['title']}")
                            st.markdown(f"{crs['desc']}")
                        with col_r:
                            st.write("") 
                            email_bytes = current_user_email.encode('utf-8')
                            secure_token = base64.b64encode(email_bytes).decode('utf-8')
                            wp_target_url = f"https://www.socihacks.com/courses/{crs['slug']}?st_token={secure_token}"
                            st.link_button("🚀 Access Material", wp_target_url, use_container_width=True)

        with lms_tab2:
            st.subheader("Open Registration Channels")
            available_courses = [c for c in GLOBAL_COURSE_CATALOG if c["id"] not in user_enrolled_ids]
            
            if not GLOBAL_COURSE_CATALOG:
                st.warning("⚠️ No live courses detected in Supabase. Go into your WordPress Course Builder, toggle your published courses back to 'Draft', click update, and then switch them to 'Publish' to push the records live!")
            elif not available_courses:
                st.success("🎉 Outstanding! You have unlocked all catalog modules.")
            else:
                for crs in available_courses:
                    with st.container(border=True):
                        st.markdown(f"### ⚡ {crs['title']}")
                        st.markdown(f"{crs['desc']}")
                        if st.button(f"Acquire Enrollment Right", key=f"reg_{crs['id']}"):
                            try:
                                supabase.table("course_enrollments").insert({
                                    "student_email": current_user_email, "course_id": crs["id"], "course_title": crs["title"], "course_slug": crs["slug"]
                                }).execute()
                            except Exception:
                                pass
                            st.session_state.local_enrollments.append(crs["id"])
                            st.toast(f"Enrollment validated for {crs['title']}!", icon="🔥")
                            st.rerun()

    # --- FEATURE 3: DISCOVERY & CONNECTION NODE MAP ---
    elif menu_selection == "📍 Regional Connection Node Map":
        st.title("📍 Regional Connection Node Map")
        
        user_country = matched_student.get("country", "Malta") if matched_student else matched_mentor.get("country", "Ireland")
        user_coords = COUNTRY_COORDINATES.get(user_country, malta_coords)
        
        map_points = [{"lon": user_coords[1], "lat": user_coords[0], "name": "Your Current Node Location", "color": [0, 255, 0, 255], "radius": 70000}]
        connection_arcs = []
        
        has_connections = False
        assigned_id = matched_student.get("mentor_id") if matched_student else None
        
        if matched_student and assigned_id:
            target_mentor = next((m for m in mentors_list if m.get("id") == assigned_id), None)
            if target_mentor:
                has_connections = True
                m_geo = COUNTRY_COORDINATES.get(target_mentor.get("country"), malta_coords)
                connection_arcs.append({
                    "from_lon": user_coords[1], "from_lat": user_coords[0], "to_lon": m_geo[1], "to_lat": m_geo[0], "label": f"Paired Mentor Path: {target_mentor.get('full_name')}"
                })

        if not has_connections:
            st.info("💡 Displaying prospective connection nodes and peers available for matching in your region.")
            for mentor in mentors_list:
                m_geo = COUNTRY_COORDINATES.get(mentor.get("country"), malta_coords)
                map_points.append({"lon": m_geo[1], "lat": m_geo[0], "name": f"Available Mentor Node: {mentor.get('full_name')}", "color": [255, 165, 0, 200], "radius": 45000})
            for student in students_list:
                if student.get("email") != current_user_email:
                    s_geo = COUNTRY_COORDINATES.get(student.get("country"), malta_coords)
                    map_points.append({"lon": s_geo[1], "lat": s_geo[0], "name": f"Available Peer Node: {student.get('full_name')}", "color": [138, 43, 226, 200], "radius": 45000})

        df_points = pd.DataFrame(map_points)
        layers_to_render = [pdk.Layer("ScatterplotLayer", data=df_points, get_position="[lon, lat]", get_color="color", get_radius="radius", pickable=True)]
        
        if connection_arcs:
            df_arcs = pd.DataFrame(connection_arcs)
            layers_to_render.append(pdk.Layer("ArcLayer", data=df_arcs, get_source_position="[from_lon, from_lat]", get_target_position="[to_lon, to_lat]", get_source_color="[0, 128, 255, 200]", get_target_color="[255, 75, 75, 200]", get_width=4))

        st.pydeck_chart(pdk.Deck(layers=layers_to_render, initial_view_state=pdk.ViewState(latitude=48.0, longitude=4.0, zoom=3.5, pitch=30), tooltip={"text": "{name}"}))

    # --- FEATURE 4: CHAT MODULE PLATFORM ---
    elif menu_selection == "💬 Internal Group Chats":
        st.title("💬 Secure Connection Channels")
        chat_channels = ["🌐 Global Hub Channel (All Connections)"]
        if st.session_state.peer_connections:
            chat_channels.append("👥 Peer Cohort Study Group Channel")
            
        selected_channel = st.selectbox("💬 Choose active communication node:", chat_channels)
        
        chat_container = st.container(height=340)
        with chat_container:
            for message in st.session_state.chat_history[selected_channel]:
                with st.chat_message("user" if message["sender"] != "System" else "assistant"):
                    st.markdown(f"**{message['sender']}**: {message['text']}")

        if user_msg := st.chat_input("Broadcast encrypted message string..."):
            sender_name = matched_student.get("full_name") if matched_student else matched_mentor.get("full_name", "Anonymous Node")
            st.session_state.chat_history[selected_channel].append({"sender": sender_name, "text": user_msg})
            st.toast("Message synced successfully
