import pandas as pd
"""
This processes the raw records read in from the csv and translates it to become
2 processed dataframes, each storing all the associated transactions of their
sale type, either buy or sell records.
"""


# Main processing function
def sort_records():
    # reading the raw records
    rawRecordsDf = pd.read_csv("./record/Transactions.csv")

    # removing all the overlapped records which simply record
    rawBuyRecordsDf = rawRecordsDf[rawRecordsDf["Details"].str.startswith('B')]
    rawSellRecordsDf = rawRecordsDf[rawRecordsDf["Details"].str.startswith('S')]

    # cleans all the information and places it in a new record dataframe
    buyRecords = pd.DataFrame(columns=["Date","Share", "Price","Units"])
    sellRecords = pd.DataFrame(columns=["Date","Share", "Price","Units"])

    buyRecords = processRecords(buyRecords, rawBuyRecordsDf)
    sellRecords = processRecords(sellRecords, rawSellRecordsDf)

    return buyRecords, sellRecords

"""
Processes the raw records of each transaction and adjusts it to a new dataframe
that contains the date, share name, price and number of units traded
"""
def processRecords(newRecord, rawRecords):
    # going through each record
    for i in range(len(rawRecords)):
        rawRecord = rawRecords.iloc[i]
        details = rawRecord["Details"]

        # cleaning up the details column so that we include only information we need
        detailsList = str(rawRecord["Details"]).split()
        shareName = detailsList[2]
        noOfUnits = int(detailsList[1])
        price = float(detailsList[4])

        # the data to be added
        recordInfo = pd.DataFrame([{
            "Date": rawRecord["Date"],
            "Share": shareName,
            "Price": price,
            "Units": noOfUnits
          }])

        # adding it to the dataframe
        # have to check if the dataframe is empty due to deprecated pandas code
        newRecord = pd.concat([
                newRecord if not newRecord.empty else None,
                recordInfo
            ],
            ignore_index=True)

    return newRecord

def main():
    print(sort_records())

if __name__ == "__main__":
    main()
