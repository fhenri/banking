const mongoose = require("mongoose");

const transactionSchema = new mongoose.Schema({
  _id: {
    type: String,
    required: true,
  },
  AccountNumber: {
    type: String,
    required: true,
  },
  Description: String,
  Comment: String,
  TransactionDate: {
    type: Date,
    required: true,
  },
  ValueDate: {
    type: Date,
    required: true,
  },
  MoneyOut: {
    type: Number,
    required: true,
    min: 0,
  },
  MoneyIn: {
    type: Number,
    required: true,
    min: 0,
  },
  Balance: {
    type: Number,
    required: true,
    min: 0,
  },
  Categories: [String],
});

// Define a virtual field to retrieve
// the user's full name
transactionSchema.virtual("Amount").get(function () {
  if (this.MoneyOut > 0) {
    return -this.MoneyOut;
  } else {
    return this.MoneyIn;
  }
});

const Transaction = mongoose.model("Transaction", transactionSchema);

module.exports = Transaction;
