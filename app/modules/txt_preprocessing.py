import re, unicodedata
from nlp_id.lemmatizer import Lemmatizer
from nlp_id.stopword import StopWord 
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize

unwanted_words = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'uaddown', 'weareuad', 'lam', 'https', 'igshid']

def hitung_kemunculan(kalimat, array_kata):
    result = {}
    print(kalimat)
    # print(kalimat.find("internet"))
    
    for i, kata in enumerate(array_kata):
        jumlah_kemunculan = 0
        for index, kataDataFrame in enumerate(kalimat):
            jumlah_kemunculan += kataDataFrame.count(kata)
            result[f'{kata}'] = jumlah_kemunculan
    return result

def Case_Folding(text):
    try:
        # Mengubah text menjadi lowercase
        text = text.lower()
        # Menghapus white space
        text = re.sub('[\s]+', ' ', text)
        
        return text
    except AttributeError as error:
        raise AttributeError(str(error))

def Cleansing(text):
    try:
        # Definisikan pola regex untuk mencocokkan tag atau tagar
        pattern = r"[@#]\w+"
        
        # Hapus tag atau tagar menggunakan metode sub() dari modul re
        text_cleaned = re.sub(pattern, "", text)

        # Definisikan pola regex untuk mendeteksi link
        pattern = r"(http://|https://|www\.)\S+"
        
        # Hapus link menggunakan metode sub() dari modul re
        text = re.sub(pattern, "", text_cleaned)
        # hapus non-ascii 
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")
        
        # Menghapus tanda baca 
        text = re.sub(r'[^\w]|_', ' ', text)
        
        # Menghapus angka
        text = re.sub("\S*\d\S*", "", text).strip()
        text = re.sub("\b\d+\b", " ", text)
        return text
    except TypeError as error:
        raise TypeError(str(error))
        

def lemmatisasi():
    """
        mengembalikan kata kepada kata dasarnya yang disesuaikan dengan kamus Bahasa Indonesia
    """
    lemmatizer = Lemmatizer()
    return lemmatizer

def stemming():
    # membuat stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer

def Slangwords(text, slang_dict):
    words = text.split()
    normalized_words = [slang_dict[word] if word in slang_dict else word for word in words]
    normalized_text = ' '.join(normalized_words)
    return normalized_text

def stopwordRemoval():
    stopword = StopWord() 
    return stopword

def RemoveUnwantedWords(text):
    word_tokens = word_tokenize(text)
    fillterd_sentence = [word for word in word_tokens if not word in unwanted_words]
    return ' '.join(fillterd_sentence)

# Menghitung kata-kata positif / negatif pada teks dan menentukan sentimennya
def lexicon_indonesia(text, list_positive, list_negative):
    positive_words = []
    negative_words = []
    neutral_words = []
    score = 0
    for word in text:
        if (word in list_positive):
            score += 1
            positive_words.append(word)
        if (word in list_negative):
            score -= 1
            negative_words.append(word)
        if (word not in list_positive and word not in list_negative): 
            neutral_words.append(word)

    polarity=''
    if (score > 0):
        polarity = 'positive'
    elif (score < 0):
        polarity = 'negative'
    else:
        polarity = 'neutral'
    
    return score, polarity, positive_words, negative_words
