import mh_z19
import RPi.GPIO as GPIO
import dht11
import serial
import ast
import time
import datetime
import schedule
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=17)

def firebase_initialize():
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

def ec_water_temperature():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)
        ser.write(str.encode('1'))
        encode_result = ''
        while encode_result == '':
            result = ser.readline()
            encode_result = result.strip().decode('UTF-8')
        dic_result = ast.literal_eval(encode_result)
        ec = dic_result['EC']
        water_temp = dic_result['WaterTemp']
        res = [ec, water_temp]
        return res
    except:
        return [-999, -999]


def co2():
    print('Start co2!!!')
    try:
        co2 = mh_z19.read()
        return co2['co2']
    except:
        return -999


def temprature_humidity():
    try:
        result = instance.read()
        print(result)
        temp = result.temperature
        hum = result.humidity
        res = [temp, hum]
        return res
    except:
        return [-999, -999]


def setData(ec, water_temperature, co2, temperature, humidity):
    date = datetime.datetime.now()
    db = firestore.client()
    ref = db.collection('sensing_data').document(str(date))
    ref.set({
        'EC': ec,
        'WaterTemperature': water_temperature,
        'CO2': co2,
        'Temperature': temperature,
        'Himifity': humidity
    })


def main():
    value1 = ec_water_temperature()
    value2 = temprature_humidity()
    result = {
        'ec': value1[0],
        'water_temperature': value1[1],
        'co2': co2(),
        'temperature': value2[0],
        'humidity': value2[1]
    }
    setData(result['ec'], result['water_temperature'],
            result['co2'], result['temperature'], result['humidity'])
    print(result)


if __name__ == "__main__":
    firebase_initialize()
    schedule.every(1).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)