# This program uses Tomo-Gravity algorithm to produce hourly O-D (Origin-Destination) Matrix using link count data
# Inputs:
# 1. .csv file for Hourly link-count probabilities produced from PeMS sensor data by Emin
# 2. .csv file for Initial estimate of daily O-D matrix (in this case, extracted from http://data5.ctpp.transportation.org/ctpp/Browse/browsetables.aspx)
# 3. .csv file produced by LR_Incidence matrix.py
# 4. .csv file with hourly link counts for all links in the network generated from PeMS sensor data by Emin

# Imports
import numpy as np
import csv

# Importing hourly probability matrix, link-route incidence matrix and initial daily O-D estimate
p=np.genfromtxt('C:\Important Stuff\Berkeley\Preparation\MATSim SF Bay\Counts Analysis\Tomo-Gravity\Hourly_Probabilities.csv', delimiter=',', usecols=(0))
A = np.genfromtxt('C:\Important Stuff\Berkeley\Preparation\MATSim SF Bay\Counts Analysis\Tomo-Gravity\Incidence_matrix.csv', delimiter=',')
A = A.T
tg = np.genfromtxt('C:\Important Stuff\Berkeley\Preparation\MATSim SF Bay\Counts Analysis\Tomo-Gravity\Original OD.csv', delimiter=',', skiprows=1, usecols=(2))
# Iterating through each hour 
for i in range(24):
    # Extracting link count for each hour
    x = np.genfromtxt('C:\Important Stuff\Berkeley\Preparation\MATSim SF Bay\Counts Analysis\Tomo-Gravity\Simplified_network_final_link_counts.csv', delimiter=',', skiprows=1, usecols=(2+i))
    # Initial hourly etimate of O-D flow
    tg = tg*p[i]
    #Executing Tomo-Gravity algorithm
    w = np.ones(len(tg))
    xw = np.subtract(np.dot(A,tg),x)
    r = len(A)
    c = len(A[0,:])
    Aw = np.dot(A,np.matlib.repmat(w,c,1))
    tw = np.dot(np.linalg.pinv(Aw),xw)
    t = tg + np.dot(w,tw)
    t_sq = np.zeros((len(t)/len(x),len(t)/len(x)))
    for j in range(len(t_sq)):
        for k in range(len(t_sq)):
            t_sq[j][k]=t[j*len(t_sq)+k]
    #Writing to .csv file
    with open('Hour_'+str(i)+'_OD_tomogravity.csv','wb') as f:
        writer = csv.writer(f)
        print t_sq[i]
        for l in range(len(t_sq)):
            writer.writerow(t_sq[l])
    f.close()

