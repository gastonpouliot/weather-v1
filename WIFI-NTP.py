import network
import time
import ntptime
import config  # Import the config file

# Day names mapping
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(config.WIFI_SSID, config.WIFI_PW)  # Use credentials from config.py
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected to WiFi')
    print('IP Address:', wlan.ifconfig()[0])

connect_wifi()

# Get time from NTP server
ntptime.settime()  # This will set the time to UTC

# Wait a bit to ensure it sets correctly
time.sleep(2)

# Get the current UTC time
current_time = time.localtime()
print("Current UTC time:", current_time)

# Adjust for Eastern Time Zone (UTC - 5 hours)
eastern_time = time.localtime(time.mktime(current_time) - 5 * 3600)
print("Current Eastern Time:", eastern_time)

# Get the day of the week name
day_of_week = day_names[eastern_time[6]]

# Format the time to include the day of the week
formatted_time_with_day = "{}, {:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
    day_of_week, eastern_time[0], eastern_time[1], eastern_time[2],
    eastern_time[3], eastern_time[4], eastern_time[5]
)

print("Formatted Eastern Time with Day:", formatted_time_with_day)
