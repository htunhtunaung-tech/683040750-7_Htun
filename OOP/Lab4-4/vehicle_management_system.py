"""
Htun Htun Aung
683040750-7
P2
"""
from abc import ABC, abstractmethod

class Vehicle(ABC):
    """
    Docstring for Vehicle

    This class defines basic vehicle information and enforces
    engine control methods for subclasses.

    Attributes:
        make (str): Manufacturer of the vehicle.
        model (str): Model name of the vehicle.
        year (int): Year of manufacture.
        is_running (bool): Engine running status.
    """
    
    def __init__(self, make, model, year):
        """
        Docstring for __init__
        
        Args:
            make (str): Manufacturer of the vehicle.
            model (str): Model name of the vehicle.
            year (int): Year of manufacture.

        Returns:
            Nothing

        Raises:
            ValueError: If any input value is invalid.
        """

        if not make or not model or year <= 0:
            raise ValueError("Invalid vehicle information")
        
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False
    
    @abstractmethod
    def start_engine(self):
        """Start the vehicle engine."""
        pass

    @abstractmethod
    def stop_engine(self):
        """Stop the vehicle engine."""
        pass

    def get_info(self):
        # return string with the vehicle's year, make, and model
        """
        Docstring for get_info

        Return basic vehicle information.

        Args:
            No argument

        Returns:
            str: Vehicle year, make, and model.
        
        Raises:
            Nothing

        Examples:
            >>> obj.get_info()
            Year: 2023
            Make: Toyota
            Model: HiAce
        """
        return (
            f"Year: {self.year}\n"
            f"Make: {self.make}\n"
            f"Model: {self.model}\n"
        )
    
# superclass
class CommercialVehicle:
    """
    Docstring for CommercialVehicle

    Represents a vehicle capable of carrying cargo.

    Attributes:
        license_number (str): Vehicle license number.
        max_load (float): Maximum cargo weight allowed.
        current_load (float): Current cargo weight.
    """
    
    def __init__(self, license_number, max_load):
        """
        Docstring for __init__
        
        Args:
            license_number (str): Vehicle license number.
            max_load (float): Maximum allowed cargo weight.

        Returns:
            Nothing

        Raises:
            ValueError: If any input value is invalid.
        """

        if not license_number or max_load <= 0:
            raise ValueError("Invalid commercial vehicle data")
        
        self.license_number = license_number 
        self.max_load = max_load
        self.current_load = 0

    def load_cargo(self, weight):
        # Returns True if cargo can be added without exceeding max_load
        """
        Docstring for load_cargo
        
        Load cargo onto the vehicle.

        Args:
            weight (float): Weight of cargo to load.

        Returns:
            bool or str: True if loading is successful,
            otherwise an error message.

        Raises:
            Nothing

        Examples:
            >>> obj.load_cargo(200)
            True
        """
        if weight <= 0:
            return "Invalid weight"
        
        if self.current_load + weight <= self.max_load:
            self.current_load += weight
            return True
        else:
            return "The weight exceeds the maximum load."

    def unload_cargo(self, weight):
        """
        Docstring for unload_cargo
        
        Unload cargo from the vehicle.

        Args:
            weight (float): Weight of cargo to remove.

        Returns:
            float: Updated current cargo load.

        Raises:
            Nothing

        Examples:
            >>> obj.unload_cargo()
            100
        """
        
        if weight <= self.current_load:
            self.current_load -= weight
            return self.current_load
        else:
            self.current_load = 0
            return self.current_load

# child class
class Car(Vehicle):
    """
    Docstring for Car

    Passenger car that inherits from Vehicle.

    Attributes:
        num_doors (int): Number of doors.
    """

    def __init__(self, make, model, year, num_doors):
        """
        Docstring for __init__
        
        Args:
            make (str): Manufacturer of the car.
            model (str): Model name.
            year (int): Year of manufacture.
            num_doors (int): Number of doors.

        Raises:
            ValueError: If num_doors is invalid.
        """

        if num_doors <= 0:
            raise ValueError("Number of doors must be positive")
        
        super().__init__(make, model, year)
        self.num_doors  = num_doors  

    # Implement 
    def start_engine(self):
        """
        Docstring for start_engine
        
        Args:
            No argument

        Returns:
            str: Status message.

        Raises:
            Nothing

        Examples:
            >>> obj.start_engine()
            Car engine started
        """
        self.is_running = True
        return "Car engine started"

    def stop_engine(self):
        """
        Docstring for stop_engine
        
        Args:
            No argument

        Returns:
            str: Status message.

        Raises:
            Nothing

        Examples:
            >>> obj.stop_engine()
            Car engine stopped
        """
        self.is_running = False
        return "Car engine stopped"

