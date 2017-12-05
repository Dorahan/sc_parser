from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import parser
import os

app = Flask(__name__)
Bootstrap(app)

alert_descriptions = {
'TOD':{'text':'The contract does not check the return value and have exceptions build around it. Since a transaction is in the mempool for a short while, one can know what actions will occur, before it is included in a block. This can be troublesome for things like decentralized markets, where a transaction to buy some tokens can be seen, and a market order implemented before the other transaction gets included.<p><strong>Check return with exceptions: </strong><code>revert();</code> or <code>throw();</code></p>'},
'TSD':{'text':'Be aware that the timestamp of the block can be manipulated by the miner, and all direct and indirect uses of the timestamp should be considered. Using <code>block.number</code> instead as an index of the block state is a better option if your contract requires exact accuracy.'},
'MHE':{'text':'Handling exceptions is a crucial part.'},
'UNKNOWN_ADDR':{'text':'Cannot do a <code>.call</code> or <code>.send</code> with an undefined address.'},
'SLD_version':{'text':'Wrong version of <code>pragma solidity</code> is being used, correct version should be <code>0.4.19</code> and you can always double check at <a href="https://github.com/ethereum/solidity/releases/latest">Solidity latest release Github repository</a>'},
'SLD_alert':{'text':'Solidity decleration is missing or wrong, it should be <code>pragma solidiy ^0.4.19</code>, correct version could be always double checked at <a href="https://github.com/ethereum/solidity/releases/latest">Solidity latest release Github repository</a>'},
'RET_warning':{'text':'The best way to avoid any problem is to use <code>send()</code> instead of <code>call.value()()</code>. This will prevent any external code from being executed. However, if you cannot remove the external call, the next simplest way to prevent this attack is to make sure you do not call an external function until you have done all the internal work you need to do'},
'RET_alert':{'text':'There is reentrancy attack vulnerability in your contract since the <code>call.value()</code> is called before the all the work is executed inside function. <p><strong>To prevent this:</strong> do your <code>call.value()</code> calls at the end of the function or use <code>send()</code> instead.</p>'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def get_contract():
    text = request.form['text']
    print(text)
    parsable_text = "'"+text+"'"
    print(parsable_text)
    return parser.parse(text)

@app.route('/background_process')
def background_process():
    try:
        risks = 0
        msg_keys = []
        contract = request.args.get('contract', 0, type=str)
        results = parser.parse(contract)
        if 'TOD_alert' in results:
            msg_keys.append({'header':'Transaction Order Dependence', 'text': alert_descriptions['TOD']['text'],'type':'alert-warning'})
            risks += 1
        if 'NO_TOD' in results:
            pass
        if 'TSD_alert' in results:
            msg_keys.append({'header':'Timestamp Dependence', 'text': alert_descriptions['TSD']['text'],'type':'alert-danger'})
            risks += 1
        if 'MHE_alert' in results:
            msg_keys.append({'header':'Mishandled Exceptions', 'text': alert_descriptions['MHE']['text'],'type':'alert-danger'})
            risks += 1
        if 'UNKNOWN_ADDR' in results:
            msg_keys.append({'header':'Undefined Address Use', 'text': alert_descriptions['UNKNOWN_ADDR']['text'],'type':'alert-warning'})
            risks += 1
        if 'SLD_version' in results:
            msg_keys.append({'header':'Incorrect Solidity Version', 'text': alert_descriptions['SLD_version']['text'],'type':'alert-warning'})
            risks += 1
        if 'SLD_alert' in results:
            msg_keys.append({'header':'Missing or Wrong Solidity Decleration', 'text': alert_descriptions['SLD_alert']['text'],'type':'alert-warning'})
            risks += 1
        if 'RET_warning' in results:
            msg_keys.append({'header':'Reentrancy Warning', 'text': alert_descriptions['RET_warning']['text'],'type':'alert-warning'})
            risks += 1
        if 'RET_alert' in results:
            msg_keys.append({'header':'Reentrancy Attack Vulnerability', 'text': alert_descriptions['RET_alert']['text'],'type':'alert-danger'})
            risks += 1
        k = {
              'riskCount': risks,
              'messageKeys': msg_keys
            }
        # outcome = 'Risk count: {}'.format(risks)
        # return jsonify(result=(outcome)
        return jsonify(k)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
