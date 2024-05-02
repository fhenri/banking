import json;

# global variable definition
config = {}

def setup_config():
    parser_configs = json.load(open("resources/parser.config.json", 'r'));
    for cfg in parser_configs:
        config[f"{cfg['alias']}-{cfg['file']}"] = { "parser": cfg['parser'], "class": cfg['class']};


def get_config(bankalias, filetype):
    if not config:
        setup_config();

    ckey = f"{bankalias}-{filetype}";
    return config[ckey]['parser'], config[ckey]['class'];
