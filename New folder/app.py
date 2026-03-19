import streamlit as st
import pandas as pd
from datetime import date

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Streamlit Student Portal", layout="wide", page_icon="🎓")

# ---------- SESSION STATE ----------
if "users" not in st.session_state:
    # Sample users: username: [password, role, name]
    st.session_state.users = {
        "student1": ["pass123", "student", "Tomiwa Akpe"],
        "teacher1": ["teach123", "teacher", "Mrs. Johnson"],
        "admin1": ["admin123", "admin", "Principal Smith"]
    }
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None
if "students" not in st.session_state:
    st.session_state.students = {}

# ---------- STYLE ----------
st.markdown("""
<style>
body {background-color: #F0F4F8; font-family: 'Arial', sans-serif;}
.card {background:white; padding:25px; border-radius:20px; box-shadow:0px 10px 25px rgba(0,0,0,0.08); margin-bottom:20px;}
.stButton>button {background:#4A90E2; color:#fff; font-size:16px; border-radius:12px; padding:10px 18px; border:none; transition:0.3s;}
.stButton>button:hover {transform: scale(1.08); background:#50E3C2;}
.title {font-size:36px; font-weight:bold; color:#2A3F5F; text-align:center;}
.subtitle {font-size:18px; text-align:center; color:#5A6B7C; margin-bottom:20px;}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.markdown("<div class='title'>🎓 Streamlit Student Portal</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Login with your credentials</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username][0] == password:
            st.session_state.logged_in = True
            st.session_state.role = st.session_state.users[username][1]
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

else:
    st.markdown(f"<div class='title'>Welcome, {st.session_state.users[st.session_state.username][2]}</div>", unsafe_allow_html=True)
    
    # ---------- LOGOUT ----------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.experimental_rerun()
    
    # ---------- NAVIGATION ----------
    tabs = ["Dashboard", "Students", "Courses", "Assignments", "Grades", "Attendance", "Timetable", "Messaging", "Events", "Resources"]
    page = st.selectbox("Menu", tabs)
    
    # ---------- DASHBOARD ----------
    if page == "Dashboard":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Quick Glance")
        st.write("📅 Today's classes: Math, Science")
        st.write("📌 Upcoming assignments: History essay due 2026-03-20")
        st.write("📝 Recent grades: Tomiwa Akpe - Math: 85 (B)")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- STUDENTS ----------
    elif page == "Students":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Student Management")
        name = st.text_input("Add Student Name")
        if st.button("Add Student"):
            if name:
                st.session_state.students[name] = {"ID": len(st.session_state.students)+1, "Subjects": {}, "GPA":0}
                st.success(f"Student {name} added!")
        st.write("All Students:")
        st.write(st.session_state.students)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- COURSES ----------
    elif page == "Courses":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Courses & Enrollment")
        st.write("Course list, enrollment status here")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- ASSIGNMENTS ----------
    elif page == "Assignments":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Assignments")
        st.write("Upload / download / submission dates")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- GRADES ----------
    elif page == "Grades":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Grades & Feedback")
        st.write("Student grades and GPA tracker")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- ATTENDANCE ----------
    elif page == "Attendance":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Attendance Tracker")
        st.write("Daily logs and bar chart visualization")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- TIMETABLE ----------
    elif page == "Timetable":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Timetable")
        st.write("Daily/Weekly view with clickable class details")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- MESSAGING ----------
    elif page == "Messaging":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Messaging")
        st.write("Send messages to teachers / students")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- EVENTS ----------
    elif page == "Events":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Events & Campus Life")
        st.write("Clubs, seminars, workshops, event registration")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- RESOURCES ----------
    elif page == "Resources":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Library & Resources")
        st.write("Searchable PDFs, e-books, documents")
        st.markdown("</div>", unsafe_allow_html=True)
