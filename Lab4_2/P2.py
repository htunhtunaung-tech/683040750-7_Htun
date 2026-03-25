"""
Htun Htun Aung
683040750-7
"""

from cat import Cat

# Create cats
cat1 = Cat("Milo", 3, "British Shorthair", "Gray")
cat2 = Cat.from_birth_year("Luna", 2016, "Siamese", "White")

# Interactions
print(cat1.meow())
print(cat1.play(10))
print(cat1.eat(15))
print(cat1.sleep(5))

# Status
print("Cat 1 status:", cat1.get_status())

# Class method usage
print("Species info:", Cat.get_species_info())
print("Total cats:", Cat.total_cats)

# Static method usage
print("Is Luna senior?", Cat.is_senior(cat2.age))
print("Recommended food (4kg):", Cat.calculate_healthy_food_amount(4), "grams")
