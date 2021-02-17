from flask import Flask, render_template, jsonify, request, redirect, url_for, session, logging, flash, make_response
from flask_mysqldb import MySQL,MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit
import json
from mysql.connector import Error
import mysql.connector
import requests
import pytz
import datetime
from datetime import datetime
from time import time
engine = create_engine("mysql+pymysql://tajsn2020:ta2020@localhost/monitoringdb")
db = scoped_session(sessionmaker(bind=engine))

import bcrypt

app = Flask(__name__,static_url_path='/static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tajsn2020'
app.config['MYSQL_PASSWORD'] = 'tajsn2020'
app.config['MYSQL_DB'] = 'monitoringdb'
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

Mysql = MySQL(app)

def begin_mysql_connection():
    conn = Mysql.connector.connect(host='localhost',database='monitoringdb',user='tajsn2020',password='tajsn2020')
    return conn

def get_latest_data():
    cursor = Mysql.connection.cursor()
    cursor.execute("select fusi_temperature, fusi_humidity, fusi_co, fusi_co2, kualitas_udara from fusi where fusi_id in (select max(fusi_id) from fusi)")
    data = cursor.fetchall()
    data = data[0]
    res = {'value': '', 'value2': '', 'value3': '', 'value4': '', 'value5': ''}
    for index, key in enumerate(res):
        res[key] = data[index]
    data = json.dumps(res, indent=4, sort_keys=True, default=str)
    return data


def queryToDatabase():
    conn = mysql.connector.connect(host='localhost',database='monitoringdb', user='tajsn2020',password='tajsn2020')
    sql_select_Query="SELECT * FROM fusi WHERE fusi_id in (select max(fusi_id) from fusi)"
    cursor = conn.cursor(buffered=True,dictionary=True)
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    conn.close()
    return records

@app.route("/post",methods=['POST'])
def post_sensor_data():
    list_sensor_data = request.get_json()
    for lokaltabel in list_sensor_data:
        insert_data_to_database(lokaltabel)
    return 'JSON'


def insert_data_to_database(lokaldb):
    conn = mysql.connector.connect(host='localhost',database='lokaldb',user='lokaluser',password='lokal2020')
    tx_1 = float(lokaltabel["tx_1"])
    rssi_1 = float(lokaltabel["rssi_1"])
    temperature_1 = float(lokaltabel["temperature_1"])
    humidity_1 = float(lokaltabel["humidity_1"])
    co_1 = float(lokaltabel["co_1"])
    co2_1 = float(lokaltabel["co2_1"])
    tx_2 = float(lokaltabel["tx_2"])
    rssi_2 = float(lokaltabel["rssi_2"])
    temperature_2 = float(lokaltabel["temperature_2"])
    humidity_2 = float(lokaltabel["humidity_2"])
    co_2 = float(lokaltabel["co_2"])
    co2_2 = float(lokaltabel["co2_2"])
    tx_3 = float(lokaltabel["tx_3"])
    rssi_3 = float(lokaltabel["rssi_3"])
    temperature_3 = float(lokaltabel["temperature_3"])
    humidity_3 = float(lokaltabel["humidity_3"])
    co_3 = float(lokaltabel["co_3"])
    co2_3 = float(lokaltabel["co2_3"])
    tx_4 = float(lokaltabel["tx_4"])
    rssi_4 = float(lokaltabel["rssi_4"])
    temperature_4 = float(lokaltabel["temperature_4"])
    humidity_4 = float(lokaltabel["humidity_4"])
    co_4 = float(lokaltabel["co_4"])
    co2_4 = float(lokaltabel["co2_4"])
    fusi_temperature = float(lokaltabel["fusi_temperature"])
    fusi_humidity = float(lokaltabel["fusi_humidity"])
    fusi_co = float(lokaltabel["fusi_co"])
    fusi_co2 = float(lokaltabel["fusi_co2"])
    kualitas_udara = str(lokaltabel["kualitas_udara"])
    args1 = (tx_1, rssi_1, temperature_1, humidity_1, co_1, co2_1)
    args2 = (tx_2, rssi_2, temperature_2, humidity_2, co_2, co2_2)
    args3 = (tx_3, rssi_3, temperature_3, humidity_3, co_3, co2_3)
    args4 = (tx_4, rssi_4, temperature_4, humidity_4, co_4, co2_4)
    args5 = (fusi_temperature, fusi_humidity, fusi_co, fusi_co2, kualitas_udara)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Node1(TX, RSSI, temperature, humidity, co, co2, from_node) VALUES (%s,%s,%s,%s,%s,%s,1)", args1)
    cursor.execute("INSERT INTO Node2(TX_2, RSSI_2, temperature_2, humidity_2, co_2, co2_2, from_node_2) VALUES (%s,%s,%s,%s,%s,%s,2)", args2)
    cursor.execute("INSERT INTO Node3(TX_3, RSSI_3, temperature_3, humidity_3, co_3, co2_3, from_node_3) VALUES (%s,%s,%s,%s,%s,%s,3)", args3)
    cursor.execute("INSERT INTO Node4(TX_4, RSSI_4, temperature_4, humidity_4, co_4, co2_4, from_node_4) VALUES (%s,%s,%s,%s,%s,%s,4)", args4)
    cursor.execute("INSERT INTO fusi(fusi_temperature, fusi_humidity, fusi_co, fusi_co2, kualitas_udara) VALUES (%s,%s,%s,%s,%s)", args5)
    conn.commit()

    
@app.route("/api/sender/", methods=['GET'])
def get_sensor_data():
    records = queryToDatabase()
    return jsonify (records)


@app.route('/data', methods=["GET", "POST"])
def data():
    data = json.loads(get_latest_data())
    Temperature = float(data['value'])
    Humidity = float(data['value2'])
    co = float(data['value3'])
    co2 = float(data['value4'])
    
    
    tz = datetime.now(pytz.timezone('Asia/Jakarta'))
    tm = tz.strftime("%Y-%m-%d- %H:%M:%S.%f")
    x = datetime.strptime(tm, "%Y-%m-%d- %H:%M:%S.%f")
    Time= (x - datetime(1970,1,1)).total_seconds()
    data = [Time*1000, Temperature, Humidity, co, co2]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@socketio.on('status')
def tes_message(message):
    #time.sleep(1)
    data = get_latest_data()
    emit('data-receiver', data)

@socketio.on('get-latest-data')
def access_new_data(latest_data):
    data = get_latest_data()
    #time.sleep(1)
    emit('data-receiver', data)
  
@app.route('/')
def main():
    NULL = 0
    cursor = Mysql.connection.cursor()
    cursor.execute("select fusi_temperature, fusi_humidity, fusi_co, fusi_co2, kualitas_udara from fusi where fusi_id in (select max(fusi_id) from fusi)")
    data = cursor.fetchall()

    data = data[0]
    cursor.close()
    return render_template('index.html', value=data[0])
    

@app.route("/monitoring_login")
def monitoring_login():
    NULL = 0
    cursor = Mysql.connection.cursor()
    cursor.execute("select fusi_temperature, fusi_humidity, fusi_co, fusi_co2, kualitas_udara from fusi where fusi_id in (select max(fusi_id) from fusi)")
    data = cursor.fetchall()

    data = data[0]
    cursor.close()
    return render_template('monitoring_login.html', value=data[0])


@app.route("/database")
def Node1():
    cur = Mysql.connection.cursor()
    cur.execute("select Node1.DATE, Node1.TX, Node1.RSSI, Node1.temperature, Node1.humidity, Node1.co, Node1.co2, Node1.from_node, Node2.DATE, Node2.TX_2, Node2.RSSI_2, Node2.temperature_2, Node2.humidity_2, Node2.co_2, Node2.co2_2, Node2.from_node_2, Node3.DATE, Node3.TX_3, Node3.RSSI_3, Node3.temperature_3, Node3.humidity_3, Node3.co_3, Node3.co2_3, Node3.from_node_3, Node4.DATE, Node4.TX_4, Node4.RSSI_4, Node4.temperature_4, Node4.humidity_4, Node4.co_4, Node4.co2_4, Node4.from_node_4 FROM Node1 INNER JOIN Node2, Node3, Node4")
    data = cur.fetchall()
    cur.close()
    return render_template('database.html', value=data)

@app.route("/login")
def login():
    return render_template("login.html", tittle="data")

@app.route("/logout")
def logout():
    return redirect(url_for("index"))

@app.route("/tabel_login")
def tabel_login():
    cur = Mysql.connection.cursor()
    cur.execute("select Node1.DATE, Node1.TX, Node1.RSSI, Node1.temperature, Node1.humidity, Node1.co, Node1.co2, Node1.from_node, Node2.DATE, Node2.TX_2, Node2.RSSI_2, Node2.temperature_2, Node2.humidity_2, Node2.co_2, Node2.co2_2, Node2.from_node_2, Node3.DATE, Node3.TX_3, Node3.RSSI_3, Node3.temperature_3, Node3.humidity_3, Node3.co_3, Node3.co2_3, Node3.from_node_3, Node4.DATE, Node4.TX_4, Node4.RSSI_4, Node4.temperature_4, Node4.humidity_4, Node4.co_4, Node4.co2_4, Node4.from_node_4 FROM Node1 INNER JOIN Node2, Node3, Node4")
    data = cur.fetchall()
    cur.close()
    return render_template("tabel_login.html", value=data)

@app.route("/checkUser", methods=["POST"])
def check():
    confirm = None
    username = str(request.form["username"])
    password = str(request.form["password"])
    cur = Mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username='" + username + "' and password='" + password + "'")
    data = cur.fetchone()
    
    if data is None:
        
        return (render_template("login.html"))
    else:
        return redirect(url_for("tabel_login"))

@app.route('/delete', methods=['GET','POST'])
def delete():
    cur = Mysql.connection.cursor()
    cur2 = Mysql.connection.cursor()
    cur3 = Mysql.connection.cursor()
    cur4 = Mysql.connection.cursor()
    cur.execute("DELETE FROM Node1")
    cur2.execute("DELETE FROM Node2")
    cur3.execute("DELETE FROM Node3")
    cur4.execute("DELETE FROM Node4")
    Mysql.connection.commit()
    return redirect(url_for('tabel_login'))

if __name__ == "__main__":
    app.secret_key="12345678dailywebcoding"
    app.run(host="localhost", port=5020, debug=True)


