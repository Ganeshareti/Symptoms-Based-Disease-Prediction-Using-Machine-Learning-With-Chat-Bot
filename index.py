from flask import Flask, render_template, request,flash
import pandas as pd
import csv
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random
from flask import Response
from DBConnection import DBConnection
import re
from flask import session
from werkzeug.utils import secure_filename
from Similarity import similarity
import sys
from symptoms_list import symptoms
from patient_registration import patient_store
from doctor_registration import doctor_store
import os
from PIL import Image
from disease_detection import prediction
from ML_Evaluations import evaluation_ml
import io
import base64
import shutil
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
import matplotlib.pyplot as plt4

from random import randint
import numpy as np
from matplotlib import pyplot as pyplt

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/')
def index():
    return render_template('index.html')






@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/patient")
def patient():
    return render_template("patient.html")


@app.route("/doct_rating/<doct_id>/")
def doct_rating(doct_id):
    print("doct_id=",doct_id)

    database = DBConnection.getConnection()
    cursor = database.cursor()
    sql = "select *from doctor where userid='"+doct_id+"' "
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        doct_id=row[7]
        spe= row[3]


    return render_template("/ratings.html", doct_id=doct_id,spe=spe)



@app.route("/patienthome")
def patienthome():
    return render_template("patienthome.html")


@app.route("/adminhome")
def adminhome():
    return render_template("adminhome.html")

@app.route("/view_patients")
def view_patients():
    database = DBConnection.getConnection()
    cursor = database.cursor()
    sql = "select *from patient "
    cursor.execute(sql)
    records = cursor.fetchall()


    return render_template("view_patients.html",rawdata=records)


@app.route("/view_doctors")
def view_doctors():
    database = DBConnection.getConnection()
    cursor = database.cursor()
    sql = "select *from doctor where status='wait'"
    cursor.execute(sql)
    records = cursor.fetchall()


    return render_template("view_doctors.html",rawdata=records)





@app.route("/doctorhome")
def doctorhome():
    return render_template("doctorhome.html")


@app.route("/disease_detection")
def disease_detection():

    symptoms_list=symptoms()

    return render_template("disease_detection.html",symptoms=symptoms_list)

@app.route("/patient_reg")
def patient_reg():
    return render_template("patient_reg.html")

@app.route("/patient_profile")
def patient_profile():
    database = DBConnection.getConnection()
    cursor = database.cursor()
    uid=session['uid']
    sql = "select *from patient where userid='" + uid + "'"
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        name=row[0]
        gen=row[1]
        age=row[2]
        contact = row[5]
        imgdata = row[6]
        data = base64.b64decode(imgdata)
        with open("../Disease_Prediction/static/picture.jpg", 'wb') as f:
            f.write(data)



    return render_template("patient_profile.html",name=name,gen=gen,age=age,contact=contact)


@app.route("/rating",methods =["GET", "POST"])
def rating():
        doct_uid = request.form.get("doct_uid")
        rating = request.form.get("rating")

        database = DBConnection.getConnection()
        cursor = database.cursor()


        sql = "update ratings set "+rating+"="+rating+"+1 where doct_id='" + doct_uid + "' "
        cursor.execute(sql)
        database.commit()

        sql = "select *from ratings where doct_id='" + doct_uid + "'"
        cursor.execute(sql)
        records = cursor.fetchall()
        for row in records:
            one = row[1]
            two = row[2]
            three = row[3]
            four = row[4]
            five = row[5]

        rating=(int(five) * 5 + int(four) * 4 + int(three) * 3 + int(two) * 2 + int(one) * 1) / (int(five) + int(four) + int(three) + int(two) + int(one))
        rating=round(rating,1)
        sql2 = "update doctor set rating='"+str(rating)+"' where userid='" + doct_uid + "'"
        cursor.execute(sql2)
        database.commit()



        records=session["bkapntmnts"]

        return render_template("view_appointments.html",records=records,msg="done")



