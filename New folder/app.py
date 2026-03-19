import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Portal Pro", layout="centered")

# ---------- SAFE STORAGE FIX ----------
if "students" not in st.session_state or not isinstance(st.session_state.students, dict):
    st.session_state.students = {}

students = st.session_state.students

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

# ---------- NAV ----------
page = st.selectbox("Menu", ["Home", "Add Student", "Search", "Statistics"])

# ---------- HOME ----------
if page == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Welcome 👋")
    st.write("Full student system with search, edit, stats.")
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
            data = {}
            for sub, sc in zip(subjects, scores):
                if sub:
                    data[sub] = sc

            if data:
                students[name] = data
                st.success("Saved ✅")
            else:
                st.error("Enter at least one subject")
        else:
            st.error("Enter name")

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
        st.write(f"Average: {avg:.2f}")

        # DELETE
        if st.button("Delete Student"):
            del students[selected]
            st.success("Deleted")
            st.rerun()

        # EDIT
        st.subheader("Edit Scores")

        new_data = {}
        for subject, score in data.items():
            new_score = st.number_input(subject, 0, 100, score, key=subject)
            new_data[subject] = new_score

        if st.button("Update"):
            students[selected] = new_data
            st.success("Updated")

    else:
        st.info("No students yet")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- STATS ----------
elif page == "Statistics":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Statistics")

    if students:
        all_scores = []
        names = []
        averages = []

        highest = ("", "", -1)
        lowest = ("", "", 101)

        for name, subs in students.items():  # FIXED ERROR HERE
            scores = list(subs.values())
            avg = sum(scores) / len(scores)

            names.append(name)
            averages.append(avg)

            for subject, score in subs.items():
                all_scores.append(score)

                if score > highest[2]:
                    highest = (name, subject, score)

                if score < lowest[2]:
                    lowest = (name, subject, score)

        st.write(f"Class Avg: {sum(all_scores)/len(all_scores):.2f}")
        st.write(f"Highest: {highest}")
        st.write(f"Lowest: {lowest}")

        # 📊 CHART
        chart_df = pd.DataFrame({
            "Student": names,
            "Average": averages
        })

        st.bar_chart(chart_df.set_index("Student"))

        # CLEAR
        if st.button("Clear All"):
            st.session_state.students = {}
            st.success("Cleared")
            st.rerun()

    else:
        st.info("No data")

    st.markdown("</div>", unsafe_allow_html=True)
