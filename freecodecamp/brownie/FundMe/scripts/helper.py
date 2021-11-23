from brownie import accounts, config, network, MockV3Aggregator
import os

LOCAL_DEV_ENVS = ["development", "ganache-local"]
FORKED_ENVS = ["mainnet-fork-dev"]
USD_DECIMAL = 8
USD_VALUE = 4000 * 10 ** 8


def get_account():
    if network.show_active() in LOCAL_DEV_ENVS + FORKED_ENVS:
        account = accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
        # account = accounts.add(os.getenv("PRIVATE_KEY"))
        # account = accounts.load("test")
    return account


def get_price_feed():
    if network.show_active() not in LOCAL_DEV_ENVS:
        price_feed = config["networks"][network.show_active()]["price_feed"]
    elif len(MockV3Aggregator) < 1:
        print(f"The current network is {network.show_active()}")
        print("Deploying Mocks...")
        contract = MockV3Aggregator.deploy(
            USD_DECIMAL, USD_VALUE, {"from": accounts[0]}
        )
        print("Mocks Deployed")
        price_feed = contract.address
    else:
        price_feed = MockV3Aggregator[0].address

    return price_feed


def is_prod():
    return network.show_active() not in LOCAL_DEV_ENVS


def get_verify_flag():
    return bool(config["networks"][network.show_active()].get("verify_flag"))


def get_deploy_vars():
    return get_account()
