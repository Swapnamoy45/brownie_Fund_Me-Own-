from brownie import FundMe, MockV3Aggregator, accounts, config, network
from scripts.helpful_scripts import (
    get_account,
    get_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_MAINNET_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # Passing Price Feed to our Solidity contract.

    # If we are on a persistent network like rinkeby, use its price feed address.
    # Otherwise use Mocks.
    # print(account)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        get_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"It is deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
