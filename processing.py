import pandas as pd
"""
This processes the raw records read in from the csv and translates it to become
2 processed dataframes, each storing all the associated transactions of their
sale type, either buy or sell records.
"""


# Main processing function
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

"""
Processes the raw records of each transaction and adjusts it to a new dataframe
that contains the date, share name, price and number of units traded
"""
def process_records(newRecord, rawRecords):
    # going through each record
    for i in range(len(rawRecords)):
        rawRecord = rawRecords.iloc[i]
        details = rawRecord["Details"]

        # cleaning up the details column so that we include only information we need
        detailsList = str(rawRecord["Details"]).split()
        shareName = detailsList[2]
        noOfUnits = int(detailsList[1])
        price = float(detailsList[4])

        if detailsList[0] == 'B':
            total_amt = rawRecord["Debit($)"]
        else:
            total_amt = rawRecord["Credit($)"]

        # the data to be added
        recordInfo = pd.DataFrame([{
            "Date": rawRecord["Date"],
            "Share": shareName,
            "Price": price,
            "Units": noOfUnits,
            "Total Value": total_amt
          }])

        # adding it to the dataframe
        # have to check if the dataframe is empty due to deprecated pandas code
        newRecord = pd.concat([
                newRecord if not newRecord.empty else None,
                recordInfo
            ],
            ignore_index=True)

    return newRecord

# Changes the variables from all strings into their respective formats
# date = datetime
# share = string
# price = float
# units = integer
def define_variables(records):
    records["Date"] = pd.to_datetime(records["Date"], format="%d/%m/%Y")
    records["Share"] = records["Share"].astype(str)
    records["Price"] = pd.to_numeric(records["Price"])
    records["Units"] = pd.to_numeric(records["Units"])
    records["Total Value"] = pd.to_numeric(records["Total Value"])

    return records

def main():
    print(get_sorted_records())

if __name__ == "__main__":
    main()
