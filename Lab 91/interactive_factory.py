from factory_pattern import VehicleFactory

def interactive_vehicle_creator():
    print("=== Interactive Vehicle Creator ===")
    print("Welcome to the Vehicle Factory!")
    
    while True:
        print(f"\nAvailable vehicle types: {', '.join(VehicleFactory.get_available_types())}")
        print("Enter 'quit' to exit")
        
        vehicle_type = input("Enter vehicle type: ").strip()
        
        if vehicle_type.lower() == 'quit':
            print("Thank you for using the Vehicle Factory!")
            break
        
        try:
            model = input("Enter model name (or press Enter for default): ").strip()
            model = model if model else None
            
            # Create vehicle using factory
            vehicle = VehicleFactory.create_vehicle(vehicle_type, model)
            
            print(f"\n✓ Created: {vehicle.get_info()}")
            
            # Interactive vehicle operations
            while True:
                action = input("Choose action (start/stop/info/new): ").strip().lower()
                
                if action == "start":
                    print(vehicle.start_engine())
                elif action == "stop":
                    print(vehicle.stop_engine())
                elif action == "info":
                    print(vehicle.get_info())
                elif action == "new":
                    break
                else:
                    print("Invalid action. Use: start, stop, info, or new")
        
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    interactive_vehicle_creator()

