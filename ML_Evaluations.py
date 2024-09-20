
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import GaussianNB,BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import numpy as np
from sklearn.metrics import f1_score, precision_score, accuracy_score, recall_score,confusion_matrix
import pandas as pd

def evaluation_ml():
    rf_list = []
    dt_list = []
    nb_list = []
    voting_list = []
    metrics=[]
    accuracy_list=[]
    precision_list = []
    recall_list = []
    f1score_list = []

    df = pd.read_csv("../Disease_Prediction/dataset/trainingset.csv")
    y=df['prognosis']
    print(y)
    del df['prognosis']
    X=df
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
    

    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    #RandomForest Classifier
    rfc_clf = RandomForestClassifier(n_estimators=300,max_depth=2)
    rfc_clf.fit(X_train, y_train)

    predicted = rfc_clf.predict(X_test)

    accuracy_rf = accuracy_score(y_test, predicted)*100

    precision_rf = precision_score(y_test, predicted, average='weighted')*100

    recall_rf = recall_score(y_test, predicted, average='weighted')*100

    fscore_rf = f1_score(y_test, predicted, average='weighted')*100

    print("RF=",accuracy_rf,precision_rf,recall_rf,fscore_rf)

    rf_list.append("RandomForestClassifier")

    rf_list.append(accuracy_rf)
    rf_list.append(precision_rf)
    rf_list.append(recall_rf)
    rf_list.append(fscore_rf)


    # NaiveBayes Classifier
    nb_clf = BernoulliNB(alpha=150)

    nb_clf.fit(X_train, y_train)

    predicted = nb_clf.predict(X_test)

    accuracy_nb = accuracy_score(y_test, predicted)*100

    precision_nb = precision_score(y_test, predicted,average='weighted')*100

    recall_nb = recall_score(y_test, predicted, average='weighted')*100

    fscore_nb = f1_score(y_test, predicted, average='weighted')*100

    print("NB=",accuracy_nb,precision_nb,recall_nb,fscore_nb)

    nb_list.append("NaiveBayes")
    nb_list.append(accuracy_nb)
    nb_list.append(precision_nb)
    nb_list.append(recall_nb)
    nb_list.append(fscore_nb)




    # Decision Tree
    dt_clf = DecisionTreeClassifier(criterion='entropy',max_depth=6)

    dt_clf.fit(X_train, y_train)

    predicted = dt_clf.predict(X_test)

    accuracy_dt = accuracy_score(y_test, predicted)*100

    precision_dt = precision_score(y_test, predicted, average='macro')*100

    recall_dt = recall_score(y_test, predicted, average='macro')*100

    fscore_dt = f1_score(y_test, predicted, average='macro')*100

    print("DT=",accuracy_dt,precision_dt,recall_dt,fscore_dt)

    dt_list.append("DecisionTreeClassifier")
    dt_list.append(accuracy_dt)
    dt_list.append(precision_dt)
    dt_list.append(recall_dt)
    dt_list.append(fscore_dt)



    #Voting Classifier
    voting_clf = VotingClassifier(estimators=[('RF', rfc_clf), ('NB', nb_clf), ('dt', dt_clf)], voting='hard')

    voting_clf.fit(X_train, y_train)

    predicted = voting_clf.predict(X_test)

    accuracy_voting = accuracy_score(y_test, predicted)*100

    precision_voting = precision_score(y_test, predicted, average='macro')*100

    recall_voting = recall_score(y_test, predicted, average='macro')*100

    fscore_voting = f1_score(y_test, predicted, average='macro')*100

    print("VC=",accuracy_voting,precision_voting,recall_voting,fscore_voting)

    voting_list.append("VotingClassifier")
    voting_list.append(accuracy_voting)
    voting_list.append(precision_voting)
    voting_list.append(recall_voting)
    voting_list.append(fscore_voting)

    metrics.append(rf_list)
    metrics.append(nb_list)
    metrics.append(dt_list)
    metrics.append(voting_list)

    accuracy_list.clear()
    accuracy_list.append(accuracy_rf)
    accuracy_list.append(accuracy_nb)
    accuracy_list.append(accuracy_dt)
    accuracy_list.append(accuracy_voting)



    precision_list.clear()
    precision_list.append(precision_rf)
    precision_list.append(precision_nb)
    precision_list.append(precision_dt)
    precision_list.append(precision_voting)



    recall_list.append(recall_rf)
    recall_list.append(recall_nb)
    recall_list.append(recall_dt)
    recall_list.append(recall_voting)

    f1score_list.append(fscore_rf)
    f1score_list.append(fscore_nb)
    f1score_list.append(fscore_dt)
    f1score_list.append(fscore_voting)

    return metrics,accuracy_list,precision_list,recall_list,f1score_list







