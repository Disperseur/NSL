import re
import serial
import time
import os


NMEA_TEST_RMC = "$GPRMC,092541.000,A,4439.6265,N,00108.1894,W,0.35,159.65,120824,,,A*72"
NMEA_TEST_DBT = "$SDDBT,19.3,f,5.8,M,3.2,F*31"
NMEA_TEST_MWV = "$WIMWV,20.5,R,13.5,N,A*23"
NMEA_TEST_MTW = "$WIMTW,25.8,C*02"
NMEA_TEST_VHW = "$VWVHW,,,,,3.1,N,4.30,K*4D"

NMEA_TEST = [NMEA_TEST_RMC, NMEA_TEST_DBT, NMEA_TEST_MWV, NMEA_TEST_MTW, NMEA_TEST_VHW]

class Boat():

    def __init__(self, serial_port):
        self.ground_speed = "-"

        self.long = "-"
        self.lat = "-"
        self.heading = "-"

        self.time = "-"

        self.date = "-"
        self.month = "-"
        self.year = "-"

        self.wind = "-"

        self.water_speed = "-"
        self.water_temp = "-"
        self.water_depth = "-"

        #connextion au bateau
        try:
            self.port = serial.Serial(serial_port, 57600)
        except:
            print("Erreur de connexion.")



    def parse_nmea(self):
        sentence = self.port.readline().decode()
        # sentence = NMEA_TEST[0]

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

            self.ground_speed = f"{nmea_rmc_parsed.group('ground_speed')}kt"
            self.heading = f"{nmea_rmc_parsed.group('heading')}°"

            self.date = f"{nmea_rmc_parsed.group('date')[0:2]}/{nmea_rmc_parsed.group('date')[2:4]}/{nmea_rmc_parsed.group('date')[4:]}"

        if (nmea_dbt_parsed != None):
            self.water_depth = f"{nmea_dbt_parsed.group('depth_m')}m"

        if (nmea_mwv_parsed != None):
            self.wind = f"{nmea_mwv_parsed.group('wind_speed_kt')}kt {nmea_mwv_parsed.group('wind_angle')}°"
        
        if (nmea_mtw_parsed != None):
            self.water_temp = f"{nmea_mtw_parsed.group('water_temp')}°"

        if (nmea_vhw_parsed != None):
            self.water_speed = f"{nmea_vhw_parsed.group('speed_kt')}kt"


#tests
STLou = Boat("/dev/ttyUSB0")

while(1):

    STLou.parse_nmea()
    
    os.system('clear')

    print("Date:\t\t", STLou.date)
    print("Time:\t\t", STLou.time[:-4])

    print("")
    
    print("Speed")
    print("Ground:\t\t", STLou.ground_speed)
    print("Water:\t\t", STLou.water_speed)

    print("")

    print("Heading:\t", STLou.heading)

    print("")

    print("GPS Position")
    print("Lat:\t\t", STLou.lat)
    print("Long:\t\t", STLou.long)

    print("")
    
    print("Wind:\t\t", STLou.wind)

    print("")

    print("Water")
    print("Temp:\t\t", STLou.water_temp)
    print("Depth:\t\t", STLou.water_depth)

    time.sleep(0.1)