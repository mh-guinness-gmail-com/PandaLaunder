from pymongo import MongoClient

dbName = "panda-launder-db"
products = "products"
packages = "packages"
providers = "providers"
uri = "mongodb+srv://Guinness1759:gsn,h1759@guinness1759-lga2g.mongodb.net/test?retryWrites=true&w=majority"

# connect to db
client = MongoClient(uri)
db = client[dbName]

# collections
packages_col = db[packages]
products_col = db[products]
providers_col = db[providers]

# create empty collections
db.create_collection(packages)
db.create_collection(products)
# db.create_collection(providers)

# create and insert data to repos coll
providers = [
    {"name": "vscode", "products": "vscode extensions",},
    {"name": "npm", "products": "npm packages",}
]
providers_col.insert_many(providers)

# close connection
client.close()
