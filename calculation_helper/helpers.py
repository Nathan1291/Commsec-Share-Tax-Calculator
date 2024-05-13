# Helper file containing main functions for calculation.py

# dependencies
from datetime import datetime
import pandas as pd


"""
extracts all the sell transactions of the given financial year
"""
def get_FY_sell_transactions(records, finYear):
    FYStartDate = datetime(finYear-1, 7, 1)
    FYEndDate = datetime(finYear, 6, 30)

    newRecord = records[(records["Date"] >= FYStartDate) & (records["Date"] <= FYEndDate)]
    return newRecord


"""
extracts all the distinct share names, returning it in a set
"""
def getAllShareNames(records):
    allShareNames = set()
    for i in range(len(records)):
        allShareNames.add(records.iloc[i]["Share"])
    return allShareNames


"""
Given a list of all the transactions made for a given stock, calculate the
taxable components for this current financial year.
Goes through each of the sale transactions for each sale record, links it up with
its associated purchase, and calculates the taxable components if it falls within
the given financial year
"""
def calculateTotalTaxableComponents(buyRecords, sellRecords, finYear):
    taxableComponents = {"CG > 1 Yr": 0,"CG < 1 Yr": 0, "CL": 0}
    FYStartDate = datetime(finYear-1, 7, 1)
    FYEndDate = datetime(finYear, 6, 30)

    # Keep track of the current buy transaction we are at (starting at the earliest transaction)
    buyRecordTracker = len(buyRecords) - 1
    sellRecordLen = len(sellRecords)

    # iterating through the sell records to link up appropriate buy records
    for i in range(sellRecordLen):
        # Keeping track of the associated buy records for the given sale
        buyTransactionRecords = pd.DataFrame(columns=["Date", "Price", "Units", "Value"])

        currSellRecord = sellRecords.iloc[sellRecordLen - (i + 1)]

        # keeping a tracker of how many units are left
        remainingUnits = currSellRecord["Units"]

        # Case when the sale falls within the given financial year
        if (currSellRecord["Date"] >= FYStartDate) and (currSellRecord["Date"] <= FYEndDate):
            # if the sale units has not been fully exhausted
            while remainingUnits > 0:
                # find the current buy record and its information
                buyTransaction = buyRecords.iloc[buyRecordTracker]
                buyUnits = buyTransaction["Units"]

                # if the buy transaction is fully exhausted on the sell transaction, use all units and move to the next transaction,  then add to the transaction records
                if remainingUnits >= buyUnits:
                    remainingUnits -= buyUnits
                    buyRecordTracker -= 1

                    transactionInfo = pd.DataFrame([{
                        "Date": buyTransaction["Date"],
                        "Price": buyTransaction["Price"],
                        "Units": buyTransaction["Units"],
                        "Total Value": buyTransaction["Total Value"]
                      }])

                    # add the transaction to the records with the related information, used up all buy units therefore no use in messing with fees
                    buyTransactionRecords = pd.concat([
                        buyTransactionRecords if not buyTransactionRecords.empty else None,
                        transactionInfo
                    ])

                # if the buy transaction is not fully exhausted on the sell transaction, use up all units and deduct the appropriate fee, then add to the transaction records
                else:
                    transactionsUsed = remainingUnits
                    unitDiff = buyUnits - remainingUnits
                    remainingUnits = 0

                    # add the transaction to the records with the related information, didnt used up all buy units therefore have to mess with fees
                    transactionInfo = pd.DataFrame([{
                        "Date": buyTransaction["Date"],
                        "Price": buyTransaction["Price"],
                        "Units": transactionsUsed,
                        "Total Value": buyTransaction["Total Value"] * transactionsUsed/buyUnits
                      }])

                    # add the transaction to the records with the related information, used up all buy units therefore no use in messing with fees
                    buyTransactionRecords = pd.concat([
                        buyTransactionRecords if not buyTransactionRecords.empty else None,
                        transactionInfo
                    ])

                    # changing the values of the original dataframe to make the fees associated with transactions match up
                    buyRecords.at[buyRecordTracker, "Total Value"] = buyRecords.iloc[buyRecordTracker]["Total Value"] * (unitDiff / buyUnits)
                    buyRecords.at[buyRecordTracker, "Units"] = unitDiff

            # calculate capital changes for the current sell transaction and add that to the total taxable components
            CG_after_1Yr, CG_Before_1Yr, CL = calculateTaxableComponents(buyTransactionRecords, currSellRecord)
            taxableComponents["CG > 1 Yr"] += CG_after_1Yr
            taxableComponents["CG < 1 Yr"] += CG_Before_1Yr
            taxableComponents["CL"] += CL

        # Case when the sale falls outside the given financial year
        else:
            # if there sell transaction has not been fully
            while remainingUnits > 0:
                # find the current buy record and its information
                buyTransaction = buyRecords.iloc[buyRecordTracker]
                buyUnits = buyTransaction["Units"]

                # if the buy transaction is fully exhausted on the sell transaction, use all units and move to the next transaction
                if remainingUnits >= buyUnits:
                    remainingUnits -= buyUnits
                    buyRecordTracker -= 1

                # if the buy transaction is not fully exhausted on the sell transaction, use up all units and deduct the appropriate fee
                elif remainingUnits < buyUnits:
                    unitDiff = buyUnits - remainingUnits
                    remainingUnits = 0
                    # changing the values of the original dataframe to make the fees associated with transactions match up
                    buyRecords.at[buyRecordTracker, "Total Value"] = buyRecords.iloc[buyRecordTracker]["Total Value"] * (unitDiff / buyUnits)
                    buyRecords.at[buyRecordTracker, "Units"] = unitDiff

    return taxableComponents


