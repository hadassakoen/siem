import datetime
import mysql.connector
from mysql.connector import errorcode


user = 'root'
password = 'P@ssw0rd'
host = '192.168.252.218'
database = 'siem'




def ConnectToDB2():
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
    cursor.execute(add)
    alllogs=[]
    for i in cursor:
        alllogs.append(i)
    return alllogs

def setit(val,new):
       val.append(new)

def GetTimeDiffreneces(start, end):
    c = end - start
    return divmod(c.days * 86400 + c.seconds, 60)



def main2():
    #c="""select SRC_IP from fwlogs WHERE PORT=444 OR PORT=4445 ;"""
    cnx, cursor = ConnectToDB2()

    print '1--------------------Specific Port:'
    c = """select SRC_IP from fwlogs WHERE PORT=444 OR PORT=4445 ;"""
    print  InsertToDB(c, cnx, cursor)

    print '2-------------------Port Scan:'
    c = """select * from fwlogs ;"""
    dic = {}
    for a in InsertToDB(c, cnx, cursor):
        ip = a[2:4]
        if ip in dic:
            dic[ip] += 1
        else:
            dic[ip] = 1
    list=[]
    for i in dic:
        if dic[i] > 10:
            list.append(i)

    for l in list:
        port=[]
        for d in InsertToDB(c, cnx, cursor):
            if l==d[2:4]:
                port.append(d[4])
        if len(set(port))>10:
            print l ,'tried to get in ' , len(set(port)), ' different port'
            print set(port)


    print '3-----------Ping Sweep:'
    c = """select SRC_IP,DST_IP,PORT,date from fwlogs WHERE PORT=0 ;"""
    dic={}
    for i in InsertToDB(c, cnx, cursor):
        if i[0] in dic:
            dic[i[0]]+=1
        else:
            dic[i[0]]=1

    for d in dic:
        if dic[d]>10:
            DST_IP=[]
            for i in InsertToDB(c, cnx, cursor):
                if i[0]==d:

                    DST_IP.append(i[1])
            if set(DST_IP)>10:
                print d

    u = """select date from fwlogs  ;"""
    t=InsertToDB(u, cnx, cursor)[0] [0]
    print t
    y=InsertToDB(u, cnx, cursor)[4] [0]
    print y
    print GetTimeDiffreneces(t,y) [1]


    cnx.commit()
    cursor.close()
    cnx.close()
main2()

'''
dic = {}
for i in cursor:
    ip= i[2:4]
    if ip in dic:
        dic[ip]+=1
    else:
        dic[ip]=1
for i in dic:
    if dic[i]>10:
        print i
'''