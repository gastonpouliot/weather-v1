from machine import Pin, I2C        # importing relevant modules & classes
from time import sleep
import bme280       # importing BME280 library

# Initialize I2C
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # initializing the I2C method 
bme = bme280.BME280(i2c=i2c)  # BME280 object created

while True:
    # Get sensor values: temperature, pressure (hPa), and humidity
    temp, pressure, humidity = bme.values
    
    # Convert pressure from hPa to kPa and round to one decimal place
    pressure_kPa = round(float(pressure[:-3]) / 10.0, 1)  # Remove "hPa" from string, convert to kPa, and round to 1 decimal
    
    # Round temperature and humidity to one decimal place
    temp = round(float(temp[:-1]), 1)  # Round temperature (remove "C" and round)
    humidity = round(float(humidity[:-1]), 1)  # Round humidity (remove "%" and round)
    
    # Print the results with temperature, pressure, and humidity rounded to one decimal place
    print("Temperature: {:.1f} C, Pressure: {:.1f} kPa, Humidity: {:.1f}%".format(temp, pressure_kPa, humidity))
    
    # Delay for 10 seconds
    sleep(10)
