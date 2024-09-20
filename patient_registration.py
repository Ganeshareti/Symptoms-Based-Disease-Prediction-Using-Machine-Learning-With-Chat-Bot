from DBConnection import DBConnection
def  patient_store(name,gender,age,uid,pwd,mno,imgdata):
    sts=0;
    database = DBConnection.getConnection()
    cursor = database.cursor()
    sql = "select count(*) from patient where userid='" + uid + "'"
    cursor.execute(sql)
    res = cursor.fetchone()[0]
    if res > 0:
        sts=0
    else:
        sql = "insert into patient values(%s,%s,%s,%s,%s,%s,%s)"
        values = (name, gender, age, uid, pwd,mno,imgdata)
        cursor.execute(sql, values)
        database.commit()
        sts=1

    return sts;

