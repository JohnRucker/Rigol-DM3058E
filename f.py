import visa
import time
import sys
from time import sleep

def printHelp():
    print ("Try ->logCurrent.py iLog.csv 172800 .5")
    print ("\tiLog.csv = output file for current data (file will be over written)")
    print ("\t172800   = number of readings to take")
    print ("\t.5       = seconds between readings")
 


x = len(sys.argv)

print("argv count = ", x)
if x==4:
    print("pass")

