#parser.py
from pyjsparser import PyJsParser
import json
import os

def setJson(dic, fn, msg):
    print(msg)
    with open(fn, 'w') as f:
        json.dump(dic, f)
        f.close()

def getJson(fn, msg):
    try:
    ## Reading data back
        with open(fn, 'r') as f:
            data = json.load(f)
            f.close()
            return data
    except:
        setJson({}, fn, msg)
        return {}

## Read/Write contract information file
def save_contract():
    smart_contract = getJson('parsed_contract.json', 'Creating parsed_contract.json')
    name = server_name
    server_info[name] = {
        "ip": host,
        "port": port
    }
    setJson(smart_contract, 'parsed_contract.json', 'Saving contract to parsed_contract.json')


def get_file():
    #read file from from folder
    #convert parts to JS (ie. uid = var)
    #run through parser
    print('')

def parse(source):
    print("------------------------------------------------------------------")
    print("")
    print("parsing...")
    p = PyJsParser()
    # source = json.load(open('data.json'))
    contract_parsed = p.parse(source)
    print("------------------------------ submited ------------------------------------")
    print("")
    print(contract_parsed)
    print("")
    print("-------------------------------- source ----------------------------------")
    print("")
    print(source)
    print("")
    print("---------------------------- comparison test --------------------------------------")
    print("")
    print(p.parse('var TEST =99;'))
    print("")
    print("------------------------------------------------------------------")
    # return contract_parsed
    test = "You submited:"
    return test
