# Gregorian Calendar Adopted: October 15, 1582

#Tropical Year: 365.24219 days/365 solar days, 5hours, 48 minutes, 45 seconds

#Average yearly error: 26 seconds
from astroquery.jplhorizons import Horizons
from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy.utils import iers

# 1. Get the current time
t = Time.now()

# 2. Use JPL Horizons to get accurate Earth's heliocentric position
# Target ID '399' is Earth, 'Sun' for the Sun, 'Geocentric' for Earth in heliocentric coordinates
obj = Horizons(id='399', location='@sun', epochs=t.jd, id_type='majorbody')
earth_ephemeris = obj.vectors()  # Get vector position and velocity

# Print Earth's heliocentric position (X, Y, Z coordinates)
heliocentric_position = earth_ephemeris['x'][0], earth_ephemeris['y'][0], earth_ephemeris['z'][0]
print(f"Earth's current heliocentric position (X, Y, Z) in AU:")
print(f"X: {heliocentric_position[0]} AU")
print(f"Y: {heliocentric_position[1]} AU")
print(f"Z: {heliocentric_position[2]} AU")

# 3. Get Earth's rotation (sidereal time)
# Update IERS data for Earth Orientation Parameters (EOP) for precise rotation tracking
iers_a = iers.IERS_A.open(iers.IERS_A_URL)
iers.conf.auto_download = True

# Get sidereal time at Greenwich (related to Earth's rotation)
sidereal_time = t.sidereal_time('mean', 'greenwich')
print(f"\nEarth's current rotation (Greenwich Sidereal Time): {sidereal_time}")