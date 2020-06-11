#four digit NACA generator
import numpy as np
from math import atan
from math import sin
from math import cos
import matplotlib.pyplot as plt

# raw_num = input('Enter 4 digit NACA airfoil number: ')
# trailing = input('Enter \'True\' for open trailing edge. Enter \'False\' for closed trailing edge: ')
# Npanel = input('Enter number of grid points: ')

## User inputs
trailing = False
raw_num = '0012'
NACA = list(raw_num)
NGrid = 500

#Breaking the NACA four digit code 
M = int(NACA[0])/100 #maximun camber
P = int(NACA[1])/10 #position of maximun camber
T = int(NACA[2]+ NACA[3])/100 #thickness of the chord

#Camber and Gradient
X = np.linspace(0,1,NGrid) # This contains the chord length as well

yc = np.zeros((0, len(X)))
dyc_dx = np.empty((0, len(X)))
theta = np.empty((0, len(X)))

for i in range(len(X)):
   
    if X[i] >= 0 and X[i] < P:
         temp = (M/P**2)*((2*P*X[i]) - X[i]**2)
         yc = np.append(yc, [temp])
         temp = (2*M/P**2)*(P-X[i])
         dyc_dx = np.append(dyc_dx, [temp])
    elif X[i] >= P and X[i] <= 1:
         temp = (M/(1-P)**2)*(1 - 2*P + 2*P*X[i] - X[i]**2)
         yc = np.append(yc, [temp])
         temp = (2*M/(1-P)**2)*(P-X[i])
         dyc_dx = np.append(dyc_dx, [temp])
     
    temp = atan(dyc_dx[i]) 
    theta = np.append(theta,[temp])
     
     

#thickness distribution
a_open = [0.2969, -0.126, -0.3516, 0.2843, -0.1015]
a_close = [0.2969, -0.126, -0.3516, 0.2843, -0.1036]

yt = np.empty((0, len(X)))
if trailing == True:
    for i in X:
        temp = (5*T)*( a_open[0]*i**0.5 + a_open[1]*i + a_open[2]*i**2 + a_open[3]*i**3 + a_open[4]*i**4)
        yt = np.append(yt, [temp])

else:
    for i in X:
        temp = (5*T)*( a_close[0]*i**0.5 + a_close[1]*i + a_close[2]*i**2 + a_close[3]*i**3 + a_close[4]*i**4)
        yt = np.append(yt, [temp])

xu = np.empty((0, len(X)))
xl = np.empty((0, len(X)))
yu = np.empty((0, len(X)))
yl = np.empty((0, len(X))) # u - upper boundary l-lower boudary

for i in range(len(X)):
     temp = X[i] - yt[i]*sin(theta[i])
     xu = np.append(xu, [temp])
     temp = X[i] + yt[i]*sin(theta[i])
     xl = np.append(xl, [temp])

     temp = yc[i] + yt[i]*cos(theta[i])
     yu = np.append(yu, [temp])
     temp = yc[i] - yt[i]*cos(theta[i])
     yl = np.append(yl, [temp])

from matplotlib.pyplot import figure
figure(num=None, figsize=(15, 5), dpi=80, facecolor='k', edgecolor='k')
plt.plot(xu,yu,xl,yl)
plt.show()






