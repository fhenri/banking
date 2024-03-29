import csv;
import io;

# global variable definition
rules = {}

def setup_rules_csv():
    with io.open ("categories.csv", "r", encoding="utf-8") as categories_file:
        # create the csv reader
        categories_reader = csv.reader(categories_file, delimiter=',')
        csv_header = next(categories_reader)

        for row in categories_reader:
            cat  = row[1].strip();
            desc = row[0];
            if desc in rules:
                rules[desc] = rules[desc] + [cat];
            else:
                rules[desc] = [cat];

def setup_rules():
    print("setup rules")
    with io.open ("categories.csv", "r", encoding="utf-8") as categories_file:
        # create the csv reader
        categories_reader = csv.reader(categories_file, delimiter=',')
        csv_header = next(categories_reader)

        for row in categories_reader:
            cat  = row[1].strip();
            desc = row[0];
            if desc in rules:
                rules[desc] = rules[desc] + [cat];
            else:
                rules[desc] = [cat];

#def get_category_for_transaction(transaction_elements) -> list[str]:
def get_category_for_transaction(transaction_elements):
    if not rules:
        setup_rules();

    tx_categories = [];

    #categories.append( datetime.strptime(transaction_elements[0], "%d-%b-%Y").year );
    tx_categories.append( transaction_elements[0][-4:] )

    for rule in rules.keys():
        print(f" evaluation {rule} for {transaction_elements[3]}")
        if rule in transaction_elements[3]:
            tx_categories.extend(rules[rule])

    print (tx_categories)
    return tx_categories;