class Trailer(CommercialVehicle):
    """
    Docstring for Trailer

    Trailer used for transporting cargo.

    Attributes:
        num_axles (int): Number of axles supporting the trailer.
    """
    def __init__(self, license_number, max_load, num_axles = 2):
        """
        Docstring for __init__
        
        Args:
            make (str): Manufacturer of the car.
            model (str): Model name.
            year (int): Year of manufacture.
            num_axles (int): Number of axles.

        Raises:
            ValueError: If num_axles is invalid.
        """

        if num_axles <= 0:
            raise ValueError("Axles must be greater than zero")
        
        super().__init__(license_number, max_load)
        self.num_axles = num_axles 

    def get_weight_per_axle(self):
        # returns the current load divided by number of axle
        """
        Docstring for get_weight_per_axle
        
        Args:
            No argument

        Returns:
            float: Weight distributed per axle.

        Raises:
            Nothing

        Examples:
            >>> obj.get_weight_per_axle()
            100.0
        """
        return self.current_load / self.num_axles

class DeliveryVan(Car, CommercialVehicle):
    """
    Docstring for DeliveryVan

    Delivery van with driving and cargo capabilities.

    Attributes:
        delivery_mode (bool): Indicates whether delivery mode is active.
    """

    def __init__(self, make, model, year, num_doors, license_number, max_load):
        """
        Docstring for __init__
        
        Args:
            make (str): Manufacturer of the van.
            model (str): Model name.
            year (int): Year of manufacture.
            num_doors (int): Number of doors.
            license_number (str): License number.
            max_load (float): Maximum cargo capacity.

        Raises:
            Nothing
        """
        Car.__init__(self, make, model, year, num_doors)
        CommercialVehicle.__init__(self, license_number, max_load)
        self.delivery_mode = False

    def toggle_delivery_mode(self):
        """
        Docstring for toggle_delivery_mode
        
        Args:
            No argument

        Returns:
            str: Delivery mode status message.

        Raises:
            Nothing

        Examples:
            >>> obj.toggle_delivery_mode()
            Delivery mode ON
        """
        # Switches delivery_mode between True and False
        self.delivery_mode = not self.delivery_mode

        # returns a status message
        return f"Delivery mode {'ON' if self.delivery_mode == True else 'OFF'}"
    
    def get_info(self):
        """
        Docstring for get_info

        Return full delivery van information.
        
        Args:
            No argument

        Returns:
            str: Complete van details.

        Raises:
            Nothing

        Examples:
            >>> obj.get_info()
            Year: 2023
            Make: Toyota
            Model: HiAce
            Doors: 4
            License: NK-2049
            Load: 0/400
            Delivery Mode: OFF
        """
        
        return (
            f"{super().get_info()}"
            f"Doors: {self.num_doors}\n"
            f"License: {self.license_number}\n"
            f"Load: {self.current_load}/{self.max_load}\n"
            f"Delivery Mode: {'ON' if self.delivery_mode == True else 'OFF'}"
        )

    def begin_service(self):
        """
        Docstring for begin_service
        
        Run the full delivery service workflow.

        Args:
            No argument

        Returns:
            Nothing

        Raises:
            Nothing

        Examples:
            >>> obj.get_info()
            Year: 2023
            Make: Toyota
            Model: HiAce
            Doors: 4
            License: NK-2056
            Load: 0/500
            Delivery Mode: OFF

            Loading cargo...
            Load: 200/500

            Car engine started

            Delivery mode ON

            Car engine stopped

            Unloading cargo...
            Load: 0/500

            Delivery mode OFF
            
        """
        print(self.get_info())
        print()

        print("Loading cargo...")
        self.load_cargo(200)
        print(f"Load: {self.current_load}/{self.max_load}\n")

        print(self.start_engine())
        print()
        print(self.toggle_delivery_mode())
        print()

        print(self.stop_engine())
        print()
        print("Unloading cargo...")
        self.unload_cargo(200)
        print(f"Load: {self.current_load}/{self.max_load}\n")

        print(self.toggle_delivery_mode())
        print()

# ===================== TEST SECTION =====================

if __name__ == "__main__":

    van = DeliveryVan("Toyota", "HiAce", 2023, 4, "NK-2056", 500)
    van.begin_service()

    trailer = Trailer("KK-5046", 1000, 4)
    print("Initial load:", trailer.current_load)

    print("Load 400 kg:", trailer.load_cargo(400))
    print("Current load:", trailer.current_load)
    print("Weight per axle:", trailer.get_weight_per_axle())

    print("Load 700 kg (should exceed):", trailer.load_cargo(700))
    print("Current load:", trailer.current_load)

    print("Unload 150 kg:", trailer.unload_cargo(150))
    print("Current load:", trailer.current_load)
    print("Weight per axle:", trailer.get_weight_per_axle())

    print("Unload 500 kg (over unload):", trailer.unload_cargo(500))
    print("Current load:", trailer.current_load)
    print("Weight per axle:", trailer.get_weight_per_axle())