from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    storage = SimpleStorage.deploy({"from": account})
    # Assert
    assert storage.address != None
    assert storage.retrieve() == 0

def test_store():
    # Arrange
    account = accounts[0]
    storage = SimpleStorage.deploy({"from": account})
    # Act
    storage.store(1, {"from": account})
    # Assert
    assert storage.retrieve() == 1

