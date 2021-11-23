from brownie import DSCToken
from scripts.helper import get_account


def get_total_supply():
    dsc_token = DSCToken[-1]
    return dsc_token.totalSupply


def main():
    print(get_total_supply())
