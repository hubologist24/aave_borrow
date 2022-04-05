from web3 import Web3
from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    print("received weth")
    tx2 = weth.approve(account, Web3.toWei(0.1, "ether"), {"from": account})
    tx2.wait(1)
    # return tx
