
'''Please run all the code in the sequence in which they are written. Thank you.'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from gatspy.periodic import LombScargle




df=pd.read_csv('Binary_data_2.csv')




r1=df['redshift1'].values.tolist()
r2=df['redshift2'].values.tolist()
vrad1 = []
vrad2 = []
for i in r1:
    vr1=3*(10**8)*i
    vrad1.append(vr1)
for j in r2:
    vr2=3*(10**8)*j
    vrad2.append(vr2)



def fit_curve():
    fig,(a1,a2) =  plt.subplots(2,1)

    y=np.array(vrad1)
    y1=np.array(vrad2)
    x=np.array(df['#time'].values.tolist())


    def test(x,a, b,c,d): 
        return a*np.sin(b * x+c)+d

    params1, params1_cov = curve_fit(test, x, y,p0=[0,2,0,2]) 
    a1.scatter(x,y,color='red',label=r'Orbital Velocity$_1$',s=0.6)
    a1.plot(x,test(x,params1[0],params1[1],params1[2],params1[3]),'b-',label="Fitted Sine Curve")
    a1.legend(loc="lower right")
    a1.title.set_text("Star 1")


    def test(x,a, b,c,d): 
        return a*np.sin(b * x+c)+d

    params2, params2_cov = curve_fit(test, x, y1,p0=[0,2,0,2]) 
    a2.scatter(x,y1,color='red',label=r'Orbital Velocity$_2$',s=0.6)
    a2.plot(x,test(x,params2[0],params2[1],params2[2],params2[3]),'b-',label="Fitted Sine Curve")
    a2.legend(loc="lower right")
    a2.title.set_text("Star 2")
    a1.set_ylabel("Velocity (m/s)")
    a2.set_ylabel("Velocity (m/s)")
    a2.set_xlabel("Time (years)")
    plt.show()
    return print(f'Parameters of star1 = {params1}\nParameters of star2 = {params2}')



params1=np.array([-1.46574182e+04, -1.79492052e+00, -1.55512404e+01,  2.61048315e+04])
params2=np.array([ 1.12782216e+04,  1.79479492e+00, -1.55991796e-01,  2.60953773e+04])
def periodogram():
    x=np.array(df['#time'].values.tolist())
    y1=params1[0]*np.sin(params1[1]*x-params1[2])+params1[3]
    y2=params2[0]*np.sin(params2[1]*x-params2[2])+params2[3]
    model1 = LombScargle().fit(x, y1)
    model2 = LombScargle().fit(x, y2)
    periods1, power1 = model1.periodogram_auto()
    periods2, power2 = model2.periodogram_auto()
    plt.title("Periodogram")
    plt.plot(periods1, power1,color='red',label='Star 1')
    plt.scatter(periods2, power2,label='Star 2')
    plt.legend(loc="lower right")
    plt.ylabel("Lomb-Scargle Power")
    plt.xlabel("Period (Years)")
    plt.xlim(2,5)
    plt.show()
    return




vorbital1=''
vorbital2=''
t=''

def velocity():
    global vorbital1
    global vorbital2
    x = np.array(df['#time'].values.tolist())
    v1=params1[0]*np.sin(params1[1]*x-params1[2])+params1[3]
    v2=params2[0]*np.sin(params2[1]*x-params2[2])+params2[3]
    vorbital1=(max(v1)-min(v1))/2
    vorbital2=(max(v2)-min(v2))/2
    print(f'Orbital velocity of star 1 is {round(vorbital1,2)} m/s \nOrbital velocity of star 2 is {round(vorbital2,2)} m/s ')
    return 
def time_period():
    global t
    x=np.array(df['#time'].values.tolist())
    y=params1[0]*np.sin(params1[1]*x-params1[2])+params1[3]
    model = LombScargle().fit(x, y)
    model.optimizer.period_range=(3, 4)
    t = model.best_period
    print(f'\n\nPeriod of revolution is: {t:.3f} years')
    return 
def mass():
    a1=(t*vorbital1*365*24*60*60)/(2*np.pi)
    a2=(t*vorbital2*365*24*60*60)/(2*np.pi)
    mtot=(t*365*24*60*60*(vorbital1+vorbital2)**3)/(2*np.pi*6.67e-11)
    m2=(mtot*a1)/(a1+a2)
    m1=(mtot*a2)/(a1+a2)
    return print(f'{a1}\n\n{a2}\n\nMass of lighter star is: {m1} kgs \nMass of heavier star is: {m2} kgs')  

velocity()
fit_curve()
periodogram()
time_period()
mass()





