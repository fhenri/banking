import json
import os
import transaction
import bankparser

from flask import Flask, jsonify, request, render_template
from mongodb import MongoDBConnection;
from werkzeug.utils import secure_filename

MONGODB_URI = os.environ.get("MONGODB_ENDPOINT")

app = Flask(__name__)
app.config["MONGO_URI"] = MONGODB_URI
client = MongoDBConnection(app);

@app.route('/')
def hello_world():
    return 'Hey Banking App!'

@app.route('/transactions', methods=['GET'])
def  get_transactions():
 return list(transaction.get_transactions());

@app.route("/loadTransaction", methods=["POST"])
def upload_transaction_file():
    print("calling parse");
    if request.files.get("bank-file") is None:
        return render_template("my_error_page.html", an_optional_message="Error uploading file");
    # Put here some other checks (security, file length etc...)
    bank_file = request.files["bank-file"];
    bank_file.save(secure_filename(bank_file.filename));
    bankparser.parse(bank_file.filename);

    return 'imported'

if __name__ == "__main__":
    app.run(debug=True)
