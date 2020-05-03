from pymongo import MongoClient

dbName = "panda-launder-db"
uri = "mongodb+srv://Guinness1759:gsn,h1759@guinness1759-lga2g.mongodb.net/test?retryWrites=true&w=majority"

# connect to db
client = MongoClient(uri)
db = client[dbName]

# collections
packages_col = db["packages"]
products_col = db["products"]
providers_col = db["providers"]

def get_providers():
    return query_obj_to_arr(providers_col.find({}, {"_id": 0}))

def get_packages_by_provider(provider):
    return query_obj_to_arr(packages_col.find({"type": provider}, {"_id": 0}))

def query_obj_to_arr(query_obj):
    result_arr = []
    for document in query_obj:
        result_arr.append(document)
    return result_arr
    
client.close()