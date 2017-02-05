#Battery Calculations

import math

#battery specs
amphour_full=2.6
res_int=0.07
c_rating=0.02
volt_full=4.18
volt_exp=3.8
volt_nom=3.62
soc_exp=0.6
soc_nom=0.08

dhour=1 #incremental hour
amps=0.5

#parameter calculation
amphour_exp=amphour_full*soc_exp
amphour_nom=amphour_full*soc_nom
a=volt_full-volt_exp
b=3/amphour_exp
k=(volt_full-volt_nom+a*(math.exp(-b*amphour_nom)-1))*(amphour_full-amphour_nom)/amphour_nom
volt_init=volt_full+k+res_int*amphour_full*c_rating-a

volt=volt_init-res_int*amps-k*(amphour_full/(amphour_full-amps*dhour))+a*math.exp(-b*amps*dhour)
print(volt)