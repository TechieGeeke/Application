from pymongo import MongoClient

mongourl = "mongodb+srv://akakak:akakak@cluster0.b6pgq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongourl)
dbname = client['vortex']
collection_name = dbname['login']

def adduser(dict):
    #make sure no usernames are repeated
    try:
        collection_name.insert_many([dict])
        return True
    except Exception as err:
        return err

def fetch(category, name):
    item_details = collection_name.find({category : name})
    items = {}
    for item in item_details:
        items.update(item)
    else:
        if items != {}:
            return items
        else:
            return False

def auth(user, passw):
    a = fetch('username',f'{user}')
    if a == False:
        return False
    else:
        if a['password'] == str(passw):
            return True
        else: return False

        

