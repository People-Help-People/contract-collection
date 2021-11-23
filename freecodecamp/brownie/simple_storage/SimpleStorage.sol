// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 number;

    struct People {
        string name;
        uint256 favoriteNumber;
    }

    People[] public people;

    mapping(string => People) nameToPeople;

    function store(uint256 _number) public {
        number = _number;
    }

    function retrieve() public view returns (uint256) {
        return number;
    }

    function add(uint256 _number, string memory _name) public {
        People memory newPerson = People({
            name: _name,
            favoriteNumber: _number
        });
        people.push(newPerson);
        nameToPeople[_name] = newPerson;
    }

    function get(string memory _name) public view returns (People memory) {
        return nameToPeople[_name];
    }
}
