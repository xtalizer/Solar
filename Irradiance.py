#Irradiance

import math

def directirradiance(azimuth_solar,altitude_solar,azimuth_mod,altitude_mod,h):
    '''
    input solar and module azimuth and altitude
    returns direct irradiance
    '''
    
    #Angles
    #azimuth_solar=4 #solar azimuth angle
    #altitude_solar=36.1094950838 #solar altitude angle
    #azimuth_mod=27 #solar altitude
    #altitude_mod=45 #module altitude
    
    #Check for validity
    if(altitude_solar<0):
        return 0

    #Convert to radians
    azimuth_solar=math.radians(azimuth_solar)
    altitude_solar=math.radians(altitude_solar)
    azimuth_mod=math.radians(azimuth_mod)
    altitude_mod=math.radians(altitude_mod)
    cosine=math.cos(altitude_mod)*math.cos(altitude_solar)*math.cos(azimuth_mod-azimuth_solar)+math.sin(altitude_mod)*math.sin(altitude_solar)

    if(cosine<0):
        return 0
    else:  
        #Irradiance Calculation
        solarconstant=1361 #solar constant
        c=0.14 #empirical constant
        am=1/(math.sin(altitude_solar)+0.50572*(6.07995+math.degrees(altitude_solar))**-1.6364)
        i_dir=solarconstant*((1-c*h)*0.7**(am**0.678)+c*h)
        
        #Direct Irradiance
        return (i_dir*cosine)