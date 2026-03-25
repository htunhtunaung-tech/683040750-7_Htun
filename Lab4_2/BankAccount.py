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
    __type_saving = 1   # Code for saving account
    __type_loan = 2     # Code for loan account


    # Constructor
    def __init__(self, name, acc_type="saving", balance=0):
        if not name:
            raise ValueError("Name is required")

        self.name = name
        self.type = acc_type
        self.balance = balance

        # Generate account number
        if acc_type == "saving":
            # Increase saving running number
            BankAccount.last_saving_number += 1
            running = BankAccount.last_saving_number
            type_code = BankAccount.__type_saving
        else:
            # Increase loan running number
            BankAccount.last_loan_number += 1
            running = BankAccount.last_loan_number
            type_code = BankAccount.__type_loan
            
        # Create account number in format: branch-type-running
        self.account_number = f"{BankAccount.branch_number}-{type_code}-{running}"

    # Instance methods
    def print_customer(self):
        print("----- Customer Record -----")
        print(f"Name: {self.name}")
        print(f"Account number: {self.account_number}")
        print(f"Account type: {self.type}")
        print(f"Balance: {self.balance}")
        print("----- End Record -----")

    def deposit(self, amount=0):
        self.balance += amount   # Add amount to balance
        return self.balance      # Return updated balance

    def pay_loan(self, amount=0):
        self.balance += amount # Paying loan reduces debt
        return self.balance    # Return updated balance