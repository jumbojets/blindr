from models import PermanentStorage, TemporaryStorage
from flask import current_app as app
import requests
from decouple import config

CESS_URL="http://localhost:9000"

def store_in_cess(constraints_hash, private, public):
    cess_url = CESS_URL

    res = requests.post(cess_url + '/upload-file', json={'constraints_hash': constraints_hash, 'private': private, 'public': public})
    res.raise_for_status()

    print('file hash is :' + res.json()["file_hash"])
    file_hash = res.json()["file_hash"]
    return file_hash


def delete_from_cess(file_hash):
    cess_url = CESS_URL
    res = requests.delete(cess_url + f'/delete-file/{file_hash}')
    res.raise_for_status()
    return True

def get_from_cess(file_hash):
    cess_url = CESS_URL
    res = requests.get(cess_url + f'/download-file/{file_hash}')
    res.raise_for_status()
    
    return res.json()


def store_permanent(constraints_hash, private_key, public_key):
    file_hash = store_in_cess(constraints_hash, private_key, public_key)
    new_entry = PermanentStorage(constraints_hash=constraints_hash, private_key=private_key, public_key=public_key, file_hash=file_hash)
    app.db.session.add(new_entry)
    app.db.session.commit()
    return True

def store_temporary(constraints_hash, private_value, public_value):
    file_hash = store_in_cess(constraints_hash, private_value, public_value)
    new_entry = TemporaryStorage(constraints_hash=constraints_hash, private_value=private_value, public_value=public_value, file_hash=file_hash)
    app.db.session.add(new_entry)
    app.db.session.commit()
    return True

def delete_temporary(constraints_hash):
    entry = TemporaryStorage.query.filter_by(constraints_hash=constraints_hash).first()
    # delete_from_cess(entry.file_hash)
    app.db.session.delete(entry)
    app.db.session.commit()
    return True

def delete_permanent(constraints_hash):
    entry = PermanentStorage.query.filter_by(constraints_hash=constraints_hash).first()
    # delete_from_cess(entry.file_hash)
    app.db.session.delete(entry)
    app.db.session.commit()
    return True

def find_permanent(constraints_hash):
    entry = PermanentStorage.query.filter_by(constraints_hash=constraints_hash).first()
    return entry

def find_temporary(constraints_hash):
    entry = TemporaryStorage.query.filter_by(constraints_hash=constraints_hash).first()
    return entry