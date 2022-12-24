import datetime

def push(sensing_data, db):
    now_date = datetime.datetime.now()
    date = now_date.strftime('%Y-%m-%d')
    time = now_date.strftime('%H:%M')
    data = {
        u'time': time,
        u'ec': sensing_data['ec'],
        u'water_temperature': sensing_data['water_temperature'],
        u'co2': sensing_data['co2'],
        u'temperature': sensing_data['temperature'],
        u'humidity': sensing_data['humidity']
    }

    sensing_data_ref = db.collection('sensing_data').document(
        date).collection('time').document(time).set(data)
