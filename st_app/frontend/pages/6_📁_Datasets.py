import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Datasets Page",
    page_icon="📁",
    layout="wide"
)


# Function to get file details
def get_csv_files(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            files.append((filename, round(file_size, 2)))
    return files

# Function to display CSV files and their content
def display_csv_files(directory, label):
    csv_files = get_csv_files(directory)
    df = pd.DataFrame(csv_files, columns=["Filename", "Size (KB)"])
    
    st.write(f"### {label} Datasets")
    st.dataframe(df)
    
    file_to_open = st.selectbox(f"Select a CSV file from {label}", df["Filename"])
    if file_to_open:
        file_path = os.path.join(directory, file_to_open)
        data = pd.read_csv(file_path)
        st.write(f"### Content of {file_to_open}")
        st.dataframe(data)

# Directories for Amazon and Flipkart datasets
azon_dbDr = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "azon")
fkart_dbDr = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "fkart")

# Create two columns for displaying datasets side by side
col1, col2 = st.columns(2)

with col1:
    display_csv_files(azon_dbDr, "Amazon")
    
with col2:
    display_csv_files(fkart_dbDr, "Flipkart")
