import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Portal Pro", layout="centered")

# ---------- SAFE STORAGE ----------
if "students" not in st.session_state or not isinstance(st.session_state.students, dict):
    st.session_state.students = {}
students = st.session_state.students

# ---------- STYLE ----------
st.markdown("""
<style>
body {
    background-color: #F4F8FB;
    font-family: 'Arial', sans-serif;
}

/* HEADER */
.title {
    text-align:center;
    font-size:36px;
    font-weight:bold;
    margin-bottom:5px;
    color: #2A3F5F;
}
.subtitle {
    text-align:center;
    font-size:18px;
    margin-bottom:25px;
    color: #5A6B7C;
}

/* CARDS */
.card {
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0px 10px 25px rgba(0,0,0,0.08);
    margin-bottom:25px;
}

/* BUTTONS */
.stButton>button {
    background:#A7C7E7;
    color:#000;
    font-size:18px;
    border-radius:12px;
    padding:12px 20px;
    border:none;
    transition:0.3s;
}
.stButton>button:hover {
    transform: scale(1.08);
    background:#91BEE0;
}

/* TABLES */
.stDataFrame>div>div>div>div {
    border-radius:12px;
    overflow:hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='title'>🎓 Student Portal Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Manage students, view reports, track performance</div>", unsafe_allow_html=True)

# ---------- NAV ----------
page = st.selectbox("Menu", ["Home", "Add Student", "Search", "Statistics"])

# ---------- HOME ----------
if page == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Welcome 👋")
    st.write("This is your professional school portal. Use the menu above to manage students, search, and track class performance.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ADD ----------
elif page == "Add Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Add Student")

    name = st.text_input("Student Name")

    subjects = []
    scores = []

    for i in range(3):
        col1, col2 = st.columns(2)
        subjects.append(col1.text_input(f"Subject {i+1}", key=f"sub{i}"))
        scores.append(col2.number_input(f"Score {i+1}", 0, 100, key=f"score{i}"))

    if st.button("Save"):
        if name:
            data = {sub: sc for sub, sc in zip(subjects, scores) if sub}
            if data:
                students[name] = data
                st.success("✅ Student saved")
            else:
                st.error("Enter at least one subject")
        else:
            st.error("Enter student name")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SEARCH ----------
elif page == "Search":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Search Student")

    if students:
        selected = st.selectbox("Select Student", list(students.keys()))
        data = students[selected]

        df = pd.DataFrame(list(data.items()), columns=["Subject", "Score"])
        st.dataframe(df)

        avg = sum(data.values()) / len(data)
        st.write(f"Average Score: **{avg:.2f}**")

        # EDIT
        st.subheader("Edit Scores")
        new_data = {}
        for subject, score in data.items():
            new_score = st.number_input(subject, 0, 100, score, key=f"edit_{subject}")
            new_data[subject] = new_score
        if st.button("Update Student"):
            students[selected] = new_data
            st.success("Student updated ✅")
            st.experimental_rerun()

        # DELETE
        if st.button("Delete Student"):
            del students[selected]
            st.success("Student deleted 🗑")
            st.experimental_rerun()
    else:
        st.info("No students yet")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- STATISTICS ----------
elif page == "Statistics":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Class Statistics")

    if students:
        all_scores = []
        names = []
        averages = []

        highest = ("", "", -1)
        lowest = ("", "", 101)

        for name, subs in students.items():
            scores = list(subs.values())
            avg = sum(scores)/len(scores)
            names.append(name)
            averages.append(avg)

            for subject, score in subs.items():
                all_scores.append(score)
                if score > highest[2]:
                    highest = (name, subject, score)
                if score < lowest[2]:
                    lowest = (name, subject, score)

        st.write(f"**Class Average:** {sum(all_scores)/len(all_scores):.2f}")
        st.write(f"**Highest Score:** {highest[0]} - {highest[1]} ({highest[2]})")
        st.write(f"**Lowest Score:** {lowest[0]} - {lowest[1]} ({lowest[2]})")

        # CHART
        chart_df = pd.DataFrame({"Student": names, "Average": averages})
        st.bar_chart(chart_df.set_index("Student"))

        # CLEAR
        if st.button("Clear All Data"):
            st.session_state.students = {}
            st.success("All data cleared")
            st.experimental_rerun()

    else:
        st.info("No data yet")
    st.markdown("</div>", unsafe_allow_html=True)
