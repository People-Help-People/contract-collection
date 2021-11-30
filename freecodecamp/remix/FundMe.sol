// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.6 <0.9.0;

import '@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';

contract FundMe {
    
    // uint256 constant DECIMAL = 10**8;
    address[] public funders;
    address public owner;
    
    constructor (){
        owner = msg.sender;
    }
    
    mapping(address => uint256) public addressToFunds;

    function printFund () public payable returns(uint256){
        return getConversionRate(msg.value);
    }
    
    function fund () public payable {
        uint256 minimumAmount = 0.0001 * 10**8 ; // in USD
        require(getConversionRate(msg.value)>=minimumAmount,"You need to send more ETH!!!");
        if(addressToFunds[msg.sender]!=0) funders.push(msg.sender);
        addressToFunds[msg.sender]+=msg.value;
    }
    
    function getPrice () public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0xd0D5e3DB44DE05E9F294BB0a3bEEaF030DE24Ada);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer);
    }
    
    function getConversionRate(uint256 _input) public view returns (uint256) {
        uint256 curValue = getPrice();
        return (_input * curValue)/(10**18);
    }
    
    modifier OnlyOwner {
        require(msg.sender == owner, "You are not the owner!!!");
        _;
    }
    
    function withdraw() public payable OnlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for(uint256 i=0;i< funders.length; i++){
            addressToFunds[funders[i]]=0;
        }
        funders= new address[](0);
    }
}
