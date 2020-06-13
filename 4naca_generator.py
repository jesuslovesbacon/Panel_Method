#four digit NACA generator
import numpy as np
from math import atan
from math import sin
from math import cos
import matplotlib.pyplot as plt

# raw_num = input('Enter 4 digit NACA airfoil number or a 5-digit airfoil number: ')
# trailing = input('Enter \'True\' for open trailing edge. Enter \'False\' for closed trailing edge: ')
# Npanel = input('Enter number of grid points: ')
# c = input('Enter chord length: ')

## User inputs
raw_num = '24012'
NACA = list(raw_num)
trailing = False
NGrid = 200
c = 100

if len(NACA) == 4:
    #Breaking the NACA four digit code 
    M = int(NACA[0])/100                                        #maximun camber
    P = int(NACA[1])/10                                         #position of maximun camber
    T = int(NACA[2]+ NACA[3])/100
else:
    # Breaking the Naca for digit code
    L = int(NACA[0])*(3/20)                                       # lift coeffcient 
    P = int(NACA[1])/20                                         #position of maximun camber
    Q = int(NACA[2])                                              # '0' for camber line, '1' reflex camber line
    T = int(NACA[3]+ NACA[4])/100                               #thickness of the chord 

X = np.linspace(0,1,NGrid)                                      # discritizing the chord length 

if len(NACA) == 4:
    Q = 'does not exist'
print(P/c)
if Q == 0: 
    if P == 0.05:
        r = 0.0580
        k1 = 361.4
    elif P == 0.1:
        r = 0.1260
        k1 = 51.64
    elif P == 0.15:
        r = 0.2025
        k1 = 15.957
    elif P == 0.20:
        r = 0.2900
        k1 = 6.643
    elif P == 0.25:
        r = 0.3910
        k1 = 3.23
elif Q == 1:
    if P == 0.1:
        r = 0.1300
        k1 = 51.99
        k2_k1 = 0.000764
    elif P == 0.15:
        r = 0.2170
        k1 = 15.793
        k2_k1 = 0.00677
    elif P == 0.20:
        r = 0.3180
        k1 = 6.520
        k2_k1 = 0.0303
    elif P == 0.25:
        r = 0.4410
        k1 = 3.191
        k2_k1 = 0.1355


#Camber and Gradient
yc = np.zeros((0, len(X)))
dyc_dx = np.zeros((0, len(X)))
theta = np.zeros((0, len(X)))                                   #initializing values 

if len(NACA) == 4:
    for i in range(len(X)):
        if X[i] >= 0 and X[i] < P:
            temp = (M/P**2)*(2*P*X[i] - X[i]**2)
            yc = np.append(yc, [temp])
            temp = (2*M/P**2)*(P-X[i])
            dyc_dx = np.append(dyc_dx, [temp])
        elif X[i] >= P and X[i] <= c:
            temp = (M/(1-P)**2)*(1 - 2*P + 2*P*X[i] - X[i]**2)
            yc = np.append(yc, [temp])
            temp = (2*M/(1-P)**2)*(P-X[i])
            dyc_dx = np.append(dyc_dx, [temp])
else:
    if Q == 0:
        for i in range(len(X)):
            if X[i] >= 0 and X[i] < r:
                temp = (k1/6)*(X[i]**3 - 3*r*X[i]**2 + r**2*(3 - r)*X[i])
                yc = np.append(yc, [temp])
                temp = (k1/6)*(3*X[i]**2 - 6*r*X[i] + r**2*(3 - r))
                dyc_dx = np.append(dyc_dx, [temp])
            elif X[i] >= r and X[i] <= c:
                temp = ((k1*r**3)/6)*(1-X[i])
                yc = np.append(yc, [temp])
                temp = -(k1*r**3)/6
                dyc_dx = np.append(dyc_dx, [temp])

    else:
        for i in range(len(X)):
            if X[i] >= 0 and X[i] < r:
                temp = (k1/6)*((X[i] - r)**3 - k2_k1*(1 - r)**3*X[i] - r**3*X[i] + r**3)
                yc = np.append(yc, [temp])
                temp = (k1/6)*(3*(X[i] - r)**2 - k2_k1*(1 - r)**3 - r**3)
                dyc_dx = np.append(dyc_dx, [temp])
            elif X[i] >= r and X[i] <= c:
                temp = (k1/6)*(k2_k1*(X[i] - r)**3 - k2_k1*(1 - r)**3*X[i] - r**3*X[i] + r**3)
                yc = np.append(yc, [temp])
                temp = (k1/6)*(3*k2_k1*(X[i] - r)**2 - k2_k1*(1 - r)**3 - r**3)
                dyc_dx = np.append(dyc_dx, [temp])
            temp = atan(dyc_dx[i]) 
            theta = np.append(theta,[temp])

for i in range(len(X)):
    temp = atan(dyc_dx[i]) 
    theta = np.append(theta,[temp])

a_open = [0.2969, -0.126, -0.3516, 0.2843, -0.1015]
a_close = [0.2969, -0.126, -0.3516, 0.2843, -0.1036]

yt = np.empty((0, len(X)))
if trailing == True:
    for i in range(len(X)):
        temp = (5*T)*( a_open[0]*(X[i])**0.5 + a_open[1]*(X[i]) + a_open[2]*(X[i])**2 + a_open[3]*(X[i])**3 + a_open[4]*(X[i])**4)
        yt = np.append(yt, [temp])

else:
    for i in range(len(X)):
        temp = (5*T)*( a_close[0]*(X[i])**0.5 + a_close[1]*(X[i]) + a_close[2]*(X[i])**2 + a_close[3]*(X[i])**3 + a_close[4]*(X[i])**4)
        yt = np.append(yt, [temp])

xu = np.empty((0, len(X)))
xl = np.empty((0, len(X)))
yu = np.empty((0, len(X)))
yl = np.empty((0, len(X))) # u - upper boundary l-lower boudary

for i in range(len(X)):
     temp = (X[i] - yt[i]*sin(theta[i]))*c
     xu = np.append(xu, [temp])
     temp = (X[i] + yt[i]*sin(theta[i]))*c
     xl = np.append(xl, [temp])

     temp = (yc[i] + yt[i]*cos(theta[i]))*c
     yu = np.append(yu, [temp])
     temp = (yc[i] - yt[i]*cos(theta[i])*c)
     yl = np.append(yl, [temp])

from matplotlib.pyplot import figure
plt.gca().set_aspect('equal', adjustable='box')
plt.plot(xu,yu,xl,yl,X*c,yc*c)
plt.show()
