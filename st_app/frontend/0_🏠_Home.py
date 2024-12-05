# import streamlit as st


# st.set_page_config(
#     page_title="CAAFR + WST",
# )
# st.markdown("""
#     #### This app compares Pros, Cons and Neutral analysis results for product reviews on Amazon and Flipkart.
#     ##### It shows the accuracy, F1 score, classification report, confusion matrix, and Pros, Cons and Neutral distribution bar graph.
# """)
import streamlit as st


# Page Configuration
st.set_page_config(
    page_title="CAAFR + WST",
    page_icon="📊",
    layout="wide"
)


# Title Section with Styling
st.markdown(
    "<h1 style='text-align: center; color: #0D6EFD;'>Comparative Analysis of Customer Reviews</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; color: #6C757D;'>Amazon vs Flipkart</h2>",
    unsafe_allow_html=True
)

# Introduction Section
st.markdown("---")
st.header("📖 Overview")
st.write("""
The e-commerce boom has led to a flood of customer reviews, making it challenging for users to make 
informed decisions. The *Comparative Analysis of Amazon and Flipkart Reviews (CAAFR)* project 
simplifies this process by leveraging Machine Learning and sentiment analysis to:
- Categorize reviews into **`positive`**, **`negative`**, and **`neutral`** sentiments.
- Compare reviews across platforms for actionable insights.
- Provide user-friendly visualizations to help businesses and consumers make better decisions.
""")

# Key Features Section with Icons
st.markdown("---")
st.header("🌟 Key Features")
st.markdown("""
- **⚡ Real-time Data Scraping**: Stay up-to-date with the latest reviews using Puppeteer.
- **📊 Sentiment Classification**: VADER and Random Forest models for precise sentiment analysis.
- **📈 Interactive Visualizations**: Explore trends with bar charts, heatmaps, and more.
- **🛒 Actionable Insights**: Simplify purchase decisions and improve business strategies.
""")

# # Team Members Section with Cards
# st.markdown("---")
# st.header("👥 Meet the Team")
# team_members = {
#     "Joel A (Team Lead)": "1DS21CS095",
#     "Karthik K H": "1DS21CS096",
#     "Katta Navya": "1DS21CS097",
#     "M Kavacin": "1DS21CS111"
# }

# for name, id_code in team_members.items():
#     st.markdown(f"**{name}** - `{id_code}`")

# Comparative Analysis Section
st.markdown("---")
st.header("🔍 Comparative Analysis of Reviews")
st.write("""
Dive deeper into customer sentiments for products across Amazon and Flipkart. Using advanced tools:
- Sentiment Analysis uncovers the polarity of reviews.
- Comparison metrics highlight platform-specific strengths and weaknesses.
- Product-specific insights help users choose the best deals.
""")
# st.image("https://via.placeholder.com/800x400", caption="Visualization of Sentiment Trends", use_container_width=True)

# Results and Performance Section
st.markdown("---")
st.header("📊 Results and Performance")
st.write("""
Our analysis reveals:
- **VADER Accuracy**: ~85-90% for sentiment classification.
- **Random Forest Model**: Achieved precision and recall scores of ~87%.
- **User Impact**: Simplifies decision-making for customers and improves business insights.
""")
st.markdown("""
<blockquote style="font-style: italic; color: #6C757D;">
"Clearer, structured insights for consumers and actionable feedback for businesses."
</blockquote>
""", unsafe_allow_html=True)

# Technologies Used Section
st.markdown("---")
st.header("💻 Technologies Used")
tech_stack = [
    "`Python (Flask, Streamlit, Scikit-learn)`",
    "`Puppeteer` for Web Scraping",
    "`Random-Forest VADER` for Sentiment Analysis",
    "`Matplotlib` & `Seaborn` for Data Visualization",
]

for t in tech_stack:
    st.write(t)

# Footer Section
st.markdown("---")
st.markdown(
    """
    <footer style='text-align: center; font-size: 14px; color: #6C757D;'>
        © 2024 CAAFR Project Team. All rights reserved. <br>
        This project is licensed under the <a href="https://opensource.org/licenses/MIT" target="_blank" style="color: #0D6EFD; text-decoration: none;">MIT License</a>.
    </footer>
    """,
    unsafe_allow_html=True
)
# st.markdown(
#     "<footer style='text-align: center; color: #6C757D;'>"
#     "Project developed by the Department of Computer Science and Engineering, DSCE."
#     "</footer>",
#     unsafe_allow_html=True
# )
