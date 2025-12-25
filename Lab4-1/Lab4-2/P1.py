from bank_account import BankAccount

# Change branch name
BankAccount.change_branch_name("KKU Engineering")

# Create saving account
s1 = BankAccount("Aung Aung", "saving", 1000)
s1.deposit(500)
s1.withdraw(200)
s1.print_customer()

print()

# Create loan account
l1 = BankAccount("Htun Htun", "loan", 0)
l1.get_loan(1000)
l1.pay_loan(200)
l1.print_customer()

print()

# Interest calculation
BankAccount.calc_interest(1000, 5, 100)
