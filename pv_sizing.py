#PV Sizing

import math   
import load_profile
import irradiance
import solar_angle

def spfloor(x):
    if (math.floor(x)==0):
        return 1
    else:
        return math.floor(x)

## Load Parameters ##
rel_load=[525,525,525,525,
          525,665,665,665,
          645,645,645,645,
          645,645,645,645,
          645,735,735,735,
          741,621,621,615]
kwhmo_load=150

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
sf_mod=1
volt_mod_mpp=31.2

#Design constraints
azimuth_mod=0
altitude_mod=10
height=5

## Battery Specifications ##

#Battery Specifications
volt_nom=3.8 #open circuit voltage
amphour_full=2.6 #charge

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
kwh_load=kwhmo_load/30.0
load=load_profile.actual_load(kwhmo_load,rel_load)

#Battery Calculations
kwh_bb=days_auto*kwh_load*sf_batt/dod
kwh_batt=volt_nom*amphour_full/1000
n_bat=math.ceil(kwh_bb/kwh_batt)
n_batser=volt_bb/volt_nom
n_batpar=math.ceil(n_bat/n_batser) #number of batteries

#Determine power generation at each time of the day
pv=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
for p in range(0,len(pv)):
    angle_solar=solar_angle.sol_angle(date,[p,0],utc,longitude,latitude)
    ir_dir=irradiance.irrad(angle_solar[0],angle_solar[1],azimuth_mod,altitude_mod,height)
    #eff_solar=solar_eff.solareff(volt_stc,amps_stc,eff_stc,pow_stc,irradiance_stc,temp_stc,ff,volt_change,amps_change,pow_change,length,width,irradiance,temp_mod)
    eff_solar=0.154
    pv[p]=ir_dir*eff_solar #unit: W

#Determine total power generation (Simpsons rule)
integral=0
pv.append(pv[0])
for q in range(1,(1+len(pv))//2):
    integral=integral+pv[2*q-2]+4*pv[2*q-1]+pv[2*q]
del pv[len(pv)-1] #remove added item
integral=integral*(24.0/len(pv))/3.0 #intensity in W/m^2

#Determine number of modules used
n_mod=math.ceil((kwh_load*sf_mod*1000)/(length*width*integral))
n_modser=spfloor(volt_bb/volt_mod_mpp)
n_modpar=math.ceil(n_mod/n_modser)

#Determine profiles
pv_total=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
load_total=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
batt_total=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
for x1 in range(0,len(load_total)):
    load_total[x1]=load[x1]*(-1000)
for x2 in range(0,len(pv_total)):
    pv_total[x2]=pv[x2]*n_mod*length*width
for x3 in range(0,len(batt_total)):
    batt_total[x3]=-(load_total[x3]+pv_total[x3])

print('Hourly load (W)')
for inc1 in range(0,len(load_total)//6):
    print(
    '{0:8}  {1:8}  {2:8}  {3:8}  {4:8}  {5:8}'
    .format(load_total[6*inc1],load_total[6*inc1+1],load_total[6*inc1+2],load_total[6*inc1+3],load_total[6*inc1+4],load_total[6*inc1+5])
    )
print('Daily load (kWh): {0:.4f}'.format(kwh_load))

print('')
print('Battery profile (W)')
for inc2 in range(0,len(batt_total)//6):
    print(
    '{0:8}  {1:8}  {2:8}  {3:8}  {4:8}  {5:8}'
    .format(batt_total[6*inc2],batt_total[6*inc2+1],batt_total[6*inc2+2],batt_total[6*inc2+3],batt_total[6*inc2+4],batt_total[6*inc2+5])
    )
print('Number of batteries: {0:.0f}'.format(n_bat))
print('Energy from batteries (kWh): {0:.4f}'.format(kwh_bb))

print('')
print('Hourly PV gains (W)')
for inc3 in range(0,len(pv_total)//6):
    print(
    '{0:8}  {1:8}  {2:8}  {3:8}  {4:8}  {5:8}'
    .format(pv_total[6*inc3],pv_total[6*inc3+1],pv_total[6*inc3+2],pv_total[6*inc3+3],pv_total[6*inc3+4],pv_total[6*inc3+5])
    )
print('Number of PV modules: {0:.0f}'.format(n_mod))
print('Energy from PV (kWh): {0:.4f}'.format(length*width*integral*n_mod/1000))

