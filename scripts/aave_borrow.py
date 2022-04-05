from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.aave_borrow_olmadi import get_weth
from brownie import config, network, interface
from web3 import Web3

GLOBAL_LEND = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        get_weth()
    lending_pool = get_lending_pool()
    print(lending_pool)
    approve_erc20(GLOBAL_LEND, lending_pool.address, erc20_address, account)
    print("depositing")
    tx = lending_pool.deposit(erc20_address, GLOBAL_LEND, account, 0, {"from": account})
    tx.wait(1)
    print("finisjed depositing")
    available_borrow_eth, total_colleteral_eth = get_user_account_data(
        lending_pool, account
    )
    print("lets borrow")
    dai_eth_price_address = config["networks"][network.show_active()]["dai_price_feed"]
    dai_eth_price = get_price_asset(dai_eth_price_address)
    amount_dai_to_borrow = (available_borrow_eth / dai_eth_price) * 0.80
    print(f"first amount borrow{amount_dai_to_borrow}")
    amount_dai_to_borrow = (1 / dai_eth_price) * (available_borrow_eth * 0.20)
    print(f"second amount borrow{amount_dai_to_borrow}")
    print(f"amount dai to borrow{amount_dai_to_borrow}")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    lending_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account,
        {"from": account},
    )
    lending_tx.wait(1)
    print("borrewed dei")
    get_user_account_data(lending_pool, account)
    # repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)


def repay_all(amount, lending_pool, account):
    erc20_address = config["networks"][network.show_active()]["dai_token"]
    approve_erc20(
        Web3.toWei(amount, "ether"), lending_pool.address, erc20_address, account
    )
    repay_tx = lending_pool.repay(
        erc20_address,
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("repayed")


def get_lending_pool():
    lending_pool_adress_provider = interface.LendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_adress_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc_address, account):
    ierc20 = interface.IERC20(erc_address)
    tx = ierc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("approved")
    return tx


def get_price_asset(price_feed_address):
    lastest_price = interface.AggregatorV3Interface(price_feed_address)
    price = lastest_price.latestRoundData()[1]
    converted_price = Web3.fromWei(price, "ether")
    print(f"die eth price feed{converted_price}")
    return float(converted_price)


def get_user_account_data(lending_pool, account):

    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = lending_pool.getUserAccountData(account.address)
    totalCollateralETH = Web3.fromWei(totalCollateralETH, "ether")
    totalDebtETH = Web3.fromWei(totalDebtETH, "ether")
    availableBorrowsETH = Web3.fromWei(availableBorrowsETH, "ether")
    # currentLiquidationThreshold = Web3.fromWei(currentLiquidationThreshold, "ether")
    # ltv = Web3.fromWei(ltv, "ether")
    # healthFactor = Web3.fromWei(healthFactor, "ether")
    print(f"yu have totalCollateralETH {totalCollateralETH}")
    print(f"yu have totalDebtETH {totalDebtETH}")
    print(f"yu have availableBorrowsETH {availableBorrowsETH}")
    return (float(availableBorrowsETH), float(totalCollateralETH))


def deposit():
    pass
