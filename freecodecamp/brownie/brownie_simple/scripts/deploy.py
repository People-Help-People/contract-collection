from brownie import accounts, config, SimpleStorage, network

import os


def get_account():    
    if network.show_active() =="developement":
        account = accounts[0]
    else:
        # account = accounts.add(os.getenv("PRIVATE_KEY"))
        account = accounts.add(config["wallets"]["from_key"])
        # account = accounts.load("test")
    return account


def deploy_simple_storage():
    account=get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    transaction = simple_storage.store(1, {"from": account})
    transaction.wait(1)
    print(simple_storage.retrieve())


def main():
    deploy_simple_storage()
