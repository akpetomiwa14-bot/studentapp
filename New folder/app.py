import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ultimate School Portal", layout="centered")

# ---------- SESSION STATE ----------
if "students" not in st.session_state or not isinstance(st.session_state.students, dict):
    st.session_state.students = {}
students = st.session_state.students

# ---------- STYLE ----------
st.markdown("""
<style>
body {background-color: #F4F8FB; font-family: 'Arial', sans-serif;}
.title {text-align:center; font-size:40px; font-weight:bold; color:#2A3F5F; margin-bottom:5px;}
.subtitle {text-align:center; font-size:18px; color:#5A6B7C; margin-bottom:25px;}
.card {background:white; padding:30px; border-radius:20px; box-shadow:0px 10px 25px rgba(0,0,0,0.08); margin-bottom:25px;}
.stButton>button {background:#A7C7E7; color:#000; font-size:18px; border-radius:12px; padding:12px 20px; border:none; transition:0.3s;}
.stButton>button:hover {transform: scale(1.08); background:#91BEE0;}
.stDataFrame>div>div>div>div {border-radius:12px; overflow:hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🎓 Ultimate School Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Manage Students | Reports | Analytics</div>", unsafe_allow_html=True)

# ---------- NAVIGATION ----------
page = st.selectbox("Menu", ["Home", "Add Student", "Search/Edit", "Class Statistics", "Reports"])

# ---------- HOME ----------
if page == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Welcome to the Ultimate School Portal! 👋")
    st.write("Use the menu to add students, search and edit records, view class statistics, and export reports.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ADD STUDENT ----------
elif page == "Add Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Add Student")
    name = st.text_input("Student Name")
    
    subjects = []
    scores = []
    for i in range(5):  # max 5 subjects per student
        col1, col2 = st.columns([2,1])
        subjects.append(col1.text_input(f"Subject {i+1}", key=f"sub{i}"))
        scores.append(col2.number_input(f"Score {i+1}", 0, 100, key=f"score{i}"))
    
    def get_grade(score):
        if score >= 70: return "A"
        elif score >= 60: return "B"
        elif score >= 50: return "C"
        elif score >= 45: return "D"
        else: return "F"

    if st.button("Save Student"):
        if not name:
            st.error("Enter student name")
        else:
            data = {sub: (sc, get_grade(sc)) for sub, sc in zip(subjects, scores) if sub}
            if data:
                students[name] = data
                st.success("✅ Student saved")
            else:
                st.error("Enter at least one subject")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- SEARCH / EDIT ----------
elif page == "Search/Edit":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Search / Edit Student")
    
    if students:
        selected = st.selectbox("Select Student", list(students.keys()))
        data = students[selected]
        
        # Show table
        df = pd.DataFrame([(sub, sc, grade) for sub, (sc, grade) in data.items()],
                          columns=["Subject","Score","Grade"])
        st.dataframe(df)
        
        # Edit
        st.subheader("Edit Scores")
        updated_data = {}
        for sub, (sc, _) in data.items():
            new_score = st.number_input(sub, 0, 100, sc, key=f"edit_{sub}")
            updated_data[sub] = (new_score, get_grade(new_score))
        
        if st.button("Update Student"):
            students[selected] = updated_data
            st.success("Student updated ✅")
            st.experimental_rerun()
        
        if st.button("Delete Student"):
            del students[selected]
            st.success("Student deleted 🗑")
            st.experimental_rerun()
    else:
        st.info("No students yet")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- CLASS STATISTICS ----------
elif page == "Class Statistics":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Class Statistics")
    
    if students:
        all_scores = []
        names, averages = [], []
        highest = ("", "", "", -1)
        lowest = ("", "", "", 101)
        
        subject_totals = {}
        subject_counts = {}
        
        for name, subs in students.items():
            scores_list = []
            for sub, (score, _) in subs.items():
                scores_list.append(score)
                subject_totals[sub] = subject_totals.get(sub,0)+score
                subject_counts[sub] = subject_counts.get(sub,0)+1
                if score > highest[3]: highest=(name,sub,_,score)
                if score < lowest[3]: lowest=(name,sub,_,score)
            avg = sum(scores_list)/len(scores_list)
            names.append(name)
            averages.append(avg)
            all_scores.extend(scores_list)
        
        st.write(f"**Class Average:** {sum(all_scores)/len(all_scores):.2f}")
        st.write(f"**Highest Score:** {highest[0]} - {highest[1]} ({highest[3]})")
        st.write(f"**Lowest Score:** {lowest[0]} - {lowest[1]} ({lowest[3]})")
        
        # Subject averages
        st.subheader("Subject Averages")
        for sub in subject_totals:
            st.write(f"{sub}: {subject_totals[sub]/subject_counts[sub]:.2f}")
        
        # Charts
        chart_df = pd.DataFrame({"Student": names, "Average": averages})
        st.bar_chart(chart_df.set_index("Student"))
    else:
        st.info("No data")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- REPORTS ----------
elif page == "Reports":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Export Student Data")
    
    if students:
        export_df = pd.DataFrame(columns=["Student","Subject","Score","Grade"])
        for name, subs in students.items():
            for sub,(score, grade) in subs.items():
                export_df = pd.concat([export_df,pd.DataFrame([[name,sub,score,grade]],columns=export_df.columns)],ignore_index=True)
        
        st.dataframe(export_df)
        st.download_button("Download CSV", export_df.to_csv(index=False), "students.csv", "text/csv")
        st.download_button("Download Excel", export_df.to_excel(index=False, engine='openpyxl'), "students.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("No data")
    st.markdown("</div>", unsafe_allow_html=True)
