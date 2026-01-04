from datetime import datetime, timedelta
from cat import Cat   # import the Cat class

cat1 = Cat("Milo", "British Shorthair", 2, "Alice")
cat2 = Cat("Luna", "Siamese", 3, "Bob")
cat3 = Cat("Oliver", "Persian", 1, "Chris")

# ---- First cat ----
# Show the date_in
print("First cat date_in:")
print(cat1.get_time_in())

# Let the cat greet you
cat1.greet()

print("\n----------------------\n")

# ---- Second cat ----
# Show the date_out
print("Second cat date_out (before):")
print(cat2.get_time_out())

# Change the date_out to be +2 days from now
new_date_out = datetime.now() + timedelta(days=2)
cat2.set_time_out(new_date_out)

# Show the date_out again
print("Second cat date_out (after +2 days):")
print(cat2.get_time_out())

print("\n----------------------\n")

# ---- Third cat ----
# Change the owner name
cat3.owner = "David"

# Change the age
cat3.age = 2

# ---- Show details of all 3 cats ----
print("Details of all cats:\n")
cat1.print_cat()
cat2.print_cat()
cat3.print_cat()

# ---- Show total number of cats ----
print("Total number of cats:", Cat.get_num())

# ---- Reset number of cats ----
Cat.reset_cat()

# ---- Show total number of cats again ----
print("Total number of cats after reset:", Cat.get_num())
