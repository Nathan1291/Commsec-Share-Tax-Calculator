from processing import get_sorted_records
from calculation.helpers import (
     get_FY_sell_transactions,
     getAllShareNames,
     # calculateTaxableComponents
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

    for share in shareNames:
        shareBuyRecords = buyRecords[buyRecords["Share"] == share]
        shareSellRecords = sellRecords[sellRecords["Share"] == share]

        print(shareBuyRecords)
        print(shareSellRecords)

def main():
    calculate(2022)


if __name__ == "__main__":
    main()
