from config.control_gpio import set_gpio
import time
import datetime
import RPi.GPIO as GPIO

def control(data, db):
    def on_snapshot(snapshot, changes, read_time):
        for doc in snapshot:
            env = {doc.id: doc.to_dict()}
            print('----------------------------------')
            gpio(env, data)

    ref = db.collection(u'control')
    watch = ref.on_snapshot(on_snapshot)
    time.sleep(240)

# 5分毎に監視，on,offを切り替える
def gpio(env, data):
    set_gpio()
    pin = {'heater': 13, 'light': 6, 'fertilizer':5, 'fan': 0}
    # fan
    if 'fan' in env:
        if data['co2'] <= env['fan']['min_co2']:
            GPIO.output(pin['fan'], 0)
            print('fan: off')
        elif data['co2'] >= env['fan']['max_co2']:
            GPIO.output(pin['fan'], 1)
            print('fan: on')

    # fertilizer
    if 'fertilizer' in env:
        if data['ec'] <= env['fertilizer']['min_ec']:
            print('fertilizer: on')
            GPIO.output(pin['fertilizer'], 1)
            time.sleep(5)
            GPIO.output(pin['fertilizer'], 0)
        else:
            print('fertilizer: off')

    # heater
    if 'heater' in env:
        if data['water_temperature'] <= env['heater']['min_w_temp']:
            print('heater: on')
            GPIO.output(pin['heater'], 1)
        elif data['water_temperature'] >= env['heater']['max_w_temp']:
            print('heater: off')
            GPIO.output(pin['heater'], 0)

    # light
    if 'light' in env:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        start_time = [int(n) for n in env['light']['start_time'].split(':')]
        end_time = [int(n) for n in env['light']['end_time'].split(':')]

        if (hour == end_time[0] and minute >= end_time[1]) or hour > end_time[0]:
            print('light: off')
            GPIO.output(pin['light'], 0)
        elif (hour == start_time[0] and minute >= start_time[1]) or hour > start_time[0]:
            print('light: on')
            GPIO.output(pin['light'], 1)

