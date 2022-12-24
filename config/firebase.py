import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initialize():
    cred = credentials.Certificate('./config/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db