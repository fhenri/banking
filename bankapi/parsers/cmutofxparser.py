import io;
import pandas as pd;
import re;

import sys
import os

# getting the name of the directory
# where this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to the sys.path.
sys.path.append(parent)

# now we can import the module in the parent directory.
import trules;
from parsers.bankparser import AbstractBankParser;

from ofxtools.Parser import OFXTree

class CMUTOFXParser(AbstractBankParser):

    '''
        Parse the csv file given by the bank.
    '''
    def parse_file(self, filename):
        print(f"run the cmut parser with file {filename}");
        parser = OFXTree();
        with open(filename, 'rb') as bank_file:
            parser.parse(bank_file);
            ofx = parser.convert()
            all_transactions = [];
            stmts = ofx.statements
            for stmt in stmts:
                account_number = stmt.acctid
                txs = stmt.transactions
                for itx in txs:
                    tx = {};
                    tx["AccountNumber"]    = account_number;
                    tx["TransactionDate"]  = itx.dtposted;
                    tx["ValueDate"]        = itx.dtuser;
                    tx["_id"]              = itx.fitid;
                    tx["Description"]      = itx.name;
                    tx["Comment"]          = "";
                    tx["Categories"]       = trules.get_category_for_transaction(itx.dtposted, itx.name);
                    tx["MoneyOut"]         = -itx.trnamt if itx.trntype=='DEBIT' else 0
                    tx["MoneyIn"]          = itx.trnamt if itx.trntype=='CREDIT' else 0
                    tx["Balance"]          = 0
                    all_transactions.append(tx);

        df = pd.DataFrame(all_transactions);
        df["MoneyOut"]         = df["MoneyOut"].astype(float);
        df["MoneyIn"]          = df["MoneyIn"].astype(float);
        df["Balance"]          = df["Balance"].astype(float);
        return df;
