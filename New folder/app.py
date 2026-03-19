import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Portal", layout="centered")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #F4F8FB;
}

.title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #A7C7E7;
    color: black;
    font-size: 18px;
    padding: 12px;
    border-radius: 12px;
    border: none;
    transition: 0.2s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background-color: #91BEE0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>🎓 Student Portal Pro</div>", unsafe_allow_html=True)

# ---------------- STORAGE ----------------
if "students" not in st.session_state:
    st.session_state.students = {}

# ---------------- NAV ----------------
page = st.radio("Navigate", ["🏠 Home", "➕ Add Student", "🔍 Search Student", "📊 Statistics"])

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Welcome 👋")
    st.write("Manage students, search records, and view stats.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ADD STUDENT ----------------
elif page == "➕ Add Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Add Student")

    name = st.text_input("Student Name")
    num_subjects = st.number_input("Number of Subjects", 1, 10, 1)

    subjects = {}

    for i in range(num_subjects):
        col1, col2 = st.columns(2)
        subject = col1.text_input(f"Subject {i+1}", key=f"sub{i}")
        score = col2.number_input(f"Score {i+1}", 0, 100, key=f"score{i}")

        if subject:
            subjects[subject] = score

    if st.button("Save Student"):
        if name and subjects:
            st.session_state.students[name] = subjects
            st.success("Student saved!")
        else:
            st.error("Enter all details")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SEARCH ----------------
elif page == "🔍 Search Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Search Student")

    search = st.text_input("Enter student name")

    if search:
        if search in st.session_state.students:
            data = st.session_state.students[search]

            st.write(f"### {search}'s Results")

            df = pd.DataFrame(list(data.items()), columns=["Subject", "Score"])
            st.dataframe(df)

            avg = sum(data.values()) / len(data)
            st.write(f"**Average Score:** {avg:.2f}")

        else:
            st.warning("Student not found")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- STATS ----------------
elif page == "📊 Statistics":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Class Statistics")

    if st.session_state.students:
        all_scores = []
        highest = ("", "", -1)
        lowest = ("", "", 101)

        for name, subjects in st.session_state.students.items():
            for subject, score in subjects.items():
                all_scores.append(score)

                if score > highest[2]:
                    highest = (name, subject, score)

                if score < lowest[2]:
                    lowest = (name, subject, score)

        st.write(f"**Class Average:** {sum(all_scores)/len(all_scores):.2f}")
        st.write(f"**Highest:** {highest[0]} - {highest[1]} ({highest[2]})")
        st.write(f"**Lowest:** {lowest[0]} - {lowest[1]} ({lowest[2]})")

    else:
        st.info("No data yet")

    if st.button("🗑 Clear All Data"):
        st.session_state.students = {}
        st.success("All data cleared")

    st.markdown("</div>", unsafe_allow_html=True)
