import pandas as pd

from ..utils import utils
from ..modules import feature_extraction
from ..modules import model
from ..modules import evaluation
from ..modules import txt_preprocessing
from ..utils.textCleaning import positiveOrNegativeDictionary

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Error Handling
import traceback

def analiystThisData(st, df, selectedColumn = "responding"):
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
        splitWords, labeling, circleDiagram, wordCloud, tfidf = st.tabs(["Split Words", "Labeling", "Circle Diagram", "WordCloud", "TF-IDF"])

        st.markdown("### Modeling")
        SVMModel, trainAndTest, naive_bayes = st.tabs(["Support Vector Machine", "Train & Test Data", "Naïve Bayes"])

        st.markdown("### Performance Evaluation")
        classificationReport, confusionMatrix = st.tabs(["Classification Report", "Confusion Matrix"])

        # ------- CaseFolding
        df["Text_Clean"] = df[selectedColumn].apply(txt_preprocessing.Case_Folding)
        with caseFolding:
            with st.expander("Show Data CaseFolding", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
                
        # ------- Cleansing
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.Cleansing)
        with cleansing:
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
            with st.expander("Show Data Stemming", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Slangword Standrization   
        slang_dictionary = pd.read_csv("https://raw.githubusercontent.com/insomniagung/kamus_kbba/main/kbba.txt", delimiter="\t", names=['slang', 'formal'], header=None, encoding='utf-8')
        slang_dict = pd.Series(slang_dictionary["formal"].values, index = slang_dictionary["slang"]).to_dict()
        df["Text_Clean"] = df["Text_Clean"].apply(lambda text: txt_preprocessing.Slangwords(text, slang_dict))
        df["Text_Clean"] = df["Text_Clean"].str.replace("mhs", "mahasiswa")        
        with slangword:
            with st.expander("Show Data Slangword Standarization", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Hasil Normalize
        with resultNormalize:
            with st.expander("Show Data Hasil Normalize", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

        # ------- Stopword Removal
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.stopwordRemoval().remove_stopword)
        with stopwordRemoval:
            with st.expander("Show Data Stopword Removal", expandData):
                st.dataframe(df['Text_Clean'].head(20), use_container_width=True)
        
        # ------- Unwanted Word Removal
        df["Text_Clean"] = df["Text_Clean"].apply(txt_preprocessing.RemoveUnwantedWords)
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
        df["Text_Clean_split"] = df["Text_Clean"].apply(feature_extraction.split_word)
        with splitWords:
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
        X, y = feature_extraction.tfidf(df=df)
        rankingData = feature_extraction.calculate_tfidf_ranking(df)
        hah = feature_extraction.hitung_kamus(df=df)
        with tfidf:
            st.markdown("####  TFIDF")
            
            ranking = pd.DataFrame(rankingData, columns=['Frequency', 'TF-IDF', 'Term'])
            ranking.sort_values('Frequency', ascending=False, inplace=True)
            st.dataframe(ranking)

            # Membuat DataFrame dari kamus
            df_kamus = pd.DataFrame.from_dict(hah, orient='index')
            df_kamus.index.name = 'Kata'
            st.dataframe(df_kamus)

            st.text(X[0:2])

        with wordCloud:
            st.markdown("#### Wordcloud")

        X_train, X_test, y_train, y_test, data_latih, data_test, all_data = model.train_test_splitTFIDF(X=X, y=y, testSize = 0.1, randState = 0)
        with trainAndTest:
            st.dataframe(pd.DataFrame({
                "Total Keseluruhan data": [all_data],
                "Total Data Latih": [data_latih],
                "Total Data Test": [data_test]
            }).reset_index(drop=True), use_container_width=True)

        with SVMModel:
            score_svmlk, svmLinear, y_pred = model.predictSVM(X_train, y_train, X_test, y_test)
            st.markdown(f"<center>Akurasi dengan menggunakan Support Vector Machine Linear Kernel: <b color='white'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
            # st.pyplot()
        with naive_bayes:
            score_svmlk, y_prednb = model.predictNaiveBayes(X_train, y_train, X_test, y_test)
            st.markdown(f"<center>Akurasi dengan menggunakan Naive Bayes: <b color='white'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
        
        if (st.checkbox("Gunakan Metode Naive Bayes")):
                y_pred = y_prednb
        with confusionMatrix:    
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