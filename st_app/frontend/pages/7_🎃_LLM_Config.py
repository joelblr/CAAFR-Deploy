import streamlit as st
import pandas as pd
import sys, os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from EnvMgr import EnvManager


st.set_page_config(
    page_title="LLM Config Page",
    page_icon="🎃",
    layout="wide"
)

## Custom Styling (you can adjust this as needed)
st.markdown("""
<style>
/* Default button style */
.stTooltipHoverTarget > button {
    font-size: 18px;
    padding: 10px;
    border-radius: 8px;
    background-color: #4CAF50; /* Default background */
    color: white; /* Default text color */
    border: none; /* No border by default */
    transition: all 0.3s ease; /* Smooth transition for changes */
}

/* Hover state: when mouse pointer is over the button */
.stTooltipHoverTarget > button:hover {
    background-color: #45a049; /* Darker background on hover */
    color: #13edcc; /* Change text color on hover */
    transform: scale(1.05); /* Slightly enlarge button on hover */
}

/* Active state: when the button is pressed (clicked) */
.stTooltipHoverTarget > button:active {
    background-color: #3e8e41; /* Darker background when clicked */
    color: #13edcc; /* Change text color when clicked */
    transform: scale(1); /* Return to original size */
}

/* Focus state: when the button is focused (e.g., clicked or tabbed) */
.stTooltipHoverTarget > button:focus {
    outline: none; /* Remove default outline */
    box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.5); /* Focus ring */
}

/* Normal state (after release) */
.stTooltipHoverTarget > button:focus:not(:active) {
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



def create_groupBy_dict(csv_fname, group_by_attribute, value_column):
    llm_md = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database")
    # Read the uploaded CSV files into DataFrames
    f = os.path.join(llm_md, csv_fname)
    df = pd.read_csv(f)
    # Get unique categories
    unique_categories = df[group_by_attribute].unique().tolist()
    # Create a dictionary that maps category to list of product names
    groupBy_dict = {}
    for category in unique_categories:
        products_in_category = df[df[group_by_attribute] == category][value_column].tolist()
        groupBy_dict[category] = sorted(products_in_category)
    return groupBy_dict


def get_chosen_options(model_name, model_src):
    for i, src in enumerate(ms_dict):
        if model_src==src:
            return (i, ms_dict[src].index(model_name))
    return (0, 0)


with st.spinner("Loading LLM Config... Plz Wait."):
    env_mgr = EnvManager(".env")
    ms_dict = create_groupBy_dict("llm_meta_data.csv", "Model_Source", "Model_Name")
    selected_model_name = env_mgr.get_env_key("LLM_MODEL")
    selected_model_src = env_mgr.get_env_key("LLM_SRC")
    src_idx, model_idx = get_chosen_options(selected_model_name, selected_model_src)


st.header("LLM Configuration")
st.info(
    body="Visit [console.groq.com](https://console.groq.com/keys) to Generate the API-Keys",
    icon="💎"
)
api_key = st.text_input(label="Enter API-KEY", placeholder="Starts with gsk_...", key="1")
model_source = st.selectbox(label="Select LLM model_source", options=ms_dict.keys(), index=src_idx)

if model_source != env_mgr.get_env_key("LLM_SRC"):
    model_idx = 0

model_name = st.selectbox("Select LLM Model", options=ms_dict[model_source], index=model_idx)


done = st.button("Update Config", icon="✔", help="Update Data")


if done:
    with st.spinner("Settings is being configured... Plz Wait."):
        if api_key:
            env_mgr.update_env_key("LLM_API_KEY", api_key)
        env_mgr.update_env_key("LLM_MODEL", model_name)
        env_mgr.update_env_key("LLM_SRC", model_source)

    st.success("LLM Model is Configured. 🎉")
    st.snow()
