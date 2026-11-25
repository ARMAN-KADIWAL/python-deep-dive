#!/usr/bin/env python3
"""
Design Patterns Demonstration Script
This script demonstrates how Singleton, Factory, and Observer patterns
can be used together to create maintainable and structured code.
"""

import time
import random
from singleton_pattern import SingletonDatabaseConnection
from factory_pattern import VehicleFactory
from observer_pattern import WeatherStation, CurrentConditionsDisplay, StatisticsDisplay

class ApplicationLogger:
    """Singleton pattern for application logging"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApplicationLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.logs = []
            ApplicationLogger._initialized = True
    
    def log(self, message, level="INFO"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def get_logs(self):
        return self.logs

class VehicleFleetManager:
    """Demonstrates Factory pattern for creating different vehicles"""
    
    def __init__(self):
        self.fleet = []
        self.logger = ApplicationLogger()
    
    def add_vehicle(self, vehicle_type, model=None):
        try:
            vehicle = VehicleFactory.create_vehicle(vehicle_type, model)
            self.fleet.append(vehicle)
            self.logger.log(f"Added {vehicle_type} to fleet: {vehicle.get_info()}")
            return vehicle
        except ValueError as e:
            self.logger.log(f"Failed to add vehicle: {e}", "ERROR")
            return None
    
    def start_all_vehicles(self):
        self.logger.log("Starting all vehicles in fleet")
        for vehicle in self.fleet:
            result = vehicle.start_engine()
            self.logger.log(result)
    
    def get_fleet_status(self):
        status = []
        for vehicle in self.fleet:
            status.append(vehicle.get_info())
        return status

class FleetMonitor:
    """Observer that monitors fleet status"""
    
    def __init__(self, name):
        self.name = name
        self.logger = ApplicationLogger()
    
    def update(self, subject, data):
        self.logger.log(f"Fleet Monitor {self.name}: Received update - {data}")

def demonstrate_patterns_integration():
    """Main demonstration function showing all patterns working together"""
    
    print("="*70)
    print("DESIGN PATTERNS INTEGRATION DEMONSTRATION")
    print("="*70)
    
    # 1. Singleton Pattern - Logger
    print("\n1. SINGLETON PATTERN - Application Logger")
    print("-" * 50)
    
    logger1 = ApplicationLogger()
    logger2 = ApplicationLogger()
    
    logger1.log("First logger instance created")
    logger2.log("Second logger instance created")
    
    print(f"Are logger1 and logger2 the same instance? {logger1 is logger2}")
    print(f"Total logs: {len(logger1.get_logs())}")
    
    # 2. Factory Pattern - Vehicle Fleet
    print("\n2. FACTORY PATTERN - Vehicle Fleet Management")
    print("-" * 50)
    
    fleet_manager = VehicleFleetManager()
    
    # Create different types of vehicles
    fleet_manager.add_vehicle("car", "Toyota Prius")
    fleet_manager.add_vehicle("truck", "Ford Transit")
    fleet_manager.add_vehicle("motorcycle", "Honda CBR")
    
    # Try to create invalid vehicle
    fleet_manager.add_vehicle("airplane", "Boeing 747")  # This will fail
    
    print(f"\nFleet Status:")
    for status in fleet_manager.get_fleet_status():
        print(f"  - {status}")
    
    fleet_manager.start_all_vehicles()
    
    # 3. Observer Pattern - Weather Monitoring
    print("\n3. OBSERVER PATTERN - Weather Monitoring System")
    print("-" * 50)
    
    weather_station = WeatherStation()
    
    # Create observers
    display1 = CurrentConditionsDisplay("Main Display")
    display2 = CurrentConditionsDisplay("Backup Display")
    stats = StatisticsDisplay("Statistics Center")
    
    # Attach observers
    weather_station.attach(display1)
    weather_station.attach(display2)
    weather_station.attach(stats)
    
    # Simulate weather changes
    weather_data = [
        (22, 60, 1013),
        (25, 65, 1015),
        (28, 70, 1012),
        (24, 55, 1018)
    ]
    
    for temp, humidity, pressure in weather_data:
        weather_station.set_weather_data(temp, humidity, pressure)
        time.sleep(1)  # Small delay for better visualization
    
    # 4. Patterns Working Together
    print("\n4. PATTERNS WORKING TOGETHER")
    print("-" * 50)
    
    # Database connection (Singleton) used by multiple components
    db1 = SingletonDatabaseConnection()
    db2 = SingletonDatabaseConnection()
    
    print(f"Database connections are same instance: {db1 is db2}")
    print(db1.execute_query("SELECT * FROM vehicles"))
    print(db2.execute_query("SELECT * FROM weather_data"))
    
    # Show final logs
    print("\n5. FINAL APPLICATION LOGS")
    print("-" * 50)
    
    final_logger = ApplicationLogger()
    print(f"Total application events logged: {len(final_logger.get_logs())}")
    
    print("\nLast 5 log entries:")
    for log in final_logger.get_logs()[-5:]:
        print(f"  {log}")

def interactive_pattern_demo():
    """Interactive demonstration allowing user to explore patterns"""
    
    print("\n" + "="*70)
    print("INTERACTIVE DESIGN PATTERNS EXPLORER")
    print("="*70)
    
    logger = ApplicationLogger()
    fleet_manager = VehicleFleetManager()
    weather_station = WeatherStation()
    display = CurrentConditionsDisplay("Interactive Display")
    weather_station.attach(display)
    
    while True:
        print("\nChoose a pattern to explore:")
        print("1. Singleton Pattern (Logger)")
        print("2. Factory Pattern (Vehicle Creation)")
        print("3. Observer Pattern (Weather Updates)")
        print("4. View Application Logs")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            message = input("Enter a log message: ")
            level = input("Enter log level (INFO/WARNING/ERROR) [INFO]: ").strip() or "INFO"
            logger.log(message, level)
            
        elif choice == "2":
            vehicle_type = input("Enter vehicle type (car/truck/motorcycle): ").strip()
            model = input("Enter model name (optional): ").strip() or None
            vehicle = fleet_manager.add_vehicle(vehicle_type, model)
            if vehicle:
                action = input("Start engine? (y/n): ").strip().lower()
                if action == "y":
                    logger.log(vehicle.start_engine())
                print(vehicle.get_info())

        elif choice == "3":
            try:
                temperature = float(input("Enter temperature (C): "))
                humidity = float(input("Enter humidity (%): "))
                pressure = float(input("Enter pressure (hPa): "))
                if not 0 <= humidity <= 100 or pressure <= 0:
                    print("Invalid humidity or pressure.")
                    continue
                weather_station.set_weather_data(temperature, humidity, pressure)
                logger.log("Weather data updated")
            except ValueError:
                print("Please enter valid numeric values.")

        elif choice == "4":
            print("\nApplication Logs:")
            for entry in logger.get_logs():
                print(entry)

        elif choice == "5":
            print("Exiting Design Patterns Explorer...")
            break

        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    demonstrate_patterns_integration()
    interactive_pattern_demo()
    print("\nLab 91 completed successfully!")

