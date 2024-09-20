from DBConnection import DBConnection
def  doctor_store(name,gender,age,prof,medication,city,workarea,uid,pwd,mno,encodestring):
    sts=0
    database = DBConnection.getConnection()
    cursor = database.cursor()
    sql = "select count(*) from doctor where userid='" + uid + "'"
    cursor.execute(sql)
    res = cursor.fetchone()[0]
    if res > 0:
        sts=0
    else:
        rating=0
        status="wait"
        sql = "insert into doctor values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (name, gender, age,prof,medication,city,workarea,uid, pwd,mno,encodestring,rating,status)
        cursor.execute(sql, values)
        database.commit()


        sts=1

    return sts;

