from Parser import *



def ConnectToDB():
    try:
        cnx = mysql.connector.connect(user=user, password=password,
                                      host=host, database=database)
        return cnx, cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def InsertToDB(add,cnx, cursor):

    add_log = (add)
    cursor.execute(add_log)
    for i in cursor:
        ip= i[2:4]
        dic={}
        if ip in dic:
            dic[ip]+=1
        else:
            dic[ip]=1
        

    cnx.commit()
    cursor.close()
    cnx.close()

def main2():
    #c="""select SRC_IP from fwlogs WHERE PORT=444 OR PORT=4445 ;"""
    c="""select * from fwlogs ;"""
    cnx, cursor = ConnectToDB()
    InsertToDB(c,cnx, cursor)



main2()