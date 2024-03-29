import pymongo;

class MongoDBConnection:

  # class variable __instance will keep track of the lone object instance
  __instance = None

  def __init__(self, app):
    if MongoDBConnection.__instance != None:
      raise Exception("MongoDB Connection already initialized!")
    else:
      if app:
        MongoDBConnection.__instance = pymongo.MongoClient(app.config["MONGO_URI"])["bankdb"]
      else:
        MongoDBConnection.__instance = pymongo.MongoClient('localhost', 27017)["bankdb"]

  @staticmethod
  def getInstance():
    if MongoDBConnection.__instance == None:
      MongoDBConnection(None)
    return MongoDBConnection.__instance
