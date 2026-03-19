import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Portal", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
body {
    background-color: #F4F8FB;
}

.main-title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.05);
}

.stButton>button {
    background-color: #A7C7E7;
    color: black;
    font-size: 18px;
    padding: 12px;
    border-radius: 10px;
    border: none;
    transition: 0.2s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background-color: #91BEE0;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<div class='main-title'>🎓 Student Portal</div>", unsafe_allow_html=True)

# ---------- STORAGE ----------
if "students" not in st.session_state:
    st.session_state.students = []

# ---------- NAV ----------
menu = st.sidebar.selectbox("Menu", ["Home", "Add Student", "View Students"])

# ---------- HOME ----------
if menu == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Welcome 👋")
    st.write("Use the sidebar to navigate.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ADD STUDENT ----------
elif menu == "Add Student":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Add Student")

    with st.form("form"):
        name = st.text_input("Student Name")
        subject = st.text_input("Subject")
        score = st.number_input("Score", min_value=0, max_value=100)

        submit = st.form_submit_button("Add Student")

        if submit:
            if name and subject:
                st.session_state.students.append({
                    "Name": name,
                    "Subject": subject,
                    "Score": score
                })
                st.success("Student added!")
            else:
                st.error("Fill all fields")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- VIEW ----------
elif menu == "View Students":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)
        st.dataframe(df)
    else:
        st.info("No students yet")

    st.markdown("</div>", unsafe_allow_html=True)