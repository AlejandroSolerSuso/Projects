import random
import sys


class BankAccount:
    def __init__(self, name, initial_deposit, rate):
        self.owner = name
        self.account_number = str(random.randint(10000000, 99999999))
        self.balance = initial_deposit
        self.rate = rate
        self.log = ["Opened account with £" + str(initial_deposit)]

    def deposit(self, deposit):
        if deposit <= 0:
            print("Can't deposit zero or less.")
            return
        self.balance += deposit
        self.log.append("Deposited £" + str(deposit) + " (Balance: £" + str(self.balance) + ")")

    def withdraw(self, withdraw):
        if withdraw <= 0:
            print("Invalid withdrawal amount.")
            return
        if withdraw > self.balance:
            print("Insufficient funds.")
            return
        self.balance -= withdraw
        self.log.append("Withdrew £" + str(withdraw) + ". Balance: £" + str(self.balance))

    def update_rate(self, new_rate):
        if new_rate < 0:
            print("Interest rate can't be negative.")
            return
        old_rate = self.rate
        self.rate = new_rate
        self.log.append("Rate changed: " + str(old_rate) + "% → " + str(new_rate) + "%")

    def prediction_rate(self, years):
        if years < 0:
            print("Years can't be negative.")
            return self.balance
        rate_decimal = self.rate / 100
        return round(self.balance * ((1 + rate_decimal) ** years), 2)

    def show_log(self):
        return self.log

    def __str__(self):
        return "Account #" + self.account_number + "\nOwner: " + self.owner + "\nBalance: £" + str(round(self.balance, 2)) + "\nInterest Rate: " + str(self.rate) + "%"


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name, deposit, rate):
        if not name.strip():
            print("Name required.")
            return None
        if deposit < 0:
            print("Deposit can't be negative.")
            return None
        if rate < 0:
            print("Invalid interest rate.")
            return None

        account = BankAccount(name, deposit, rate)
        self.accounts[account.account_number] = account
        return account

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def show_all_accounts(self):
        if not self.accounts:
            print("No accounts in system.")
            return
        for account in self.accounts.values():
            print(account)
            print("-" * 40)


def display_menu():
    print("\n==== Bank Menu ====")
    print("1. Open new account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Update interest rate")
    print("5. Project future balance")
    print("6. View account details")
    print("7. View all accounts")
    print("8. View transaction history")
    print("9. Exit")


def main():
    bank = Bank()

    while True:
        display_menu()
        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            name = input("Enter full name: ").strip()
            try:
                deposit = float(input("Initial deposit: £"))
                rate = float(input("Interest rate (%): "))
            except ValueError:
                print("Please enter valid numbers.")
                continue

            account = bank.create_account(name, deposit, rate)
            if account:
                print("Account created! Your number is: " + account.account_number)

        elif choice == "2":
            account_number = input("Account number: ")
            account = bank.get_account(account_number)
            if account:
                try:
                    deposit = float(input("Amount to deposit: £"))
                    account.deposit(deposit)
                except ValueError:
                    print("Invalid number.")
            else:
                print("Account not found.")

        elif choice == "3":
            account_number = input("Account number: ")
            account = bank.get_account(account_number)
            if account:
                try:
                    withdraw = float(input("Amount to withdraw: £"))
                    account.withdraw(withdraw)
                except ValueError:
                    print("Invalid input.")
            else:
                print("Account not found.")

        elif choice == "4":
            account_number = input("Account number: ")
            account = bank.get_account(account_number)
            if account:
                try:
                    new_rate = float(input("New interest rate (%): "))
                    account.update_rate(new_rate)
                except ValueError:
                    print("Enter a valid rate.")
            else:
                print("Account not found.")

        elif choice == "5":
            account_number = input("Account number: ")
            account = bank.get_account(account_number)
            if account:
                try:
                    years = int(input("Years to project: "))
                    future_balance = account.prediction_rate(years)
                    print("In " + str(years) + " years, you’ll have: £" + str(future_balance))
                except ValueError:
                    print("Enter a valid number of years.")
            else:
                print("No such account.")

        elif choice == "6":
            account_number = input("Account number: ")
            account = bank.get_account(account_number)
            print(account if account else "Account not found.")

        elif choice == "7":
            bank.show_all_accounts()

        elif choice == "8":
            account_number = input("Account number: ")
            account = bank.get_account(account_number)
            if account:
                print("Transaction History:")
                for entry in account.show_log():
                    print("• " + entry)
            else:
                print("Account not found.")

        elif choice == "9":
            print("Thanks for using our bank!")
            break
        else:
            print("That’s not a valid option.")


if __name__ == "__main__":
    main()