@app.route("/doctor_profile")
def doctor_profile():
    database = DBConnection.getConnection()
    cursor = database.cursor()
    dct_uid=session['dct_uid']
    sql = "select *from doctor where userid='" + dct_uid + "'"
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        name=row[0]
        gen=row[1]
        age=row[2]
        prof = row[3]
        medication = row[4]
        city = row[5]
        workarea=row[6]

        contact = row[9]
        imgdata = row[10]
        rating = row[11]
        data = base64.b64decode(imgdata)
        with open("../Disease_Prediction/static/picture.jpg", 'wb') as f:
            f.write(data)



    return render_template("doctor_profile.html",name=name,gen=gen,age=age,rating=rating,medication=medication,city=city,workarea=workarea,contact=contact,prof=prof)




@app.route("/appointments")
def appointments():
    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor2 = database.cursor()
    dct_uid=session['dct_uid']
    sql = "select *from bkappointments where doctor_uid='" + dct_uid + "' and status='wait' "
    cursor.execute(sql)
    records = cursor.fetchall()
    bkapntmnts=[]
    for row in records:
        sno=row[0]
        pid=row[1]
        pname = row[2]
        age = row[3]
        gen = row[4]

        symptoms = row[5]
        disease = row[6]
        dt_time = row[8]

        bkapntmnts.append([pid,pname,age,gen,symptoms,disease,dt_time,dct_uid,sno])

    session["bkapntmnts"]=bkapntmnts



    return render_template("appointments.html",bkapntmnts=bkapntmnts)



@app.route("/appointments_list")
def appointments_list():
    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor2 = database.cursor()
    dct_uid=session['dct_uid']
    sql = "select *from bkappointments where doctor_uid='" + dct_uid + "' and status='accept' "
    cursor.execute(sql)
    records = cursor.fetchall()
    bkapntmnts=[]
    for row in records:
        sno=row[0]
        pid=row[1]
        pname = row[2]
        age = row[3]
        gen = row[4]
        symptoms = row[5]
        disease = row[6]
        dt = row[8]
        time = row[9]

        bkapntmnts.append([pid,pname,age,gen,symptoms,disease,dt,dct_uid,time])



    return render_template("appointments_list.html",bkapntmnts=bkapntmnts)





@app.route("/patient_reg_store",methods =["GET", "POST"])
def patient_reg_store():
    try:
        name = request.form.get('name')
        gender = request.form.get('gen')
        age = request.form.get('age')
        uid = request.form.get('uid')
        pwd = request.form.get('pwd')
        mno = request.form.get('mno')
        image_file = request.files['file']
        imgdata = image_file.read()
        #print("img=",image)
        #imgdata = secure_filename(image.filename)
        encodestring = base64.b64encode(imgdata)

        sts=patient_store(name,gender,age,uid,pwd,mno,encodestring)


        if sts==1:
            return render_template("patient.html", msg="Registered Successfully..! Login Here.")


        else:
            return render_template("patient_reg.html", msg="User Id already exists..!")



    except Exception as e:
        print(e)

    return ""

@app.route("/patient_login_check",methods =["GET", "POST"])
def patient_login_check():
        uid = request.form.get("unm")
        pwd = request.form.get("pwd")
        database = DBConnection.getConnection()
        cursor = database.cursor()
        sql = "select count(*) from patient where userid='" + uid + "' and passwrd='" + pwd + "'"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        if res > 0:
            session['uid'] = uid

            return render_template("patienthome.html")
        else:

            return render_template("patient.html",msg2="Invalid Credentials")



        return render_template("admin.html")


@app.route("/admin_login_check",methods =["GET", "POST"])
def admin_login_check():
        uid = request.form.get("unm")
        pwd = request.form.get("pwd")


        if uid=="admin" and pwd=="admin":

            return render_template("adminhome.html")
        else:

            return render_template("admin.html",msg="Invalid Credentials")



        return render_template("admin.html")


@app.route("/doctor_login_check",methods =["GET", "POST"])
def doctor_login_check():
        unm = request.form.get("unm")
        pwd = request.form.get("pwd")
        database = DBConnection.getConnection()
        cursor = database.cursor()
        sql = "select count(*) from doctor where userid='" + unm + "' and passwrd='" + pwd + "' and status='active'"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        if res > 0:
            session['dct_uid'] = unm

            return render_template("doctorhome.html")
        else:

            return render_template("doctor.html",msg2="Invalid Credentials")

        return ""

