import streamlit as st
import requests
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


st.set_page_config(
    page_title="CAAFR",
    page_icon="🚀",
    layout="wide",
)

## Images
imgDr = os.path.join(os.path.dirname(__file__), "..", "images")
azon_ico = os.path.join(imgDr, "azon.svg")
fkart_ico = os.path.join(imgDr, "fkart.svg")


## Custom Styling (you can adjust this as needed)
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


def display_final_results(data):

    cols = st.columns([2,1,2])
    with cols[0]:
        cols[0].text("")
        cols[0].text("")
        cols[0].text("")
        st.image(azon_ico, width=170)
    with cols[1]:
        st.markdown("# vs")
    with cols[2]:
        cols[2].text("")
        cols[2].text("")
        st.image(fkart_ico, width=200)

    col1,col2 = st.columns(2)
    with col1:
        # Display results for Amazon
        st.subheader("Amazon Pros, Cons and Neutral Analysis Results")
        st.write(f"Accuracy: {data['azon']['accuracy']:.4f}")
        st.write(f"F1 Score (Weighted): {data['azon']['f1_score']:.4f}")
        st.subheader("Classification Report - Amazon:")
        st.dataframe(data['azon']['classification_report'])
        st.subheader("Confusion Matrix - Amazon:")
        display_confusion_matrix(data['azon']['confusion_matrix_image'])

    with col2:
        # Display results for Flipkart
        st.subheader("Flipkart Pros, Cons and Neutral Analysis Results")
        st.write(f"Accuracy: {data['fkart']['accuracy']:.4f}")
        st.write(f"F1 Score (Weighted): {data['fkart']['f1_score']:.4f}")
        st.subheader("Classification Report - Flipkart:")
        st.dataframe(data['fkart']['classification_report'])
        st.subheader("Confusion Matrix - Flipkart:")
        display_confusion_matrix(data['fkart']['confusion_matrix_image'])

    # Display the grouped bar chart
    azon_counts = [
        data['azon']['positive_count'],
        data['azon']['neutral_count'],
        data['azon']['negative_count']
    ]
    fkart_counts = [
        data['fkart']['positive_count'],
        data['fkart']['neutral_count'],
        data['fkart']['negative_count']
    ]
    plot_grouped_bar_chart(azon_counts, fkart_counts)

    ## %ile wrt two companies
    # total_pos = data['azon']['positive_count'] + data['fkart']['positive_count']
    # total_neu = data['azon']['neutral_count'] + data['fkart']['neutral_count']
    # total_neg = data['azon']['negative_count'] + data['fkart']['negative_count']
    # posper_azon = (data['azon']['positive_count']/(total_pos))
    # posper_fkart = (data['fkart']['positive_count']/(total_pos))
    # negper_azon = (data['azon']['negative_count']/(total_neg))
    # negper_fkart = (data['fkart']['negative_count']/(total_neg))

    ## %ile wrt a company itself
    azon_total = 0
    fkart_total = 0
    for key in ["positive_count", "neutral_count", "negative_count"]:
        azon_total += data['azon'][key]
        fkart_total += data['fkart'][key]

    posper_azon = (data['azon']['positive_count']/(azon_total))
    posper_fkart = (data['fkart']['positive_count']/(fkart_total))
    negper_azon = (data['azon']['negative_count']/(azon_total))
    negper_fkart = (data['fkart']['negative_count']/(fkart_total))
    neuper_azon = (data['azon']['neutral_count']/(azon_total))
    neuper_fkart = (data['fkart']['neutral_count']/(fkart_total))

    # joel's ideas to be added
    # if posper_azon > posper_fkart and negper_azon > negper_fkart:
    #     with cols[1]:
    #         cols[1].text("")
    #         st.image(azon_ico, width=150)
    #     with cols[0]:
    #         st.success("You may or may not get a good product amazon")
    # elif posper_fkart > posper_azon and negper_fkart > negper_azon:
    #     with cols[1]:
    #         st.image(fkart_ico, width=200)
    #     with cols[0]:
    #         st.success("You may or may not get a good product in flipkart")

    st.markdown("---")
    st.subheader("Suggestions")
    st.markdown(data["llm_suggestion"])
    # cols = st.columns([1, 1])
    # if posper_azon > posper_fkart:
    #     with cols[1]:
    #         cols[1].text("")
    #         st.image(azon_ico, width=150)
    #     with cols[0]:
    #         st.success("If Count of Positive Comments should have greatest Percentile, then Amazon is a Better.")
    # elif posper_fkart > posper_azon:
    #     with cols[1]:
    #         st.image(fkart_ico, width=200)
    #     with cols[0]:
    #         st.success("If Count of Positive Comments should have greatest Percentile, then Flipkart is a Better.")
    # st.markdown("---")
    # cols = st.columns([1, 1])
    # if negper_azon > negper_fkart:
    #     with cols[1]:
    #         st.image(fkart_ico, width=200)
    #     with cols[0]:
    #         st.success("If Count of Negative Comments should have least Percentile, then Flipkart is a Better.")
    # elif negper_fkart > negper_azon:
    #     with cols[1]:
    #         cols[1].text("")
    #         st.image(azon_ico, width=150)
    #     with cols[0]:
    #         st.success("If Count of Negative Comments should have least Percentile, then Amazon is a Better.")
    st.markdown("---")


