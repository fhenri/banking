import csv;
import io;
import pandas as pd;
import re;
import trules;
import transaction;

from datetime import datetime
from mongodb import MongoDBConnection

def parse_line (pattern, text) -> str:
    found = re.search(pattern, text);
    if found:
        return found.group(1).rstrip();
    return '';

'''
    Parse the csv file given by the bank.
'''
def parse_file(filename):
    print(f"run the parser with file {filename}");
    with io.open (filename, "r", encoding="utf-8") as bank_file:
        # create the csv reader and filter blank lines
        bank_reader = csv.reader(filter(lambda line: line.strip(), bank_file), delimiter=',' )

        # MCB really sucks with their csv export (but does so with ofx so csv still better)
        # need to skip line by line
        account_number   = parse_line('Account Number (\\d+)', next(bank_reader)[0])
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
                tx["_id"]              = row[2];
                tx["Description"]      = row[3];
                tx["Comments"]         = "";
                tx["Categories"]       = trules.get_category_for_transaction(row);
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

def parse(filename):
    df_transactions = parse_file(filename);
    transaction.save_transactions(df_transactions);

def main():
    client = MongoDBConnection(None);
    #trules.setup_rules();
    parse('1181583_SRReport_1711609254045.CSV');

if __name__ == "__main__":
    print("running bank parser");
    main();
