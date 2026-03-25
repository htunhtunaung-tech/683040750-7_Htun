"""
Htun Htun Aung
683040750-7
"""

from datetime import datetime

class Cat:
    # 1. Class Attributes
    species = "Felis catus"
    total_cats = 0
    average_lifespan = 15

    # 2. Constructor (Instance Attributes)
    def __init__(self, name, age, breed, color):
        self.name = name
        self.age = age
        self.breed = breed
        self.color = color

        # State tracking
        self.hungry = False
        self.energy = 100
        self.happiness = 100

        Cat.total_cats += 1

    # 3. Instance Methods
    def meow(self):
        if self.hungry:
            return f"{self.name} meows loudly: MEEEOOW!"
        elif self.energy < 30:
            return f"{self.name} meows softly: mew..."
        else:
            return f"{self.name} says: Meow!"

    def eat(self, food_amount):
        if food_amount <= 0:
            return "Food amount must be positive."

        self.hungry = False
        self.energy = min(100, self.energy + food_amount * 2)
        self.happiness = min(100, self.happiness + food_amount)

        return f"{self.name} enjoyed the meal."

    def play(self, play_time):
        if play_time <= 0:
            return "Play time must be positive."

        self.energy = max(0, self.energy - play_time * 5)
        self.happiness = min(100, self.happiness + play_time * 4)

        if self.energy < 20:
            self.hungry = True

        return f"{self.name} had fun playing!"

    def sleep(self, hours):
        if hours <= 0:
            return "Sleep hours must be positive."

        self.energy = min(100, self.energy + hours * 10)
        self.hungry = False

        return f"{self.name} slept for {hours} hours."

    def get_status(self):
        return {
            "name": self.name,
            "age": self.age,
            "hungry": self.hungry,
            "energy": self.energy,
            "happiness": self.happiness
        }

    # 4. Class Methods
    @classmethod
    def from_birth_year(cls, name, birth_year, breed, color):
        current_year = datetime.now().year
        age = current_year - birth_year
        return cls(name, age, breed, color)

    @classmethod
    def get_species_info(cls):
        return {
            "species": cls.species,
            "average_lifespan": cls.average_lifespan
        }

    # 5. Static Methods
    @staticmethod
    def is_senior(age):
        return age > 7

    @staticmethod
    def calculate_healthy_food_amount(weight_kg):
        return weight_kg * 20  # grams
