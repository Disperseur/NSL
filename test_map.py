import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


carte = np.asarray(Image.open('arcachon.png'))
plt.imshow(carte)
plt.show(block = False)

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def gps_to_map(lat, lon):
    """
    Fonction de remap des coordonées GPS sur la carte affichée par matplotlib

    lat = y
    lon = x
    """


    lat_deg = int(lat[:2]) + float(lat[3:-3]) / 60
    lon_deg = -int(lon[:3]) - float(lon[4:-3]) / 60

    print(lon_deg, lat_deg)

    x = mapping(lon_deg, -1.31777, -1.01110, 0, 756)
    y = mapping(lat_deg, 44.53533, 44.77666, 855, 0)

    return x, y

x, y = gps_to_map("44°38.3991' N", "001°12.9532' W")
print(x, y)

plt.scatter(x, y, color = 'red')
plt.show()