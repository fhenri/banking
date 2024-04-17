const fs = require("fs");
/*
class PrivateParser {
  constructor() {
    console.log("creating parser");
    let parserList;
    try {
      parserList = JSON.parse(fs.readFileSync("./bankres/parser.config.json"));
    } catch (err) {
      // made for local tests
      parserList = JSON.parse(`[
          {
            "bank": "Crédit Mutuel",
            "alias": "cmut",
            "file": "ofx",
            "parser": "parsers.cmutofxparser",
            "class": "CMUTOFXParser"
          },
          {
            "bank": "Mauritius Commercial Bank",
            "alias": "mcb",
            "file": "csv",
            "parser": "parsers.mcbcsvparser.py",
            "class": "MCBCSVParser"
          }
        ]`);
    }

    this.parsers = new Map();
    parserList.forEach((parser) => {
      this.parsers.set(`${parser.bank} - ${parser.file}`, {
        name: parser.alias,
        file: parser.file,
      });
    });
  }
}

class Parser {
  constructor() {
    throw new Error("Use Singleton.getInstance()");
  }
  static getInstance() {
    if (!Parser.instance) {
      Parser.instance = new PrivateParser();
    }
    return Parser.instance;
  }
}
module.exports = Parser;
*/

class Parser {
  constructor() {
    let parserList;
    try {
      parserList = JSON.parse(fs.readFileSync("./bankres/parser.config.json"));
    } catch (err) {
      // made for local tests
      parserList = JSON.parse(`[
          {
            "bank": "Crédit Mutuel",
            "alias": "cmut",
            "file": "ofx",
            "parser": "parsers.cmutofxparser",
            "class": "CMUTOFXParser"
          },
          {
            "bank": "Mauritius Commercial Bank",
            "alias": "mcb",
            "file": "csv",
            "parser": "parsers.mcbcsvparser.py",
            "class": "MCBCSVParser"
          }
        ]`);
    }

    this.parsers = new Map();
    parserList.forEach((parser) => {
      this.parsers.set(`${parser.bank} - ${parser.file}`, {
        name: parser.alias,
        file: parser.file,
      });
    });
  }
}

module.exports = new Parser();
