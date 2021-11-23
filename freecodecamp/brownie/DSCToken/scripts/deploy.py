from brownie import DSCToken
from scripts.helper import get_account


def deploy_dsc_token():
    account = get_account()
    dsc_token = DSCToken.deploy(1000*10**18, {"from": account})
    return dsc_token


def main():
    deploy_dsc_token()
