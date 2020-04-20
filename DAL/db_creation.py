from pymongo import MongoClient

dbName = "panda-launder-db"
products = "products"
packages = "packages"
repositories = "repositories"
uri = "mongodb://panda-launder-db:b99muqSYTrNlGrLpC3MZgxSPSk46nDIBx3XFvbCyZLyAtI8by5ILwRbixhRI8bPYw7EsKSd0AueWIBKP6Sl8aw==@panda-launder-db.mongo.cosmos.azure.com:10255/?retryWrites=false&ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@panda-launder-db@"

# connect to db
client = MongoClient(uri)
db = client[dbName]

# collections
packages_col = db[packages]
products_col = db[products]
repo_col = db[repositories]

# create empty collections
db.create_collection(packages)
db.create_collection(products)
# db.create_collection(repositories)

# create and insert data to repos coll
repos = [
    {"type": "vscode"},
    {"type": "npm"}
]
repo_col.insert_many(repos)

# mock data insertion - remove later
packages_data = [
    {
        "name": "react-dom",
        "type": "npm"
    },
    {
        "name": "@material-ui/core",
        "type": "npm"
    },
    {
        "name": "Logstash Editor",
        "type": "vscode"
    },
    {
        "name": "Git Graph",
        "type": "vscode"
    },
]

products_data = [
    {
        "name": "react-dom",
        "version": "16.13.1",
        "downloaded": "20/04/2020 12:51",
        "metatdata": {
            "registry": "https://registry.npmjs.org",
            "os": "",
            "arch": "",
        },
        "package_zip": "Dc5njjAh7P6uDiwoVgyZ"
    },
    {
        "name": "@material-ui/core",
        "version": "4.9.11",
        "downloaded": "20/04/2020 12:51",
        "metatdata": {
            "registry": "https://registry.npmjs.org",
            "os": "",
            "arch": "",
        },
        "package_zip": "Dc5njjAh7P6uDiwoVgyZ"
    },
    {
        "name": "@material-ui/core",
        "version": "3.9.2",
        "downloaded": "20/04/2020 12:51",
        "metatdata": {
            "registry": "http://my-internal-registry.local",
            "os": "",
            "arch": "",
        },
        "package_zip": "xz6oS6lFcpajNURb7yYG"
    },
    {
        "name": "react-dom",
        "version": "15.3.1",
        "downloaded": "20/04/2020 12:51",
        "metatdata": {
            "registry": "https://registry.npmjs.org",
            "os": "",
            "arch": "",
        },
        "package_zip": "xz6oS6lFcpajNURb7yYG"
    },
    {
        "name": "Git Graph",
        "downloaded": "20/04/2020 12:51",
        "metatdata": {
            "registry": "http://my-internal-registry.local",
            "os": "",
            "arch": "",
        },
        "package_zip": "2JpSMyCFrcMLN2qGB9dh"
    },
]

packages_col.insert_many(packages_data)
products_col.insert_many(products_data)

# close connection
client.close()
