from mongodb import MongoDBConnection;
import pymongo;


def save_transactions(transactions):
    print("save transactions")
    db = MongoDBConnection.getInstance();
    try:
        db.transactions.insert_many(transactions.to_dict('records'))
        print("saved")
        return None
        #transaction_collection.insert_many(transactions)
    except pymongo.errors.BulkWriteError as bwe:
        print(bwe)
        raise

def get_transactions():
    db = MongoDBConnection.getInstance();
    #transaction_collection = db["transactions"]
    return db.transactions.find();
