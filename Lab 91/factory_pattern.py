from abc import ABC, abstractmethod

# Abstract base class for vehicles
class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def stop_engine(self):
        pass
    
    @abstractmethod
    def get_info(self):
        pass

# Concrete vehicle classes
class Car(Vehicle):
    def __init__(self, model="Generic Car"):
        self.model = model
        self.engine_running = False
    
    def start_engine(self):
        self.engine_running = True
        return f"{self.model} engine started. Vroom!"
    
    def stop_engine(self):
        self.engine_running = False
        return f"{self.model} engine stopped."
    
    def get_info(self):
        status = "running" if self.engine_running else "stopped"
        return f"Car: {self.model}, Engine: {status}"

class Motorcycle(Vehicle):
    def __init__(self, model="Generic Motorcycle"):
        self.model = model
        self.engine_running = False
    
    def start_engine(self):
        self.engine_running = True
        return f"{self.model} engine started. Roar!"
    
    def stop_engine(self):
        self.engine_running = False
        return f"{self.model} engine stopped."
    
    def get_info(self):
        status = "running" if self.engine_running else "stopped"
        return f"Motorcycle: {self.model}, Engine: {status}"

class Truck(Vehicle):
    def __init__(self, model="Generic Truck"):
        self.model = model
        self.engine_running = False
    
    def start_engine(self):
        self.engine_running = True
        return f"{self.model} engine started. Rumble!"
    
    def stop_engine(self):
        self.engine_running = False
        return f"{self.model} engine stopped."
    
    def get_info(self):
        status = "running" if self.engine_running else "stopped"
        return f"Truck: {self.model}, Engine: {status}"

# Factory class
class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type, model=None):
        vehicle_type = vehicle_type.lower()
        
        if vehicle_type == "car":
            return Car(model or "Toyota Camry")
        elif vehicle_type == "motorcycle":
            return Motorcycle(model or "Harley Davidson")
        elif vehicle_type == "truck":
            return Truck(model or "Ford F-150")
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
    
    @staticmethod
    def get_available_types():
        return ["car", "motorcycle", "truck"]

# Demonstration of Factory Pattern
def demonstrate_factory():
    print("=== Vehicle Factory Demonstration ===")
    print(f"Available vehicle types: {VehicleFactory.get_available_types()}")
    print()
    
    # Create different vehicles using the factory
    vehicles = [
        VehicleFactory.create_vehicle("car", "Honda Civic"),
        VehicleFactory.create_vehicle("motorcycle", "Yamaha R1"),
        VehicleFactory.create_vehicle("truck", "Chevrolet Silverado")
    ]
    
    # Test each vehicle
    for vehicle in vehicles:
        print(vehicle.get_info())
        print(vehicle.start_engine())
        print(vehicle.get_info())
        print(vehicle.stop_engine())
        print("-" * 40)

if __name__ == "__main__":
    demonstrate_factory()

