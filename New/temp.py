from RPI_I2C_LCD_driver import RPi_I2C_driver
import Adafruit_DHT as dht
import subprocess
import RPi.GPIO as GPIO
import datetime as ti
import time
import pandas as pd

# DHT11
sensor = dht.DHT11
pin = 4

# GPIO pin
pin1 = 18
pin2 = 17
pin3 = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)

# temp
ssd_temp = []
air_temp = []

# time
now = ti.datetime.now()
hour = int(now.hour)
minute = int(now.minute)
past = 0
time_ = []

# lcd
lcd = RPi_I2C_driver.lcd(0x27)


def LCD(ssd, air, h, rpi):
    lcd.setCursor(0, 0)
    lcd.print("SSD Temperature:" + str(ssd))
    lcd.print("AIR Temperature:" + str(air))
    lcd.print("AIR Humidity   :" + str(h))
    lcd.print("RPI Temperature:" + str(rpi))


def Control(temp_SSD):
    if 45 <= temp_SSD < 55:
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.LOW)
        GPIO.output(pin3, GPIO.LOW)
    elif 55 <= temp_SSD < 60:
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.HIGH)
        GPIO.output(pin3, GPIO.LOW)
    elif 60 <= temp_SSD:
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.HIGH)
        GPIO.output(pin3, GPIO.HIGH)
    else:
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
        GPIO.output(pin3, GPIO.LOW)


def Read_ssdTemp():
    cmd_ssd = "sudo smartctl -a -d sntrealtek /dev/sda1"  # smartctl info
    sysMsg = subprocess.getstatusoutput(cmd_ssd)

    f = open("temp.txt", 'w')
    f.write(sysMsg[1])
    f.close

    time.sleep(1)

    with open('temp.txt', 'r') as f:
        temp = float(f.readlines()[44][36:38])
    f.close()

    return temp


def Read_AIR():
    h, t = dht.read_retry(sensor, pin)

    return h, t


def Read_RPITemp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = str(int(f.readline().strip()) / 1000)
        temp = float(temp[:4])

    f.close()
    return temp


def Tempe_per_hour(ssd, air):
    h = hour - int(now.hour)
    m = minute - int(now.minute)

    if m % 10 == 0:
        t = str(h) + "-" + str(m)
        time_.append(t)
        ssd_temp.append(ssd)
        air_temp.append(air)



try:
    while True:
        temp_SSD = Read_ssdTemp()
        h, temp_Air = Read_AIR()
        temp_RPI = Read_RPITemp()

        LCD(temp_SSD, temp_Air, h, temp_RPI)

        Control(temp_SSD)

        now = ti.datetime.now()
        minute = int(now.minute)
        if (past != minute):
            Tempe_per_hour(temp_SSD, temp_Air)
            past = minute
        else:
            pass
        print(ssd_temp)

except KeyboardInterrupt:
    print("\n stop")
    GPIO.cleanup()
    data = {'SSD_Temp': ssd_temp, 'AIR_Temp': air_temp}
    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)
