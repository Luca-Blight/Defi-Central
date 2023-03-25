# Defi-Central

The purpose of this project is to provide a central location for all DeFi data. This will be done by aggregating data from various sources and providing a single API endpoint. This will allow for easy integration into other projects. The project is currently in development and is not ready for production use yet.  Additionally, bot scripts are provided for integration into Discord and Twitter. Twitter API approval is pending.



# Data Sources


[Defi Llama](https://defillama.com/)

[Bittrex](https://bittrex.com/)

[Messari](https://messari.io/)



# API



# Lexicon

Total Value Locked (TVL) is a metric used in decentralized finance (DeFi) to measure the amount of assets locked in various DeFi protocols. It helps assess the popularity and growth of DeFi projects. The formula for calculating TVL varies depending on the specific protocol, but in general, it can be represented as:

TVL = Σ (Token_Quantity \* Price)

where:

TVL is the total value locked in the DeFi protocol
Token_i represents the quantity of token i locked in the protocol
Price_i represents the current market price of token i in a common currency (typically USD)
TVL is calculated by multiplying the quantity of each locked token by its corresponding market price and summing the products for all tokens involved. This provides an estimate of the total value of all assets locked within the DeFi protocol. Note that this is a simplified version of the formula, and different DeFi protocols may have unique ways of calculating TVL based on their specific use cases or requirements.


# TVL Historical Chart Example

![](https://github.com/Luca-Blight/Defi-Central/blob/main/tvl_over_time.png)

# Current ERD

![](https://github.com/Luca-Blight/Defi-Central/blob/main/app/scripts/DeFi%20ERD.png)


# TO DO

### Finish Models
### Load Fees
### Twitter Bot

### ASYNC refactor of older code

### Frontend?
