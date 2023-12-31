from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.tokenize import word_tokenize

from scipy.stats import rankdata
from nlp_id.tokenizer import Tokenizer

from nltk import word_tokenize, download

tokenizer = Tokenizer()
download("punkt")

def split_word(text):
    return tokenizer.tokenize(text)

def tfidf(df):
    tfidf = TfidfVectorizer(max_features=len(df['Text_Clean_new']))
    review = df["Text_Clean_new"].values.tolist()
    tfidf_vector = tfidf.fit(review)
    X = tfidf_vector.transform(review)
    y = df["polarity"]
    # print(X[0:2])
    return X, y 

def calculate_tfidf_ranking(df): 
        max_features = 10

        count_vectorizer = CountVectorizer(tokenizer=word_tokenize)
        ulasan = df['Text_Clean_new'].values.tolist()
        X_count = count_vectorizer.fit_transform(ulasan)

        tf_idf = TfidfVectorizer(max_features=max_features, binary=True)
        tfidf_mat = tf_idf.fit_transform(df["Text_Clean_new"]).toarray()
        print(tfidf_mat)
        terms = tf_idf.get_feature_names_out()
        # print(tfidf_mat)
        # sum tfidf frequency dari setiap dokumen
        sums = tfidf_mat.sum(axis=0)
        ranks = rankdata(-sums)
        
        # connecting term to its sums frequency
        data = list(zip(sums, tf_idf.idf_, terms))

        # sorting data based on frequency
        data_sorted = sorted(data, key=lambda x: x[1])

        return data_sorted

def hitung_kamus(df):
    # Mengubah kolom 'Text_Clean' menjadi tipe data string
    df['Text_Clean_New'] = df['Text_Clean'].astype(str)

    # Menghitung frekuensi kemunculan kata dengan CountVectorizer
    count_vectorizer = CountVectorizer(tokenizer=word_tokenize)
    ulasan = df['Text_Clean_New'].values.tolist()
    X_count = count_vectorizer.fit_transform(ulasan)

    # Menginisialisasi dan melatih model TF-IDF dengan TfidfVectorizer
    tfidf = TfidfVectorizer()
    X_tfidf = tfidf.fit_transform(ulasan)

    # Mendapatkan kata-kata unik dari kamus
    kata_unik = count_vectorizer.get_feature_names()

    # Menghitung frekuensi kemunculan dan nilai TF-IDF untuk setiap kata
    kamus = {}
    for i, kata in enumerate(kata_unik):
        kamus[kata] = {
            'TF': X_count[:, i].sum(),
            'IDF': tfidf.idf_[tfidf.vocabulary_[kata]]
        }

    return kamus