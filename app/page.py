import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import pickle
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from .data.textCleaning import sentimentAnalysis, textCleaning, countTotalSentimentFrequency, positiveOrNegativeDictionary
from .utils import utils
from . import algorithm
import database as db  # local import
import streamlit_authenticator as stauth
import seaborn as sns

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
    
    # --- INPUT & SAVE PERIODS ---
    if selected == "Twitter":
        # Text Cleaning ======
        df = pd.read_csv("app/data/indihome3_scrape.csv")
        if st.checkbox("Show Data Limit 50"):
            st.write(df.head(50))

        expandData = st.checkbox("Expand All Data")

        st.markdown("### Text Cleaning")        
        resultCleaning, caseFolding, cleansing = st.tabs(["Hasil Text Cleaning", "CaseFolding", "Cleansing"])

        st.markdown("### Data Normalization")
        resultNormalize, lemmatization, stemming, slangword = st.tabs(["Hasil Normalize", "Lemmatization", "Stemming", "SlangWord"])

        st.markdown("### Word Removal")
        resultWordRemoval, stopwordRemoval, unwantedRemoval, shortWord = st.tabs(["Hasil Word Removal", "Stopword Removal", "Unwanted Word", "ShortWord"])

        st.markdown("### Tokenizing")
        splitWords, labeling, circleDiagram, wordCloud, tfidf = st.tabs(["Split Words", "Labeling", "Circle Diagram", "WordCloud", "TF-IDF"])

        st.markdown("### Modeling")
        SVMModel, trainAndTest = st.tabs(["Support Vector Machine", "Train & Test Data"])

        st.markdown("### Performance Evaluation")
        classificationReport, confusionMatrix = st.tabs(["Classification Report", "Confusion Matrix"])

        # ------- CaseFolding
        df["Text_Clean"] = df["responding"].apply(utils.Case_Folding)
        with caseFolding:
            with st.expander("Show Data CaseFolding", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
                
        # ------- Cleansing
        df["Text_Clean"] = df["Text_Clean"].apply(utils.Cleansing)
        with cleansing:
            with st.expander("Show Data Cleansing", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        # ------- Result Text Cleaning
        with resultCleaning:
            with st.expander("Show Data Hasil Cleaning", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Lemmatisasi
        df["Text_Clean"] = df["Text_Clean"].apply(utils.lemmatisasi().lemmatize)
        with lemmatization:
            with st.expander("Show Data Lemmatisasi", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Steaming
        df["Text_Clean"] = df["Text_Clean"].apply(utils.stemming().stem)
        with stemming:
            with st.expander("Show Data Stemming", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Slangword Standrization   
        slang_dictionary = pd.read_csv("https://raw.githubusercontent.com/insomniagung/kamus_kbba/main/kbba.txt", delimiter="\t", names=['slang', 'formal'], header=None, encoding='utf-8')
        slang_dict = pd.Series(slang_dictionary["formal"].values, index = slang_dictionary["slang"]).to_dict()
        df["Text_Clean"] = df["Text_Clean"].apply(lambda text: utils.Slangwords(text, slang_dict))
        df["Text_Clean"] = df["Text_Clean"].str.replace("mhs", "mahasiswa")        
        with slangword:
            with st.expander("Show Data Slangword Standarization", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Hasil Normalize
        with resultNormalize:
            with st.expander("Show Data Hasil Normalize", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Stopword Removal
        df["Text_Clean"] = df["Text_Clean"].apply(utils.stopwordRemoval().remove_stopword)
        with stopwordRemoval:
            with st.expander("Show Data Stopword Removal", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        # ------- Unwanted Word Removal
        df["Text_Clean"] = df["Text_Clean"].apply(utils.RemoveUnwantedWords)
        with unwantedRemoval:
            st.markdown("## Unwanted Word Removal")
            with st.expander("Show Data Unwanted Word Removal", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        ## Menghapus kata yang kurang dari 3 huruf
        df["Text_Clean"] = df["Text_Clean"].str.findall('\w{3,}').str.join(' ')
        with shortWord:
            with st.expander("Show Data Shortword", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        with resultWordRemoval:
            with st.expander("Show Data Hasil Word Removal", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- SplitWord    
        df["Text_Clean_split"] = df["Text_Clean"].apply(utils.split_word)
        with splitWords: 
            with st.expander("Show Data Splitword", expandData):
                st.dataframe(df['Text_Clean_split'].head(20), use_container_width=True)
        
        # ------- labeling
        list_positive, list_negative = positiveOrNegativeDictionary()
        result = df["Text_Clean_split"].apply(lambda text: utils.sentiment_analysis_lexicon_indonesia(text=text, list_positive=list_positive, list_negative=list_negative))
        result = list(zip(*result))
        df["polarity_score"] = result[0]
        df["polarity"] = result[1]
        df = df[df.polarity != "neutral"]
        with labeling:
            textAndPolarity = {
                "TextClean": df['Text_Clean'],
                "polarity": df["polarity"]
            }
            st.markdown("#### Daftar Library Positive & Negative")
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe({"Positive Dictionary": list_positive}, use_container_width=True)
            with col2:
                st.dataframe({"Negative Dictionary": list_negative}, use_container_width=True)

            with st.expander("Show Data Labeling", expandData):
                st.dataframe(pd.DataFrame(textAndPolarity).head(20), use_container_width=True)
            
            st.dataframe(pd.DataFrame([{
                "Total Positive": len(result[2]),
                "Total Negative": len(result[3])
            }]), use_container_width=True)
        
        # ------- Circle Diagram
        with circleDiagram:
            st.markdown("####  Sentiment count")
            sentimentPolarity = df['polarity'].value_counts()
            PdSentimentPolarity = pd.DataFrame({'Sentiment':sentimentPolarity.index,'Tweets':sentimentPolarity.values})
            st.markdown(f"total keseluruhan ulasan yang sudah melewati tahap cleaning adalah sebanyak: **{sentimentPolarity['positive'] + sentimentPolarity['negative']}**")
            fig = px.pie(PdSentimentPolarity, values='Tweets', names='Sentiment')
            st.plotly_chart(fig)
            st.markdown(f"Dari hasil perhitungan diketahui sentiment positive sebanyak **{sentimentPolarity['positive']}** dan sentiment negative sebanyak **{sentimentPolarity['negative']}**\n")
            
        # ----- TFIDF
        df["Text_Clean_new"] = df["Text_Clean_split"].astype(str)
        X, y = algorithm.tfidf(df=df)
        with tfidf:
            st.markdown("####  TFIDF")
            st.text(X[0:2])

        with wordCloud:
            st.markdown("#### Wordcloud")

        X_train, X_test, y_train, y_test, data_latih, data_test, all_data = algorithm.train_test_splitTFIDF(X=X, y=y, testSize = 0.1, randState = 0)
        with trainAndTest:
            st.dataframe(pd.DataFrame({
                "Total Keseluruhan data": [all_data],
                "Total Data Latih": [data_latih],
                "Total Data Test": [data_test]
            }).reset_index(drop=True), use_container_width=True)

        score_svmlk, svmLinear, y_pred = algorithm.predictSVM(X_train, y_train, X_test, y_test)
        with SVMModel:
            st.markdown(f"<center>Akurasi dengan menggunakan Support Vector Machine Linear Kernel: <b color='white'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
            # st.pyplot()

        with confusionMatrix:
            accuracy, confusionMatrixData = algorithm.plot_confusion_matrix_box(svmLinear=svmLinear, X_test=X_test, y_test=y_test, y_pred=y_pred)
            cm_df = pd.DataFrame(confusionMatrixData, index=["Positive", "Negative"], columns=["Positive", "Negative"])

            plt.figure(figsize=(5,4))
            sns.heatmap(cm_df, annot=True, fmt='g')
            plt.title('Confusion Matrix')
            plt.ylabel("Actual Value")
            plt.xlabel("Predicted Value")
            st.write({
                "True Positive": confusionMatrixData[1,1],
                "True Negative": confusionMatrixData[0,0],
                "False Positive": confusionMatrixData[0,1],
                "False Negative": confusionMatrixData[1,0]
            })
            st.pyplot()

        data = {}
        perHeader = {}
        class_label = ""
        index = 0
        with classificationReport:
            report = algorithm.classificationReport(y_test, y_pred)
            lines = report.strip().split("\n")
            header = lines[0].split(" ")
            header = list(filter(bool, header))
            header.insert(0," ")

            for line in lines[1:]:
                perHeader = {}
                class_label = ""
                index = 0
                columns = line.strip().split(" ")
                columns = list(filter(bool, columns)) 
                if(len(columns) != 0):
                    class_label = columns[0]
                    if (not utils.isfloat(columns[1])): class_label += " " + columns[1]
                    data[class_label] = ""

                    for column in columns: 
                        if (utils.isfloat(column)):
                            index += 1
                            perHeader[header[index]] = column
                    
                    data[class_label] = perHeader
                    
            st.dataframe(data, use_container_width=True)

        # df, result = sentimentAnalysis(df, False)
        # df, df_positive, df_negative, total_freq_by_month = countTotalSentimentFrequency(df, result)

        # st.write(total_freq_by_month)
        # data = df
        # # ====================
        # st.markdown("### <center> Total Sentiment Berdasarkan Topik</center>", unsafe_allow_html=True)
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.dataframe(df_positive, use_container_width=True)
        # with col2:
        #     st.dataframe(df_negative, use_container_width=True)
        
        # tweets=st.sidebar.radio('Sentiment Type',('nothing','positive','negative'))
        # dataPolarity = data
        # if (tweets == "nothing"):
        #     dataPolarity = data
        # else:
        #     dataPolarity = data.query('polarity==@tweets')
        # st.markdown("**Review Ulasan**")
        # st.markdown(f"{dataPolarity[['Text_Clean']].sample(1).iat[0,0]}\n**[{dataPolarity[['polarity']].sample(1).iat[0,0]}]**")
        
        # sentiment=dataPolarity['polarity'].value_counts()
        # sentiment=pd.DataFrame({'Sentiment':sentiment.index,'Tweets':sentiment.values})
        # st.markdown("###  Sentiment count")
        # fig = px.pie(sentiment, values='Tweets', names='Sentiment')
        # st.plotly_chart(fig)

        # # ----- SVM
        # X_train, X_test, y_train, y_test, data_latih, data_test, all_data = algorithm.train_test_splitTFIDF(X=X, y=y, testSize = 0.1, randState = 0)

        # st.table(pd.DataFrame({
        #     "Total Keseluruhan data": [all_data],
        #     "Total Data Latih": [data_latih],
        #     "Total Data Test": [data_test]
        # }).reset_index(drop=True))
        
        # score_svmlk, svmLinear, y_pred = algorithm.predictSVM(X_train, y_train, X_test, y_test)
        # st.markdown(f"<center>Akurasi dengan menggunakan Support Vector Machine Linear Kernel: <b color='white'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
        # accuracy = algorithm.plot_confusion_matrix_box(svmLinear=svmLinear, X_test=X_test, y_test=y_test, y_pred=y_pred)
        # st.pyplot()
        # ====== end svm

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
        text_predictor, _ = textCleaning(pd.DataFrame([text_predictor], columns=["responding"]), neutral=True)

        textPolarity = { "positive": [], "negative": [], "neutral": [] }
        for text in text_predictor['Text_Clean_split'][0]:
            y_pred, _ = algorithm.predictFromPKL(tfidf, svm, [text])
            if (y_pred[0] == "negative"):
                textPolarity['negative'].append(text)
            elif (y_pred[0] == "neutral"):
                textPolarity['neutral'].append(text)
            else:
                textPolarity['positive'].append(text)

        if (len(textPolarity['positive']) > len(textPolarity['negative'])):
            st.success("Ulasan tersebut bernada positive 😊")
        elif (len(textPolarity['negative']) > len(textPolarity['positive'])):
            st.error("Ulasan tersebut bernada negative 😡")
        else:
            st.warning("Ulasan tersebut bernada neutral 😔")
        
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