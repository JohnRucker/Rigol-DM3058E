import visa
import time
import sys
from time import sleep

def printHelp():
    print ("Try ->logCurrent.py iLog.csv 172800 .5")
    print ("\tiLog.csv = output file for current data (file will be over written)")
    print ("\t172800   = number of readings to take")
    print ("\t.5       = seconds between readings")
 


def main():
    rm = visa.ResourceManager()
    print('Connected VISA resources:')
    print(rm.list_resources())

    dmm = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R192701216::INSTR')
    print('Instrument ID (IDN:) = ', dmm.query('*IDN?'))
    #print("Volts DC   = ", dmm.query(":MEASure:VOLTage:DC?"))
    print("DC Current = ", dmm.query(":MEASure:CURRent:DC?"))

    f = open('iLog.csv','w')
    fStr = "Time, DC Current, Raw\n"
    f.write(fStr)

    print("Poll rate = 500mS. Will run for 24 hours collecting 172,800 readings")
    print("output file = iLog.csv\n\n")
    print(" Seconds Count    ", "DC Current", "Raw Meter Response", sep="\t|\t")
    print("----------------------------------------------------------------------------------")
    for x in range(0, 172800):
        rawStr = dmm.query(":MEASure:CURRent:DC?")
        iStr = rawStr
        rawStr = rawStr.replace ("\n", "") 
        iStr = iStr.replace("\n", "")
        iStr = iStr.replace("#9000000015", "")

        iFlt = float(iStr)
        now = time.time()
        print(now, iFlt ,rawStr, sep="\t|\t")
        fStr = str(now) + "," + str(iFlt) + "," + rawStr + "\n"
        f.write(fStr)
        sleep(.5)

    f.close()

if len(sys.argv) == 3:
    logFile = sys.argv[1]
    samples = sys.argv[2]
    delay = sys.argv[3]
    print(logFile, samples, delay, sep=" | ")
else:
    printHelp()
