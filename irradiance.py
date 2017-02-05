#Irradiance

import math

def irrad(azimuth_solar,altitude_solar,azimuth_mod,altitude_mod,elevation):
    '''
    input solar and module azimuth and altitude
    returns direct irradiance
    '''
    
    if(altitude_solar<0):
        return 0 #check if sun is above ground

    #convert to radians
    azimuth_solar=math.radians(azimuth_solar)
    altitude_solar=math.radians(altitude_solar)
    azimuth_mod=math.radians(azimuth_mod)
    altitude_mod=math.radians(altitude_mod)
    
    #cosine of angle between solar module and sun
    cosine=math.cos(altitude_mod)*math.cos(altitude_solar)*math.cos(azimuth_mod-azimuth_solar)+math.sin(altitude_mod)*math.sin(altitude_solar)

    if(cosine<0):
        return 0 #check if sun is in front of module
    else:  
        #irradiance calculation
        SOLAR=1361 #solar constant
        am=1/(math.sin(altitude_solar)+0.50572*(6.07995+math.degrees(altitude_solar))**-1.6364)
        i_dir=SOLAR*((1-0.14*elevation)*0.7**(am**0.678)+0.14*elevation)
        
        return i_dir*cosine #direct irradiance