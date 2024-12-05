import streamlit as st
import os
import base64


st.set_page_config(
    page_title="About",
    page_icon="ℹ",
    layout="wide"
)


# Custom Styling (you can adjust this as needed)
st.markdown("""
<style>
/* Default button style */
.stDownloadButton > button {
    font-size: 18px;
    padding: 10px;
    border-radius: 8px;
    background-color: #4CAF50; /* Default background */
    color: white; /* Default text color */
    border: none; /* No border by default */
    transition: all 0.3s ease; /* Smooth transition for changes */
}

/* Hover state: when mouse pointer is over the button */
.stDownloadButton > button:hover {
    background-color: #45a049; /* Darker background on hover */
    color: #13edcc; /* Change text color on hover */
    transform: scale(1.05); /* Slightly enlarge button on hover */
}

/* Active state: when the button is pressed (clicked) */
.stDownloadButton > button:active {
    background-color: #3e8e41; /* Darker background when clicked */
    color: #13edcc; /* Change text color when clicked */
    transform: scale(1); /* Return to original size */
}

/* Focus state: when the button is focused (e.g., clicked or tabbed) */
.stDownloadButton > button:focus {
    outline: none; /* Remove default outline */
    box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.5); /* Focus ring */
}

/* Normal state (after release) */
.stDownloadButton > button:focus:not(:active) {
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


mainDr = os.path.join(os.path.dirname(__file__), "..", "..", "..", "docs")

# Load a PDF file
pdf_url = os.path.join(mainDr, "Report.pdf")
with open(pdf_url, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()
# Encode the PDF to base64
base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
# Embed the PDF in the app
st.subheader("Report")
pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)
st.text("")
st.text("")
st.download_button(label="Download CAAFR-WST Report", data=pdf_bytes, file_name="Report-46.pdf", mime="application/pdf")
st.markdown("---")

# Load the image file
image_path = os.path.join(mainDr, "Banner.jpg")
with open(image_path, "rb") as img_file:
    img_bytes = img_file.read()
# Encode the image to base64
base64_img = base64.b64encode(img_bytes).decode('utf-8')
# Embed the image in the app
st.subheader("Banner")
st.image(image_path)
st.text("")
st.text("")
# Download button for the image
st.download_button(label="Download CAAFR-WST Banner", data=img_bytes, file_name="Banner.jpg", mime="image/jpeg")
# Separator
st.markdown("---")
