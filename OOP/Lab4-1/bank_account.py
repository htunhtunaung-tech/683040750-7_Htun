"""
Htun Htun Aung
683040750-7
"""

class BankAccount:
    # Class attribute
    branch_name = "KKU Complex"
    branch_number = 1724
    last_loan_number = 0
    last_saving_number = 0

    # Private class attributes (account types)
    __type_saving = 1
    __type_loan = 2

    # Constructor
    def __init__(self, name, acc_type, balance=0):
        self.name = name
        self.balance = balance

        if acc_type == "saving":
            BankAccount.last_saving_number += 1
            self.account_type = BankAccount.__type_saving
            self.account_number = BankAccount.last_saving_number

        elif acc_type == "loan":
            BankAccount.last_loan_number += 1
            self.account_type = BankAccount.__type_loan
            self.account_number = BankAccount.last_loan_number

        else:
            raise ValueError("Invalid account type")

    # Class method
    @classmethod
    def change_branch_name(cls, new_name):
        cls.branch_name = new_name

    # Instance methods
    def print_customer(self):
        acc = "Saving" if self.account_type == BankAccount.__type_saving else "Loan"
        print("Name:", self.name)
        print("Account Type:", acc)
        print("Account Number:", self.account_number)
        print("Balance:", self.balance)
        print("Branch:", BankAccount.branch_name)

    def deposit(self, amount=0):
        if self.account_type != BankAccount.__type_saving:
            print("Deposit allowed only for saving account")
            return self.balance
        self.balance += amount
        return self.balance

    def withdraw(self, amount=0):
        if self.account_type != BankAccount.__type_saving:
            print("Withdraw allowed only for saving account")
            return self.balance
        self.balance -= amount
        return self.balance

    def pay_loan(self, amount=0):
        if self.account_type != BankAccount.__type_loan:
            print("Pay loan allowed only for loan account")
            return self.balance
        self.balance += amount
        return self.balance

    def get_loan(self, amount=0):
        if self.account_type != BankAccount.__type_loan:
            print("Loan allowed only for loan account")
            return self.balance

        if self.balance >= -50000:
            self.balance -= amount
        else:
            print("Cannot get more loan")
        return self.balance

    # Static method
    @staticmethod
    def calc_interest(bal, int_rate, payment):
        print("----- Loan Plan -----")
        year = 1

        while bal > 0:
            bal = bal + (bal * int_rate / 100)
            pay = min(payment, bal)
            bal -= pay

            print(
                f"Year {year}: loan = {bal + pay:.2f}  "
                f"payment = {pay:.2f}  bal = {bal:.2f}"
            )
            year += 1

        print("----- End Plan -----")
