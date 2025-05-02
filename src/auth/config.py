import firebase_admin  # type:ignore[import]
from firebase_admin import credentials  # type:ignore[import]


def init_firebase():
    print("Initializing Firebase")
    cred = credentials.Certificate("firebaseConfig.json")
    firebase_admin.initialize_app(cred)  # type:ignore[no-untyped-call]
