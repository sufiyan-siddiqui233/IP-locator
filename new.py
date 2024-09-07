import requests
from selenium import webdriver
import folium
import datetime
import time
import os

# This method will return coordinates for a given IP address
def locationCoordinates(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        print(f"Fetched location for IP {ip}: {city}, {state} ({lat}, {long})")
        return lat, long, city, state
    except Exception as e:
        # Displaying the error message
        print(f"Error fetching location coordinates for IP {ip}: {e}")
        return None

# Function to get locations for a list of IP addresses
def get_locations(ip_list):
    locations = []
    for ip in ip_list:
        loc = locationCoordinates(ip)
        if loc:
            locations.append(loc)
    return locations

def gps_locator(ip_list):
    obj = folium.Map(location=[0, 0], zoom_start=2)

    try:
        locations = get_locations(ip_list)

        if not locations:
            print("No valid locations to display.")
            return False

        # Add markers for each location
        for lat, long, city, state in locations:
            folium.Marker([lat, long], popup=f'{city}, {state}').add_to(obj)

        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fileName = os.path.join(script_dir, f"Locations_{datetime.date.today()}.html")
        print(f"Saving map to: {fileName}")
        obj.save(fileName)

        return fileName

    except Exception as e:
        print(f"Error in gps_locator: {e}")
        return False

# Main method
if __name__ == "__main__":
    print("---------------GPS Using Python---------------\n")

    # List of example IPs
    ip_list = [
        '8.8.8.8',  # Google Public DNS (Mountain View, CA, USA)
        '1.1.1.1',  # Cloudflare Public DNS (Sydney, Australia)
        '208.67.222.222',  # OpenDNS (San Francisco, CA, USA)
        '128.101.101.101',  # University of Minnesota (Minneapolis, MN, USA)
        '216.58.217.206'    # Google (Mountain View, CA, USA)
    ]

    # Function Calling
    page = gps_locator(ip_list)

    if page and os.path.exists(page):
        print("\nOpening File.............")
        try:
            dr = webdriver.Chrome()
            dr.get(f"file:///{page}")  # Use 'file:///' for local files
            time.sleep(4)
        except Exception as e:
            print(f"Error opening the file in browser: {e}")
        finally:
            dr.quit()
            print("\nBrowser Closed..............")
    else:
        print("Failed to create or find the map file.")













