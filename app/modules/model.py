from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics

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

def predictNaiveBayes(X_train, y_train, X_test, y_test):
    nb = BernoulliNB()

    nb.fit(X_train, y_train)
    y_pred = nb.predict(X_test)
    score = metrics.accuracy_score(y_test, y_pred)
    score_nb = score
    return score_nb, y_pred

def predictFromPKL(tfidf, svm, text):
    new_features = tfidf.transform(text)
    y_pred = svm.predict(new_features)
    # score = metrics.accuracy_score(new_features, y_pred)
    print("============= SCORE")
    print(new_features)
    return y_pred, new_features