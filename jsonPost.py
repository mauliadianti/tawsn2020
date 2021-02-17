import json
import requests
from mysql.connector import Error
import mysql.connector
import datetime
from time import sleep

def datetimeConverter(o):
    if isinstance(o,datetime.datetime):
        return o.__str__()
    
def queryToDatabase():
    conn = mysql.connector.connect(host='localhost',database = 'lokaldb',user='lokaluser',password='lokal2020')
    sql_select_Query="SELECT * FROM lokaltabel WHERE is_sent = '0' ORDER BY tanggal"
    cursor = conn.cursor(buffered=True,dictionary=True)
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    lokaltabel = json.dumps(records, default = datetimeConverter)
    return lokaltabel

def SendingData(lokaltabel):
    create_row_data = lokaltabel
    api_url = 'http://0.0.0.0:5020/post'
    header = {'Content-Type':'application/json'}
    try:
        r = requests.post(url=api_url,headers = header,data=create_row_data)
        print (r.status_code, r.reason, r.text)
        feedback = r.reason
        return feedback
    except:
        print ("waiting for connection!")
        print (create_row_data,type(create_row_data))
        
def updateTable(feedback):
    if feedback == ("OK"):
        conn = mysql.connector.connect(host='localhost',database='lokaldb', user='lokaluser', password='lokal2020')
        sql_update_query = "update lokaltabel set is_sent = '1' where is_sent = 0"
        cursor = conn.cursor(buffered=True,dictionary=True)
        cursor.execute(sql_update_query)
        conn.commit()
        print ("Record Updated succesfully")
       
        
def main():
    while True:
        lokaltabel = queryToDatabase()
        if lokaltabel != '[]':
            feedback = SendingData(lokaltabel)
            updateTable(feedback)
            sleep(4)
            
if __name__ == '__main__':
    main()