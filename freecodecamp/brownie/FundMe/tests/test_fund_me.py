from brownie import network, accounts, exceptions
from scripts.deploy import deploy_fund_me
from scripts.helper import get_account, LOCAL_DEV_ENVS
import pytest

# deploy the contract
# send funds to the contract
# withdraw funds from the contract
# check balance
def test_can_transact():
    account = get_account()
    fund_me = deploy_fund_me()
    minimum_amount = fund_me.getEntranceFee() + 10

    tx1 = fund_me.fund({"from": account, "value": minimum_amount})
    tx1.wait(1)
    assert fund_me.addressToFunds(account) == minimum_amount

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToFunds(account) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_DEV_ENVS:
        pytest.skip("Skipping test in production")

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
