from sklearn.metrics import accuracy_score, plot_confusion_matrix, confusion_matrix
from sklearn.metrics import classification_report

def plot_confusion_matrix_box(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)

    return accuracy, cm

def classificationReport(y_test, y_pred):
    report = classification_report(y_test, y_pred)
    return report
