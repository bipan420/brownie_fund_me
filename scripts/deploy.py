from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()

    # note that we can pass the constructor from our solidity code here while calling deploy function.
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise deploy mocks (the replica version) for the eth to usd price rate

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # publish_source=True means that we would like to publish our source code (or deploy) through etherscan
    # instead of making publish_source= True,
    #  we dynamically want to have its value based on what chain we are on.
    # ie, if we are on local chain(eg, ganase) we want it to be False.
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Deployed to the server:{fund_me}")
    return fund_me


def main():
    deploy_fund_me()
