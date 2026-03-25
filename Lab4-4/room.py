"""
Htun Htun Aung
683040750-7
"""

from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    @abstractmethod
    def get_purpose(self):
        """Returns a string describing purposes of the room"""
        pass

    @abstractmethod
    def get_recommended_lighting(self):
        """Returns recommended lighting in lumens per square foot"""
        pass

    def calculate_area(self):
        return self.length * self.width
    
    def describe_room(self):
        area = self.calculate_area()
        return f"A {self.__class__.__name__} of {area} sq ft used for {self.get_purpose()}"
    
class Bedroom(Room):
    def __init__(self, length, width, bed_size):
        super().__init__(length, width)
        self.bed_size = bed_size
        
    def get_purpose(self):
        return f"sleeping and resting (bed size: {self.bed_size} ft)"
    
    def get_recommended_lighting(self):
        return 120
    
class Kitchen(Room):
    def __init__(self, length, width, has_island=True):
        super().__init__(length, width)
        self.has_island = has_island
        
    def get_purpose(self):
        return "Cooking and Food Preparation"
    
    def get_recommended_lighting(self):
        return 400
    
    def calculate_counter_space(self):
        """
        Calculates the counter space distribution in the kitchen.

        Parameters
        ----------
        self : Kitchen
        The Kitchen object for which counter space is calculated

        Returns
        -------
        tuple
        A tuple containing:
            - island_counter : float
        Counter space from the kitchen island (0 if no island)
            - wall_counter : float
        Counter space along the kitchen walls

        Examples
        --------
        >>> kitchen = Kitchen(15, 12)
        >>> kitchen.calculate_counter_space()
        (36.0, 45.0)
        """

        area = self.calculate_area()
        
        if self.has_island:
            island_counter = area * (1/5)
            wall_counter = area * (1/4)
        else:
            island_counter = 0
            wall_counter = area * (1/2)
        return island_counter, wall_counter