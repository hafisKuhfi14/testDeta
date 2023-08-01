import pickle
import streamlit as st  # pip install streamlit
import pandas as pd
from ..modules import model
from ..utils.textCleaning import textCleaning
from ..utils.analiyst import analiystThisData
from ..modules import feature_extraction
from sklearn import metrics

async def text_predictor():
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
            return
        
        text_predictor_clean, _ = textCleaning(pd.DataFrame([text_predictor], columns=["responding"]), neutral=True)
        if (algoritm == "all"):
            svm, tfidf_svm = pickle.load(pickle_in_svm)
            nb, tfidf_nb = pickle.load(pickle_in_nb)
            st.markdown("### Support Vector Machine")
            textPolarity2 = {"term": [], "label": [], "score": []}
            st.write(text_predictor_clean['Text_Clean_split'])
            score = 0
            if (text_predictor_clean['Text_Clean_split'].empty):
                st.info("Maaf sentimen ini bersifat neutral")
                return
            for text in text_predictor_clean['Text_Clean_split'][0]:
                y_pred, _ = model.predictFromPKL(tfidf_svm, svm, [text])
                textPolarity2['term'].append(text)
                textPolarity2['label'].append(y_pred[0])
                if (y_pred[0] == "negative"):
                    score -= 1
                    textPolarity2["score"].append(-1) 
                if (y_pred[0] == "positive"):
                    score += 1
                    textPolarity2["score"].append(1) 
                if (y_pred[0] == "neutral"):
                    textPolarity2["score"].append(0)

            text_predictor_clean['polarity_score'] = score
            # y_pred, _ = model.predictFromPKL(tfidf_svm, svm, [text_predictor])
            if (score > 0):
                st.success("Ulasan tersebut bernada positive 😊")
            elif(score < 0):
                st.error("Ulasan tersebut bernada negative 😡")
            else:
                st.info("Ulasan tersebut bernada neutral")
            # del textPolarity['neutral']
            st.write("Sentimen Per-kata suatu ulasan")
            # Temukan panjang maksimum dari array dalam dictionary
            max_length = max(len(textPolarity2[key]) for key in textPolarity2) 
            # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
            data_equal_length = {key: textPolarity2[key] + [""] * (max_length - len(textPolarity2[key])) for key in textPolarity2}
            df = pd.DataFrame(data_equal_length) 
            st.table(df)
            st.markdown("### TextPreprocessing")
            st.markdown("Text preprocessing adalah suatu proses untuk menyeleksi data text agar menjadi lebih terstruktur lagi dengan melalui serangkaian tahapan yang meliputi tahapan case folding, tokenizing, filtering dan stemming")
            text_preprocessing(text_predictor_clean)

            st.markdown("### Naive Bayes")
            textPolarity = { "positive": [], "negative": [], "neutral": []}
            textPolarity2 = {"term": [], "label": [], "score": []}

            score = 0
            for text in text_predictor_clean['Text_Clean_split'][0]:
                y_pred, _ = model.predictFromPKL(tfidf_nb, nb, [text])
                textPolarity2['term'].append(text)
                textPolarity2['label'].append(y_pred[0])
                if (y_pred[0] == "negative"):
                    score -= 1
                    textPolarity2["score"].append(-1) 
                if (y_pred[0] == "positive"):
                    score += 1
                    textPolarity2["score"].append(1) 
                if (y_pred[0] == "neutral"):
                    textPolarity2["score"].append(0) 

            text_predictor_clean['polarity_score'] = score
            # y_pred, _ = model.predictFromPKL(tfidf_nb, nb, [text_predictor])
            if (score > 0):
                st.success("Ulasan tersebut bernada positive 😊")
            elif(score < 0):
                st.error("Ulasan tersebut bernada negative 😡")
            else:
                st.info("Ulasan tersebut bernada neutral")
            # del textPolarity['neutral']
            st.write("Sentimen Per-kata suatu ulasan")
            # Temukan panjang maksimum dari array dalam dictionary
            max_length = max(len(textPolarity2[key]) for key in textPolarity2) 
            # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
            data_equal_length = {key: textPolarity2[key] + [""] * (max_length - len(textPolarity2[key])) for key in textPolarity2}
            df = pd.DataFrame(data_equal_length) 
            st.table(df)

            st.markdown("### TextPreprocessing")
            st.markdown("Text preprocessing adalah suatu proses untuk menyeleksi data text agar menjadi lebih terstruktur lagi dengan melalui serangkaian tahapan yang meliputi tahapan case folding, tokenizing, filtering dan stemming")

            text_preprocessing(text_predictor_clean)
            return

        svm, tfidf = pickle.load(pickle_in)
        textPolarity = { "positive": [], "negative": [], "neutral": []}
        for text in text_predictor_clean['Text_Clean_split'][0]:
            y_pred, _ = model.predictFromPKL(tfidf, svm, [text])
            print(y_pred)
            if (y_pred[0] == "negative"):
                textPolarity['negative'].append(text)
            if (y_pred[0] == "positive"):
                textPolarity['positive'].append(text)
            if (y_pred[0] == "neutral"):
                textPolarity['neutral'].append(text)

        y_pred, _ = model.predictFromPKL(tfidf, svm, [text_predictor])
        if (y_pred[0] == "positive"):
            st.success("Ulasan tersebut bernada positive 😊")
        elif(y_pred[0] == "negative"):
            st.error("Ulasan tersebut bernada negative 😡")
        del textPolarity['neutral']
        st.write("Sentimen Per-kata suatu ulasan")
        # Temukan panjang maksimum dari array dalam dictionary
        max_length = max(len(textPolarity[key]) for key in textPolarity) 
        # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
        data_equal_length = {key: textPolarity[key] + [""] * (max_length - len(textPolarity[key])) for key in textPolarity}
        df = pd.DataFrame(data_equal_length)
        st.table(df)

        st.markdown("### TextPreprocessing")
        st.markdown("Text preprocessing adalah suatu proses untuk menyeleksi data text agar menjadi lebih terstruktur lagi dengan melalui serangkaian tahapan yang meliputi tahapan case folding, tokenizing, filtering dan stemming")

        text_preprocessing(text_predictor_clean)

# Fungsi untuk mengatur CSS styling untuk kotak berwarna
def kotak_berwarna(color, text):
    return f"""
        <div style="
            background-color: {color};
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            color: black;
            font-weight: 600;
        ">{text}</div>
    """


def text_preprocessing(df):
    with st.expander("Show Data TextPreprocessing"):
        st.markdown(kotak_berwarna("#dadada4d", f"Casefolding: {df['Text_Clean'][0]}"), unsafe_allow_html=True)
        st.markdown(kotak_berwarna("#c2c2c27a", f"Cleansing: {df['Cleansing'][0]}"), unsafe_allow_html=True)
        st.markdown(kotak_berwarna("#dadada4d", f"Stemming: {df['Stemming'][0]}"), unsafe_allow_html=True)
        st.markdown(kotak_berwarna("#c2c2c27a", f"Slangword: {df['Slangword'][0]}"), unsafe_allow_html=True)
        st.markdown(kotak_berwarna("#dadada4d", f"Stopword: {df['Stopword'][0]}"), unsafe_allow_html=True)
        st.markdown(kotak_berwarna("#c2c2c27a", f"Shortword: {df['Shortword'][0]}"), unsafe_allow_html=True)
        df_labeling = {
                "split_word": df['Text_Clean_split'],
                "polarity": df['polarity'],
                "bobot": df['polarity_score']
        }
        st.dataframe(df_labeling, use_container_width=True)
        # st.dataframe(df['Text_Clean'].head(20), use_container_width=True)