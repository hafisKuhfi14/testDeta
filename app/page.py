import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import pickle
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from .data.textCleaning import textCleaning
from .utils import utils
from . import algorithm
import database as db  # local import
import streamlit_authenticator as stauth

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

def home():
    st.markdown("### Ulasan Pelanggan Berdasarkan Platform Media Sosial")
    st.write("pilih media sosial mana yang ingin kamu analisis")
    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["Twitter"],
        icons=["twitter"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # Text Cleaning ======
    df = pd.read_csv("app/data/indihome3_scrape.csv")
    df = textCleaning(df) 
    data=df
    # ====================
    
    # --- INPUT & SAVE PERIODS ---
    if selected == "Twitter":
        if st.checkbox("Show Data Limit 50"):
            st.write(data.head(50))
        tweets=st.sidebar.radio('Sentiment Type',('nothing','positive','negative'))
        dataPolarity = data
        if (tweets == "nothing"):
            dataPolarity = data
        else:
            dataPolarity = data.query('polarity==@tweets')
        st.markdown("**Review Ulasan**")
        st.markdown(f"{dataPolarity[['Text_Clean']].sample(1).iat[0,0]}\n**[{dataPolarity[['polarity']].sample(1).iat[0,0]}]**")
        
        select=st.sidebar.selectbox('Visualisation Of Tweets',['Histogram','Pie Chart'],key=1)
        sentiment=dataPolarity['polarity'].value_counts()
        sentiment=pd.DataFrame({'Sentiment':sentiment.index,'Tweets':sentiment.values})
        st.markdown("###  Sentiment count")
        if select == "Histogram":
            fig = px.bar(sentiment, x='Sentiment', y='Tweets', color = 'Tweets', height= 500)
            st.plotly_chart(fig)
        else:
            fig = px.pie(sentiment, values='Tweets', names='Sentiment')
            st.plotly_chart(fig)
        
        # ----- TFIDF
        df["Text_Clean_new"] = df["Text_Clean"].astype(str)
        X, y = algorithm.tfidf(df=df)

        # ----- SVM
        X_train, X_test, y_train, y_test, data_latih, data_test, all_data = algorithm.train_test_splitTFIDF(X=X, y=y, testSize = 0.1, randState = 0)

        st.table(pd.DataFrame({
            "Total Keseluruhan data": [all_data],
            "Total Data Latih": [data_latih],
            "Total Data Test": [data_test]
        }).reset_index(drop=True))
        
        score_svmlk, svmLinear, y_pred = algorithm.predictSVM(X_train, y_train, X_test, y_test)
        st.markdown(f"<center>Akurasi dengan menggunakan Support Vector Machine Linear Kernel: <b color='white'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
        accuracy = algorithm.plot_confusion_matrix_box(svmLinear=svmLinear, X_test=X_test, y_test=y_test, y_pred=y_pred)
        st.pyplot()
        # ====== end svm

        st.sidebar.subheader("Tweet layanan IndiHome berdasarkan sentimen")
        choice = st.sidebar.multiselect("Layanan", ('internet', 'telepon', 'tv', 'paket', 'jaringan', 'indihome'), key = '0')  
        if len(choice)>0:
            st.markdown("### Tweet berdasarkan sentimen")
            air_data = utils.hitung_kemunculan(data.Text_Clean_split, choice)
            data = pd.DataFrame(list(air_data.items()), columns=['polarity', 'Text_Clean_split'])
            air_data=data[data.polarity.isin(choice)]

            # air_data = pd.DataFrame({'Text_Clean_split': list(air_data.values()), 'polarity': choice})
            # air_data=data[data.Text_Clean_split.isin([f"{choice}"])]
            # facet_col = 'airline_sentiment'
            print(air_data)
            print(choice)
            fig1 = px.histogram(data_frame=air_data, x='polarity', y='Text_Clean_split', histfunc='sum', color='polarity',labels={'polarity':'tweets'}, height=600, width=800)
            st.plotly_chart(fig1)

def complaint(username):
    st.markdown("### Input Keluhan Pelanggan")
    with st.form('complaint_form', clear_on_submit=True):
        comment = st.text_area("masukan keluhan kamu", placeholder="Masukan komplen anda terkait layanan tertentu......")
        submit = st.form_submit_button("Send")
    "---"
    if submit:
        db.insert_complaint(username, comment)
        st.success("Data Saved..!")

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
        text_predictor = textCleaning(pd.DataFrame([text_predictor], columns=["responding"]), neutral=True)
        print("========== PRED")
        print(text_predictor)
        y_pred, new_features = algorithm.predictFromPKL(tfidf, svm, text_predictor['responding'][0])
        if (y_pred[0] == "negative" or text_predictor['polarity'][0] == 'negative'):
            st.warning("Ulasan tersebut bernada negative 😔")
        else:
            st.success("Ulasan tersebut bernada positive 😊")

        # ============= TABLE =====================
        textPolarity = { "positive": [], "negative": [] }
        for text in text_predictor['responding'][0].split(" "):
            text = textCleaning(pd.DataFrame([text], columns=["responding"]), neutral=True)
            y_pred, new_features = algorithm.predictFromPKL(tfidf, svm, text['responding'][0])
            if (y_pred[0] == "negative" or text['polarity'][0] == 'negative'):
                textPolarity['negative'].append(text['responding'][0])
            else:
                textPolarity['positive'].append(text['responding'][0])

        st.write("Sentimen Per-kata suatu ulasan")
        # Temukan panjang maksimum dari array dalam dictionary
        max_length = max(len(textPolarity[key]) for key in textPolarity) 
        # Buat dictionary baru dengan panjang array yang sama untuk setiap kunci
        data_equal_length = {key: textPolarity[key] + [""] * (max_length - len(textPolarity[key])) for key in textPolarity}
        df = pd.DataFrame(data_equal_length) 
        st.table(df)

def register_user(form_name: str, location: str='main', preauthorization=True) -> bool:
    if location == 'main':
        register_user_form = st.form('Register user')

    register_user_form.subheader(form_name)
    new_username = register_user_form.text_input('Username').lower()
    new_name = register_user_form.text_input('Name')
    new_password = register_user_form.text_input('Password', type='password')
    new_password_repeat = register_user_form.text_input('Repeat password', type='password')

    if register_user_form.form_submit_button('Register'):
        if len(new_username) and len(new_name) and len(new_password) > 0:
            users = db.get_username(new_username)
            if users != None:
                st.error(f"❌ Ooops username dengan '{new_username}' sudah tersedia.")
                return False;
            if new_password == new_password_repeat:
                hashed_passwords = stauth.Hasher([new_password]).generate()[0]
                db.insert_user(new_username, new_name, hashed_passwords)
                st.success(f"✔ Selamat anda sudah terdaftar {new_name}, **Silahkan login...**")
            else:
                st.warning("⚠ Oops.. password tidak valid")
        else:
            st.warning("⚠ Tolong masukan username, name and password")