@app.route("/doctor_reg_store",methods =["GET", "POST"])
def doctor_reg_store():
    try:
        name = request.form.get('name')
        gender = request.form.get('gen')
        age = request.form.get('age')
        prof = request.form.get('prof')
        uid = request.form.get('uid')
        pwd = request.form.get('pwd')
        mno = request.form.get('mno')
        medication = request.form.get('medication')
        city = request.form.get('city')
        workarea = request.form.get('adrs')


        image_file = request.files['file']
        imgdata = image_file.read()

        encodestring = base64.b64encode(imgdata)



        sts=doctor_store(name,gender,age,prof,medication,city,workarea,uid,pwd,mno,encodestring)

        if sts==1:

            return render_template("doctor.html", msg="done")
        else:
            return render_template("doctor_reg.html", msg="duplicate")



    except Exception as e:
        print(e)

    return ""

@app.route("/doctor")
def doctor():
    return render_template("doctor.html")

@app.route("/doctor_reg")
def doctor_reg():
    return render_template("doctor_reg.html")


@app.route("/view_appointments")
def view_appointments():

    p_uid = session['uid']

    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor2 = database.cursor()
   # dct_uid = session['dct_uid']
    sql = "select *from bkappointments where patient_uid='" + p_uid + "'  "
    cursor.execute(sql)
    records = cursor.fetchall()
    bkapntmnts = []
    for row in records:
        sno = row[0]
        pid = row[1]
        pname = row[2]
        age = row[3]
        gen = row[4]
        symptoms = row[5]
        disease = row[6]
        dt = row[8]
        const_doct = row[7]
        time = row[9]
        status= row[10]

        bkapntmnts.append([pid, pname, age, gen, symptoms, disease, dt, const_doct,time,status])



    session["bkapntmnts"] = bkapntmnts
    return render_template("view_appointments.html",records=bkapntmnts)



@app.route("/book_appointment/<spec>/<doct_id>")
def book_appointment(spec,doct_id):

    return render_template("book_appointment.html",spec=spec,doct_id=doct_id)


@app.route("/doctor_accept/<sno>")
def doctor_accept(sno):
    database = DBConnection.getConnection()
    cursor = database.cursor()
    sql = "select *from bkappointments where sno='" + sno + "'"
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        pname=row[2]
        page=row[3]
        pgen = row[4]
        date = row[8]

    return render_template("doctor_accept.html",sno=sno,pname=pname,page=page,date=date,pgen=pgen)


@app.route("/doctor_reject/<sno>")
def doctor_reject(sno):
    database = DBConnection.getConnection()
    cursor = database.cursor()
    sql = "update bkappointments set status='Rejected' where sno='" + sno + "'"
    cursor.execute(sql)
    database.commit()

    database2 = DBConnection.getConnection()
    cursor2 = database2.cursor()
    dct_uid = session['dct_uid']
    sql = "select *from bkappointments where doctor_uid='" + dct_uid + "' and status='wait' "
    cursor2.execute(sql)
    records = cursor2.fetchall()
    bkapntmnts = []
    for row in records:
        sno = row[0]
        pid = row[1]
        pname = row[2]
        age = row[3]
        gen = row[4]
        symptoms = row[5]
        disease = row[6]
        dt_time = row[8]

        bkapntmnts.append([pid, pname, age, gen, symptoms, disease, dt_time, dct_uid, sno])





    return render_template("appointments.html", bkapntmnts=bkapntmnts,msg2='rejected')




@app.route("/doct_approved/<doct_id>")
def doct_approved(doct_id):
    database = DBConnection.getConnection()
    cursor = database.cursor()
    print("doct=",doct_id)
    sql = "update doctor set status='active',rating=5 where userid='" + doct_id + "'"
    cursor.execute(sql)
    database.commit()

    cursor.execute("insert into ratings values('" + doct_id + "',0,0,0,0,1)")
    database.commit()

    return render_template("/view_doctors.html",msg="approved")




