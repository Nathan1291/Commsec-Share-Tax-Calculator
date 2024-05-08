import pandas as pd

def sort_records():
    recordsDf = pd.read_csv("./record/Transactions.csv")
    print(recordsDf)

def main():
    sort_records()


if __name__ == "__main__":
    main()
