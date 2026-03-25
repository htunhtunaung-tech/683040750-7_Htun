"""
Htun Htun Aung
683040750-7
Lab 4-4 
P2
"""

from vehicle_management_system import Vehicle, CommercialVehicle, Car, Trailer, DeliveryVan


def main():
    """Main function to test all vehicle classes."""
    
    print("=" * 60)
    print("VEHICLE MANAGEMENT SYSTEM - TESTING")
    print("=" * 60)
    
    # Test Car class
    print("\n### Testing Car Class ###")
    car1 = Car("Toyota", "Camry", 2023, 4)
    print(f"Car created: {car1.get_info()}")
    car1.start_engine()
    car1.start_engine()  # Try starting again
    car1.stop_engine()
    car1.stop_engine()  # Try stopping again
    
    # Test Trailer class
    print("\n### Testing Trailer Class ###")
    trailer1 = Trailer("TRL-12345", 5000, 3)
    print(f"Trailer created with license: {trailer1.license_number}")
    print(f"Max load: {trailer1.max_load}, Axles: {trailer1.num_axles}")
    trailer1.load_cargo(3000)
    print(f"Weight per axle: {trailer1.get_weight_per_axle()}")
    trailer1.load_cargo(2500)  # Should fail - exceeds max load
    trailer1.unload_cargo(1000)
    print(f"Weight per axle: {trailer1.get_weight_per_axle()}")
    trailer1.unload_cargo(5000)  # Unload more than current - should reset to 0
    
    # Test edge case: zero axles
    print("\n### Testing Edge Case: Zero Axles ###")
    trailer2 = Trailer("TRL-99999", 1000, 0)
    trailer2.load_cargo(500)
    print(f"Weight per axle with 0 axles: {trailer2.get_weight_per_axle()}")
    
    # Test DeliveryVan class
    print("\n### Testing DeliveryVan Class (Multiple Inheritance) ###")
    van1 = DeliveryVan("Ford", "Transit", 2024, 4, "VAN-ABC123", 1500)
    print(f"Van created: {van1.get_info()}")
    
    # Test toggle delivery mode
    print("\n### Testing Delivery Mode Toggle ###")
    van1.toggle_delivery_mode()
    van1.toggle_delivery_mode()
    
    # Test begin_service workflow
    print("\n### Testing Complete Service Workflow ###")
    van1.begin_service()
    
    # Test input validation
    print("\n### Testing Input Validation ###")
    van2 = DeliveryVan("Mercedes", "Sprinter", 2024, 2, "VAN-XYZ789", 2000)
    van2.load_cargo(-100)  # Negative weight
    van2.load_cargo(2500)  # Exceeds max load
    van2.load_cargo(1000)  # Valid load
    van2.unload_cargo(-50)  # Negative weight
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()