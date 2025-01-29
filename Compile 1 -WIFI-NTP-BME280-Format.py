import network
import time
import ntptime
import config  # Import the config file
from machine import Pin, I2C
import bme280       # BME280 library

# Day names mapping
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Initialize I2C for the BME280 sensor
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # initializing the I2C method
bme = bme280.BME280(i2c=i2c)  # BME280 object created

def connect_wifi():
    """Connects the Raspberry Pi Pico W to WiFi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(config.WIFI_SSID, config.WIFI_PW)  # Use credentials from config.py
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected to WiFi')
    print('IP Address:', wlan.ifconfig()[0])

def get_time_in_eastern():
    """Fetches the time from an NTP server and adjusts it to Eastern Time."""
    ntptime.settime()  # This will set the time to UTC
    time.sleep(2)  # Allow time for the NTP time to be set

    # Get the current UTC time
    current_time = time.localtime()

    # Adjust for Eastern Time Zone (UTC - 5 hours)
    eastern_time = time.localtime(time.mktime(current_time) - 5 * 3600)

    # Get the day of the week name
    day_of_week = day_names[eastern_time[6]]

    # Format the time to include the day of the week
    formatted_time_with_day = "{:04}/{:02}/{:02}, {:02}:{:02}:{:02}".format(
        eastern_time[0], eastern_time[1], eastern_time[2],
        eastern_time[3], eastern_time[4], eastern_time[5]
    )
    
    return formatted_time_with_day

def read_bme280_sensor():
    """Reads and returns temperature, pressure, and humidity from the BME280 sensor."""
    temp, pressure, humidity = bme.values
    
    # Convert pressure from hPa to kPa and round to one decimal place
    pressure_kPa = round(float(pressure[:-3]) / 10.0, 1)  # Remove "hPa" from string, convert to kPa, and round to 1 decimal
    
    # Round temperature and humidity to one decimal place
    temp = round(float(temp[:-1]), 1)  # Round temperature (remove "C" and round)
    humidity = round(float(humidity[:-1]), 1)  # Round humidity (remove "%" and round)
    
    return temp, pressure_kPa, humidity

def main():
    """Main function to connect to WiFi, get time, and display sensor data every 5 minutes."""
    connect_wifi()

    while True:
        # Get the current time in Eastern Time format
        current_time = get_time_in_eastern()
        
        # Read sensor data
        temp, pressure, humidity = read_bme280_sensor()

        # Print the formatted data
        print(f"{current_time}, {temp:.1f}C, {pressure:.1f} kPa, {humidity:.1f}%")
        
        # Wait for 5 minutes (300 seconds) before refreshing the data
        time.sleep(300)

if __name__ == "__main__":
    main()
