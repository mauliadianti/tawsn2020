import os
import json
import serial
import mysql.connector

def begin_mysql_connection():
    conn = mysql.connector.connect(host='localhost',database='monitoringdb',user='tajsn2020',password='tajsn2020')
    return conn

def begin_serial():
    try:
        ser = serial.Serial('/dev/ttyUSB0',baudrate=9600, timeout=1.0)
    except:
        ser = serial.Serial('/dev/ttyUSB1',baudrate=9600, timeout=1.0)
    return ser

def process_json(jsondata):
    try:
        data = json.loads(jsondata)
        return (data["TX"], data["RSSI"], data["temperature"], data["humidity"], data["co"], data["co2"], data["TX_2"], data["RSSI_2"], data["temperature_2"], data["humidity_2"], data["co_2"], data["co2_2"], data["TX_3"], data["RSSI_3"], data["temperature_3"], data["humidity_3"], data["co_3"], data["co2_3"], data["TX_4"], data["RSSI_4"], data["temperature_4"], data["humidity_4"], data["co_4"], data["co2_4"], data["fusi_temperature"], data["fusi_humidity"], data["fusi_co"], data["fusi_co2"], data["Kualitas_udara"])
    except:
        pass

def save_to_db(conn, TX, RSSI, temperature, humidity, co, co2):
    args = (TX, RSSI, temperature, humidity, co, co2)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Node1(TX, RSSI, temperature, humidity, co, co2, from_node) VALUES(%s, %s, %s, %s, %s, %s, 1)", args)
    conn.commit()
    
def save_to_db2(conn, TX_2, RSSI_2, temperature_2, humidity_2, co_2, co2_2):
    args2 = (TX_2, RSSI_2, temperature_2, humidity_2, co_2, co2_2)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Node2(TX_2, RSSI_2, temperature_2, humidity_2, co_2, co2_2, from_node_2) VALUES(%s, %s, %s, %s, %s, %s, 2)", args2)
    conn.commit()
    
def save_to_db3(conn, TX_3, RSSI_3, temperature_3, humidity_3, co_3, co2_3):
    args3 = (TX_3, RSSI_3, temperature_3, humidity_3, co_3, co2_3)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Node3(TX_3, RSSI_3, temperature_3, humidity_3, co_3, co2_3, from_node_3) VALUES(%s, %s, %s, %s, %s, %s, 3)", args3)
    conn.commit()
    
def save_to_db4(conn, TX_4, RSSI_4, temperature_4, humidity_4, co_4, co2_4):
    args4= (TX_4, RSSI_4, temperature_4, humidity_4, co_4, co2_4)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Node4(TX_4, RSSI_4, temperature_4, humidity_4, co_4, co2_4, from_node_4) VALUES(%s, %s, %s, %s, %s, %s, 4)", args4)
    conn.commit()
    
def save_to_db5(conn, fusi_temperature, fusi_humidity, fusi_co, fusi_co2, Kualitas_udara):
    args5 = (fusi_temperature, fusi_humidity, fusi_co, fusi_co2, Kualitas_udara)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fusi(fusi_temperature, fusi_humidity, fusi_co, fusi_co2, Kualitas_udara) VALUES(%s, %s, %s, %s, %s)", args5)
    conn.commit()
 
def main():
    ser = begin_serial()
    conn = begin_mysql_connection()

    while True:
        jsondata = ser.readline().decode("utf-8")
        if jsondata !='':
            TX, RSSI, temperature, humidity, co, co2, TX_2, RSSI_2, temperature_2, humidity_2, co_2, co2_2, TX_3, RSSI_3, temperature_3, humidity_3, co_3, co2_3, TX_4, RSSI_4, temperature_4, humidity_4, co_4, co2_4, fusi_temperature, fusi_humidity, fusi_co, fusi_co2, Kualitas_udara = process_json(jsondata)
            #print(jsondata)
            save_to_db(conn, TX, RSSI, temperature, humidity, co, co2)
            save_to_db2(conn, TX_2, RSSI_2, temperature_2, humidity_2, co_2, co2_2)
            save_to_db3(conn, TX_3, RSSI_3, temperature_3, humidity_3, co_3, co2_3)
            save_to_db4(conn, TX_4, RSSI_4, temperature_4, humidity_4, co_4, co2_4)
            save_to_db5(conn, fusi_temperature, fusi_humidity, fusi_co, fusi_co2, Kualitas_udara)
            
            print (TX, RSSI, temperature, humidity, co, co2)
            print (TX_2, RSSI_2, temperature_2, humidity_2, co_2, co2_2)
            print (TX_3, RSSI_3, temperature_3, humidity_3, co_3, co2_3)
            print (TX_4, RSSI_4, temperature_4, humidity_4, co_4, co2_4)
            print ("{Fusi Temperature = ",fusi_temperature, "}", "{Fusi Humidity = ",fusi_humidity, "}","{Fusi co = ",fusi_co, "}", "{Fusi co2 = ",fusi_co2, "}" "{Kualitas_udara = ",Kualitas_udara, "}")           
            print("")

if __name__ == '__main__':
    main()
