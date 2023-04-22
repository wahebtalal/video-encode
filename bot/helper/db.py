import mysql.connector

host = "sql8.freemysqlhosting.net"
user = "sql8613918"
db_name = "sql8613918"
password = "arsyCF3rtp"
port = "3306"

mydb = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=db_name
)


def insert(id, username, name):
    mycursor = mydb.cursor()
    sql = "INSERT INTO Users (id,username,name) VALUES (%s, %s, %s)"
    val = (id, username, name)
    mycursor.execute(sql, val)
    mydb.commit()


def search(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Users where id=%s", [id])
    return mycursor.fetchone()


def usage(id, duration):
    mycursor = mydb.cursor()
    mycursor.execute("update Users set lim=lim- %s where id = %s", [duration, id])
    mydb.commit()


def usage(id):
    mycursor = mydb.cursor()
    mycursor.execute("select lim from Users where id = %s", [id])
    return mycursor.fetchone()


def ban_change(id, ban):
    mycursor = mydb.cursor()
    mycursor.execute("update Users set ban= %s where id = %s", [ban, id])
    mydb.commit()


def ban(id):
    ban_change(id, 1)


def unban(id):
    ban_change(id, 0)


def is_ban(id):
    mycursor = mydb.cursor()
    mycursor.execute("select ban from Users where id = %s", [id])
    if mycursor.fetchone().__contains__(1):
        print(True)
        return True
    else:
        return False


def admin_change(id, admin):
    mycursor = mydb.cursor()
    mycursor.execute("update Users set admin= %s where id = %s", [admin, id])
    mydb.commit()


def admin(id):
    admin_change(id, 1)


def unadmin(id):
    admin_change(id, 0)


def is_admin(id):
    mycursor = mydb.cursor()
    mycursor.execute("select admin from Users where id = %s ", [id])
    if mycursor.fetchone().__contains__(1):
        return True
    else:
        return
    False


def set_limit(lim):
    mycursor = mydb.cursor()
    mycursor.execute("update Users set lim = %s", [lim])
    mydb.commit()


def set_limit(id, lim):
    mycursor = mydb.cursor()
    mycursor.execute("update Users set lim = %s where id  = %s", [lim, id])
    mydb.commit()
