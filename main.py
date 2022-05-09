from picamera import PiCamera
from time import sleep
from datetime import datetime, timedelta
from pathlib import Path
from orbit import ISS
from skyfield.api import load
from sense_hat import SenseHat
import csv
from logzero import logger, logfile
import reverse_geocoder

# Define needed functions


def convert(angle):
    """
    Convert a `skyfield` Angle to an EXIF-appropriate
    representation (rationals)
    e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    Return a tuple containing a boolean and the converted angle,
    with the boolean indicating if the angle is negative.
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle

def capture(camera, image):
    """Use `camera` to capture an `image` file with lat/long EXIF data."""
    point = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    # Capture the image
    camera.capture(image)

def create_csv(data_file):
    '''Write header in the created .csv file'''
    with open(data_file, 'w', buffering=1) as f:
        writer = csv.writer(f)
        header = header = ("Counter", "Date/time", "Latitude (deg)", "Longitude (deg)", "Altitude (km)", "Location", "B_x", "B_y", "B_z")
        writer.writerow(header)

def add_csv_data(data_file, data):
    '''Add data in a row in the .csv file'''
    with open(data_file, 'a', buffering=1) as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Create a ‘datetime’ variable to store the start time
start_time = datetime.now()

# Create a `datetime` variable to store the current time
now_time = datetime.now()

# Create a 'location of ISS' variable
location = ISS.coordinates()


# Load an 'ephemeris' variable to calculate the position of the Sun with respect the ISS
eph = load('de421.bsp')
timescale = load.timescale()

# Activate the sense_nat
sense = SenseHat()

# Create file and directory where to store data and pictures
base_folder = Path(__file__).parent.resolve()
data_file = base_folder/'data.csv'

create_csv(data_file)

# Create a logfile
logfile(base_folder/"history.log")

# Initialize a counter
counter = 1

# Activate camera
camera = PiCamera()
camera.resolution = (2592,1944)
camera.framerate = 15
#camera.start_preview(alpha=200)

# Run a loop for 180 minutes of experiment 
while (now_time < start_time + timedelta(minutes=176)):
    try:
        # Obtain coordinates of the ISS
        lat = location.latitude.degrees
        long = location.longitude.degrees
        alt = location.elevation.km
        nearest_city = reverse_geocoder.search((lat,long))
        # Measure magnetic field every 12 s
        magnetic = sense.get_compass_raw()
        m_x = magnetic['x']
        m_y = magnetic['y']
        m_z = magnetic['z']
        data = (counter, now_time, lat, long, alt, nearest_city, m_x, m_y, m_z)
        add_csv_data(data_file, data)
        
        # Take a picture every 12 s if it is daylight
        t = timescale.now()
        if ISS.at(t).is_sunlit(eph) == True:
            logger.info("Daylight")
            capture(camera, f"{base_folder}/image_{counter:03d}.jpg")
        elif ISS.at(t).is_sunlit(eph) == False:
            logger.info("Night")

        # log info
        logger.info(f"Iteration {counter}")
        sleep(12)
        # Update the current time, ephemeris, location and counter
        now_time = datetime.now()
        location = ISS.coordinates()
        counter+=1
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}') 

# Deactivate camera for finishing experiment
# camera.stop_preview()