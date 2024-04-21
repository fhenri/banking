import csv;
import io;
import datetime;
from mongodb import MongoDBConnection;
import pymongo;

# global variable definition
rules = {}

# The `rules` dictionary is structured to map transaction descriptions to their corresponding categories.
# Each key in the dictionary represents a transaction description in uppercase, 
# and its value is a list of categories associated with that description.
# This structure allows for efficient lookup of categories based on transaction descriptions.
def setup_rules():
    categories_list = [];
    with io.open ("resources/categories.csv", "r", encoding="utf-8") as categories_file:
        # create the csv reader
        categories_reader = csv.reader(categories_file, delimiter=',')
        csv_header = next(categories_reader)

        for row in categories_reader:
            cat  = row[1].strip();
            categories_list.append(cat.lower()) if cat.lower() not in categories_list else None
            desc = row[0].upper();
            if desc in rules:
                rules[desc] = rules[desc] + [cat];
            else:
                rules[desc] = [cat];

    # add all categories to mongodb
    db = MongoDBConnection.getInstance();
    try:
        for category in categories_list:
            # upsert category (ie create if it does not exist)
            db.categories.update_one(
                {"CategoryName": category},
                {'$set':{'CategoryName': category}},
                upsert=True
            )
    except pymongo.errors.BulkWriteError as bwe:
        print(bwe)
        raise


#def get_category_for_transaction(transaction_elements) -> list[str]:
def get_category_for_transaction(tx_date, tx_description):
    if not rules:
        setup_rules();

    tx_categories = [];

    #print(f"{tx_date} - type : {type(tx_date)}")
    match tx_date:
        case str():
            tx_categories.append( tx_date[-4:] );
        case datetime.datetime():
            tx_categories.append( tx_date.year );

    for rule in rules.keys():
        if rule in tx_description.upper():
            # we can have multiple categories set for a rule
            # so need to make sure not to add duplicate
            tx_categories.extend(cat for cat in rules[rule]  if cat not in tx_categories)

    return tx_categories;
