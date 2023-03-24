# head block number is 226m
# last block number is 1
# negative numbers is backwards from the time the query is executed.s
# ~5m blocks = ~1 month
# need to pull 6 months or 30m.

Query = """ 
    subscription ($query: String!, $low: Int64, $high: Int64, $cursor: String, $limit: Int64) {
    searchTransactionsForward(query: $query, lowBlockNum: $low, highBlockNum: $high, cursor: $cursor, limit: $limit) {
    undo
    cursor
    trace {
        block {
            num
            id
            confirmed
            timestamp
            previous
                }
        id
        matchingActions {
            account
            name
            json
            seq
            receiver
                }
            }
    }
  }
"""


def query_update(currency_column: str) -> str:
    query: str = f"""UPDATE conversion_rate cr
                SET {currency_column} = tcr.{currency_column}
                FROM  temp_conversion_rate tcr
                WHERE cr.block_date = tcr.block_date"""

    return query
