const mongoose = require("mongoose");

const accountSchema = new mongoose.Schema({
  _id: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
  },
  BankName: {
    type: String,
    required: true,
  },
  AccountNumber: {
    type: String,
    required: true,
  },
  Description: String,
  Currency: String,
});

const Account = mongoose.model("Account", accountSchema);

module.exports = Account;
