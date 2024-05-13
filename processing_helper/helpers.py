# Dependencies
import pandas as pd


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

        total_amt = rawRecord["Debit($)"] if detailsList[0] == 'B' else rawRecord["Credit($)"]

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

"""
Changes the variables from all strings into their respective formats
date = datetime
share = string
price = float
units = integer
"""
def define_variables(records):
    # cant change the values if the array is empty
    if len(records.index) != 0:
        records["Date"] = pd.to_datetime(records["Date"], format="%d/%m/%Y")
        records["Share"] = records["Share"].astype(str)
        records["Price"] = pd.to_numeric(records["Price"])
        records["Units"] = pd.to_numeric(records["Units"])
        records["Total Value"] = pd.to_numeric(records["Total Value"])

    return records
