from processing import get_sorted_records
from datetime import datetime


"""
main function that calculates the total taxable income due for a given financial year
"""
def calculate_taxable_income(finYear):
    buyRecords, sellRecords = get_sorted_records()

    # gets all the sale transactions associated with that financial year
    FYSellRecords = get_FY_sell_transactions(sellRecords, finYear)

    # get all the unique share names from the given records
    shareNames = getAllShareNames(FYSellRecords)

    for share in shareNames:
        shareBuyRecords = buyRecords[buyRecords["Share"] == share]
        shareSellRecords = FYSellRecords[FYSellRecords["Share"] == share]

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



def main():
    calculate_taxable_income(2022)


if __name__ == "__main__":
    main()