@app.route("/book_appointment_doctor",methods =["GET", "POST"])
def book_appointment_doctor():

    symptom=""
    doct_uid = request.form.get('doct_uid')
    date = request.form.get('date')
    p_uid=session['uid']
    sql = "select *from patient where userid='" + p_uid + "'"
    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        name = row[0]
        gen = row[1]
        age = row[2]
    selected_symptoms=session['selected_symptoms']
    predicted_disease= session['predicted_disease']
    date_time=date

    for row in selected_symptoms:
        symptom=symptom+row+","

    symptom=symptom[0:-1]


    database2 = DBConnection.getConnection()
    cursor2 = database2.cursor()
    sql = "insert into bkappointments(patient_uid,patient_name,patient_age,patient_gender,symptoms,disease,doctor_uid,apdate,aptime,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (p_uid,name,age,gen, symptom,predicted_disease,doct_uid,date_time,"","wait")
    cursor2.execute(sql, values)
    database2.commit()

    symptoms_list=symptoms()




    return render_template("disease_detection.html", msg="done",symptoms=symptoms_list)


@app.route("/doctor_accept2",methods =["GET", "POST"])
def doctor_accept2():
    sno = request.form.get('sno')
    time = request.form.get('time')
    database = DBConnection.getConnection()
    cursor = database.cursor()

    sql = "update bkappointments set status='accept', aptime='"+time+"' where sno='" + sno + "'"
    cursor.execute(sql)
    database.commit()

    return render_template("/appointments.html",msg="accepted")


@app.route("/get_selected_symptoms",methods =["GET", "POST"])
def get_selected_symptoms():
    try:
        selected_symptoms = request.form.getlist('symptom')
        print("selected_symptoms=",selected_symptoms)

        consultdoctor,predicted_disease=prediction(selected_symptoms)

        session['selected_symptoms']=selected_symptoms
        session['predicted_disease'] = predicted_disease

        database = DBConnection.getConnection()
        cursor = database.cursor()
        #sql="select *from doctor where specialties='" + consultdoctor + "' "
        sql = "select *from doctor"
        cursor.execute(sql)
        rawdata = cursor.fetchall()


        return render_template("disease_prediction.html",selected_symptoms=selected_symptoms, consultdoctor=consultdoctor,predicted_disease=predicted_disease,rawdata=rawdata)



    except Exception as e:
        print(e)
        tb = sys.exc_info()[2]
        print(tb.tb_lineno)


    return ""


@app.route("/doctors_list", methods =["GET", "POST"])
def doctors_list():
    try:
        pname = request.form.get('pname')
        page = request.form.get('page')
        pgen = request.form.get('pgen')

        medication = request.form.get('medication')
        city = request.form.get('city')

        prof = request.form.get('prof')


        selected_symptoms=session['selected_symptoms']
        predicted_disease=session['predicted_disease']

        database = DBConnection.getConnection()
        cursor = database.cursor()
        #sql="select *from doctor where specialties='" + consultdoctor + "' "
        sql = "select *from doctor where specialties='"+prof+"' and medication='"+medication+"' and city='"+city+"' and status='active'"
        cursor.execute(sql)
        rec_doct_list = cursor.fetchall()

        sql2= "select *from doctor where status='active'"
        cursor.execute(sql2)
        available_doct_list = cursor.fetchall()

        patient_info=[]

        patient_info.append(pname)
        patient_info.append(page)
        patient_info.append(pgen)
        patient_info.append(city)



        return render_template("doctors_list.html",patient_info=patient_info,selected_symptoms=selected_symptoms,
                               consultdoctor=prof,predicted_disease=predicted_disease,
                               rec_doct_list=rec_doct_list,
                               available_doct_list=available_doct_list)



    except Exception as e:
        print(e)
        tb = sys.exc_info()[2]
        print(tb.tb_lineno)


    return ""



@app.route("/evaluations" )
def evaluations():

    metrics,accuracy_list,precision_list,recall_list,f1score_list = evaluation_ml()

    session["accuracy_list"]=accuracy_list

    session["precision_list"] = precision_list

    session["recall_list"] = recall_list

    session["f1score_list"] = f1score_list

    session["metrics"] = metrics

    ml_accuracy()
    ml_precision()
    ml_recall()
    ml_f1score()

    return render_template("ml_evaluations.html", metrics=metrics)

