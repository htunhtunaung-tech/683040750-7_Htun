from BankAccount import BankAccount   # import class from another file

# Create accounts
john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1_000_000)
sarah = BankAccount("Sarah", "saving")

# Transactions
john.deposit(3000)
tim.pay_loan(500_000)

sarah.deposit(50_000_000)
sarah_loan = BankAccount("Sarah", "loan", -100_000_000)

# Print customer information
john.print_customer()
tim.print_customer()
sarah.print_customer()
sarah_loan.print_customer()
