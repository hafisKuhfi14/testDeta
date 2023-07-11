import pickle
import streamlit as st  # pip install streamlit
import pandas as pd
from ..modules import model
from ..utils.textCleaning import textCleaning

async def text_predictor():
    st.markdown("### Input Ulasan")
    with st.form("text_predictor_form", clear_on_submit=True):
        text_predictor = st.text_area("Text Predictor", placeholder="Masukan ulasan anda yang akan dianalis")

        submit = st.form_submit_button("Analyze")
    "---"
    if submit:
        if text_predictor == "":
            st.error("OOPPSS... Kolom ulasan tidak terisi")
            return

        pickle_in = open('model.pkl', 'rb')
        svm, tfidf = pickle.load(pickle_in)
        text_predictor, _ = textCleaning(pd.DataFrame([text_predictor], columns=["responding"]), neutral=True)

        textPolarity = { "positive": [], "negative": []}
        for text in text_predictor['Text_Clean_split'][0]:
            y_pred, _ = model.predictFromPKL(tfidf, svm, [text]) 
            if (y_pred[0] == "negative"):
                textPolarity['negative'].append(text)
            if (y_pred[0] == "positive"):
                textPolarity['positive'].append(text)

        if (len(textPolarity['positive']) > len(textPolarity['negative']) 
            or len(textPolarity["positive"]) == 0 or len(textPolarity["negative"]) == 0):
            st.success("Ulasan tersebut bernada positive 😊")
        else:
            st.error("Ulasan tersebut bernada negative 😡")
        st.write("Sentimen Per-kata suatu ulasan")
        # Temukan panjang maksimum dari array dalam dictionary
        max_length = max(len(textPolarity[key]) for key in textPolarity) 
        # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
        data_equal_length = {key: textPolarity[key] + [""] * (max_length - len(textPolarity[key])) for key in textPolarity}
        df = pd.DataFrame(data_equal_length) 
        st.table(df)

