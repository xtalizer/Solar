#Solar Efficiency
    
import math
    
def solareff(volt_stc,amps_stc,eff_stc,pow_stc,irradiance_stc,temp_stc,ff,volt_change,amps_change,pow_change,length,width,irradiance,temp_mod):
    
    #STC parameters
    #volt_stc=68.2
    #amps_stc=6.39
    #eff_stc=1
    #pow_stc=1
    #irradiance_stc=300
    #temp_stc=298
    
    #Module parameters
    #ff=0.23
    #volt_change=1 #partial derivative of voltage with temperature
    #amps_change=1 #partial derivative of current with temperature
    #pow_change=1
    #length=1
    #width=1
    
    #External parameters
    #irradiance=350
    #temp_mod=299
    
    if(irradiance>0):
        #constant temp conditions
        volt_temp=volt_stc*math.log(irradiance)/math.log(irradiance_stc)
        amps_temp=amps_stc*irradiance/irradiance_stc
        pow_temp=ff*volt_temp*amps_temp
        eff_temp=pow_temp/(length*width*irradiance)
        
        #constant irradiation conditions
        pow_irad=pow_stc+pow_change*(temp_mod-temp_stc)
        eff_irad=pow_irad/irradiance_stc
        eff_change=(eff_irad-eff_stc)/(temp_mod-temp_stc)
        
        #efficiency calculation
        eff_solar=eff_temp*(1+(temp_mod-temp_stc)*eff_change/eff_stc)
    else:
        eff_solar=0

    return eff_solar