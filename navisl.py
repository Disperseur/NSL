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
    """
    
    """

    def __init__(self, serial_port):
        """
        
        """
        self.ground_speed = 0

        self.long = 0
        self.lat = 0
        self.heading = 0

        self.hour = 0
        self.minut = 0
        self.sec = 0

        self.day = 0
        self.month = 0
        self.year = 0

        self.wind_speed = 0
        self.wind_direction = 0

        self.water_speed = 0
        self.water_temp = 0
        self.water_depth = 0

        #connextion au bateau
        try:
            self.port = serial.Serial(serial_port, 57600)
        except:
            print("Erreur de connexion.")



    def parse_nmea(self):
        # sentence = self.port.readline().decode()
        sentence = NMEA_TEST[0]


        nmea_rmc_re = re.compile(r"\$(?P<type>.*),(?P<champ0>.*),(?P<champ1>.*),(?P<champ2>.*),(?P<champ3>.*),(?P<champ4>.*),(?P<champ5>.*),(?P<champ6>.*),(?P<champ7>.*),(?P<champ8>.*),(?P<champ9>.*),(?P<champ10>.*),(?P<champ11>.*)\*(?P<checksum>.*)")
        nmea_dbt_re = re.compile(r"\$(?P<type>.*),(?P<champ0>.*),(?P<champ1>.*),(?P<champ2>.*),(?P<champ3>.*),(?P<champ4>.*),(?P<champ5>.*)\*(?P<checksum>.*)")
        nmea_mwv_re = re.compile(r"\$(?P<type>.*),(?P<champ0>.*),(?P<champ1>.*),(?P<champ2>.*),(?P<champ3>.*),(?P<champ4>.*)\*(?P<checksum>.*)")
        nmea_mtw_re = re.compile(r"\$(?P<type>.*),(?P<champ0>.*),(?P<champ1>.*)\*(?P<checksum>.*)")
        nmea_vhw_re = re.compile(r"\$VWVHW,,,,,(?P<speed_kt>.*),N,(?P<speed_kmh>.*),K\*(?P<checksum>.*)")

        nmea_rmc_parsed = nmea_rmc_re.match(sentence)
        nmea_dbt_parsed = nmea_dbt_re.match(sentence)
        nmea_mwv_parsed = nmea_mwv_re.match(sentence)
        nmea_mtw_parsed = nmea_mtw_re.match(sentence)
        nmea_vhw_parsed = nmea_vhw_re.match(sentence)


        if (nmea_rmc_parsed != None and nmea_rmc_parsed.group('type')[2:] == "RMC"):
            #cas d'un message RMC
            self.hour = f"{nmea_rmc_parsed.group('champ0')[0:2]}h"
            self.minut = f"{nmea_rmc_parsed.group('champ0')[2:4]}m"
            self.sec = f"{nmea_rmc_parsed.group('champ0')[4:]}s"

            self.lat = f"{nmea_rmc_parsed.group('champ2')[0:2]}°{nmea_rmc_parsed.group('champ2')[2:]}' {nmea_rmc_parsed.group('champ3')}"
            self.long= f"{nmea_rmc_parsed.group('champ4')[0:3]}°{nmea_rmc_parsed.group('champ4')[3:]}' {nmea_rmc_parsed.group('champ5')}"

            self.ground_speed = f"{nmea_rmc_parsed.group('champ6')} kt"
            self.heading = f"{nmea_rmc_parsed.group('champ7')} °"

            self.day = nmea_rmc_parsed.group('champ8')[0:2]
            self.month = nmea_rmc_parsed.group('champ8')[2:4]
            self.year = nmea_rmc_parsed.group('champ8')[4:]

        if (nmea_dbt_parsed != None and nmea_dbt_parsed.group('type')[2:] == "DBT"):
            self.water_depth = f"{nmea_dbt_parsed.group('champ2')} m"

        if (nmea_mwv_parsed != None and nmea_mwv_parsed.group('type') == "WIMWV"):
            self.wind_direction = f"{nmea_mwv_parsed.group('champ0')}° {nmea_mwv_parsed.group('champ2')}{nmea_mwv_parsed.group('champ3')}"
        
        if (nmea_mtw_parsed != None and nmea_mtw_parsed.group('type') == "WIMTW"):
            self.water_temp = f"{nmea_mtw_parsed.group('champ0')}°"

        if (nmea_vhw_parsed != None):
            self.water_speed = f"{nmea_vhw_parsed.group('speed_kt')} kt"


#tests
STLou = Boat("/dev/ttyUSB0")

while(1):

    


    STLou.parse_nmea()
    
    os.system('clear')
    print(STLou.ground_speed)
    print(STLou.long)
    print(STLou.lat)
    print(STLou.heading)
    print(STLou.hour)
    print(STLou.minut)
    print(STLou.sec)
    print(STLou.day)
    print(STLou.month)
    print(STLou.year)
    print(STLou.wind_speed)
    print(STLou.wind_direction)
    print(STLou.water_speed)
    print(STLou.water_temp)
    print(STLou.water_depth)

    time.sleep(0.1)