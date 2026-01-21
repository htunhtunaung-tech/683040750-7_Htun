"""
Htun Htun Aung
683040750-7
Lab 4-4 
P2
"""

from abc import ABC, abstractmethod

class Vehicle(ABC):
    
    def __init__(self, make, model, year):
        """
        Initialize a Vehicle instance.

        Args:
            make (str): The manufacturer of the vehicle
            model (str): The model name of the vehicle
            year (int): The year the vehicle was manufactured
        """
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False
        
    @abstractmethod
    def start_engine(self):
        """Abstract method to start the vehicle's engine."""
        pass
    
    @abstractmethod
    def stop_engine(self):
        """Abstract method to stop the vehicle's engine."""
        pass
    
    
    def get_info(self):
        """
        Get formatted information about the vehicle.
        
        Returns:
            str: A string containing the year, make, and model
        """
        return f"{self.year} {self.make} {self.model}"
    
class CommercialVehicle:
    """
    Class representing a commercial vehicle with cargo capabilities.
    
    This class manages the commercial aspects of vehicles including
    licensing and cargo loading/unloading.
    """
    
    def __init__(self, license_number, max_load):
        """
        Initialize a CommercialVehicle instance.

        Args:
            license_number (str): The license plate number
            max_load (float): Maximum weight capacity in appropraite units
        """
        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0
        
    def load_cargo(self, weight):
        """
        Attempt to load cargo onto the vehicle.

        Args:
            weight (float): Weight of cargo to load
            
        Returns:
            bool: True if cargo was successfully loaded, False otherwise
        """
        
        if weight < 0:
            print("Error: Weight cannot be negative")
            return False
        
        if self.current_load + weight <= self.max_load:
            self.current_load += weight
            print(f"Loaded {weight} units. Current load: {self.current_load}/{self.max_load}")
            return True
        else:
            print(f"Cannot load {weight} units. Would exceed max load of {self.max_load}")
            return False
        
    def unload_cargo(self, weight):
        """
        Unload cargo from the vehicle.
        
        Args:
            weight (float): Weight of cargo to unload
            
        Returns:
            float: Current load after unloading
        """
        if weight < 0:
            print("Error: Weight cannot be negative")
            return self.current_load
        
        if weight >= self.current_load:
            print(f"Unloading all cargo. Removed {self.current_load} units.")
            self.current_load = 0
        else:
            self.current_load -= weight
            print(f"Unloaded {weight} units. Current load: {self.current_load}")
        
        return self.current_load


class Car(Vehicle):
    """
    Class representing a car, inheriting from Vehicle.
    
    Implements the abstract methods from Vehicle and adds car-specific
    attributes like number of doors.
    """
    
    def __init__(self, make, model, year, num_doors):
        """
        Initialize a Car instance.
        
        Args:
            make (str): The manufacturer of the car
            model (str): The model name of the car
            year (int): The year the car was manufactured
            num_doors (int): Number of doors on the car
        """
        super().__init__(make, model, year)
        self.num_doors = num_doors
    
    def start_engine(self):
        """Start the car's engine."""
        if not self.is_running:
            self.is_running = True
            print(f"{self.get_info()} engine started.")
        else:
            print(f"{self.get_info()} engine is already running.")
    
    def stop_engine(self):
        """Stop the car's engine."""
        if self.is_running:
            self.is_running = False
            print(f"{self.get_info()} engine stopped.")
        else:
            print(f"{self.get_info()} engine is already off.")


class Trailer(CommercialVehicle):
    """
    Class representing a trailer, inheriting from CommercialVehicle.
    
    Adds trailer-specific functionality like axle-based weight distribution.
    """
    
    def __init__(self, license_number, max_load, num_axles=2):
        """
        Initialize a Trailer instance.
        
        Args:
            license_number (str): The license plate number
            max_load (float): Maximum weight capacity
            num_axles (int): Number of axles (default: 2)
        """
        super().__init__(license_number, max_load)
        self.num_axles = num_axles
    
    def get_weight_per_axle(self):
        """
        Calculate the weight distributed per axle.
        
        Returns:
            float: Weight per axle, or 0 if no axles
        """
        if self.num_axles == 0:
            print("Error: Cannot divide by zero axles")
            return 0
        
        weight_per_axle = self.current_load / self.num_axles
        return weight_per_axle


class DeliveryVan(Car, CommercialVehicle):
    """
    Class representing a delivery van with multiple inheritance.
    
    Inherits from both Car and CommercialVehicle, combining passenger
    vehicle capabilities with commercial cargo handling.
    """
    
    def __init__(self, make, model, year, num_doors, license_number, max_load):
        """
        Initialize a DeliveryVan instance.
        
        Args:
            make (str): The manufacturer of the van
            model (str): The model name of the van
            year (int): The year the van was manufactured
            num_doors (int): Number of doors on the van
            license_number (str): The license plate number
            max_load (float): Maximum cargo weight capacity
        """
        Car.__init__(self, make, model, year, num_doors)
        CommercialVehicle.__init__(self, license_number, max_load)
        self.delivery_mode = False
    
    def toggle_delivery_mode(self):
        """
        Toggle the delivery mode on or off.
        
        Returns:
            str: Status message indicating the current delivery mode
        """
        self.delivery_mode = not self.delivery_mode
        status = "ON" if self.delivery_mode else "OFF"
        message = f"Delivery mode is now {status}"
        print(message)
        return message
    
    def get_info(self):
        """
        Get comprehensive information about the delivery van.
        
        Returns:
            str: Detailed information including vehicle details and commercial info
        """
        base_info = super().get_info()
        return (f"{base_info}, {self.num_doors} doors, "
                f"License: {self.license_number}, "
                f"Max Load: {self.max_load}, Current Load: {self.current_load}")
    
    def begin_service(self):
        """
        Execute a complete delivery service cycle.
        
        This method demonstrates the full workflow of a delivery:
        displaying info, loading cargo, starting engine, enabling delivery mode,
        stopping engine, unloading cargo, and disabling delivery mode.
        """
        print("\n=== Beginning Delivery Service ===")
        
        # Display van info
        print(f"Van Info: {self.get_info()}")
        
        # Load cargo
        print("\n--- Loading Cargo ---")
        self.load_cargo(500)
        
        # Start engine
        print("\n--- Starting Engine ---")
        self.start_engine()
        
        # Enable delivery mode
        print("\n--- Activating Delivery Mode ---")
        self.toggle_delivery_mode()
        
        print("\n[Simulating delivery in progress...]")
        
        # Stop engine
        print("\n--- Stopping Engine ---")
        self.stop_engine()
        
        # Unload cargo
        print("\n--- Unloading Cargo ---")
        self.unload_cargo(500)
        
        # Disable delivery mode
        print("\n--- Deactivating Delivery Mode ---")
        self.toggle_delivery_mode()
        
        print("\n=== Delivery Service Complete ===\n")