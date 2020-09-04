import sys
sys.path.append(r'C:\Users\Lehnert Lab\Documents\GitHub\measurement\pna_control')
import pna_control as PNA
import numpy as np
import os

# VNA parameters
AVERAGES = 80 # Number of averages for first (highest) power
EDELAY = 61.1 #ns
IFBAND = 0.05 #kHz
CENTERF = [7.41255,5.51414] #GHz
SPAN = [3,3] #MHz
POINTS = 801

TEMP = 12 #mK
SAMPLEID = 'E06_02' #project ID followed by sample number and die number

STARTPOWER = -65
ENDPOWER = -80
NUMSWEEPS = 4

for i in np.arange(len(CENTERF)):
    OUTPUTFILE = SAMPLEID+'_'+str(CENTERF[i])+'GHz_'+'LPsweep'
    PNA.power_sweep(STARTPOWER, ENDPOWER, NUMSWEEPS, CENTERF[i], SPAN[i], TEMP, AVERAGES, EDELAY, IFBAND, POINTS, OUTPUTFILE,str(CENTERF[i])+'GHz_LPsweep')