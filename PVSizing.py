#PV Sizing

import math   
import LoadProfile
import SolarAngle    
import Irradiance
import SolarEfficiency

def spfloor(x):
    if (math.floor(x)==0):
        return 1
    else:
        return math.floor(x)

## Load Parameters ##
rel_load=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
kWhmo_load=700

## PV Module Specifications ##

#STC Specifications
volt_stc=68.2
amps_stc=6.39
eff_stc=1
pow_stc=1
irradiance_stc=300 #watts
temp_stc=298.15

#Partial Derivatives
volt_change=1 #partial derivative of voltage with temperature
amps_change=1 #partial derivative of current with temperature
pow_change=1

#Misc
ff=0.23
length=1.625
width=1.019
temp_mod=318.85
sf_mod=1.1
volt_mod_mpp=31.2

#Design constraints
azimuth_mod=0
altitude_mod=10
height=5

## Battery Specifications ##

#Battery Specifications
volt_batt=12 #open circuit voltage
amphour_batt=1000 #charge

#Design Constraints
days_auto=1 #days of autonomy
sf_batt=1 #sizing factor
dod=0.8 #max discharge (temporary)
volt_bb=96 #battery bank voltage

## Date and Location ##
date=[1,29,17]
utc=8
latitude=121.066269
longitude=14.654284

## Calculations ##

#Load Profile Calculations
load=LoadProfile. loadprofile(kWhmo_load,rel_load)
kWh_load=kWhmo_load/30.0

#Battery Calculations
kWh_bb=days_auto*kWh_load*sf_batt/dod
kWh_batt=volt_batt*amphour_batt/1000
N_bat=math.ceil(kWh_bb/kWh_batt)
N_batser=volt_bb/volt_batt
N_batpar=math.ceil(N_bat/N_batser) #number of batteries

#Determine power generation at each time of the day
pv=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
for p in range(0,len(pv)):
    angle_solar=SolarAngle.solarangle(date,[p,0],utc,longitude,latitude)
    irradiance=Irradiance.directirradiance(angle_solar[0],angle_solar[1],azimuth_mod,altitude_mod,height)
    #eff_solar=SolarEfficiency.solareff(volt_stc,amps_stc,eff_stc,pow_stc,irradiance_stc,temp_stc,ff,volt_change,amps_change,pow_change,length,width,irradiance,temp_mod)
    eff_solar=0.154
    pv[p]=irradiance*eff_solar
pv.append(pv[0])

#Determine total power generations (Simpsons rule)
integral=0
for q in range(1,(1+len(pv))//2):
    integral=integral+pv[2*q-2]+4*pv[2*q-1]+pv[2*q]
del pv[len(pv)-1] #remove added item
integral=integral*(24.0/len(pv))/3.0

#Determine number of modules used
N_mod=math.ceil((kWh_load*sf_mod*1000)/(length*width*integral))
N_modser=spfloor(volt_bb/volt_mod_mpp)
N_modpar=math.ceil(N_mod/N_modser)

print('kWh from batt',kWh_bb)
print('kWh from PV',length*width*integral*N_mod/1000)