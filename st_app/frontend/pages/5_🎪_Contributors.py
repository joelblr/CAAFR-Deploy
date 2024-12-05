import streamlit as st
import os


st.set_page_config(
    page_title="Contributors",
    page_icon="🎯",
    layout="wide"
)


imgDr = os.path.join(os.path.dirname(__file__), "..", "images")
# Contributors data
contributors = [
    {
        "name": "Joel A",
        "status": "4th-year CSE student @DSCE.",
        "usn": "1DS21CS095",
        "mobile": "9739687558",
        "GitHub": "github.com/joelblr",
        "role": "Team Lead & Developer",
    },
    {
        "name": "Karthik K H",
        "status": "4th-year CSE student @DSCE.",
        "usn": "1DS21CS096",
        "mobile": "6361898559",
        "GitHub": "github.com/katrathik",
        "role": "Team Lead & Developer",
    },
    {
        "name": "Katta Navya",
        "status": "4th-year CSE student @DSCE.",
        "usn": "1DS21CS097",
        "mobile": "8125674312",
        "GitHub": "github.com/kattanavya18",
        "role": "Team Lead & Developer",
    },
    {
        "name": "M Kavacin",
        "status": "4th-year CSE student @DSCE.",
        "usn": "1DS21CS111",
        "mobile": "9019969885",
        "GitHub": "github.com/kavacin",
        "role": "Team Lead & Developer",
    },
]

# Page title
st.title("Meet the Team 🛡️")
# st.title("🏆🔥Meet the Team🔥🏆")

# Display contributors
cols = st.columns(4)  # Adjust based on number of contributors

for i, contributor in enumerate(contributors):
    with cols[i % 4]:
        # for key, value in contributor.items():
        st.markdown(f'#### {contributor["name"]}')
        st.text(contributor["status"])
        st.markdown(f"⭐ **`{contributor['usn']}`**")
        st.markdown(f"📞 **`{contributor['mobile']}`**")
        st.markdown(f"🚀 **`{contributor['GitHub']}`**")
        # st.markdown(f"**Role:** {contributor['role']}")


st.markdown("---")
st.markdown(" ##### Various Roles Played")
st.markdown("`Team Lead` `Research Analyst` `Technical Writer` `Designer`")
st.markdown("`Data Engineer` `Data Analyst` `AI/ML Engineer` `Prompt Engineer`")
st.markdown("`Frontend Developer` `Backend Developer` `Software Testing Engineer`")
st.markdown("---")
st.markdown(" ##### Various Skills Displayed")
st.markdown("`Python` `Streamlit` `Flask` `Pandas/Numpy`")
st.markdown("`Matplotlib/Seaborn` `Scikit-learn` `NlTK` `LLMs`")
st.markdown("`Custom-tkinter` `Javascript` `Web` `APIs`")
st.markdown("`Git/GitHub`")
st.markdown("---")
