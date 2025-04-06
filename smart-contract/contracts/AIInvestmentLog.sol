// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AIInvestmentLog {
    event InvestmentLogged(address indexed sender, string message);

    string[] public logs;

    function logInvestment(string memory _message) external {
        logs.push(_message);
        emit InvestmentLogged(msg.sender, _message);
    }

    function getLog(uint index) external view returns (string memory) {
        return logs[index];
    }

    function totalLogs() external view returns (uint) {
        return logs.length;
    }
}
