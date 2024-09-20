
from symptoms_list import symptoms
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import GaussianNB,BernoulliNB
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
def prediction(selected_symptoms):
    symptomslist=symptoms()


    testingsymptoms = []
    # append zero in all coloumn fields...
    for x in range(0, len(symptomslist)):
        testingsymptoms.append(0)

    # update 1 where symptoms gets matched...
    for k in range(0, len(symptomslist)):
        for z in selected_symptoms:
            if z == symptomslist[k]:
                testingsymptoms[k] = 1

    inputtest = [testingsymptoms]
    print(inputtest)

    dataset=pd.read_csv("../Disease_Prediction/dataset/trainingset.csv")
    y_train=dataset["prognosis"]

    del dataset["prognosis"]
    x_train=dataset

    rfc_clf = RandomForestClassifier()
    nb_clf = BernoulliNB()
    dt_clf = DecisionTreeClassifier()


    voting_clf = VotingClassifier(estimators=[('RF', rfc_clf), ('NB', nb_clf), ('dt', dt_clf)], voting='hard')

    voting_clf.fit(x_train, y_train)

    predicted = voting_clf.predict(inputtest)





    '''clf_rf = RandomForestClassifier(max_depth=2, random_state=0)
    model=clf_rf.fit(x_train,y_train)

    predicted= model.predict(inputtest)'''

    predicted_disease=predicted[0]

    #Specializations list

    Rheumatologist = ['Osteoarthristis', 'Arthritis']

    Cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']

    ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']


    Neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

    Allergist_Immunologist = ['Allergy', 'Pneumonia',
                              'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

    Urologist = ['Urinary tract infection',
                 'Dimorphic hemmorhoids(piles)']

    Dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']

    Gastroenterologist = ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Gastroenteritis',
                          'Hepatitis E',
                          'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                          'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']


    if predicted_disease in Rheumatologist:
        consultdoctor = "Rheumatologist"

    elif predicted_disease in Cardiologist:
        consultdoctor = "Cardiologist"

    elif predicted_disease in ENT_specialist:
        consultdoctor = "ENT specialist"

    elif predicted_disease in Neurologist:
        consultdoctor = "Neurologist"

    elif predicted_disease in Allergist_Immunologist:
        consultdoctor = "Allergist/Immunologist"

    elif predicted_disease in Urologist:
        consultdoctor = "Urologist"

    elif predicted_disease in Dermatologist:
        consultdoctor = "Dermatologist"

    elif predicted_disease in Gastroenterologist:
        consultdoctor = "Gastroenterologist"
    else:
        consultdoctor = "other"



    return consultdoctor,predicted_disease

















