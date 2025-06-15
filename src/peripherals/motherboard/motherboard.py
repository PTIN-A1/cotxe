import os
import subprocess

ENVIRONMENT = os.getenv("ENVIRONMENT", "virtual")

class Motherboard:

def read_temperature():
    if ENVIRONMENT == "physical":
        route = "/sys/class/thermal/thermal_zone0/temp"
        try:
            with open(route, "r") as read_file:
                temperature_raw = read_file.read().strip()
                temperature_c = int(temperature_raw) / 1000
                return f"{temperature_c:.1f} °C"
        except FileNotFoundError:
            return f"Error: File {route} not found. Are you in a Raspberry Pi?"
        except Exception as e:
            return f"Error while reading temperature: {e}"
    else:
        try:
            result = subprocess.run(["sensors"], capture_output=True, text=True, check=True)
            return result.stdout
        except FileNotFoundError:
            return "Error: Command 'sensors' is not available in this system."
        except subprocess.CalledProcessError as e:
            return f"Error while executing 'sensors': {e}"
