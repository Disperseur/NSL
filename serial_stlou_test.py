import serial


port = serial.Serial('/dev/ttyUSB0', 57600)

while(1):
    print(port.readline().decode())