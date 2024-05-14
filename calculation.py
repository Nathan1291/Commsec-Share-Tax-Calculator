from processing import get_sorted_records
from calculation_helper.helpers import (
     get_FY_sell_transactions,
     getAllShareNames,
     calculateTotalTaxableComponents,
     calculateNetCapitalChange
)

from datetime import datetime


"""
main function that calculates the total taxable income due for a given financial year
"""
def calculate(finYear):
    # Defining Global Variables for total Use
    totalTaxableComponents = {"CG > 1 Yr": 0,"CG < 1 Yr": 0, "CL": 0}

    buyRecords, sellRecords = get_sorted_records()

    # gets all the sale transactions associated with that financial year
    FYSellRecords = get_FY_sell_transactions(sellRecords, finYear)

    # get all the unique share names from the given records
    shareNames = getAllShareNames(FYSellRecords)

    # for each share we sold, calculate the values of each category
    for share in shareNames:
        shareBuyRecords = buyRecords[buyRecords["Share"] == share]
        shareSellRecords = sellRecords[sellRecords["Share"] == share]

        shareBuyRecords = shareBuyRecords.reset_index(drop=True)
        shareSellRecords = shareSellRecords.reset_index(drop=True)

        taxableComponents = calculateTotalTaxableComponents(shareBuyRecords, shareSellRecords, finYear)

        totalTaxableComponents["CG > 1 Yr"] += taxableComponents["CG > 1 Yr"]
        totalTaxableComponents["CG < 1 Yr"] += taxableComponents["CG < 1 Yr"]
        totalTaxableComponents["CL"] += taxableComponents["CL"]

    # calculate the final change in capital
    netCapitalChange = calculateNetCapitalChange(totalTaxableComponents)

    return netCapitalChange, totalTaxableComponents

def main():
    calculate(2022)


if __name__ == "__main__":
    main()
