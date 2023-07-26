import pandas as pd
from collections import Counter
from ..modules import txt_preprocessing
from ..modules import feature_extraction
import streamlit as streamlitParam  # pip install streamlit
import calendar


def textCleaning(df, neutral = False):
    """TextCleaning

    `>> Return`\n
    function will return 2 variables, dataframe and result, 
    in result there are 2 values namely, 
    result[2] as positive, and result[3] as negative

    ## Example 
    ```python
    df, result = textCleaning(dataframe)
    print(result[2]) # positive 
    print(result[3]) # negative
    ```
    """
    # ------- CaseFolding
    df["Text_Clean"] = df["responding"].apply(txt_preprocessing.Case_Folding)

    # ------- Cleansing
    df["Cleansing"] = df["Text_Clean"].apply(txt_preprocessing.Cleansing)

    # ------- Lemmatisasi
    df["Lemmatisasi"] = df["Cleansing"].apply(txt_preprocessing.lemmatisasi().lemmatize)

    # ------- Steaming
    df["Stemming"] = df["Lemmatisasi"].apply(txt_preprocessing.stemming().stem)

    # ------- Slangword Standrization
    slang_dictionary = pd.read_csv("https://raw.githubusercontent.com/insomniagung/kamus_kbba/main/kbba.txt", delimiter="\t", names=['slang', 'formal'], header=None, encoding='utf-8')
    slang_dict = pd.Series(slang_dictionary["formal"].values, index = slang_dictionary["slang"]).to_dict()
    df["Slangword"] = df["Stemming"].apply(lambda text: txt_preprocessing.Slangwords(text, slang_dict))
    df["Slangword"] = df["Slangword"].str.replace("mhs", "mahasiswa")

    # ------- Stopword Removal
    df["Stopword"] = df["Slangword"].apply(txt_preprocessing.stopwordRemoval().remove_stopword)

    # ------- Unwanted Word Removal
    df["UnwantedWord"] = df["Stopword"].apply(txt_preprocessing.RemoveUnwantedWords)

    ## Menghapus kata yang kurang dari 3 huruf
    df["Shortword"] = df["UnwantedWord"].str.findall('\w{3,}').str.join(' ')

    # ------- SplitWord    
    df["Text_Clean_split"] = df["Shortword"].apply(feature_extraction.split_word)
    
    ## Memberi label pada data ulasan
    ### Pada dataset belum terdapat label positif dan negatif pada ulasan, sehingga perlu dilakukan pelabelan.
    df, result = sentimentAnalysis(df, neutral)

    return df, result

def positiveOrNegativeDictionary():
    ## Daftar kosa kata positif Bahasa Indonesia
    df_positive = pd.read_csv("https://raw.githubusercontent.com/dhino12/ID-NegPos/main/positive.txt", sep="\t")
    list_positive = list(df_positive.iloc[::, 0])

    ## Daftar kosa kata negatif Bahasa Indonesia
    df_negative = pd.read_csv("https://raw.githubusercontent.com/dhino12/ID-NegPos/main/negative.txt", sep="\t")
    list_negative = list(df_negative.iloc[::, 0]) 
    return list_positive, list_negative

def sentimentAnalysis(df, neutral):
    """Melakukan labeling terhadap sentiment pada `dataframe['Text_Clean_split']`

    Parameters
    -------
    `df` 
        sebagai dataframe dan 
    `neutral` 
        adalah indikator apakah menggunakan netral atau tidak\n
    Returns
    -------
    `result[2] as positive and result[3] as negative`
    """
    list_positive, list_negative = positiveOrNegativeDictionary()
    result = df["Text_Clean_split"].apply(lambda text: txt_preprocessing.lexicon_indonesia(
        text=text, list_positive=list_positive, list_negative=list_negative
    ))
    result = list(zip(*result))
    df["polarity_score"] = result[0]
    df["polarity"] = result[1]
    
    if neutral == False :
        df = df[df.polarity != "neutral"]
    
    return df, result

def countTotalSentimentFrequency(df, result):
    """Counting total sentiment positive & negative based on topik popular as frequency"""

    # Menggabungkan semua list kata positif dan negatif menjadi satu list
    all_positive_words = [word for sublist in result[2] for word in sublist]
    all_negative_words = [word for sublist in result[3] for word in sublist]

    # Menghitung frekuensi kata-kata positif dan negatif
    positive_df = pd.DataFrame(Counter(all_positive_words).most_common(20), columns=['Words Positive', 'frequency'])
    negative_df = pd.DataFrame(Counter(all_negative_words).most_common(20), columns=['Words Negative', 'frequency'])

    return positive_df, negative_df

def countMonthTotalSentimen(df):
    df["month"] = pd.DatetimeIndex(df["postDate"]).month

    # Menghitung frekuensi kata-kata positif dan negatif berdasarkan bulan
    freq_by_month = df.groupby(["month", "polarity"]).size().reset_index(name="frequency")

    # Membentuk pivot table untuk mendapatkan total frekuensi berdasarkan bulan
    total_freq_by_month = freq_by_month.pivot_table(index="month", columns="polarity", values="frequency", aggfunc="sum", fill_value=0).reset_index()
    return df, total_freq_by_month
    