import mh_z19
import Adafruit_DHT as DHT
import serial
import ast
import time

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
    try:
        co2 = mh_z19.read()
        return co2['co2']
    except:
        return -999

def temprature_humidity():
    try:
        hum, temp = DHT.read_retry(DHT.DHT22, 4)
        res = [temp, hum]
        return res
    except:
        return [-999, -999]

def sensing_data():
    ec_water_temperature_result = ec_water_temperature()
    temprature_humidity_result = temprature_humidity()
    result = {
        'ec': ec_water_temperature_result[0],
        'water_temperature': ec_water_temperature_result[1],
        'co2': co2(),
        'temperature': temprature_humidity_result[0],
        'humidity': temprature_humidity_result[1]
    }
    return result
