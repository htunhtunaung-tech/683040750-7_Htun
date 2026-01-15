"""
Htun Htun Aung
683040750-7
"""
from room import Bedroom, Kitchen

bedroom = Bedroom(12, 10, 5)

print(bedroom.describe_room())
print("Area:", bedroom.calculate_area(), "sq ft")
print("Recommended lighting:", bedroom.get_recommended_lighting(), "lumens/sq ft")
print()

kitchen1 = Kitchen(15, 12)

print(kitchen1.describe_room())
print("Area:", kitchen1.calculate_area(), "sq ft")
print("Recommended lighting:", kitchen1.get_recommended_lighting(), "lumens/sq ft")

print("\ncalculate_counter_space docstring:")
print(Kitchen.calculate_counter_space.__doc__)

island_space, wall_space = kitchen1.calculate_counter_space()
print("Island counter space:", island_space, "sq ft")
print("Wall counter space:", wall_space, "sq ft")
print()

kitchen2 = Kitchen(15, 12, has_island=False)

print(kitchen2.describe_room())
print("Area:", kitchen2.calculate_area(), "sq ft")

island_space, wall_space = kitchen2.calculate_counter_space()
print("Isalnd counter space:", island_space, "sq ft")
print("Wall counter space:", wall_space, "sq ft")