from sklearn.feature_extraction.text import TfidfVectorizer
  
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn import metrics

from sklearn.metrics import accuracy_score, plot_confusion_matrix 

def tfidf(df):
    tfidf = TfidfVectorizer()
    review = df["Text_Clean_new"].values.tolist()
    tfidf_vector = tfidf.fit(review)
    X = tfidf_vector.transform(review)
    y = df["polarity"]
    print(X[0:2])
    return X, y 

def train_test_splitTFIDF(X, y, testSize, randState):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize, random_state=randState)
    data_latih = len(y_train)
    data_test = len(y_test)
    all_data = len(y)
    return X_train, X_test, y_train, y_test, data_latih, data_test, all_data

def predictSVM(X_train, y_train, X_test, y_test):
    svmLinear = SVC(
    kernel = 'linear',
        C = 1)

    svmLinear.fit(X_train, y_train)
    y_pred = svmLinear.predict(X_test)
    score = metrics.accuracy_score(y_test, y_pred)
    score_svmlk = score
    return score_svmlk, svmLinear, y_pred

def predictFromPKL(tfidf, svm, text):
    new_features = tfidf.transform([text]) 
    y_pred = svm.predict(new_features)
    return y_pred, new_features

def plot_confusion_matrix_box(svmLinear, X_test, y_test, y_pred):
    plot_confusion_matrix(svmLinear, X_test, y_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy