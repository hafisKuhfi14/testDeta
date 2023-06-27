import pandas as pd
from collections import Counter
from ..utils import utils

def textCleaning(df, neutral = False):
    # ------- CaseFolding
    df["Text_Clean"] = df["responding"].apply(utils.Case_Folding)
    # ------- Lemmatisasi
    df["Text_Clean"] = df["Text_Clean"].apply(utils.lemmatisasi().lemmatize)
    # ------- Steaming
    df["Text_Clean"] = df["Text_Clean"].apply(utils.steamming().stem)

    # ------- Slangword Standrization
    slang_dictionary = pd.read_csv("https://raw.githubusercontent.com/insomniagung/kamus_kbba/main/kbba.txt", delimiter="\t", names=['slang', 'formal'], header=None, encoding='utf-8')
    slang_dict = pd.Series(slang_dictionary["formal"].values, index = slang_dictionary["slang"]).to_dict()
    df["Text_Clean"] = df["Text_Clean"].apply(lambda text: utils.Slangwords(text, slang_dict))
    df["Text_Clean"] = df["Text_Clean"].str.replace("mhs", "mahasiswa")
    # ------- Stopword Removal
    df["Text_Clean"] = df["Text_Clean"].apply(utils.stopwordRemoval().remove_stopword)
    # ------- Unwanted Word Removal
    df["Text_Clean"] = df["Text_Clean"].apply(utils.RemoveUnwantedWords)
    ## Menghapus kata yang kurang dari 3 huruf
    df["Text_Clean"] = df["Text_Clean"].str.findall('\w{3,}').str.join(' ')
    # ------- SplitWord    
    df["Text_Clean_split"] = df["Text_Clean"].apply(utils.split_word)
    
    ## Memberi label pada data ulasan
    ### Pada dataset belum terdapat label positif dan negatif pada ulasan, sehingga perlu dilakukan pelabelan.
    df, df_positive, df_negative = sentimentAnalysis(df, neutral)

    return df, df_positive, df_negative

def positiveOrNegativeDictionary():
    ## Daftar kosa kata positif Bahasa Indonesia
    df_positive = pd.read_csv("https://raw.githubusercontent.com/masdevid/ID-OpinionWords/master/positive.txt", sep="\t")
    list_positive = list(df_positive.iloc[::, 0])

    ## Daftar kosa kata negatif Bahasa Indonesia
    df_negative = pd.read_csv("https://raw.githubusercontent.com/masdevid/ID-OpinionWords/master/negative.txt", sep="\t")
    list_negative = list(df_negative.iloc[::, 0]) 
    return list_positive, list_negative

def sentimentAnalysis(df, neutral):
    list_positive, list_negative = positiveOrNegativeDictionary()
    result = df["Text_Clean_split"].apply(lambda text: utils.sentiment_analysis_lexicon_indonesia(text=text, list_positive=list_positive, list_negative=list_negative))
    result = list(zip(*result))
    df["polarity_score"] = result[0]
    df["polarity"] = result[1]
    if neutral == False :
        df = df[df.polarity != "neutral"]
    # Menggabungkan semua list kata positif dan negatif menjadi satu list
    all_positive_words = [word for sublist in result[2] for word in sublist]
    all_negative_words = [word for sublist in result[3] for word in sublist]

    # Menghitung frekuensi kata-kata positif dan negatif
    positive_df = pd.DataFrame(Counter(all_positive_words).most_common(10), columns=['Words Positive', 'frequency'])
    negative_df = pd.DataFrame(Counter(all_negative_words).most_common(10), columns=['Words Negative', 'frequency'])

    return df, positive_df, negative_df