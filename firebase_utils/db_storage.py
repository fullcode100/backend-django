import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join("firebase_utils","perak-peserta-cred.json")

config = {
    "apiKey": "AIzaSyB1XnTyvgkciFtIxqEho4WJm2TxvhIBgA8",
    "authDomain": "perak-peserta.firebaseapp.com",
    "databaseURL": "https://perak-peserta.firebaseio.com",
    "projectId": "perak-peserta",
    "storageBucket": "perak-peserta.appspot.com",
    "messagingSenderId": "531372502220",
    "appId": "1:531372502220:web:dd39a5b778f97d6eb16669"
}

cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
firebase_admin.initialize_app(cred, config)

db = firestore.client()
bucket = storage.bucket()

