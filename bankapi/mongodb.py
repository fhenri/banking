import os;
import pymongo;

'''
    Singleton class to maintain connection with the database
'''
class MongoDBConnection:

  # class variable __instance will keep track of the lone object instance
  __instance = None

  def __init__(self, uri):
    if MongoDBConnection.__instance != None:
      raise Exception("MongoDB Connection already initialized!")
    else:
      if not uri:
        uri = os.environ.get("MONGODB_ENDPOINT");
      MongoDBConnection.__instance = pymongo.MongoClient(uri)["bankdb"]

  @staticmethod
  def getInstance():
    if MongoDBConnection.__instance == None:
      MongoDBConnection(None)
    return MongoDBConnection.__instance
