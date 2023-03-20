import asyncio
import calendar
import pandas as pd
import os

from bittrex_api import *
from bittrex_api.models.v3.candle_interval import CandleInterval
from models.ConversionRate import ConversionRate
from datetime import datetime, timedelta
from query import query_update
from database import engine
from itertools import chain
from typing import List


####CUT THIS DOWN TO 1 YEAR####, Make ASYNC if possible

### USE COINMARKETCAP API TO GET CONVERSION RATES ###
v3 = BittrexV3(
    api_key=os.environ.get("BITTREX_API_KEY"),
    api_secret=os.environ.get("BITTREX_SECRET"),
    max_request_try_count=1,
    sleep_time=2,
    debug_level=3,
    reverse_market_names=True,
)


def merge_with(minutes_df: pd.DataFrame, prefix: str, engine=engine):

    current_table = pd.read_sql(f"SELECT * FROM conversion_rate", con=engine)

    conversion_rate_column: str = f"{prefix}_conversion_rate"

    query: str = query_update(conversion_rate_column)

    conversion_rate: pd.DataFrame = minutes_df[["startsAt", "close"]].rename(
        columns={"startsAt": "block_date", "close": conversion_rate_column}
    )
    conversion_rate["block_date"] = conversion_rate["block_date"].astype("datetime64")
    conversion_rate[conversion_rate_column] = conversion_rate[
        conversion_rate_column
    ].astype("float")

    if prefix == "waxp":
        conversion_rates = dict(
            zip(conversion_rate.block_date, conversion_rate.waxp_conversion_rate)
        )
    else:
        conversion_rates = dict(
            zip(conversion_rate.block_date, conversion_rate.matic_conversion_rate)
        )

    current_table[conversion_rate_column] = (
        current_table["block_date"]
        .map(conversion_rates)
        .fillna(current_table[conversion_rate_column])
    )

    current_table.to_sql(
        con=engine, name="temp_conversion_rate", if_exists="replace", index=False
    )

    with engine.connect() as connection:
        connection.execute(query)
        connection.close()

    return current_table


def get2020_conv_rates(
    MARKET_NAME: str, prefix: str, months: int = 12, engine=engine
) -> str:

    all_minutes = []

    try:
        for month in range(months):
            month: int = month + 1
            days = calendar.monthrange(2020, month)
            for day in range(days[1]):
                day: int = day + 1
                result = v3.get_historical_candles(
                    market=MARKET_NAME,
                    candle_interval=CandleInterval.MINUTE_1,
                    year=2020,
                    month=month,
                    day=day,
                )
                all_minutes.append(result)
        minutes_df = pd.DataFrame(list(chain.from_iterable(all_minutes)))
        if prefix == "eth":
            conversion_rate: pd.DataFrame = minutes_df[["startsAt", "close"]].rename(
                columns={"startsAt": "block_date", "close": f"{prefix}_conversion_rate"}
            )
            conversion_rate.to_sql(
                con=engine,
                name=ConversionRate.__tablename__,
                if_exists="append",
                index=False,
            )
            return print(f"Table has been updated with {prefix} 2020 conversion rates")
        else:
            merge_with(minutes_df, prefix, engine)
            return print(f"Table has been updated with {prefix} 2020 conversion rates")
    except KeyError:
        print(month, day, all_minutes)


def get2021_conv_rates(
    MARKET_NAME: str, prefix: str, months: int = 12, engine=engine
) -> str:

    all_minutes = []

    try:
        for month in range(months):
            month: int = month + 1
            days: int = calendar.monthrange(2021, month)
            for day in range(days[1]):
                day: int = day + 1
                result: List[dict] = v3.get_historical_candles(
                    market=MARKET_NAME,
                    candle_interval=CandleInterval.MINUTE_1,
                    year=2021,
                    month=month,
                    day=day,
                )
                all_minutes.append(result)
        minutes_df = pd.DataFrame(list(chain.from_iterable(all_minutes)))
        if prefix == "eth":
            conversion_rate: pd.DataFrame = minutes_df[["startsAt", "close"]].rename(
                columns={"startsAt": "block_date", "close": f"{prefix}_conversion_rate"}
            )
            conversion_rate.to_sql(
                con=engine,
                name=ConversionRate.__tablename__,
                if_exists="append",
                index=False,
            )
            return print(f"Table has been updated with {prefix} 2021 conversion rates")
        else:
            merge_with(minutes_df, prefix, engine)
            return print(f"Table has been updated with {prefix} 2021 conversion rates")
    except KeyError:
        print(month, day, all_minutes)


