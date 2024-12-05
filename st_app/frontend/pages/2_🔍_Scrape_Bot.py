import streamlit as st
import threading
import os, sys, subprocess
import time
import logging


# Set up Streamlit page configuration
st.set_page_config(
    page_title="Web Scraper Tool",
    page_icon="🔍",
    layout="wide"
)

# Path to your script (adjust as necessary)
run_app_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "wst_app", "app", "run.py")

# Configure logging to save logs to a file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='st_app_logs.log',
    filemode='w'
)


# Function to run the script
def run_py_script(script_path):
    py_exec = sys.executable
    logging.debug(f"Attempting to run script using Python executable: {py_exec}")

    if not os.path.exists(script_path):
        logging.error(f"Script not found: {script_path}")
        return

    try:
        logging.info(f"Running script: {script_path}")
        result = subprocess.run([py_exec, script_path], check=True, capture_output=True, text=True)

        logging.info(f"Script ran successfully. Output:\n{result.stdout}")
    except Exception as e:
        logging.error(f"An error occurred while running the script: {e}")

    st.session_state.is_scraping = False  # Mark the process as complete



# Custom Styling (you can adjust this as needed)
st.markdown("""
<style>
/* Default button style */
.stButton > button {
    font-size: 18px;
    padding: 10px;
    border-radius: 8px;
    background-color: #4CAF50; /* Default background */
    color: white; /* Default text color */
    border: none; /* No border by default */
    transition: all 0.3s ease; /* Smooth transition for changes */
}

/* Hover state: when mouse pointer is over the button */
.stButton > button:hover {
    background-color: #45a049; /* Darker background on hover */
    color: #13edcc; /* Change text color on hover */
    transform: scale(1.05); /* Slightly enlarge button on hover */
}

/* Active state: when the button is pressed (clicked) */
.stButton > button:active {
    background-color: #3e8e41; /* Darker background when clicked */
    color: #13edcc; /* Change text color when clicked */
    transform: scale(1); /* Return to original size */
}

/* Focus state: when the button is focused (e.g., clicked or tabbed) */
.stButton > button:focus {
    outline: none; /* Remove default outline */
    box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.5); /* Focus ring */
}

/* Normal state (after release) */
.stButton > button:focus:not(:active) {
    font-size: 18px;
    padding: 10px;
    border-radius: 8px;
    background-color: #4CAF50; /* Default background */
    color: white; /* Default text color */
    border: none; /* No border by default */
    transition: all 0.3s ease; /* Smooth transition for changes */
}
</style>
""", unsafe_allow_html=True)

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

st.title("Web Scraper Tool")
st.warning(icon="⚠", body="Ensure to Scrap Reviews in both Amazon & Flipkart for a given Category/Product to perform Comparative Analysis")
st.write("Click the button below to start the data scraping process.")

# Session State to track if the process is running
if "is_scraping" not in st.session_state:
    st.session_state.is_scraping = False

# Placeholder to update the UI dynamically (spinner or button)
if st.button("Launch Web Scraper Bot", key="b123") :
    with st.spinner("Scraping data in progress... Please wait."):
        st.code(docs, language="json")
        run_py_script(run_app_path)
    st.snow()
