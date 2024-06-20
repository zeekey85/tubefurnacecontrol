import time
import board
import digitalio
import busio
import statistics
import subprocess
import matplotlib.pyplot as plt
import datetime
import numpy

#defining variables for turning the motor
motor = digitalio.DigitalInOut(board.D18)
motor.direction = digitalio.Direction.OUTPUT
ms1 = digitalio.DigitalInOut(board.D17)
ms2 = digitalio.DigitalInOut(board.D4)
ms1.direction = digitalio.Direction.OUTPUT
ms2.direction = digitalio.Direction.OUTPUT
ms2.value = False
ms1.value = False
direc = digitalio.DigitalInOut(board.D26)
direc.direction = digitalio.Direction.OUTPUT
direc.value = True
#turns motor a number of degrees z
def manualTurn(z):
    direc.value = True
    if z < 0:
        direc.value = True
    elif z >= 0:
        direc.value = False
    for x in range(int((abs(z)/360)*1600)):
        motor.value = True
        time.sleep(0.001)
        motor.value = False
        time.sleep(0.001)
    motor.value = True
    direc.value = False

#voltage measurement imports and object defining
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)
ads.gain = 1
tran = AnalogIn(ads, ADS.P0, ADS.P1)
ref = AnalogIn(ads, ADS.P2, ADS.P3)

# gets an average of 10 voltage measurements
def getVoltage(det):
    hey = det
    list = []
    for x in range(5):
        list.append(det.voltage)

        time.sleep(.1)
    avg = sum(list)/len(list)
    stdev = statistics.pstdev(list)
    #           the number below is the
    if hey == tran:
        value = avg/(-0.2269699)
    elif hey == ref:
        value = avg/(-0.2265714)
    return round(value, 4)

def singleVolt():
    print((tran.voltage)/(-0.2269699))


#this function may not have to be used, but it will spin the wheel until an led shines through a hole
led = digitalio.DigitalInOut(board.D25)
led.direction = digitalio.Direction.OUTPUT
filterNum = 0
def goHome():
    led.value = True
    for x in range(2000):
        motor.value = True
        time.sleep(.0001)
        motor.value = False
        time.sleep(.0001)

        if (det.voltage > 0.15):
            motor.value = True
            led.value = False
            print("home :)")
            break
        elif (x>1800):
            print("im lost! :(")
            led.value = False
            motor.value = True
            break
        else:
            pass

    motor.value = True


#measures a set number of filters one time at a given temperature and returns voltage readings as a list
import csv
def measureX(i):
    data = []
    avg = 0
    data.append(datetime.datetime.now().strftime("%H"))
    data.append(datetime.datetime.now().strftime("%M"))
    data.append(datetime.datetime.now().strftime("%S"))
    for x in range(i):
        if (x==0):
            avg = getVoltage(tran)
        elif (x > 0):
            direc.value = False
            manualTurn(27.69)
            #this will change the time between filter rotations
            time.sleep(4)
            avg = getVoltage(tran)
        data.append(avg)
    data.append(getVoltage(ref))

    for z in range(i-1):
        #spins motor opposite direction back to starting point
        manualTurn(-27.69)
    #this will return a list of values first the temperature and then
    #all of the voltages from the detector
    return data
#this is the full measurement function, it takes in an int for the number of filters to be measured
#the output is a csv file with the voltage measurements and a header
def fullMeasure():
    name = input("File Name: ")
    filters = 9
    header = ['Temp']
    measurements = []
    #creates header
    header.append('hr')
    header.append('min')
    header.append('sec')
    header.append('900')
    header.append('1000')
    header.append('1100')
    header.append('1200')
    header.append('1300')
    header.append('1400')
    header.append('1500')
    header.append('1600')
    header.append('1650')
    header.append('Reflection')
    #this set of loops will ask for a temperature, then collect the data
    #if you type exit as the input, it will move on from this block
    yn = ""
    while yn != "exit":
        yn = input("What is the temperature (type exit to stop) ")
        if yn != "exit":
            yah = measureX(filters)
            #puts the temperature at the front of the list
            yah.insert(0, yn)
            measurements.append(yah)
            print(measurements)
            with open('data/'+name+'.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
                for j in range(len(measurements)):
                    writer.writerow(measurements[j])
            csvfile.close()
           # plotting(measurements,name)
            print(subprocess.run(["/home/surface/Documents/syncData.sh"], shell=True))
    else:
        print("goodbye")
    #this is the part that creates the .csv file
    print(header)
    print(measurements)

def optimize():
    count = []
    startVolt = getVoltage(tran)
    count.append(startVolt)
    for x in range(10):
        manualTurn(1)
        count.append(getVoltage(tran))
    manualTurn(-10)
    for x in range(10):
        manualTurn(-1)
        count.append(getVoltage(tran))
    manualTurn(10)
    x = count.index(max(count))
    if x == 0:
        print("done")
    elif x<=10:
        manualTurn(x)
        print("done1")
    elif x>10:
        w = (x)-10
        z = w*-1
        manualTurn(z)
        print("done2")
        
def plotting(data,fname):
    x=[900,1000,1100,1200,1300,1400,1500,1600,1650]
    plt.clf()
    for idy, y in enumerate(data):
        plt.plot(x,y[4:13],marker='o',linestyle='none',label=y[0])
    plt.legend()
    plt.savefig('/home/surface/Documents/data/'+fname+'PLOT')
    #plt.show()
    











