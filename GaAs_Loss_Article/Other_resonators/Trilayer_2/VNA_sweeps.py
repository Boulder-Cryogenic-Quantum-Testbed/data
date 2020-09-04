import numpy as np
import pyvisa
import os
from os import path

#set parameters for the PNA for the sweep (number of points, center frequency, span of frequencies, IF bandwidth, power, electrical delay and number of averages)
def vna_setup(vna, points: int, centerf: float, span: float, ifband: float, power: float, edelay: float, averages: int):
    #setup
    if (vna.query('CALC:PAR:CAT:EXT?') != '"MyMeas,S21"\n'):
        vna.write('CALCulate1:PARameter:DEFine:EXT \'MyMeas\',S21')
        vna.write('DISPlay:WINDow1:STATE ON')
        vna.write('DISPlay:WINDow1:TRACe1:FEED \'MyMeas\'')
        vna.write('DISPlay:WINDow1:TRACe2:FEED \'MyMeas\'')
    #set parameters
    vna.write('SENSe1:SWEep:POINts {}'.format(points))
    vna.write('SENSe1:FREQuency:CENTer {}GHZ'.format(centerf))
    vna.write('SENSe1:FREQuency:SPAN {}MHZ'.format(span))
    vna.write('SENSe1:BANDwidth {}KHZ'.format(ifband))
    vna.write('SENSe1:SWEep:TIME:AUTO ON')
    vna.write('SOUR:POW1 {}'.format(power))
    vna.write('CALCulate1:CORRection:EDELay:TIME {}NS'.format(edelay))
    vna.write('SENSe1:AVERage:STATe ON')
    if(averages < 10):
        averages = 10
    averages = averages//1
    print(averages)
    vna.write('SENSe1:AVERage:Count {}'.format(averages))

#function to read in data from the vna and output it into a file
def read_data(vna, points, outputfile, power, temp):
    #read in frequency
    freq = np.linspace(float(vna.query('SENSe1:FREQuency:START?')), float(vna.query('SENSe1:FREQuency:STOP?')), points)

    #read in phase
    vna.write('CALCulate1:FORMat PHASe')
    phase = vna.query_ascii_values('CALCulate1:DATA? FDATA', container=np.array)

    #read in mag
    vna.write('CALCulate1:FORMat MLOG')
    mag = vna.query_ascii_values('CALCulate1:DATA? FDATA', container=np.array)

    #open output file and put data points into the file
    file = open(outputfile[0:-4]+'_'+str(power)+'dBm'+'_'+str(temp)+'mK'+'.csv',"w")
    count = 0
    for i in freq:
        file.write(str(i)+','+str(mag[count])+','+str(phase[count])+'\n')
        count = count + 1

    file.close()

#function to get data and put it into a user specified file
def getdata(centerf, span, temp, averages = 100, power = -30, edelay = 40, ifband = 5, points = 201, outputfile = "results.csv"):
    #set up the PNA to measure s21
    rm = pyvisa.ResourceManager()
    keysight = rm.open_resource('GPIB0::16::INSTR')
    vna_setup(keysight, points, centerf, span, ifband, power, edelay, averages)

    #start taking data for S21
    keysight.write('CALCulate1:PARameter:SELect \'MyMeas\'')
    keysight.write('FORMat ASCII')

    #wait until the averages are done being taken
    count = 10000000
    while(count > 0):
        count = count - 1
    while(True):
        if (keysight.query('STAT:OPER:AVER1:COND?')[1] != "0"):
            break;
    
    read_data(keysight, points, outputfile, power, temp)
    
#run a power sweep for specified power range with a certain number of sweeps
def powersweep(startpower, endpower, numsweeps, centerf, span, temp, averages = 100, edelay = 40, ifband = 5, points = 201, outputfile = "results.csv"):
    sweeps = np.linspace(startpower, endpower, numsweeps)
    stepsize = sweeps[0]-sweeps[1]
    
    #create a new directory for the output to be put into
    if (path.isdir(outputfile[0:-4]+'_'+'_'+str(temp)+'mK')):
        dircount = 1
        while (True):
            if (not path.isdir(outputfile[0:-4]+'_'+'_'+str(temp)+'mK'+str(dircount))):
                break;
            dircount = dircount + 1
        os.mkdir(outputfile[0:-4]+'_'+'_'+str(temp)+'mK'+str(dircount))
        outputfile = outputfile[0:-4]+'_'+'_'+str(temp)+'mK'+str(dircount) + '/' + outputfile
    else:
        os.mkdir(outputfile[0:-4]+'_'+'_'+str(temp)+'mK')
        outputfile = outputfile[0:-4]+'_'+'_'+str(temp)+'mK' + '/' + outputfile
        
    #write an output file with conditions
    file = open(outputfile[0:-4]+'_'+str(temp)+'mK_conditions'+'.csv',"w")
    file.write('STARTPOWER: '+str(startpower)+'\n')
    file.write('ENDPOWER: '+str(endpower)+'\n')
    file.write('NUMSWEEPS: '+str(numsweeps)+'\n')
    file.write('CENTERF: '+str(centerf)+'\n')
    file.write('SPAN: '+str(span)+'\n')
    file.write('TEMP: '+str(temp)+'\n')
    file.write('AVERAGES: '+str(averages)+'\n')
    file.write('EDELAY: '+str(edelay)+'\n')
    file.write('IFBAND: '+str(ifband)+'\n')
    file.write('POINTS: '+str(points)+'\n')
    file.close()
        
    #run each sweep
    for i in sweeps:
        getdata(centerf, span, temp, averages, i, edelay, ifband, points, outputfile)
        averages = averages * ((10**(stepsize/10))**0.5)
