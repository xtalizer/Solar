#Solar Angle Calculations
    
import math
    
def daysinmonth(month,year):
    normal=[31,28,31,30,31,30,31,31,30,31,30,31]
    leap=[31,29,31,30,31,30,31,31,30,31,30,31]
    daysum=0
    if(year%4==0):
        for p in range(0,month-1):
            daysum=daysum+leap[p]
    else:
        for q in range(0,month-1):
            daysum=daysum+normal[q]
    return daysum

def invtan(y,x):
    theta=math.atan2(y,x)
    if(theta<0):
        theta=2*math.pi+theta
    return theta

def solarangle(date,time,utc,longitude,latitude):
    '''
    input date[mm,dd,yy] time[hh,mm], utc h in advance, longitude, latitude in degrees
    returns the solar angles as [azimuth,altitude] in degrees.
    '''
    
    #Date and time
    #date=[4,14,14] #mm/dd/yy
    #time=[11,0] #24h format, hh:mm
    #utc=2 #hours in advance of UTC
    
    #Coordinates in degrees (+) if N or E (-) if S or W
    #longitude=4.36
    #latitude=52.01
    
    #Initialized Variables
    D=0 #days since Jan 1 2000 12nn UTC
    q=0 #mean lognitude
    g=0 #mean anomaly
    lambda_s=0 #ecliptic longitude
    R=0 #radiation
    epsilon=0 #tilt from equatorial to ecliptic
    gmst=0 #Greenwich mean sidereal time
    theta_l=0 #local mean sidereal time
    x_s=0 #x coordinate
    y_s=0
    z_s=0
    
    #Preliminary Calcs
    D=math.floor(365.25*date[2])+daysinmonth(date[0],date[2])+date[1]-0.5+(time[0]+time[1]/60.0-utc)/24.0
    q=(280.459+0.98564736*D)%360
    g=(357.529+0.98560028*D)%360
    lambda_s=q+1.915*math.sin(math.radians(g))+0.020*math.sin(2*math.radians(g))
    #R=1.00014-0.0167*math.cos(math.radians(g))-0.00014*math.cos(2*math.radians(g))
    epsilon=23.429-0.00000036*D
    gmst=(18.697374558+24.06570982441908*D+0.000026*(D/36525)**2)%24
    theta_l=gmst*15+longitude
    #print(D)
    
    #Conversion to Radians
    theta_l=math.radians(theta_l)
    lambda_s=math.radians(lambda_s)
    epsilon=math.radians(epsilon)
    latitude=math.radians(latitude)
    
    #Azimuth and Altitude
    y_s=-math.sin(theta_l)*math.cos(lambda_s)+math.cos(theta_l)*math.cos(epsilon)*math.sin(lambda_s)
    x_s=-math.sin(latitude)*math.cos(theta_l)*math.cos(lambda_s)-(math.sin(latitude)*math.sin(theta_l)*math.cos(epsilon)-math.cos(latitude)*math.sin(epsilon))*math.sin(lambda_s)
    z_s=math.cos(latitude)*math.cos(theta_l)*math.cos(lambda_s)+(math.cos(latitude)*math.sin(theta_l)*math.cos(epsilon)+math.sin(latitude)*math.sin(epsilon))*math.sin(lambda_s)
    
    #azimuth,altitude
    return [math.degrees(invtan(y_s,x_s)),math.degrees(math.asin(z_s))]