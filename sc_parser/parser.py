#parser.py
# from pyjsparser import PyJsParser
import json
import os

msg = {
'solidiy_checker':[
    'Solidity declared correctly.',
    'Solidity version is wrong.',
    'Solidity decleration is missing or wrong! ie."pragma solidiy ^0.4.0"'
    ],
'test':[
    'this is a test',
    'this is a test 2'
    ]
}

assignment_operators = ['=', '|=', '^=', '&=', '<<=', '>>=', '+=', '-=', '*=', '/=', '%=']

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
    smart_contract = getJson('smart_contract.json', 'Creating smart_contract.json')
    setJson(smart_contract, 'smart_contract.json', 'Saving contract to smart_contract.json')


def check_solidity_decleration(param, checker):
    print("------------------------------------------------------------------")
    print('Checking solidity validity:')
    if param[0:3] == ['pragma','solidity','^0.4.19;']:
        checker = 0
        print('check_solidity : checker is', checker)
        return checker
    if param[0:2] == ['pragma','solidity'] and param[2] != ['^0.4.19;']:
        checker = 1
        # print('Solidity version is wrong')
        print('check_solidity : checker is', checker)
        return checker
    else:
        checker = 2
        # print('Solidity decleration is missing ie."pragma solidiy ^0.4.0"')
        print('check_solidity : checker is', checker)
        return checker

def check_solidity(param):
    try:
        split_data = param
        does_it_pass = None
        does_it_pass = check_solidity_decleration(split_data, does_it_pass)
        print(does_it_pass)
        if does_it_pass == 0:
            print(msg['solidiy_checker'][does_it_pass])
            return 'SLD_declared'
        if does_it_pass == 1:
            print(msg['solidiy_checker'][does_it_pass])
            return 'SLD_version'
        if does_it_pass != 0 and 1:
            print(msg['solidiy_checker'][does_it_pass])
            return 'SLD_alert'
    except:
        print(msg[3])
        return 'SLD_alert'

def check_TOD(param):
    print("------------------------------------------------------------------")
    print('Checking Transaction Order Dependence:')
    print(assignment_operators)
    for i in assignment_operators:
        print(i)
        print(param)
        if i in param:
            if 'revert();' in param or 'throw();' in param:
                return 'NO_TOD'
            else:
                return 'TOD_alert'
        else:
            return 'NO_TOD'
    # 'if(msg.sender != owner) { revert(); }'

def check_TSD(param):
    print("------------------------------------------------------------------")
    print('Checking Timestamp Dependence:')
    for i, j in enumerate(param):
        if any("block.timestamp" in j for i in param):
            return 'TSD_alert'
    for i in param:
        if 'timestamp' in param or 'block.timestamp' in param or 'now' in param:
            return 'TSD_alert'
        else:
            return 'NO_TSD'

def check_MHE(param, param_list):
    print("------------------------------------------------------------------")
    print('Checking Mishandled Exceptions:')
    address_decleration_index = []
    address_names = []
    exception_handler = True
    unknown_address_counter = 0
    for i, j in enumerate(param_list):
        if j == 'address':
            address_decleration_index.append(i)
            address_names.append(param_list[i+1])
    print(address_decleration_index)
    print(address_names)
    if '.call' in param or '.send' in param:
        for i in address_names:
            send_to_addr = '{}.send'.format(i)
            call_to_addr = '{}.call'.format(i)
            if send_to_addr in param or call_to_addr in param:
                exception_handler = False
            else:
                unknown_address_counter += 1
        if 'returns (bool success)' in param:
            exception_handler = True

    if unknown_address_counter >= len(address_names):
        print('unknown address')
        return 'UNKNOWN_ADDR'

    if exception_handler == False:
        return 'MHE_alert'

def check_RET(param, param_list):
    print("------------------------------------------------------------------")
    print('Checking Re-entrancy Condition:')
    function_end = None
    if '.call.value' in param:
        for i, j in enumerate(param_list):
            if any(".call.value" in j for i in param_list):
                function_end = (i+1)
                if param_list[function_end] != '}':
                    print('Danger: .call.value is not the last call in function')
                    return 'RET_alert'
                else:
                    print('Warning: .send is recommended option over .call.value')
                    return 'RET_warning'


def parse(data):
    split_data = data.split()
    print(data)
    print (split_data)
    smart_contract = setJson(split_data, 'smart_contract.json', 'Saving contract to smart_contract.json')

    SLD_checker = check_solidity(split_data)
    TOD_checker = check_TOD(split_data)
    TSD_checker = check_TSD(split_data)
    MHE_checker = check_MHE(data, split_data)
    RET_checker = check_RET(data, split_data)
    print(TOD_checker)
    print(TSD_checker)
    print(MHE_checker)

    return SLD_checker, TOD_checker, TSD_checker, MHE_checker, RET_checker
