# Dependencies
import pandas as pd
from processing_helper.helpers import (
    process_records,
    define_variables
)


"""
This processes the raw records read in from the csv and translates it to become
2 processed dataframes, each storing all the associated transactions of their
sale type, either buy or sell records.
"""
def get_sorted_records():
    # reading the raw records
    rawRecordsDf = pd.read_csv("./record/Transactions.csv")

    # removing all the overlapped records which simply record
    rawBuyRecordsDf = rawRecordsDf[rawRecordsDf["Details"].str.startswith('B')]
    rawSellRecordsDf = rawRecordsDf[rawRecordsDf["Details"].str.startswith('S')]

    # cleans all the information and places it in a new record dataframe
    buyRecords = pd.DataFrame(columns=["Date","Share", "Price","Units"])
    sellRecords = pd.DataFrame(columns=["Date","Share", "Price","Units"])

    # processes all the records to match the given format
    buyRecords = process_records(buyRecords, rawBuyRecordsDf)
    sellRecords = process_records(sellRecords, rawSellRecordsDf)

    # adjusts all variable formats they match their given type
    buyRecords = define_variables(buyRecords)
    sellRecords = define_variables(sellRecords)

    return buyRecords, sellRecords

def main():
    print(get_sorted_records())

if __name__ == "__main__":
    main()
