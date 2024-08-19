import re
import serial
import time
import os
import tkinter
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#settings
DEBUG = True

FONT_INFOS = "Mono 25"
UPDATE_PERIOD_MS = 100



class Boat():

    def __init__(self, serial_port):
        self.ground_speed = "0 kt"
        self.ground_speed_tbl = [0]*(36000//UPDATE_PERIOD_MS) #36000     tableau pour la moyenne glissante de vitesse sol
        self.ground_speed_tbl_i = 0
        self.ground_speed_avg_30min = 0
        self.ground_speed_avg_1h = 0

        self.long = "001°08.9214' W"
        self.lat = "44°39.6210' N"
        self.heading = "-"

        self.time = "-"

        self.date = "-"
        self.month = "-"
        self.year = "-"

        self.wind_speed = "0 kt"
        self.wind_speed_avg_30min = "0 kt"
        self.wind_speed_avg_1h = "0 kt"
        self.wind_angle = "0°"

        self.water_speed = "-"
        self.water_temp = "-"
        self.water_depth = "-"



        #connextion au bateau ou ouverture du fichier log
        if not DEBUG:
            self.port = serial.Serial(serial_port, 57600)
        else:
            log_file = open("log.txt", 'r')
            self.log_file_lines = log_file.readlines()
            self.log_file_index = 0



        # carte de fond
        self.map = np.asarray(Image.open('arcachon.png'))



    def parse_nmea(self):
        
        #lecture du port serie ou de la ligne du fichier de log
        if not DEBUG:
            sentence = self.port.readline().decode()
        else:
            sentence = self.log_file_lines[self.log_file_index]
            if self.log_file_index < len(self.log_file_lines)-1:
                self.log_file_index += 1
            else:
                self.log_file_index = 0 #retour au debut du fichier pour test
        
        nmea_rmc_re = re.compile(r"\$GPRMC,(?P<time>.*),(?P<champ1>.*),(?P<lat>.*),(?P<champ3>.*),(?P<long>.*),(?P<champ5>.*),(?P<ground_speed>.*),(?P<heading>.*),(?P<date>.*),,,(?P<champ11>.*)\*(?P<checksum>.*)")
        nmea_dbt_re = re.compile(r"\$SDDBT,(?P<depth_ft>.*),(?P<champ1>.*),(?P<depth_m>.*),(?P<champ3>.*),(?P<depth_f>.*),(?P<champ5>.*)\*(?P<checksum>.*)")
        nmea_mwv_re = re.compile(r"\$WIMWV,(?P<wind_angle>.*),(?P<champ1>.*),(?P<wind_speed_kt>.*),(?P<champ3>.*),(?P<champ4>.*)\*(?P<checksum>.*)")
        nmea_mtw_re = re.compile(r"\$WIMTW,(?P<water_temp>.*),(?P<champ1>.*)\*(?P<checksum>.*)")
        nmea_vhw_re = re.compile(r"\$VWVHW,,,,,(?P<speed_kt>.*),N,(?P<speed_kmh>.*),K\*(?P<checksum>.*)")

        nmea_rmc_parsed = nmea_rmc_re.match(sentence)
        nmea_dbt_parsed = nmea_dbt_re.match(sentence)
        nmea_mwv_parsed = nmea_mwv_re.match(sentence)
        nmea_mtw_parsed = nmea_mtw_re.match(sentence)
        nmea_vhw_parsed = nmea_vhw_re.match(sentence)


        if (nmea_rmc_parsed != None):
            self.time = f"{nmea_rmc_parsed.group('time')[0:2]}:{nmea_rmc_parsed.group('time')[2:4]}:{nmea_rmc_parsed.group('time')[4:]}"
            
            self.lat = f"{nmea_rmc_parsed.group('lat')[0:2]}°{nmea_rmc_parsed.group('lat')[2:]}' {nmea_rmc_parsed.group('champ3')}"
            self.long= f"{nmea_rmc_parsed.group('long')[0:3]}°{nmea_rmc_parsed.group('long')[3:]}' {nmea_rmc_parsed.group('champ5')}"

            self.ground_speed = f"{nmea_rmc_parsed.group('ground_speed')[:-1]} kt"
            self.heading = f"{nmea_rmc_parsed.group('heading')}°"

            self.date = f"{nmea_rmc_parsed.group('date')[0:2]}/{nmea_rmc_parsed.group('date')[2:4]}/{nmea_rmc_parsed.group('date')[4:]}"

        if (nmea_dbt_parsed != None):
            self.water_depth = f"{nmea_dbt_parsed.group('depth_m')} m"

        if (nmea_mwv_parsed != None):
            self.wind_speed = f"{nmea_mwv_parsed.group('wind_speed_kt')} kt"
            self.wind_angle = f"{nmea_mwv_parsed.group('wind_angle')[:-2]}°"
        
        if (nmea_mtw_parsed != None):
            self.water_temp = f"{nmea_mtw_parsed.group('water_temp')[:-2]}°"

        if (nmea_vhw_parsed != None):
            self.water_speed = f"{nmea_vhw_parsed.group('speed_kt')[:-1]} kt"


    def calcul_stats(self):
        #moyennes de vitesse sol
        self.ground_speed_tbl[self.ground_speed_tbl_i] = float(self.ground_speed[:-3]) #ajout element
        
        #rotation indice ecriture dans tableau
        if self.ground_speed_tbl_i < len(self.ground_speed_tbl) - 1:
            self.ground_speed_tbl_i += 1
        else:
            self.ground_speed_tbl_i = 0

        #calcul des moyennes
        for i in range(len(self.ground_speed_tbl)):
            self.ground_speed_avg_1h += self.ground_speed_tbl[i]
            if i >= len(self.ground_speed_tbl) // 2:
                self.ground_speed_avg_30min += self.ground_speed_tbl[i]
        
        self.ground_speed_avg_1h /= len(self.ground_speed_tbl)
        self.ground_speed_avg_30min /= (len(self.ground_speed_tbl)/2)





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




def update_affichage():

    STLou.parse_nmea()
    STLou.calcul_stats()
    # print(STLou.ground_speed_avg_30min)

    x, y = gps_to_map(STLou.lat, STLou.long)

    plt.scatter(x, y, color='red')
    plt.show(block = False)
    

    duree_nav = int(time.monotonic()) - t_start
    duree_nav_sec = duree_nav%60
    duree_nav_min = (duree_nav//60)%60
    duree_nav_heu = (duree_nav//3600)

    label_dateheure.config(text=f"{STLou.date}\n{STLou.time[:-4]}\nDurée nav: {duree_nav_heu}:{duree_nav_min}:{duree_nav_sec}")
    label_vitesse.config(text=f"Sol: {STLou.ground_speed} (moy: {round(STLou.ground_speed_avg_30min, 1)})\nEau: {STLou.water_speed}")
    label_gps.config(text=f"Cap: {STLou.heading}\nLat: {STLou.lat}\nLon: {STLou.long}")
    label_vent.config(text=f"{STLou.wind_speed} {STLou.wind_angle}")
    label_eaux.config(text=f"Température: {STLou.water_temp}\nProfondeur:  {STLou.water_depth}")

    angle_vent = math.radians(float(STLou.wind_angle[:-1]) - 90)
    vitesse_vent = float(STLou.wind_speed[:-3])
    
    rose_vent.coords(axe_vent, 75, 75, int(3*vitesse_vent*math.cos(angle_vent))+75, int(3*vitesse_vent*math.sin(angle_vent)+75))



    fenetre.after(UPDATE_PERIOD_MS, update_affichage)


#main
STLou = Boat("/dev/ttyUSB0")
t_start = int(time.monotonic())

plt.imshow(STLou.map)
plt.show(block = False)

#description de l'affichage de l'appli

fenetre = tkinter.Tk()
fenetre.title("NSL")
fenetre.geometry('500x1100')
fenetre.resizable(width=False, height=True)


frame_dateheure = tkinter.LabelFrame(fenetre, text="Date / Heure", padx=20, pady=20, font="Mono 20")
frame_dateheure.pack(fill="both", expand="yes")

frame_vitesse = tkinter.LabelFrame(fenetre, text="Vitesses", padx=20, pady=20, font="Mono 20")
frame_vitesse.pack(fill="both", expand="yes")

frame_gps = tkinter.LabelFrame(fenetre, text="GPS", padx=20, pady=20, font="Mono 20")
frame_gps.pack(fill="both", expand="yes")

frame_vent = tkinter.LabelFrame(fenetre, text="Vent", padx=20, pady=20, font="Mono 20")

rose_vent = tkinter.Canvas(frame_vent, width=150, height=150)
axe_vent = rose_vent.create_line(75, 75, 75, 10, width=4)
contour_rose = rose_vent.create_oval(10, 10, 140, 140, width=4)

rose_vent.pack()

frame_vent.pack(fill="both", expand="yes")

frame_eaux = tkinter.LabelFrame(fenetre, text="Eaux", padx=20, pady=20, font="Mono 20")
frame_eaux.pack(fill="both", expand="yes")

label_dateheure = tkinter.Label(frame_dateheure, text="-\n-", font=FONT_INFOS)
label_vitesse = tkinter.Label(frame_vitesse, text="Eau: -\nSol: -", font=FONT_INFOS, justify="left")
label_gps = tkinter.Label(frame_gps, text="Cap: -\nLat: -\nLon: -", font=FONT_INFOS, justify="left")
label_vent = tkinter.Label(frame_vent, text="- -", font=FONT_INFOS)
label_eaux = tkinter.Label(frame_eaux, text="Température: -\nProfondeur: -", font=FONT_INFOS, justify="left")

label_dateheure.pack()
label_vitesse.pack(anchor="w")
label_gps.pack(anchor="w")
label_vent.pack()
label_eaux.pack(anchor="w")


fenetre.after(UPDATE_PERIOD_MS, update_affichage)
fenetre.mainloop()
