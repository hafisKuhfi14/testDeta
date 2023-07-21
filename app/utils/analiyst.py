import pandas as pd

from ..utils import utils
from ..modules import feature_extraction
from ..modules import model
from ..modules import evaluation
from ..modules import txt_preprocessing
from ..utils.textCleaning import positiveOrNegativeDictionary, countTotalSentimentFrequency

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as streamlitdata  # pip install streamlit
import calendar
from wordcloud import WordCloud

# Error Handling
import traceback

# @streamlitdata.cache_data(experimental_allow_widgets=True)
def analiystThisData(st: streamlitdata, df, selectedColumn = "responding"):
    try:   
        # Menampilkan DataFrame
        st.dataframe(df.head(10))
        
        expandData = st.checkbox("Expand All Data")
        st.write('You selected:', selectedColumn)
        
        st.markdown("### Text Cleaning")        
        resultCleaning, caseFolding, cleansing = st.tabs(["Hasil Text Cleaning", "CaseFolding", "Cleansing"])

        st.markdown("### Data Normalization")
        resultNormalize, lemmatization, stemming, slangword = st.tabs(["Hasil Normalize", "Lemmatization", "Stemming", "SlangWord"])

        st.markdown("### Word Removal")
        resultWordRemoval, stopwordRemoval, unwantedRemoval, shortWord = st.tabs(["Hasil Word Removal", "Stopword Removal", "Unwanted Word", "ShortWord"])

        st.markdown("### Tokenizing")
        splitWords, labeling, tfidf = st.tabs(["Split Words", "Labeling", "TF-IDF"])

        st.markdown("### Visualisasi Data")
        garis, topwords, wordCloud, circleDiagram = st.tabs(["garis", "topwords", "WordCloud", "Circle Diagram"])

        st.markdown("### Modeling")
        SVMModel, trainAndTest, naive_bayes = st.tabs(["Support Vector Machine", "Train & Test Data", "Naïve Bayes"])

        st.markdown("### Performance Evaluation")
        classificationReport, confusionMatrix = st.tabs(["Classification Report", "Confusion Matrix"])

        # ------- CaseFolding
        df["Text_Clean"] = df[selectedColumn].apply(txt_preprocessing.Case_Folding)
        with caseFolding:
            st.markdown("Proses melakukan perubahan text. Mengubah huruf besar menjadi kecil, serta menghilangkan karakter-karakter tidak diperlukan")
            with st.expander("Show Data CaseFolding", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
                
        # ------- Cleansing
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.Cleansing)
        with cleansing:
            st.markdown("Proses melakukan pembersihan text. Menghilangkan noise seperti angka, emoji, link, tagar, spasi berlebih, baris enter (linebreak)")
            with st.expander("Show Data Cleansing", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        # ------- Result Text Cleaning
        with resultCleaning:
            with st.expander("Show Data Hasil Cleaning", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Lemmatisasi
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.lemmatisasi().lemmatize)
        with lemmatization:
            with st.expander("Show Data Lemmatisasi", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Steaming
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.stemming().stem)
        with stemming:
            st.markdown("Proses menghilangkan kata imbuhan menjadi kata dasar, seperti 'membanggakan' akan diubah menjadi 'bangga'")
            with st.expander("Show Data Stemming", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Slangword Standrization   
        slang_dictionary = pd.read_csv("https://raw.githubusercontent.com/dhino12/kamus_kbba/main/kbba.txt", delimiter="\t", names=['slang', 'formal'], header=None, encoding='utf-8')
        slang_dict = pd.Series(slang_dictionary["formal"].values, index = slang_dictionary["slang"]).to_dict()
        df["Text_Clean"] = df["Text_Clean"].apply(lambda text: txt_preprocessing.Slangwords(text, slang_dict))
        df["Text_Clean"] = df["Text_Clean"].str.replace("mhs", "mahasiswa")        
        with slangword:
            st.markdown("Proses mengubah kata non-baku (slang) atau sering disebut kata gaul menjadi kata baku, seperti kata 'lemot' akan diubah menjadi 'lambat'")
            with st.expander("Show Data Slangword Standarization", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Hasil Normalize
        with resultNormalize:
            with st.expander("Show Data Hasil Normalize", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Stopword Removal
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.stopwordRemoval().remove_stopword)
        with stopwordRemoval:
            st.markdown("Proses menghilangkan seluruh kata yang terdapat kata hubung seperti 'yang' 'dan' 'dari'")
            with st.expander("Show Data Stopword Removal", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        # ------- Unwanted Word Removal
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.RemoveUnwantedWords)
        with unwantedRemoval:
            st.markdown("Proses menghilangkan kata-kata yang kurang bermakna berdasarkan kamus. Kata yang dianggap kurang bermakna yaitu nama bulan dalam kalender, 'replaying', 'balas', 'to'.")
            with st.expander("Show Data Unwanted Word Removal", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        ## Menghapus kata yang kurang dari 3 huruf
        df["Text_Clean"] = df["Text_Clean"].str.findall('\w{3,}').str.join(' ')
        df = df[df['Text_Clean'].str.split().str.len() >= 3]
        with shortWord:
            st.markdown("Proses menghapus kata atau kalimat yang kurang dari 3 karakter. Seperti kata 'di' 'hi'.")
            with st.expander("Show Data Shortword", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        with resultWordRemoval:
            with st.expander("Show Data Hasil Word Removal", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- SplitWord    
        df["Text_Clean_split"] = df["Text_Clean"].apply(feature_extraction.split_word)
        with splitWords:
            st.markdown("Proses memecah suatu kata menjadi beberapa bagian-bagian.")
            with st.expander("Show Data Splitword", expandData):
                st.dataframe(df['Text_Clean_split'].head(20), use_container_width=True)
        
        # ------- labeling
        list_positive, list_negative = positiveOrNegativeDictionary()
        result = df["Text_Clean_split"].apply(lambda text: txt_preprocessing.lexicon_indonesia(
            text=text, list_positive=list_positive, list_negative=list_negative
        ))

        result = list(zip(*result))
        df["polarity_score"] = result[0]
        df["polarity"] = result[1]
        df = df[df.polarity != "neutral"]
        
        with labeling:
            st.markdown("Proses melakukan pelabelan (positive / negative) pada ulasan.")
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
            
            st.dataframe(pd.DataFrame([
                len(df[df.polarity == 'positive']), len(df[df.polarity == 'negative']), len(df)
            ], index=['Total Positive', 'Total Negative', 'Total Polarity']), use_container_width=True)
        
        # ----- TFIDF
        df["Text_Clean_new"] = df["Text_Clean_split"].astype(str)
        X, y = feature_extraction.tfidf(df=df)
        rankingData = feature_extraction.calculate_tfidf_ranking(df)
        hah = feature_extraction.hitung_kamus(df=df)
        with tfidf:
            st.markdown("Proses memberikan nilai pembobotan pada dokumen. Proses TF-IDF (Term Frequency-Inverse Document Frequency) dilakukan dengan tujuan untuk mengetahui seberapa penting dan seberapa sering suatu kata muncul dalam dokumen tersebut.")
            
            with st.expander("Pembobotan TF-IDF", expandData):
                st.text(X[0:])

        _, positive_df, negative_df, total_freq_by_month = countTotalSentimentFrequency(df, result)
        # ------- Circle Diagram
        with circleDiagram:
            st.markdown("####  Sentiment count")
            st.markdown("Proses melakukan visualisasi total sentimen positif dan negatif pada ulasan menggunakan diagram pie")
            sentimentPolarity = df['polarity'].value_counts()
            PdSentimentPolarity = pd.DataFrame({'Sentiment':sentimentPolarity.index,'Tweets':sentimentPolarity.values})
            fig = px.pie(PdSentimentPolarity, values='Tweets', names='Sentiment')
            st.plotly_chart(fig)
            st.markdown(f"total keseluruhan ulasan yang sudah melewati tahap cleaning adalah sebanyak: **{sentimentPolarity['positive'] + sentimentPolarity['negative']}**")
            st.markdown(f"Dari hasil perhitungan diketahui sentiment positive sebanyak **{sentimentPolarity['positive']}** dan sentiment negative sebanyak **{sentimentPolarity['negative']}**\n")
            
        with wordCloud:
            st.markdown("#### Wordcloud")
            st.markdown("Proses menampilkan seluruh kata sentimen pada wordcloud. Wordcloud adalah sebuah visualisasi yang menampilkan kata-kata, kata yang sering muncul akan memiliki ukuran font lebih besar")
            df_positive = df[df["polarity"] == "positive"]
            df_negative = df[df["polarity"] == "negative"]
            text_positive = ' '.join(df_positive['Text_Clean'])
            text_negative = ' '.join(df_negative['Text_Clean'])

            wordcloud_positive = WordCloud(width=800, height=800, background_color='white', colormap='Greens').generate(text_positive)
            wordcloud_negative = WordCloud(width=800, height=800, background_color='white', colormap='Reds').generate(text_negative)

            fig, axs = plt.subplots(1, 2, figsize=(8, 3))
            axs[0].imshow(wordcloud_positive, interpolation='bilinear')
            axs[0].set_title('Positive Words')
            axs[0].axis('off')

            axs[1].imshow(wordcloud_negative, interpolation='bilinear')
            axs[1].set_title('Negative Words')
            axs[1].axis('off')

            plt.show()
            st.pyplot()

        with topwords:
            st.markdown("Top 20 kata dari label positif dan negatif")
            with st.expander("All Positive Words", expandData):
                st.dataframe(positive_df, use_container_width=True)
            with st.expander("All Negative Words", expandData):
                st.dataframe(negative_df, use_container_width=True)

        with garis:
            st.markdown("### Sentimen Bulanan")
            st.markdown("Proses menampilkan jumlah sentimen positif dan negatif berdasarkan bulan dengan menggunakan diagram garis")
            # _, positive_df, negative_df, total_freq_by_month = countTotalSentimentFrequency(df, result)
            total_freq_by_month["month"] = total_freq_by_month["month"].apply(lambda x: f"{int(x)}_{calendar.month_name[int(x)]}")
            
            st.line_chart(total_freq_by_month, x='month')
            st.dataframe(total_freq_by_month, use_container_width=True)

        X_train, X_test, y_train, y_test, data_latih, data_test, all_data = model.train_test_splitTFIDF(X=X, y=y, testSize = 0.1, randState = 0)
        with trainAndTest:
            st.markdown("Proses memisahkan data latih (train) & data uji (test). Data latih (train) sebanyak **90%**, dan data uji (test) sebanyak **10%**")
            st.dataframe(pd.DataFrame({
                "Total Keseluruhan data": [all_data],
                "Total Data Latih": [data_latih],
                "Total Data Test": [data_test]
            }).reset_index(drop=True), use_container_width=True)

        with SVMModel:
            st.markdown("Proses modeling menggunakan Support Vector Machine berdasarkan data yang sudah dibagi pada tahap __Train & Test Data__")
            score_svmlk, svmLinear, y_pred = model.predictSVM(X_train, y_train, X_test, y_test)
            with st.expander("Hasil Modeling"):
                st.markdown(f"<center>Akurasi dengan menggunakan Support Vector Machine Linear Kernel: <b color='green'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
            # st.pyplot()
        with naive_bayes:
            st.markdown("Proses modeling menggunakan Naive Bayes berdasarkan data yang sudah dibagi pada tahap __Train & Test Data__")
            score_svmlk, y_prednb = model.predictNaiveBayes(X_train, y_train, X_test, y_test)
            with st.expander("Hasil Modeling"):
                st.markdown(f"<center>Akurasi dengan menggunakan Naive Bayes: <b color='green'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
        
        if (st.checkbox("Gunakan Metode Naive Bayes")):
                y_pred = y_prednb
        with confusionMatrix:    
            st.markdown("Proses menampilkan Confusion Matrix dan menghitung akurasi model. Confusion Matrix menghasilkan output True Positive, True Negative, False Positive, False Negative. Jika jumlah True (Positive & Negative) lebih banyak dari False (Positive & Negative), maka hasil data uji (test) dikatakan sudah baik")
            accuracy, confusionMatrixData = evaluation.plot_confusion_matrix_box(y_test=y_test, y_pred=y_pred)
            cm_df = pd.DataFrame(confusionMatrixData, index=["Positive", "Negative"], columns=["Positive", "Negative"])
            plt.figure(figsize=(5,4))
            sns.heatmap(cm_df, annot=True, fmt='g')
            plt.title('Confusion Matrix')
            plt.ylabel("Actual Value")
            plt.xlabel("Predicted Value")
            
            TP = confusionMatrixData[0,0]
            TN = confusionMatrixData[1,1]
            FP = confusionMatrixData[1,0]
            FN = confusionMatrixData[0,1]
            resultAccuracy = (TN + TP) / (TP + TN + FP + FN)
            
            st.table({
                "Result Predict": [TP,TN,FP,FN],
                "Label": [
                    "True Positive", "True Negative", "False Positive", "False Negative"
                ],
                "alias": ["TP", "TN", "FP", "FN"]
            })
            rumusCol1, perhitunganCol2 = st.columns(2)
            with rumusCol1:    
                st.markdown("#### Rumus Accuracy")
                st.latex(r'''
                    \frac{TP + TN}{TP + TN + FP + FN} = Accuracy
                ''')
            with perhitunganCol2:
                st.markdown("#### Calculate Accuracy")
                st.latex(r'''
                    \frac{%d + %d}{%d + %d + %d + %d} = %s
                ''' % (TP, TN, TP, TN, FP, FN, resultAccuracy))

            st.pyplot()

        with classificationReport:
            st.markdown("Proses menampilkan hasil kinerja model klasifikasi, proses ini membantu memahami seberapa baik model dapat memprediksi label dengan benar, Jika semakin tinggi persentase Precision, Recall, dan F1-score maka model sudah seimbang dan baik")
            report = evaluation.classificationReport(y_test, y_pred)
            data1 = []
            lines = report.strip().split("\n")
            header = lines[0].split(" ")
            header = list(filter(bool, header))
            header.insert(0," ")
            data1.append(header)

            for line in lines[1:]:
                columns = line.strip().split(" ")
                columns = list(filter(bool, columns)) 
                
                if (len(columns) == 3):
                    columns.insert(1, " ")
                    columns.insert(2, " ")
                if(len(columns) != 0):
                    if (not utils.isfloat(columns[1]) and columns[1] != " "):
                        columns[0] += " " + columns[1]
                        columns.pop(1) 
                    data1.append(columns)
            
            st.dataframe(pd.DataFrame(data1[1:], columns=data1[0]), use_container_width=True)
    except KeyError as errorKeyError:
        print(traceback.format_exc())
        st.error(f"""Maaf terjadi error {str(errorKeyError)}\n
            Pastikan kolom yang dipilih adalah kolom yang berisi review / ulasan, bukan yang lain
        """)
    except AttributeError as errorAttribute:
        print(traceback.format_exc())
        st.error(f"""Maaf terjadi error {str(errorAttribute)}\n
            Pastikan kolom yang dipilih adalah kolom yang berisi review / ulasan
        """)
    except TypeError as errorTypeError:
        print(traceback.format_exc())
        st.error(f"""Maaf terjadi error {str(errorTypeError)}\n
            Pastikan kolom dipilih adalah kolom yang berisi review / ulasan, bukan yang lain
        """)
    except:
        print(traceback.format_exc())
        st.error(f"""Maaf terjadi error {str(traceback.format_exc())}\n""")
