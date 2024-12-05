import streamlit as st
import os


st.set_page_config(
    page_title="Guide Page",
    page_icon="🔰",
    layout="wide"
)

hints = {
    0: 'At the Side-Nav-Bar you have various options. Select "CAAFR" to Launch the Comparative Analysis.',
    1: 'Select your desired Products\' Category & hit "Overall Stats" button to run the Comparative Analysis for that particular Category.',
    2: 'Select your desired Product (after choosing desired Product Category) & hit "Product-Wise Stats" button to run the Comparative Analysis for that particular Product.',
    3: 'Finally, after viewing the Stat-Analysis, click the "Back" Button to navigate back to Initial Phase.',
    4: 'To Scrape the Customer Reviews (Real Data) in Real Time, navigate to the "Scrape-Bot" from the Side-Nav-Bar. Click on the "Launch App" Button.',
    5: 'When the "Web Scraping Tool App" launches, we have various options from the Side-Nav-Bar.',
    6: 'Select the "Login" option from the Side-Nav-Bar, Enter the respective Credentials and hit "Login" Button to generate the Session Keys, with which we can initiate scraping process.',
    7: 'To locate all the Session Keys, Click on "Session History" option from Side-Nav-Bar & refresh the app. You can now copy-to-clipboard any key.',
    8: 'To scrape Customer Reviews, Click on "Amazon/Flipkart Scraper" option from Side-Nav-Bar. Enter the required details such as "Session-Key", "Product-Base-URL", "Product-Category". Further you can create a New Category (if not available in drop-down menu). To Refresh the Category-Menu, just toggle back & forth the Scrape-Mode.',
    9: 'Down below in the Scraper-Frame, you can find the Advanced Settings. You can toogle the Scrape-Mode which allows you to save the datasets in respective locations; You can further toggle the Browser-Visibility which enables/disable visibility of browser during scraping process. For the rest, you can choose to modify the values or leave it as recommended by the Developers.',
    10: 'Finally, after giving all the required & appropriate information, hit the "Generate" Button to generate "REAL-DATA in REAL-TIME" ✨✨',
}



gimgsDr = os.path.join(os.path.dirname(__file__), "..", "guide_imgs")

# st.header("Road Map")
st.subheader("Road Map, In case you got lost...!! 📌😅")
for i in range(11):
    st.markdown(f"### Step-{i+1}:")
    st.write(hints[i])
    st.image(os.path.join(gimgsDr, f"{i}.jpeg"))#, width=150)
    st.markdown("---")

docs = """
{

    "azon_data" : {
        "SSN_ID": "1",
        "PRODUCT_BASE_URL": "https://www.amazon.in/Samsung-Storage-Display-Charging-Security/product-reviews/B0DFY3XCB6/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
        "PRODUCT_NAME" : "Samsung_Galaxy_M05",
        "CATEGORY": "electronics",
        "FILE_NAME" : "Samsung_Galaxy_M05"
    },

    "fkart_data" : {
        "SSN_ID": "1",
        "PRODUCT_BASE_URL": "https://www.flipkart.com/motorola-g85-5g-viva-magenta-128-gb/product-reviews/itme67cc98574a7f?pid=MOBH35ZQFGVJFJ3W&lid=LSTMOBH35ZQFGVJFJ3WA8SV9M&marketplace=FLIPKART",
        "PRODUCT_NAME" : "Motorola_g85_5G",
        "CATEGORY": "electronics",
        "FILE_NAME" : "Motorola_g85_5G"
    }

}
"""
st.markdown("### Sample Inputs")
st.code(docs, language="json")