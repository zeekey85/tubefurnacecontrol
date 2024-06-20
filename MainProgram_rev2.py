import board
import time
import digitalio
import busio
import VincentProgramLib_rev2_dev
import csv
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)
ads.gain = 1
tran = AnalogIn(ads, ADS.P0, ADS.P1)
ref = AnalogIn(ads, ADS.P2, ADS.P3)
while True:
    i = input("what would you like to do? (full, turn, voltage, optimize, exit):  ")
    if i == "exit":
        print("goodbye")
        break
    elif i == "full":
        VincentProgramLib_rev2_dev.fullMeasure()
    elif i == "turn":
        try:
            d = int(input("degrees of rotation: "))
        except ValueError:
            print("input not recognized")
        else:
            VincentProgramLib_rev2_dev.manualTurn(d)


    elif i == "voltage":
        VincentProgramLib_rev2_dev.singleVolt()
    elif i == "optimize":
        VincentProgramLib_rev2_dev.optimize()
    else:
        print("input not recognized")