# Function to display confusion matrix from base64
def display_confusion_matrix(img_b64):
    img_data = base64.b64decode(img_b64)
    img = BytesIO(img_data)

    fig, ax = plt.subplots(figsize=(6, 6))
    img = plt.imread(img, format='png')
    ax.imshow(img)
    ax.axis('off')  # Hide axis labels
    st.pyplot(fig)


def plot_grouped_bar_chart(amazon_counts, flipkart_counts):

    width = 0.4  # Width of the bars
    labels = ['POSITIVE', 'NEUTRAL', 'NEGATIVE']
    x = np.arange(len(labels))  # Label positions

    # Create a bar chart with the selected colors
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width / 2, amazon_counts, width, label='Amazon')
    ax.bar(x + width / 2, flipkart_counts, width, label='Flipkart')

    # Set chart labels and title
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    ax.set_title('Pros, Cons and Neutral Distribution in Amazon vs Flipkart')
    ax.legend()

    # Display the plot
    st.pyplot(fig)

st.title("Comparitive Analysis: Amazon vs Flipkart")

st.warning(icon="⚠", body="Ensure to Scrap Reviews in both Amazon & Flipkart for a given Category/Product to perform Comparative Analysis")


def create_category_product_dict(df):
    # Get unique categories
    unique_categories = df['Category'].unique().tolist()
    # Create a dictionary that maps category to list of product names
    category_dict = {}
    for category in unique_categories:
        products_in_category = df[df['Category'] == category]['Product_Name'].tolist()
        category_dict[category] = products_in_category
    return category_dict


def get_common_catg_prods():
    md_azon = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "azon")
    md_fkart = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "fkart")
    # Read the uploaded CSV files into DataFrames
    f1 = os.path.join(md_azon, "meta_data.csv")
    f2 = os.path.join(md_fkart, "meta_data.csv")
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)
    # Create category-product dictionaries for both CSV files
    dict_1 = create_category_product_dict(df1)
    dict_2 = create_category_product_dict(df2)
    # Find the intersection of categories
    common_categories = set(dict_1.keys()).intersection(set(dict_2.keys()))
    # Create a new dictionary to store the intersection of products for each common category
    common_dict = {}
    for category in common_categories:
        # Find the intersection of products for the current category
        products_in_common = list(set(dict_1[category]).intersection(set(dict_2[category])))
        if products_in_common:  # Only add category if it has intersecting products
            common_dict[category] = products_in_common
    return common_dict


catg_prod = get_common_catg_prods()


col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    col1.text(""); col1.text("")
    st.write("Product Category")
    col1.text(""); col1.text("")
    st.write("Select a Product")
with col2:
    category = st.selectbox(label="Select Category", options=sorted(catg_prod.keys()))
    productName = st.selectbox("Select Product", options=sorted(catg_prod[category]))
with col3:
    col3.text("")
    overall_stats = st.button("Overall Stats")
    col3.text("")
    pw_stats = st.button("Product-Wise Stats")


# # Fetch the analysis results <category-wise> from the Flask API
if overall_stats:
    with st.spinner("Model is getting Trained... Plz wait"):
        try:
            url = f"http://127.0.0.1:5000/analysis?category={category}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Analysis for {category.capitalize()} Completed !!")
                display_final_results(data)
                st.snow()

        except Exception as e:
            st.error(f"Error fetching data: {e}")

        finally:
            if st.button("Back"):
                st.experimental_redirect("/")


# # Fetch the analysis results <product-wise> from the Flask API
if pw_stats:
    with st.spinner("Model is getting Trained... Plz wait"):
        try:
            url = f"http://127.0.0.1:5000/analysis?category={category}&productName={productName}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Analysis for {productName}:({category.capitalize()}) Completed !!")
                display_final_results(data)
                st.snow()

        except Exception as e:
            st.error(f"Error fetching data: {e}")

        finally:
            if st.button("Back"):
                st.experimental_redirect("/")
