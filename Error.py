# Gregorian Calendar Adopted: October 15, 1582

#Tropical Year: 365.24219 days/365 solar days, 5hours, 48 minutes, 45 seconds

#Average yearly error: 26 seconds
import math
import cv2
import tkinter as tk
import numpy as np
from astroquery.jplhorizons import Horizons
from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy.utils import iers

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

width = int(screen_width/2)
height = int(screen_height/2)

AU_in_view = 3
pixel_per_AU = int(width/AU_in_view)

image = np.zeros((height, width, 3), np.uint8)

#Draw Sun
#sun_AU = 0.0047
sun_radius = 20
sun_location = (int(width/2),int(height/2))
image = cv2.circle(image, sun_location, sun_radius, (130,230,250), -1) 

#Draw Earth
#earth_AU = 0.000043
earth_radius = 10
t = Time.now()
# Target ID '399' is Earth, 'Sun' for the Sun, 'Geocentric' for Earth in heliocentric coordinates
obj = Horizons(id='399', location='@sun', epochs=t.jd, id_type='majorbody')
earth_ephemeris = obj.vectors()  # Get vector position and velocity
heliocentric_position = earth_ephemeris['x'][0], earth_ephemeris['y'][0], earth_ephemeris['z'][0]
earth_location = (int(heliocentric_position[0]*pixel_per_AU+sun_location[0]),int(heliocentric_position[1]*pixel_per_AU+sun_location[1]))
image = cv2.circle(image, earth_location, earth_radius, (250,230,130), -1) 

#Draw Earth Rotation Line
# Update IERS data for Earth Orientation Parameters (EOP) for precise rotation tracking
iers_a = iers.IERS_A.open(iers.IERS_A_URL)
iers.conf.auto_download = True

# Get sidereal time at Greenwich (related to Earth's rotation)
sidereal_time = t.sidereal_time('mean', 'greenwich').hour
#print(f"{sidereal_time}")
theta = math.atan(abs((sun_location[1]-earth_location[1])/(sun_location[0]-earth_location[0])))
theta += math.radians(sidereal_time*15)
line_end = (int((earth_radius+2)*math.cos(theta)+earth_location[0]),int((earth_radius+2)*math.sin(theta)+earth_location[1]))
image = cv2.line(image, line_end, earth_location, (0,0,255), 2)

cv2.imshow("Simulation", image)

cv2.waitKey(0)

cv2.destroyAllWindows()