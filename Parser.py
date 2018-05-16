import mysql.connector
from mysql.connector import errorcode

user = 'root'
password = 'P@ssw0rd'
host = '192.168.60.135'
database = 'siem'

#1
def log(line):
    list= line.split()
    dic={}
    dic['DATE']=list[0] +' '+ list[1]
    dic['SRC_IP'] = list[2]
    dic['DST_IP'] = list[3]
    dic['PORT'] = list[4]
    dic['ACTION'] = list[5]
    return dic


#2
def PortToProtocol(num):
    ports = {'21':'FTP', '22':'SSH', '23':'TELNET', '25':'SMTP', '67':'DHCP', '53':'DNS', '80':'HTTP', '445':'SMB', '443':'HTTPS'}
    if str(num) in ports.keys():
        return ports[str(num)]
    else:
        return 'UNKOWN'

#3
def all(text):
    dic=log(text)
    proto= PortToProtocol(dic['PORT'])
    dic['PROTOCOL']=proto
    return dic


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

def InsertToDB(log, cnx, cursor):

    add_log = ("""INSERT INTO fwlogs (ID, date, SRC_IP, DST_IP, PORT, PROTOCOL, ACTION) VALUES (NULL, %(DATE)s, %(SRC_IP)s, %(DST_IP)s, %(PORT)s, %(PROTOCOL)s, %(ACTION)s)""")
    cursor.execute(add_log,log)
    cnx.commit()

    cursor.close()
    cnx.close()

def main():
    opened_file = open(r'C:\Users\Owner\PycharmProjects\untitled\raz\Ping_Sweep.txt', 'r')
    for log in opened_file:
        dic=all(log)

        cnx, cursor = ConnectToDB()
        InsertToDB(dic , cnx, cursor)

main()
















