from util import *

def printWelcomeMessage():
    print("Select an option.")
    print("1) Convert Data After Match")
    print("2) Convert All Match Data")
    print("3) Convert Shot Data")
    print("4) Convert Pit Data")
    print("5) Custom SQL Query")
    print("6) Exit")

def main():
    while True:
        command = input("Would you like to pull? (y/n): ")
        if command.lower() == "y":
            if not pullData():
                print("failed to pull data")
                exit(1)

        printWelcomeMessage()
        command = input(">>> ")
        if command == "6":
            break

        if not command.isnumeric():
            print("invalid command")
            exit(1)
        command = int(command)
        if command < 1 or command > 6:
            print("invalid command")
            exit(1)
        executeCommand(command)

if __name__ == "__main__":
    main()

