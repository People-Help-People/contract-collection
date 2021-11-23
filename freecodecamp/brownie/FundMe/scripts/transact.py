from brownie import accounts, FundMe
from scripts.helper import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    minimum_amount = fund_me.getEntranceFee()
    fund_me.fund({"from": account, "value": minimum_amount})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
