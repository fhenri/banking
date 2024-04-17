import csv;
import io;
import datetime;

# global variable definition
rules = {}

def setup_rules():
    with io.open ("resources/categories.csv", "r", encoding="utf-8") as categories_file:
        # create the csv reader
        categories_reader = csv.reader(categories_file, delimiter=',')
        csv_header = next(categories_reader)

        for row in categories_reader:
            cat  = row[1].strip();
            desc = row[0].upper();
            if desc in rules:
                rules[desc] = rules[desc] + [cat];
            else:
                rules[desc] = [cat];

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
