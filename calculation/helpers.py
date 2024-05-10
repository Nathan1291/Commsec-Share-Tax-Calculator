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
