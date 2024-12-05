from models.RF_Vader import *


def install_packages():
    install_dependencies()


def fetch_stats(product_name, category, company):

    df = get_filtered_df(product_name, category, company)
    remove_short_words(df)
    handle_NAN(df)

    vaders = get_polarity_scores(df)
    apply_sentiment_function(vaders)
    posCount, neuCount, negCount = get_count_vectors(vaders)

    X = get_fit_transform(vaders)
    y = encode_labels(vaders)
    X_train, X_test, y_train, y_test = split_data_train_test(X, y)
    y_pred = train_test_RF_model(X_train, y_train, X_test)

    accuracy, f1_score, report = get_scores(y_test, y_pred)
    cm = get_confusion_matrix(y_test, y_pred)
    matrix_b64 = convert_confusion_matrix_to_base64(cm)

    info =  {
            'accuracy': accuracy,
            'f1_score': f1_score,
            'classification_report': report,
            'positive_count': posCount,
            'neutral_count': neuCount,
            'negative_count': negCount,
            'confusion_matrix_image': matrix_b64
        }

    return info
