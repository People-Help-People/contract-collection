// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.9.0;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage{
    SimpleStorage[] public storageContracts;
    
    function create() public {
        SimpleStorage newContract = new SimpleStorage();
        storageContracts.push(newContract);
    }
    
    function factoryStore(uint256 _storageIndex,uint256 _favoriteNumber) public {
        SimpleStorage storageContract = SimpleStorage(address(storageContracts[_storageIndex]));
        storageContract.store(_favoriteNumber);
    }
    
    function factoryRetrieve(uint256 _storageIndex) public view returns (uint256){
        SimpleStorage storageContract = SimpleStorage(address(storageContracts[_storageIndex]));
        return storageContract.retrieve();
    }
}
