import invoice;

from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hey Invoice Generation App!'

@app.route("/invoice", methods=["POST"])
def generate_invoice():
    if request.files.get("invoice-file") is None:
        return 'No file provided', 500
    # Put here some other checks (security, file length etc...)
    invoice_file = request.files["invoice-file"];
    invoice_file.save(secure_filename(invoice_file.filename));
    print(f"run invoice generation with {invoice_file.filename}");
    invoice.generate();

    return 'Invoice Generated', 204

if __name__ == "__main__":
    app.run(debug=True)