#@app.route("/ml_accuracy")
def ml_accuracy():
    accuracy_list=session["accuracy_list"]
    bars = ('RF', 'NB', 'DT', 'VotingClassifier')
    plt.figure(1)
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, accuracy_list, color=['red', 'green', 'blue','orange'])
    plt.xticks(y_pos, bars)
    plt.xlabel('Classification Algorithms')
    plt.ylabel('Accuracy')
    plt.title('Accuracy of ML Techniques')
    plt.savefig('static/accuracy.png')
    #plt.show()

    #metrics=session["metrics"]
    #return render_template("ml_evaluations.html", metrics=metrics)

    #pyplt.savefig('accuracy.png')
    #fig = pyplt.gcf()

    #return fig

#@app.route("/ml_precision")
def ml_precision():

    precision_list=session["precision_list"]
    bars = ('RF', 'NB', 'DT', 'VotingClassifier')
    plt2.figure(2)
    y_pos = np.arange(len(bars))
    plt2.bar(y_pos, precision_list, color=['blue', 'orange', 'red','green'])
    plt2.xticks(y_pos, bars)
    plt2.xlabel('Classification Algorithms')
    plt2.ylabel('Precision')
    plt2.title('Precision of ML Techniques')
    plt2.savefig('static/precision.png')
    #plt2.show()
    #metrics = session["metrics"]
    #return render_template("ml_evaluations.html", metrics=metrics)

def ml_accuracy():
    accuracy_list=[]
    accuracy_list.clear()
    accuracy_list=session["accuracy_list"]

    bars = ('RF', 'NB', 'DT', 'VotingClassifier')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, accuracy_list, color=['red', 'green', 'blue','orange'])
    plt.xticks(y_pos, bars)
    plt.xlabel('Classification Algorithms')
    plt.ylabel('Accuracy')
    plt.title('Accuracy of ML Techniques')
    plt.savefig('static/accuracy.png')

    accuracy_list.clear()
    #fig = pyplt.gcf()

    #return fig

def ml_precision():
    precision_list = []
    precision_list.clear()
    precision_list=session["precision_list"]
    bars = ('RF', 'NB', 'DT', 'VotingClassifier')
    y_pos = np.arange(len(bars))
    plt2.bar(y_pos, precision_list, color=['blue', 'orange', 'red','green'])
    plt2.xticks(y_pos, bars)
    plt2.xlabel('Classification Algorithms')
    plt2.ylabel('Precision')
    plt2.title('Precision of ML Techniques')
    plt2.savefig('static/precision.png')
    precision_list.clear()

def ml_recall():
    recall_list=session["recall_list"]
    bars = ('RF', 'NB', 'DT', 'VotingClassifier')
    plt3.figure(3)
    y_pos = np.arange(len(bars))
    plt3.bar(y_pos, recall_list, color=['green','red','orange','blue'])
    plt3.xticks(y_pos, bars)
    plt3.xlabel('Classification Algorithms')
    plt3.ylabel('Recall')
    plt3.title('Recall of ML Techniques')
    plt3.savefig('static/recall.png')
    recall_list.clear()

def ml_f1score():
    f1score_list=session["f1score_list"]
    bars = ('RF', 'NB', 'DT', 'VotingClassifier')
    plt4.figure(4)
    y_pos = np.arange(len(bars))
    plt4.bar(y_pos, f1score_list, color=['orange', 'blue', 'green','red'])
    plt4.xticks(y_pos, bars)
    plt4.xlabel('Classification Algorithms')
    plt4.ylabel('F1-Score')
    plt4.title('F1-Score of ML Techniques')
    plt4.savefig('static/fscore.png')
    f1score_list.clear()
#chatbot in main page
@app.route("/chat1")
def chat1():
    #uid = session['uid']
    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor2 = database.cursor()
    cursor.execute("delete from chat")
    database.commit()

    cursor.execute("insert into chat(msg,user_) values('Hello','chatbot')")
    database.commit()
    msg="Dear user"#+uid
    cursor.execute("insert into chat(msg,user_) values('"+msg+"','chatbot')")
    database.commit()
    cursor.execute("insert into chat(msg,user_) values('How can I help you..', 'chatbot')")
    database.commit()

    sql = "select * from chat order by sno "
    cursor2.execute(sql)
    records = cursor2.fetchall()

    return render_template("chatbot1.html", rawdata=records,res="")

