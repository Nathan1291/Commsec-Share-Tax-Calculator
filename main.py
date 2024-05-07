from calculation.calculation import calculate

def main():
        year = int(input("\nWhat is the financial year you want to calculate tax on?: "))
        netCapitalChange, totalTaxableComponents = calculate(year)
        print("\n-------------------------------------------------------------------------------------\n")
        print("Net Capital Change is: ", netCapitalChange, "\n")
        print("-------------------------------------------------------------------------------------\n")
        print("Components are: ", totalTaxableComponents, "\n")
        print("-------------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
