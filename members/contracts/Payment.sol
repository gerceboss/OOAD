// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Payment {
    address admin;
    constructor(address _address){
        admin = _address;
    }
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "You are not the Admin!");
        _;
    }

    function checkWalletBalance(address _from, uint _amount ) public view onlyAdmin() returns(bool) {
        bool res = _amount > _from.balance;
        return res;
    }

    function makePayment( address _to,uint _amount) public payable {
        payable(_to).transfer(_amount);
    }
}