def get2022_conv_rates(
    MARKET_NAME: str, prefix: str, months: int = 0, engine=engine
) -> str:

    end_of_month = datetime.now() - timedelta(days=1)

    current_day: int = datetime.now().day
    current_month: int = datetime.now().month if current_day > 1 else end_of_month.month
    current_year: int = datetime.now().year

    current_month: int = current_month if months == False else months

    prev_day: int = (current_day - 1) if current_day > 1 else end_of_month.day

    df_current_year = pd.read_sql(
        f"SELECT block_date, {prefix}_conversion_rate FROM conversion_rate WHERE EXTRACT(YEAR FROM block_date) = {current_year}",
        con=engine,
    )

    all_minutes = []

    if df_current_year.empty or df_current_year.iloc[-1][1] == None:
        for month in range(current_month):
            month: int = month + 1
            if month < current_month:
                days = calendar.monthrange(current_year, month)
                for day in range(days[1]):
                    day: int = day + 1
                    result: List[dict] = v3.get_historical_candles(
                        market=MARKET_NAME,
                        candle_interval=CandleInterval.MINUTE_1,
                        year=current_year,
                        month=month,
                        day=day,
                    )
                    all_minutes.append(result)

            else:
                for day in range(current_day):
                    day: int = day + 1
                    if day == current_day:
                        pass
                    else:
                        result: List[dict] = v3.get_historical_candles(
                            market=MARKET_NAME,
                            candle_interval=CandleInterval.MINUTE_1,
                            year=current_year,
                            month=month,
                            day=day,
                        )
                        all_minutes.append(result)

                minutes_df = pd.DataFrame(list(chain.from_iterable(all_minutes)))

                if prefix == "eth":
                    Conversion_Rate: pd.DataFrame = minutes_df[
                        ["startsAt", "close"]
                    ].rename(
                        columns={
                            "startsAt": "block_date",
                            "close": f"{prefix}_conversion_rate",
                        }
                    )
                    Conversion_Rate.to_sql(
                        con=engine,
                        name=ConversionRate.__tablename__,
                        if_exists="append",
                        index=False,
                    )
                    return print(
                        f"Table is up to date with {current_month}-{prev_day}-{current_year} {prefix} conversion rates"
                    )

                else:
                    merge_with(minutes_df, prefix, engine)
                    return print(
                        f"Table is up to date with {current_month}-{prev_day}-{current_year} {prefix} conversion rates"
                    )
    else:

        result: List[dict] = v3.get_historical_candles(
            market=MARKET_NAME,
            candle_interval=CandleInterval.MINUTE_1,
            year=current_year,
            month=current_month,
            day=prev_day,
        )
        all_minutes.append(result)
        minutes_df = pd.DataFrame(list(chain.from_iterable(all_minutes)))

        if prefix == "eth":

            conversion_rate: pd.DataFrame = minutes_df[["startsAt", "close"]].rename(
                columns={"startsAt": "block_date", "close": f"{prefix}_conversion_rate"}
            )
            conversion_rate.to_sql(
                con=engine,
                name=ConversionRate.__tablename__,
                if_exists="append",
                index=False,
            )
            return print(
                f"Table is up to date with {current_month}-{prev_day}-{current_year} {prefix} conversion rates"
            )

        else:

            merge_with(minutes_df, prefix, engine)
            return print(
                f"Table is up to date with {current_month}-{prev_day}-{current_year} {prefix} conversion rates"
            )

    pass


async def get_current_conv_rates(MARKET_NAME: str, months: int = 12, engine=engine):

    prefix: str = MARKET_NAME.split("-")[1].lower()

    df_2020 = pd.read_sql(
        f"SELECT block_date,{prefix}_conversion_rate FROM conversion_rate WHERE EXTRACT(YEAR FROM block_date) = 2020 ORDER BY block_date DESC",
        con=engine,
    )
    df_2021 = pd.read_sql(
        f"SELECT block_date,{prefix}_conversion_rate FROM conversion_rate WHERE EXTRACT(YEAR FROM block_date) = 2021",
        con=engine,
    )

    if (df_2020.empty or df_2020.iloc[0][1] == None) and prefix != "matic":
        get2020_conv_rates(MARKET_NAME, prefix, months, engine)
        if df_2021.empty or df_2021.iloc[-1][1] == None:
            get2021_conv_rates(MARKET_NAME, prefix, months, engine)
        else:
            pass
    else:
        pass

    get2022_conv_rates(MARKET_NAME, prefix, engine=engine)


if __name__ == "__main__":

    asyncio.run(get_current_conv_rates("USD-ETH"))
    asyncio.run(get_current_conv_rates("USD-MATIC"))