@app.route("/chatbot3", methods=["GET", "POST"])
def chatbot3():

    dict = {}
    #uid = session['uid']
    text = request.form.get('text')
    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor4 = database.cursor()
    cursor5 = database.cursor()
    cursor.execute("insert into chat(msg) values('" + text + "')")
    database.commit()

    cursor2 = database.cursor()
    sql = "select qtns,sno from questions"
    cursor2.execute(sql)
    res = cursor2.fetchall()

    for row in res:
        score = similarity(row[0], text)
        dict[row[1]] = score

    key = max(dict, key=dict.get)
    print("Highest value from dictionary:", key)

    if dict[key] > 0.1:
        cursor3 = database.cursor()
        sql2 = "select answrs from questions where sno='" + str(key) + "' "
        cursor3.execute(sql2)
        res2 = cursor3.fetchall()

        for row2 in res2:
            replay = row2[0]

            cursor4.execute("insert into chat(msg,user_) values('" + replay + "','chatbot')")
            database.commit()

        sql3 = "select * from chat order by sno "
        cursor5.execute(sql3)
        records = cursor5.fetchall()

        return render_template("chatbot1.html", rawdata=records, res="")




    else:
        cursor4.execute("insert into chat(msg,user_) values('Sorry, I am not understood..','chatbot')")
        database.commit()

        sql3 = "select * from chat order by sno "
        cursor5.execute(sql3)
        records = cursor5.fetchall()

        return render_template("chatbot1.html", rawdata=records, res="")

    return render_template("")

#chatbot in patient page

@app.route("/chat")
def chat():
    uid = session['uid']
    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor2 = database.cursor()
    cursor.execute("delete from chat")
    database.commit()

    cursor.execute("insert into chat(msg,user_) values('Hello','chatbot')")
    database.commit()
    msg="Dear "+uid
    cursor.execute("insert into chat(msg,user_) values('"+msg+"','chatbot')")
    database.commit()
    cursor.execute("insert into chat(msg,user_) values('How can I help you..', 'chatbot')")
    database.commit()

    sql = "select * from chat order by sno "
    cursor2.execute(sql)
    records = cursor2.fetchall()

    return render_template("chatbot.html", rawdata=records,res="")

@app.route("/chatbot2", methods=["GET", "POST"])
def chatbot2():

    dict = {}
    uid = session['uid']
    text = request.form.get('text')
    database = DBConnection.getConnection()
    cursor = database.cursor()
    cursor4 = database.cursor()
    cursor5 = database.cursor()
    cursor.execute("insert into chat(msg,user_) values('" + text + "','" + uid + "')")
    database.commit()

    cursor2 = database.cursor()
    sql = "select qtns,sno from questions"
    cursor2.execute(sql)
    res = cursor2.fetchall()

    for row in res:
        score = similarity(row[0], text)
        dict[row[1]] = score

    key = max(dict, key=dict.get)
    print("Highest value from dictionary:", key)

    if dict[key] > 0.1:
        cursor3 = database.cursor()
        sql2 = "select answrs from questions where sno='" + str(key) + "' "
        cursor3.execute(sql2)
        res2 = cursor3.fetchall()

        for row2 in res2:
            replay = row2[0]

            cursor4.execute("insert into chat(msg,user_) values('" + replay + "','chatbot')")
            database.commit()

        sql3 = "select * from chat order by sno "
        cursor5.execute(sql3)
        records = cursor5.fetchall()

        return render_template("chatbot.html", rawdata=records, res="")




    else:
        cursor4.execute("insert into chat(msg,user_) values('Sorry, I am not understood..','chatbot')")
        database.commit()

        sql3 = "select * from chat order by sno "
        cursor5.execute(sql3)
        records = cursor5.fetchall()

        return render_template("chatbot.html", rawdata=records, res="")

    return render_template("")


if __name__ == '__main__':
    app.run(host="localhost", port=5678, debug=True)
