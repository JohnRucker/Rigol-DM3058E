import visa
import time
import sys
from time import sleep

def printHelp():
    print ("Try ->logCurrent.py iLog.csv 172800 .5")
    print ("\tiLog.csv = output file for current data (file will be over written)")
    print ("\t172800   = number of readings to take")
    print ("\t.5       = seconds between readings")
 


def main(lgFile, numSamples, delayBetweenSamples):
    rm = visa.ResourceManager()
    #print('Connected VISA resources:')
    #print(rm.list_resources())

    dmm = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R192701216::INSTR')
    #dmm.timeout = 10000
    print("Instrument ID (IDN:) = ", dmm.query('*IDN?'))
    

    print("Setting current range to 300ma", dmm.write(":MEASure:CURRent:DC 3")) 
    print("Reading current range", dmm.query(":MEASure:CURRent:DC:RANGe?")) 

    f = open(lgFile,'w')
    fStr = "Time, DC Current, Avg I\n"
    f.write(fStr)

    numSamples = int(numSamples)
    delayBetweenSamples = float(delayBetweenSamples)
    print("Poll rate in seconds = ", delayBetweenSamples)
    print("Number of Samples    = ", numSamples)
    print("Output csv log file  = ", lgFile ,"\n\n")

    runTotal = 0
    ampHourEst = 0
    print("count", " Seconds Count    ", "DC Current", "Estimated Amp Hours", sep="\t|\t")
    print("----------------------------------------------------------------------------------")
    for x in range(1, numSamples):
        iStr = dmm.query(":MEASure:CURRent:DC?")
        iStr = iStr.replace("\n", "")
        iFlt = float(iStr)

        runTotal = runTotal + iFlt
        ampHourEst = runTotal / x

        now = time.time()
        now = int(now)        
        print(numSamples - x, now, iFlt ,ampHourEst, sep="\t|\t")
        fStr = str(now) + "," + str(iFlt) + "," + str(ampHourEst) + "\n"
        f.write(fStr)
        sleep(delayBetweenSamples)

    f.close()

x = len(sys.argv)

print("argv count = ", x)

if x == 4:
    logFile = sys.argv[1]
    samples = sys.argv[2]
    delay = sys.argv[3]
    print(logFile, samples, delay, sep=" | ")
    main(logFile, samples, delay)
else:
    printHelp()
