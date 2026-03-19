import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Portal Pro", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
body {background-color: #F4F8FB;}
.title {text-align:center; font-size:32px; font-weight:bold; margin-bottom:20px;}
.card {
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.05);
    margin-bottom:20px;
}
.stButton>button {
    background:#A7C7E7;
    font-size:16px;
    border-radius:10px;
    padding:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎓 Student Portal Pro</div>", unsafe_allow_html=True)

# ---------- STORAGE ----------
if "students" not in st.session_state:
    st.session_state.students = {}

# ---------- NAV ----------
page = st.selectbox("Menu", ["Home", "Add Student", "Search Student", "Statistics"])

# ---------- HOME ----------
if page == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Welcome 👋")
    st.write("Manage students, search, and view stats.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ADD STUDENT ----------
elif page == "Add Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Add Student")

    name = st.text_input("Student Name")

    subjects = []
    scores = []

    for i in range(3):  # fixed 3 subjects (more stable)
        col1, col2 = st.columns(2)
        subjects.append(col1.text_input(f"Subject {i+1}", key=f"sub{i}"))
        scores.append(col2.number_input(f"Score {i+1}", 0, 100, key=f"score{i}"))

    if st.button("Save Student"):
        if not name:
            st.error("Enter student name")
        else:
            data = {}

            for sub, sc in zip(subjects, scores):
                if sub:  # only save filled subjects
                    data[sub] = sc

            if data:
                st.session_state.students[name] = data
                st.success("Student saved ✅")
            else:
                st.error("Enter at least one subject")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SEARCH ----------
elif page == "Search Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Search Student")

    search = st.text_input("Enter name")

    if search:
        student = st.session_state.students.get(search)

        if student:
            df = pd.DataFrame(list(student.items()), columns=["Subject", "Score"])
            st.dataframe(df)

            avg = sum(student.values()) / len(student)
            st.write(f"Average Score: {avg:.2f}")
        else:
            st.warning("Student not found")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- STATS ----------
elif page == "Statistics":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Class Statistics")

    students = st.session_state.students

    if students:
        all_scores = []
        highest = ("", "", -1)
        lowest = ("", "", 101)

        for name, subs in students.items():
            for subject, score in subs.items():
                all_scores.append(score)

                if score > highest[2]:
                    highest = (name, subject, score)

                if score < lowest[2]:
                    lowest = (name, subject, score)

        st.write(f"Class Average: {sum(all_scores)/len(all_scores):.2f}")
        st.write(f"Highest: {highest[0]} - {highest[1]} ({highest[2]})")
        st.write(f"Lowest: {lowest[0]} - {lowest[1]} ({lowest[2]})")

        if st.button("Clear Data"):
            st.session_state.students = {}
            st.success("Data cleared")

    else:
        st.info("No data yet")

    st.markdown("</div>", unsafe_allow_html=True)                
