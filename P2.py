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
    def __init__(self, name, acc_type="saving", balance=0):
        if not name:
            raise ValueError("Name is required")

        self.name = name
        self.type = acc_type
        self.balance = balance

        # Generate account number
        if acc_type == "saving":
            BankAccount.last_saving_number += 1
            running = BankAccount.last_saving_number
            type_code = BankAccount.__type_saving
        else:
            BankAccount.last_loan_number += 1
            running = BankAccount.last_loan_number
            type_code = BankAccount.__type_loan

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
        self.balance += amount
        return self.balance

    def pay_loan(self, amount=0):
        self.balance += amount
        return self.balance

john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1_000_000)
sarah = BankAccount("Sarah", "saving")

john.deposit(3000)
tim.pay_loan(500_000)

sarah.deposit(50_000_000)
sarah_loan = BankAccount("Sarah", "loan", -100_000_000)

john.print_customer()
tim.print_customer()
sarah.print_customer()
sarah_loan.print_customer()
