import ArduinoSerial
from KoalbyHumanoid.Robot import Robot

robot = Robot()
arduino_serial = ArduinoSerial.ArduinoSerial()


def read_battery_level():
    command = "25,"
    arduino_serial.send_command(command)
    battery_level = arduino_serial.read_command()
    print("battery level is")
    print(battery_level)


read_battery_level()
