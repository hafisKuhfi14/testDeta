import streamlit as st  # pip install streamlit
import pandas as pd

from ..utils.textCleaning import textCleaning
from ..utils.table_text_preprocessing import text_preprocessing

"""Fitur ini digunakan di halaman text_predictor.py"""
def history(reviewtests): 
    for index, review_test in enumerate(reviewtests):
        with st.expander(f"Sentimen Predictor Testing ke-{index + 1}"):
            if "svm" in review_test["testing_model"].keys():
                st.markdown("### Sentimen Predictor SVM")
                textPolarity = review_test["testing_model"]["svm"]
                score = review_test["testing_model"]["svm"]["predictor"]
                text_predictor = review_test['text']
                del review_test["testing_model"]["svm"]["predictor"]
                text_predictor_clean, _ = textCleaning(pd.DataFrame([text_predictor], columns=["responding"]), neutral=True)
                sentimen_predictor(textPolarity, score, text_predictor_clean)

            if "nb" in review_test["testing_model"].keys():
                st.markdown("### Sentimen Predictor NB")
                textPolarity = review_test["testing_model"]["nb"]
                score = review_test["testing_model"]["nb"]["predictor"]
                del review_test["testing_model"]["nb"]["predictor"]
                sentimen_predictor(textPolarity, score, text_predictor_clean)

def sentimen_predictor(textPolarity, score, text_predictor_clean):
    # Temukan panjang maksimum dari array dalam dictionary
    max_length = max(len(textPolarity[key]) for key in textPolarity) 
    # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
    data_equal_length = {key: textPolarity[key] + [""] * (max_length - len(textPolarity[key])) for key in textPolarity}
    df = pd.DataFrame(data_equal_length) 
    st.table(df)
    
    if (score > 0):
        st.success("Ulasan tersebut bernada positive 😊")
        text_predictor_clean["polarity"] = "positive"
    elif(score < 0):
        st.error("Ulasan tersebut bernada negative 😡")
        text_predictor_clean["polarity"] = "negative"
    else:
        st.info("Ulasan tersebut bernada neutral")
        text_predictor_clean["polarity"] = "neutral"

    text_predictor_clean["polarity_score"] = score
    st.markdown("#### TextPreprocessing")
    text_preprocessing(text_predictor_clean)