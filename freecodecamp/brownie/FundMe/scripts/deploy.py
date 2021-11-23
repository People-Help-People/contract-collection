from brownie import FundMe
from scripts.helper import get_deploy_vars


def deploy_fund_me():
    account, price_feed, verify_flag = get_deploy_vars()
    fund_me = FundMe.deploy(
        price_feed,
        {"from": account},
        publish_source=verify_flag,
    )
    return fund_me


def main():
    deploy_fund_me()
