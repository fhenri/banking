const mongoose = require("mongoose");

const categorySchema = new mongoose.Schema({
  _id: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
  },
  CategoryName: {
    type: String,
    required: true,
  }
});

const Category = mongoose.model("Category", categorySchema);

module.exports = Category;
