import json;
import os;
import transaction;

from bankparser import AbstractBankParser;
from bson import json_util;
from flask import Flask, jsonify, request;
from mongodb import MongoDBConnection;
from werkzeug.utils import secure_filename;

app = Flask(__name__)
client = MongoDBConnection(os.environ.get("MONGODB_ENDPOINT"));

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/')
def hello_world():
    return json.dumps({'message':"Hello Bankers!"}), 200, {'ContentType':'application/json'}

@app.route('/transactions', methods=['GET'])
def  get_transactions():
    items = list(transaction.get_transactions())
    return parse_json(items), 200

@app.route("/loadTransaction", methods=["POST"])
def upload_transaction_file():
    print("calling parse");

    if request.files.get("bank-file") is None:
        return json.dumps({'imported': False, 'error': 'no file provided'}), 500, {'ContentType':'application/json'}
    # Put here some other checks (security, file length etc...)
    bank_file = request.files["bank-file"];
    bank_file_location = os.path.join("./tmp/", secure_filename(bank_file.filename));
    bank_file.save(bank_file_location);
    try:
        args = request.form;
        parser = AbstractBankParser.getParserForBank(args.get('bankname'), args.get('filetype'));
        parser.parse(bank_file_location);
    except Exception as e:
        print(e)
        raise e
        return json.dumps({'imported': False, 'error': str(e)}), 500, {'ContentType':'application/json'}

    return json.dumps({'imported':True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(debug=True)
