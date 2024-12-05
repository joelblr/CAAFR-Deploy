import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm import tqdm

# # Initialize Flask app
import os
dbDir = os.path.join(os.path.dirname(__file__), "..", "..", "database")


# Initialize Sentiment Intensity Analyzer
# nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
# Vectorize the text data
vectorizer = TfidfVectorizer(max_features=5000)

# Install Dependencies
def install_dependencies():
    nltk.download("vader_lexicon")


# Load datasets
def get_filtered_df(product_name, category, company):

    dsDir = os.path.join(dbDir, company)
    filename = f"final_{company}_{category}.csv"
    df = pd.read_csv(os.path.join(dsDir, filename))
    if len(product_name.strip()) != 0:
        filtered_df =  df[df["Product_Name"] == product_name]
        if not filtered_df.empty:
            df = filtered_df
    return df


# Remove short words and handle NaN values
def remove_short_words(df) :
    df["Review_Text"] = df["Review_Text"].fillna("").apply(lambda x: " ".join([w for w in str(x).split() if len(w) > 2]))


# Handle NaN in Customer_Name (if exists)
def handle_NAN(df) :
    df["Customer_Name"] = df["Customer_Name"].fillna("Unknown")


# Function to calculate sentiment score
def run_sentiment_analysis(df):
    res = {}
    for i, row in tqdm(df.iterrows(), total=len(df)):
        text = row["Review_Text"]
        myid = row["Customer_Name"]
        res[myid] = sia.polarity_scores(text)

    vaders = pd.DataFrame(res).T
    vaders = vaders.reset_index().rename(columns={"index": "Customer_Name"})
    return vaders.merge(df, on="Customer_Name", how="left")


# Run sentiment analysis for both datasets
def get_polarity_scores(df) :
    vaders = run_sentiment_analysis(df)
    return vaders


def Rating_to_sentiment(compound):
    try:
        compound = min(max(float(compound), -0.7), 0.7)
    except:
        return "neutral"

    a, b, c, d = -0.7, -0.55, 0.33, 0.7
    if a <= compound < b:
        return "negative"
    elif b <= compound <= c:
        return "neutral"
    elif c < compound <= d:
        return "positive"
    return "neutral"


# Apply sentiment function to both datasets
def apply_sentiment_function(vaders):
    vaders["sentiment"] = vaders["compound"].apply(Rating_to_sentiment)


# Count sentiment distribution
def count_sentiment(df):
    posCount = int((df["sentiment"] == "positive").sum())
    neuCount = int((df["sentiment"] == "neutral").sum())
    negCount = int((df["sentiment"] == "negative").sum())
    return posCount, neuCount, negCount


def get_count_vectors(vaders):
    posCount, neuCount, negCount = count_sentiment(vaders)
    return (posCount, neuCount, negCount)


def get_fit_transform(vaders):
    X = vectorizer.fit_transform(vaders["Review_Text"])
    return X


# Encode the labels
def encode_labels(vaders):
    y = vaders["sentiment"].map({"negative": -1, "neutral": 0, "positive": 1})
    return y


# Split data into training and testing sets
def split_data_train_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return (X_train, X_test, y_train, y_test)


# Train Random Forest models
# if want, add thsi too --> n_estimators=100, max_depth=10
def train_test_RF_model(X_train, y_train, X_test):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred


# Calculate metrics for both datasets
def calculate_metrics(y_test, y_pred):
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    report = classification_report(y_test, y_pred, output_dict=True)
    return (accuracy, f1, report)

def get_scores(y_test, y_pred):
    accuracy, f1_score, report = calculate_metrics(y_test, y_pred)
    return (accuracy, f1_score, report)


# Generate confusion matrices
def get_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    return cm


# Function to convert confusion matrix to base64
def confusion_matrix_to_base64(cm):
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, annot_kws={"size": 16})
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_b64


# Convert confusion matrices to base64
def convert_confusion_matrix_to_base64(cm):
    matrix_b64 = confusion_matrix_to_base64(cm)
    return matrix_b64
