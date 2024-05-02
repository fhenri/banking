const axios = require("axios");
const express = require("express");
const FormData = require("form-data");
const fs = require("fs");
const mongoose = require("mongoose");
const path = require("path");

const multipart = require("./multipart");
const Account = require("./models/accounts");
const Category = require("./models/categories");
const Transaction = require("./models/transactions");

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
  const { actDescription, actCurrency, accountId, ...act} = req.body;

  let account = await Account.findById(accountId);
  if (account == null) {
    account = new Account({
      _id: new mongoose.Types.ObjectId(),
      BankName: act.actBankName,
      AccountNumber: act.actNumber,
      Description: actDescription,
      Currency: actCurrency,
    });
  } else {
    account.Currency = actCurrency;
    account.Description = actDescription;
  }
  await account.save();
  res.redirect("/transactions?account=" + account.AccountNumber);
});

app.post("/transactions", async (req, res) => {
  //console.log(req.body)
  const { actId, txId, txComment, delCategory, txNewCategory } = req.body;

  const transaction = await Transaction.findById(txId);
  transaction.Comment = txComment;
  if (delCategory) {
    transaction.Categories.pull(delCategory.trim());
  }
  if (txNewCategory) {
    const existCategory = 
      await Category.findOne({ CategoryName: txNewCategory }).exec();
    if (!existCategory) {
      const newCategory = new Category({
        _id: new mongoose.Types.ObjectId(),
        CategoryName: txNewCategory
      });
      await newCategory.save();
    }

    transaction.Categories.push(txNewCategory);
  }
  await transaction.save();
  
  res.redirect("/transactions?account=" + actId);
});

app.get("/transactions.json", async (req, res) => {
  //const data = [100, 50, 300, 40, 350, 250, 7, 14]; // assuming this is coming from the database
  //res.json(data);
  //res.json({a: 9, b: 20, c:30, d:8, e:12, f:3, g:7, h:14});

  // db.transactions.find({},{ AccountNumber: 1, Categories: { $slice: [0, 1] }, MoneyOut: 1, MoneyIn: 1, _id: 0 })
  const txList = await Transaction.find({}, { AccountNumber: 1, Categories: 1, MoneyOut: 1, MoneyIn: 1, _id: 0 });
  console.log(txList);
})

app.get("/transactions", async (req, res) => {
  const accountList = await Transaction.distinct("AccountNumber");
  const accountSelectedId = req.query.account;

  let queryFilter = {};
  if (accountSelectedId) {
    queryFilter = {
      AccountNumber: accountSelectedId,
    };
  }

  const categoryList = await Category.find({ });

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
    categoryList,
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

app.get("/statement", (req, res) => {
  res.render("bankStatement");
});

var port = process.env.NODE_PORT || 6001;
app.listen(port, () =>
  console.log(`⚡️[bootup]: Server is running at port: ${port}`),
);
