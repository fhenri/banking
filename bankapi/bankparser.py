import abc
import importlib
import json;
import sys;
import parserconfig;
import transaction;

class AbstractBankParser():

    @staticmethod
    def getParserForBank(bankalias, filetype) -> 'AbstractBankParser':
        parser, pclass = parserconfig.get_config(bankalias, filetype);
        MyClass = getattr(importlib.import_module(parser), pclass)
        return MyClass()

    @abc.abstractmethod
    def parse_file(self, filename):
        """ Implement me! """
        pass

    def parse(self, filename):
        df_transactions = self.parse_file(filename);
        if not df_transactions.empty:
            print("importing data in mongodb");
            transaction.save_transactions(df_transactions);


def main():
    bank_filename = sys.argv[1];
    bank_alias = sys.argv[2];
    file_type = sys.argv[3];
    parser = AbstractBankParser.getParserForBank(bank_alias, file_type);
    parser.parse(bank_filename);

if __name__ == "__main__":
    print("running bank parser");
    main();
