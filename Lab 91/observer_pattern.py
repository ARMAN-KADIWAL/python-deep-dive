from abc import ABC, abstractmethod
from typing import List

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, subject, data):
        pass

# Subject interface
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass
    
    @abstractmethod
    def detach(self, observer: Observer):
        pass
    
    @abstractmethod
    def notify(self):
        pass

# Concrete Subject - Weather Station
class WeatherStation(Subject):
    def __init__(self):
        self._observers: List[Observer] = []
        self._temperature = 0
        self._humidity = 0
        self._pressure = 0
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer {observer.__class__.__name__} attached")
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Observer {observer.__class__.__name__} detached")
    
    def notify(self):
        print(f"Notifying {len(self._observers)} observers...")
        for observer in self._observers:
            observer.update(self, {
                'temperature': self._temperature,
                'humidity': self._humidity,
                'pressure': self._pressure
            })
    
    def set_weather_data(self, temperature, humidity, pressure):
        print(f"\nWeather Station: New data received")
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Pressure: {pressure} hPa")
        
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        
        self.notify()
    
    def get_weather_data(self):
        return {
            'temperature': self._temperature,
            'humidity': self._humidity,
            'pressure': self._pressure
        }

# Concrete Observers
class CurrentConditionsDisplay(Observer):
    def __init__(self, name="Current Conditions"):
        self.name = name
    
    def update(self, subject, data):
        print(f"\n[{self.name}] Current conditions:")
        print(f"  Temperature: {data['temperature']}°C")
        print(f"  Humidity: {data['humidity']}%")
        print(f"  Pressure: {data['pressure']} hPa")

class StatisticsDisplay(Observer):
    def __init__(self, name="Statistics"):
        self.name = name
        self.temperatures = []
        self.max_temp = float('-inf')
        self.min_temp = float('inf')
    
    def update(self, subject, data):
        temp = data['temperature']
        self.temperatures.append(temp)
        
        if temp > self.max_temp:
            self.max_temp = temp
        if temp < self.min_temp:
            self.min_temp = temp
        
        avg_temp = sum(self.temperatures) / len(self.temperatures)
        
        print(f"\n[{self.name}] Temperature Statistics:")
        print(f"  Average: {avg_temp:.1f}°C")
        print(f"  Max: {self.max_temp}°C")
        print(f"  Min: {self.min_temp}°C")
        print(f"  Readings: {len(self.temperatures)}")

class ForecastDisplay(Observer):
    def __init__(self, name="Forecast"):
        self.name = name
        self.last_pressure = 0
    
    def update(self, subject, data):
        current_pressure = data['pressure']
        
        if self.last_pressure == 0:
            forecast = "Initial reading - no forecast available"
        elif current_pressure > self.last_pressure:
            forecast = "Weather improving - expect clear skies"
        elif current_pressure < self.last_pressure:
            forecast = "Weather deteriorating - expect storms"
        else:
            forecast = "Weather stable - no significant changes"
        
        print(f"\n[{self.name}] Weather Forecast:")
        print(f"  Pressure trend: {current_pressure} hPa (was {self.last_pressure} hPa)")
        print(f"  Forecast: {forecast}")
        
        self.last_pressure = current_pressure

# Mobile App Observer
class MobileAppNotification(Observer):
    def __init__(self, user_name):
        self.user_name = user_name
    
    def update(self, subject, data):
        # Simulate mobile notification
        if data['temperature'] > 30:
            alert = "🔥 Hot weather alert!"
        elif data['temperature'] < 0:
            alert = "❄️ Freezing weather alert!"
        elif data['humidity'] > 80:
            alert = "💧 High humidity alert!"
        else:
            alert = "📱 Weather update"
        
        print(f"\n[Mobile App - {self.user_name}] {alert}")
        print(f"  Current: {data['temperature']}°C, {data['humidity']}% humidity")

# Demonstration function
def demonstrate_observer_pattern():
    print("=== Weather Station Observer Pattern Demo ===")
    
    # Create weather station (subject)
    weather_station = WeatherStation()
    
    # Create observers
    current_display = CurrentConditionsDisplay()
    stats_display = StatisticsDisplay()
    forecast_display = ForecastDisplay()
    mobile_app1 = MobileAppNotification("John")
    mobile_app2 = MobileAppNotification("Sarah")
    
    # Attach observers
    print("\n--- Attaching Observers ---")
    weather_station.attach(current_display)
    weather_station.attach(stats_display)
    weather_station.attach(forecast_display)
    weather_station.attach(mobile_app1)
    weather_station.attach(mobile_app2)
    
    # Simulate weather data changes
    print("\n" + "="*50)
    weather_station.set_weather_data(25, 65, 1013)
    
    print("\n" + "="*50)
    weather_station.set_weather_data(32, 70, 1015)
    
    print("\n" + "="*50)
    weather_station.set_weather_data(18, 85, 1008)
    
    # Detach an observer
    print("\n--- Detaching Mobile App (John) ---")
    weather_station.detach(mobile_app1)
    
    print("\n" + "="*50)
    weather_station.set_weather_data(-2, 45, 1020)

if __name__ == "__main__":
    demonstrate_observer_pattern()

