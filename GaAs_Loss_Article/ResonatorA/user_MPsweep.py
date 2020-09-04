import sys
sys.path.append(r'C:\Users\Lehnert Lab\Documents\GitHub\measurement\pna_control')
import pna_control as PNA
import numpy as np
import os

# VNA parameters
AVERAGES = 20 # Number of averages for first (highest) power
EDELAY = 61.1 #ns
IFBAND = 0.1 #kHz
CENTERF = [5.1544,5.51414,5.95095,7.41255] #GHz
SPAN = [2,2,2,2,2] #MHz
POINTS = 1001

TEMP = 12 #mK
SAMPLEID = 'E06_02' #project ID followed by sample number and die number

STARTPOWER = -30
ENDPOWER = -60
NUMSWEEPS = 16

for i in np.arange(len(CENTERF)):
    OUTPUTFILE = SAMPLEID+'_'+str(CENTERF[i])+'GHz_'+'MPsweep'
    PNA.power_sweep(STARTPOWER, ENDPOWER, NUMSWEEPS, CENTERF[i], SPAN[i], TEMP, AVERAGES, EDELAY, IFBAND, POINTS, OUTPUTFILE,str(CENTERF[i])+'GHz_MPsweep')