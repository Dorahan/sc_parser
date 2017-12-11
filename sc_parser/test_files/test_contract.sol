//Transaction Order Dependence contract
pragma solidity ^0.4.0;

contract SimpleStorage {
    uint storedData;

    function set(uint x) {
        storedData = x;
    }

    function get() constant returns (uint) {
        return storedData;
    }
}

//Transaction Order Dependence checker
pragma solidity ^0.4.0;

contract SimpleStorage {
    uint storedData;
    uint beforeSend;

    function set(uint x) {
        if(msg.sender.value != owner) { revert(); }
            storedData = x;
    }

    function get() constant returns (uint) {
        return storedData;
    }
}

//King of Ether older example without exception handler
contract KingOfTheEtherThrone {
    struct Monarch {
        // address of the king.
        address ethAddr;
        string name;
        // how much he pays to previous king
        uint claimPrice;
        uint coronationTimestamp;
    }
    Monarch public currentMonarch;
    // claim the throne
    function claimThrone(string name) {
        if (currentMonarch.ethAddr != wizardAddress)
            currentMonarch.ethAddr.send(compensation);
        // assign the new king
    currentMonarch = Monarch(
        msg.sender, name,
        valuePaid , block.timestamp);
}}

//King of Ether example with exception handler
function carefulSendWithFixedGas(
        address _toAddress,
        uint _valueWei,
        uint _extraGasIncluded
    ) internal returns (bool success) {
        return _toAddress.call.value(_valueWei).gas(_extraGasIncluded)();
    }

}
// CONTRACT EXAMPLE
contract ContractExample {
    uint someValue;
    address _addr

    function set(uint x) {
        returns (bool success) {
            someValue = x;
            _addr.send(someValue);
        }
    }

    function get() constant returns (uint) {
        return someValue;
    }
}

contract HasAnOwner {
    address owner;

    function useSuperPowers(){
        if (msg.sender != owner) { throw; }
        // do something only the owner should be allowed to do
    }
}

// INSECURE Reentrancy example
mapping (address => uint) private userBalances;

function withdrawBalance() public {
    uint amountToWithdraw = userBalances[msg.sender];
    require(msg.sender.call.value(amountToWithdraw)());
    userBalances[msg.sender] = 0;
}

// SECURE Reentrancy example
mapping (address => uint) private userBalances;

function withdrawBalance() public {
    uint amountToWithdraw = userBalances[msg.sender];
    userBalances[msg.sender] = 0;
    require(msg.sender.call.value(amountToWithdraw)());
}

//Timestamp dependence example
uint someVariable = now + 1;

if (now % 2 == 0) { // the now can be manipulated by the miner

}

if ((someVariable - 100) % 2 == 0) { // someVariable can be manipulated by the miner

}
