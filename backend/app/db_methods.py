from models import PermanentStorage, TemporaryStorage
from flask import current_app as app


def store_permanent(constraints_hash, private_key, public_key):
    new_entry = PermanentStorage(constraints_hash=constraints_hash, private_key=private_key, public_key=public_key)
    app.db.session.add(new_entry)
    app.db.session.commit()
    return True

def store_temporary(constraints_hash, private_value, public_value):
    new_entry = TemporaryStorage(constraints_hash=constraints_hash, private_value=private_value, public_value=public_value)
    app.db.session.add(new_entry)
    app.db.session.commit()
    return True

def delete_temporary(constraints_hash):
    entry = TemporaryStorage.query.filter_by(constraints_hash=constraints_hash).first()
    app.db.session.delete(entry)
    app.db.session.commit()
    return True

def find_permanent(constraints_hash):
    entry = PermanentStorage.query.filter_by(constraints_hash=constraints_hash).first()
    return entry

def find_temporary(constraints_hash):
    entry = TemporaryStorage.query.filter_by(constraints_hash=constraints_hash).first()
    return entry