"""
Calculate how much gains/losses are associated with the given transactions
and their given time frames for the given stock
"""
def calculateTaxableComponents(buyRecords, sellRecord):
    # setting up components
    CG_after_1Yr = 0
    CG_Before_1Yr = 0
    CL = 0

    # pulling sell unit info and calculating value of the transaction
    sellUnits = sellRecord["Units"]
    sellDate = sellRecord["Date"]
    sellValue = sellRecord["Total Value"]

    # going through the buy transactions associated with the sell transaction and calculating the capital gain/loss on each one
    for i in range(len(buyRecords)):
        buyUnits = buyRecords.iloc[i]["Units"]
        buyDate = buyRecords.iloc[i]["Date"]
        buyValue = buyRecords.iloc[i]["Total Value"]

        # calculating the change in capital value associated with the buy transaction
        capital_Change = round(sellValue * (buyUnits/sellUnits) - buyValue, 2)


        # sorting the transaction into the 3 categories based on its characteristics
        if capital_Change < 0:
            CL += capital_Change
        else:
            dateDifference = sellDate - buyDate
            if dateDifference.days > 365:
                CG_after_1Yr += capital_Change
            else:
                CG_Before_1Yr += capital_Change

    # return the values associated with the current sell transaction
    return CG_after_1Yr, CG_Before_1Yr, CL


"""
Calculate the total capital change given each of the components
"""
def calculateNetCapitalChange(totalTaxableComponents):
    # Defining variables for later use
    netCapitalChange = 0
    CG_after_1Yr = totalTaxableComponents["CG > 1 Yr"]
    CG_before_1Yr = totalTaxableComponents["CG < 1 Yr"]
    CL = totalTaxableComponents["CL"]

    # keeping a tracker for how much CL we have left
    capitalLossTracker = CL

    # if the capital loss is fully exhausted on capital gains before 1 year
    if CG_before_1Yr > capitalLossTracker:
        netCapitalChange = round(CG_before_1Yr + CL + CG_after_1Yr * 0.5, 2)
    else:
        capitalLossTracker += CG_before_1Yr

        # if the capital loss is fully exhausted on capital gains after 1 year
        if CG_after_1Yr > capitalLossTracker:
            netCapitalChange = round((CG_after_1Yr + capitalLossTracker) * 0.5, 2)

        # if there is a net capital loss
        else:
            netCapitalChange = round(capitalLossTracker + CG_after_1Yr, 2)

    return netCapitalChange
