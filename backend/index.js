const axios = require("axios");
const express = require("express");
const FormData = require("form-data");
const fs = require("fs");
const mongoose = require("mongoose");
const path = require("path");

const multipart = require("./multipart");
const Transaction = require("./models/transactions");
const Account = require("./models/accounts");

const parsers = require("./parserconf");

const app = express();
const mongoDbUrl = process.env.MONGODB_ENDPOINT;

mongoose
  .connect(mongoDbUrl)
  .then(() => {
    console.log(`Mongo connection open to ${mongoDbUrl}`);
  })
  .catch((err) => {
    console.log(`Cannot open Mongo connection to ${mongoDbUrl}`);
    console.log(err);
  });

/*
const files = fs.readdirSync("invoicedata");
console.log(files);
*/

app.use(express.urlencoded({ extended: true }));
//app.use(express.json());

app.use(express.static(path.join(__dirname, "public")));

app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.redirect("/transactions");
});

app.post("/accounts", async (req, res) => {
  const accountId = req.body.actId;

  let account = await Account.findById(accountId);
  if (account == null) {
    account = new Account({
      _id: new mongoose.Types.ObjectId(),
      BankName: req.body.actBankName,
      AccountNumber: req.body.actNumber,
      Description: req.body.actDescription,
      Currency: req.body.actCurrency,
    });
  } else {
    account.Currency = req.body.actCurrency;
    account.Description = req.body.actDescription;
  }
  await account.save();
  res.redirect("/transactions?account=" + account.AccountNumber);
});

app.post("/transactions", async (req, res) => {
  const accountId = req.body.actId;
  const transaction = await Transaction.findById(req.body.txId);
  transaction.Comment = req.body.txComment;
  if (req.body.txNewCategory) {
    transaction.Categories.push(req.body.txNewCategory);
  }
  await transaction.save();
  res.redirect("/transactions?account=" + accountId);
});

app.get("/transactions", async (req, res) => {
  const accountList = await Transaction.distinct("AccountNumber");
  const accountSelectedId = req.query.account;

  let queryFilter = {};
  if (accountSelectedId) {
    queryFilter = {
      AccountNumber: accountSelectedId,
    };
  }

  const accountSelected = await Account.findOne({
    AccountNumber: accountSelectedId,
  });

  const transactionList = await Transaction.find(queryFilter).sort({
    TransactionDate: "desc",
  });
  //const resp = await fetch("http://bankapi:5000/transactions");
  //const transactionList = await resp.json();
  //console.log(transactionList);

  res.render("transactions", {
    accountList,
    accountSelected,
    accountSelectedId,
    transactionList,
    parserNames: parsers.parsers.keys(),
  });
});

app.post(
  "/transactions/import",
  multipart.single("txFile"),
  async (req, res) => {
    console.log(`Loading bank transactions with ${req.file.path}`);

    const formData = new FormData();
    formData.append("bank-file", fs.createReadStream(req.file.path));
    const parser = parsers.parsers.get(req.body.txName);
    formData.append("bankname", parser.name);
    formData.append("filetype", parser.file);

    try {
      const fileResp = await axios.post(
        "http://bankapi:5000/loadTransaction",
        formData,
        {
          headers: {
            "Content-Type": `multipart/form-data; boundary=${formData._boundary}`,
          },
        },
      );

      console.log(fileResp);
      data = await fileResp.json();
      console.log(data);
    } catch (err) {
      if (err.response) {
        console.log("err->", err.response.data);
      } else {
        console.log("err->", err);
      }
      return res.redirect("/transactions"); // TODO add error message
    }

    /*
      //const resp = await fetch("http://bankapi:5000/loadTransaction", {
      const resp = await fetch("http://127.0.0.1:5000/loadTransaction", {
        method: "POST",
        headers: {
          "Content-Type": `multipart/form-data; boundary=${formData._boundary}`,
        },
        body: formData,
      });
      */
    res.redirect("/transactions");
  },
);

app.get("/analysis", (req, res) => {
  res.render("analysis");
});

app.get("/invoice", (req, res) => {
  res.render("invoice");
});

var port = process.env.NODE_PORT || 6001;
app.listen(port, () =>
  console.log(`⚡️[bootup]: Server is running at port: ${port}`),
);
