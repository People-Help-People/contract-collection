// SPDX-License-Identifier: GPL-3.0

// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;
    uint256 minimumAmount = 50 * 10**18; // USD

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    mapping(address => uint256) public addressToFunds;

    function fund() public payable {
        require(
            getConversionRate(msg.value) >= minimumAmount,
            "You need to send more ETH!!!"
        );
        if (addressToFunds[msg.sender] == 0) funders.push(msg.sender);
        addressToFunds[msg.sender] += msg.value;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10**10);
    }

    function getConversionRate(uint256 _input) public view returns (uint256) {
        uint256 curValue = getPrice();
        return (_input * curValue) / 10**18;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 curValue = getPrice();
        return (minimumAmount * 10**18) / curValue;
    }

    modifier OnlyOwner() {
        require(msg.sender == owner, "You are not the owner!!!");
        _;
    }

    function withdraw() public payable OnlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 i = 0; i < funders.length; i++) {
            addressToFunds[funders[i]] = 0;
        }
        funders = new address[](0);
    }
}
