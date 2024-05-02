import csv;
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

class MCBCSVParser(AbstractBankParser):

    def parse_line (self, pattern, text) -> str:
        found = re.search(pattern, text);
        if found:
            return found.group(1).rstrip();
        return '';

    '''
        Parse the csv file given by the bank.
    '''
    def parse_file(self, filename):
        print(f"run the MCB parser with file {filename}");
        with io.open (filename, "r", encoding="utf-8") as bank_file:
            # create the csv reader and filter blank lines
            bank_reader = csv.reader(filter(lambda line: line.strip(), bank_file), delimiter=',' )

            # MCB really sucks with their csv export (but does so with ofx so csv still better)
            # need to skip line by line
            account_number   = self.parse_line('Account Number (\\d+)', next(bank_reader)[0])
            account_currency = next(bank_reader)
            opening_balance  = next(bank_reader)
            closing_balance  = next(bank_reader)
            period           = next(bank_reader)

            # grab the first row and keep as header references
            # ['Transaction Date', 'Value Date', 'Reference', 'Description', 'Money out', 'Money in', 'Balance ']
            csv_header = next(bank_reader)

            all_transactions = [];
            for row in bank_reader:
                tx = {};
                try:
                    tx["AccountNumber"]    = account_number;
                    tx["TransactionDate"]  = row[0];
                    tx["ValueDate"]        = row[1];
                    # we need to build an id - standing order for MCB are not 
                    # generic term repeating
                    tx["_id"]              = f"{row[2]}-{row[6]}";
                    tx["Description"]      = row[3];
                    tx["Comment"]          = "";
                    #tx["Categories"]       = trules.get_category_for_transaction(row[3]);
                    tx["Categories"]       = trules.get_category_for_transaction(row[0], row[3]);
                    tx["MoneyOut"]         = row[4].replace(',', '');
                    tx["MoneyIn"]          = row[5].replace(',', '');
                    tx["Balance"]          = row[6].replace(',', '');
                    all_transactions.append(tx);
                except Exception as e:
                    print(e);

            # using pandas to fix bunch of issues
            # - convert data into expected
            # - be able to insert many in mongo
            # - run analysis
            df = pd.DataFrame(all_transactions);
            df["TransactionDate"]  = pd.to_datetime(df["TransactionDate"], format="%d-%b-%Y");
            df["ValueDate"]        = pd.to_datetime(df["ValueDate"], format="%d-%b-%Y");
            df["MoneyOut"]         = df["MoneyOut"].astype(float);
            df["MoneyIn"]          = df["MoneyIn"].astype(float);
            df["Balance"]          = df["Balance"].astype(float);

            #df = df.assign(Categories = lambda x: (x["TransactionDate"].year))
            return df;
