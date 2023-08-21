import pickle
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

import pandas as pd

from ..modules import model
import app.db.database as db  # local import
from ..utils.textCleaning import textCleaning
from .history import history
from ..utils.table_text_preprocessing import text_preprocessing

async def text_predictor():
    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["Sentimen Predictor", "History"],
        icons=["review", "history"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )
    
    # --- INPUT & SAVE PERIODS ---
    if (selected == "Sentimen Predictor"):
        prediction_result  = await sentimen_predictor()
        if prediction_result is not None:
            result_predictor, text = prediction_result
            if result_predictor is not None:
                db.insert_review(result_predictor, text)
        
    if (selected == "History"):
        all_testing_reviews = db.fetch_all_reviewtest()
        history(all_testing_reviews)

async def sentimen_predictor():
    st.markdown("### Input Ulasan")
    with st.form("text_predictor_form"):
        text_predictor = st.text_area("Text Predictor", placeholder="Masukan ulasan anda yang akan dianalis")

        submit = st.form_submit_button("Analyze")
    "---"
    
    algoritm = st.radio("Pilih Algoritma: ", ("Support Vector Machine", "Naive Bayes", "all"), horizontal=True)
    if (algoritm == "Support Vector Machine"):
        pickle_in = open('model_svm.pkl', 'rb')
    elif(algoritm == "all"):
        pickle_in_svm = open('model_svm.pkl', 'rb')
        pickle_in_nb = open('model_nb.pkl', 'rb')
    else:
        pickle_in = open('model_nb.pkl', 'rb')
    if submit:
        if text_predictor == "":
            st.error("OOPPSS... Kolom ulasan tidak terisi")
            return None, text_predictor
        
        text_predictor_clean, _ = textCleaning(pd.DataFrame([text_predictor], columns=["responding"]), neutral=True)
        if (algoritm == "all"):
            svm, tfidf_svm = pickle.load(pickle_in_svm)
            nb, tfidf_nb = pickle.load(pickle_in_nb)
            st.markdown("### Support Vector Machine")
            text_polarity_svm = {"term": [], "label": [], "score": []} 
            score = 0
            if (text_predictor_clean['Text_Clean_split'].empty):
                st.info("Maaf sentimen ini bersifat neutral")
                return None, text_predictor
            for text in text_predictor_clean['Text_Clean_split'][0]:
                y_pred, _ = model.predictFromPKL(tfidf_svm, svm, [text])
                text_polarity_svm['term'].append(text)
                text_polarity_svm['label'].append(y_pred[0])
                if (y_pred[0] == "negative"):
                    score -= 1
                    text_polarity_svm["score"].append(-1)
                if (y_pred[0] == "positive"):
                    score += 1
                    text_polarity_svm["score"].append(1)
                if (y_pred[0] == "neutral"):
                    text_polarity_svm["score"].append(0)

            text_predictor_clean['polarity_score'] = score
            # del textPolarity['neutral']
            st.write("Sentimen Per-kata suatu ulasan")
            # Temukan panjang maksimum dari array dalam dictionary
            max_length = max(len(text_polarity_svm[key]) for key in text_polarity_svm) 
            # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
            data_equal_length = {key: text_polarity_svm[key] + [""] * (max_length - len(text_polarity_svm[key])) for key in text_polarity_svm}
            df = pd.DataFrame(data_equal_length) 
            st.table(df)
            
            # y_pred, _ = model.predictFromPKL(tfidf_svm, svm, [text_predictor])
            if (score > 0):
                st.success("Ulasan tersebut bernada positive 😊")
            elif(score < 0):
                st.error("Ulasan tersebut bernada negative 😡")
            else:
                st.info("Ulasan tersebut bernada neutral")
                
            st.markdown("### TextPreprocessing")
            st.markdown("Text preprocessing adalah suatu proses untuk menyeleksi data text agar menjadi lebih terstruktur lagi dengan melalui serangkaian tahapan yang meliputi tahapan case folding, tokenizing, filtering dan stemming")
            text_preprocessing(text_predictor_clean)

            st.markdown("### Naive Bayes")
            textPolarity = { "positive": [], "negative": [], "neutral": []}
            text_polarity_nb = {"term": [], "label": [], "score": []}

            score_nb = 0
            for text in text_predictor_clean['Text_Clean_split'][0]:
                y_pred, _ = model.predictFromPKL(tfidf_nb, nb, [text])
                text_polarity_nb['term'].append(text)
                text_polarity_nb['label'].append(y_pred[0])
                if (y_pred[0] == "negative"):
                    score_nb -= 1
                    text_polarity_nb["score"].append(-1) 
                if (y_pred[0] == "positive"):
                    score_nb += 1
                    text_polarity_nb["score"].append(1) 
                if (y_pred[0] == "neutral"):
                    text_polarity_nb["score"].append(0) 

            text_predictor_clean['polarity_score'] = score_nb
            # del textPolarity['neutral']
            st.write("Sentimen Per-kata suatu ulasan")
            # Temukan panjang maksimum dari array dalam dictionary
            max_length = max(len(text_polarity_nb[key]) for key in text_polarity_nb) 
            # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
            data_equal_length = {key: text_polarity_nb[key] + [""] * (max_length - len(text_polarity_nb[key])) for key in text_polarity_nb}
            df = pd.DataFrame(data_equal_length) 
            st.table(df)

            # y_pred, _ = model.predictFromPKL(tfidf_nb, nb, [text_predictor])
            if (score_nb > 0):
                st.success("Ulasan tersebut bernada positive 😊")
            elif(score_nb < 0):
                st.error("Ulasan tersebut bernada negative 😡")
            else:
                st.info("Ulasan tersebut bernada neutral")

            st.markdown("### TextPreprocessing")
            st.markdown("Text preprocessing adalah suatu proses untuk menyeleksi data text agar menjadi lebih terstruktur lagi dengan melalui serangkaian tahapan yang meliputi tahapan case folding, tokenizing, filtering dan stemming")
            with st.expander("Show Data TextPreprocessing"):
                text_preprocessing(text_predictor_clean)

            # ======= SAVE TO DB
            result_predictor = {
                "svm": {
                    **text_polarity_svm,
                    "predictor": score
                },
                "nb": {
                    **text_polarity_nb,
                    "predictor":score_nb
                }
            }
            return result_predictor, text_predictor

        svm, tfidf = pickle.load(pickle_in)
        textPolarity = {"term": [], "label": [], "score": []}
        score = 0
        for text in text_predictor_clean['Text_Clean_split'][0]:
            y_pred, _ = model.predictFromPKL(tfidf, svm, [text])
            textPolarity['term'].append(text)
            textPolarity['label'].append(y_pred[0])
            if (y_pred[0] == "negative"):
                score -= 1
                textPolarity["score"].append(-1) 
            if (y_pred[0] == "positive"):
                score += 1
                textPolarity["score"].append(1) 
            if (y_pred[0] == "neutral"):
                textPolarity["score"].append(0) 

        # del textPolarity['neutral']
        st.write("Sentimen Per-kata suatu ulasan")
        # Temukan panjang maksimum dari array dalam dictionary
        max_length = max(len(textPolarity[key]) for key in textPolarity) 
        # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
        data_equal_length = {key: textPolarity[key] + [""] * (max_length - len(textPolarity[key])) for key in textPolarity}
        df = pd.DataFrame(data_equal_length)
        st.table(df)

        # y_pred, _ = model.predictFromPKL(tfidf, svm, [text_predictor])
        if (score > 0):
            st.success("Ulasan tersebut bernada positive 😊")
        elif(score < 0):
            st.error("Ulasan tersebut bernada negative 😡")
        else:
            st.info("Ulasan tersebut bernada neutral")

        st.markdown("### TextPreprocessing")
        st.markdown("Text preprocessing adalah suatu proses untuk menyeleksi data text agar menjadi lebih terstruktur lagi dengan melalui serangkaian tahapan yang meliputi tahapan case folding, tokenizing, filtering dan stemming")

        with st.expander("Show Data TextPreprocessing"):
            text_preprocessing(text_predictor_clean)
        
        if algoritm == "Support Vector Machine":
            algoritma = "svm"
        else:
            algoritma = "nb"
        # ======= SAVE TO DB
        result_predictor = {
            algoritma: {
                **textPolarity,
                "predictor": score
            }
        }
        return result_predictor, text_predictor
