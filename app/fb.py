import pyrebase

def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

def fetch_last(db, collection, n=20):
    objects = db.child(collection).order_by_key().limit_to_last(n).get()
    # print("Objects are", [i.val() for i in objects.each()])
    return objects
