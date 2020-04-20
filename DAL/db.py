from pymongo import MongoClient

dbName = "panda-launder-db"
uri = "mongodb://panda-launder-db:b99muqSYTrNlGrLpC3MZgxSPSk46nDIBx3XFvbCyZLyAtI8by5ILwRbixhRI8bPYw7EsKSd0AueWIBKP6Sl8aw==@panda-launder-db.mongo.cosmos.azure.com:10255/?retryWrites=false&ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@panda-launder-db@"

# connect to db
client = MongoClient(uri)
db = client[dbName]

# collections
packages_col = db["packages"]
products_col = db["products"]
repo_col = db["repositories"]


def add_packages(packages):
    packages_col.insert_many(packages)

def remove_packages(packages):
    if packages != {}:
        packages_col.delete_many(packages)

def get_packages(name = None, type = None):
    """ 
    Gets all packages by name and type filter, if not provided
    then returns all packages.

    Parameters: 
        name (str array): Array of package's names. 
        type (str array): Array of package's types. 
        
    Returns: 
        
    """
    packages = None
    if name and type:
        packages = packages_col.find({"name": name, "type": type})
    elif name:
        packages = packages_col.find({"name": name})
    elif type:
        packages = packages_col.find({"type": type})
    else:
        packages = packages_col.find()
    return packages

def get_all_repos_types():
  return repo_col.find()

def add_products(products):
    packages_col.insert_many(products)

def remove_products(products):
    if products != {}:
        packages_col.remove_many(products)

def find_products(filter_query = {}):
    return products_col.find(filter_query)
    