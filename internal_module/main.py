import machine, time, math

mq4_pin = machine.ADC(machine.Pin(32))
mq7_pin = machine.ADC(machine.Pin(35))
mq135_pin = machine.ADC(machine.Pin(34))

RL_MQ4 = 20000 # 20K
RL_MQ7 = 10000 # 10K
RL_MQ135 = 20000 # 20K

RESOLUTION = 4095

R0_MQ4 = 0
R0_MQ7 = 0
R0_MQ135 = 0

RCA_MQ4 = 4.452
RCA_MQ7 = 26.402
RCA_MQ135 = 3.597

# Calibration

def calibrate_mq4():

    global R0_MQ4

    avg_voltage = 0

    for i in range(0, 50):
        avg_voltage += mq4_pin.read() * 5 / RESOLUTION
        print('MQ4 Calibration: ' + i*2 + '%')
        time.sleep(1)

    avg_voltage = avg_voltage / 50

    if avg_voltage >= 5:
        avg_voltage = 4.999

    rs = RL_MQ4 * (5-avg_voltage) / avg_voltage

    R0_MQ4 = rs / RCA_MQ4
    
    print('MQ4 Sensor Calibrated Successfully, R0 = ' + str(R0_MQ4))

def calibrate_mq7():
    
    global R0_MQ7

    avg_voltage = 0
    
    for i in range(0, 50):
        avg_voltage += mq7_pin.read() * 5 / RESOLUTION
        print('MQ7 Calibration: ' + i*2 + '%')
        time.sleep(1)

    avg_voltage = avg_voltage / 50

    if avg_voltage >= 5:
        avg_voltage = 4.999

    rs = RL_MQ7 * (5-avg_voltage) / avg_voltage

    R0_MQ7 = rs / RCA_MQ7
    
    print('MQ7 Sensor Calibrated Successfully, R0 = ' + str(R0_MQ7))

def calibrate_mq135():
    
    global R0_MQ135

    avg_voltage = 0
    
    for i in range(0, 50):
        avg_voltage += mq135_pin.read() * 5 / RESOLUTION
        print('MQ135 Calibration: ' + i*2 + '%')
        time.sleep(1)

    avg_voltage = avg_voltage / 50

    if avg_voltage >= 5:
        avg_voltage = 4.999

    rs = RL_MQ135 * (5-avg_voltage) / avg_voltage

    R0_MQ135 = rs / RCA_MQ135
    
    print('MQ135 Sensor Calibrated Successfully, R0 = ' + str(R0_MQ135))

# MQ4

def get_ch4_ppm():

    # MQ4 CH4 Calculation

    global R0_MQ4
    
    mq4_voltage = 0
    
    for i in range(0, 25):
        mq4_voltage += mq4_pin.read() * 5 / RESOLUTION
        time.sleep(0.1)

    mq4_voltage = mq4_voltage / 25

    if mq4_voltage >= 5:
        mq4_voltage = 4.999

    rs = RL_MQ4 * (5-mq4_voltage) / mq4_voltage

    rs_r0_ratio = rs/R0_MQ4

    ch4 = pow(rs_r0_ratio/11.5, 1/-0.353)
    # ch4 = pow(10,-2.78*math.log10(rs_r0_ratio)+2.98)

    if(ch4 > 10000):
        ch4 = '+10K'
    else:
        if(ch4 >= 1000):
            ch4 = str(round(ch4/1000, 2)) + 'K'

    return ch4

def get_lpg_ppm():

    # MQ4 LPG Calculation

    global R0_MQ4
    
    mq4_voltage = 0
    
    for i in range(0, 25):
        mq4_voltage += mq4_pin.read() * 5 / RESOLUTION
        time.sleep(0.1)

    mq4_voltage = mq4_voltage / 25

    if mq4_voltage >= 5:
        mq4_voltage = 4.999

    rs = RL_MQ4 * (5-mq4_voltage) / mq4_voltage

    rs_r0_ratio = rs/R0_MQ4

    lpg = pow(rs_r0_ratio/13.6, 1/-0.317)

    if(lpg > 10000):
        lpg = '+10K'
    else:
        if(lpg >= 1000):
            lpg = str(round(lpg/1000, 2)) + 'K'

    return lpg

# MQ7

def get_co_ppm():

    # MQ7 CO Calculation

    global R0_MQ7
    
    mq7_voltage = 0
    
    for i in range(0, 25):
        mq7_voltage += mq7_pin.read() * 5 / RESOLUTION
        time.sleep(0.1)

    mq7_voltage = mq7_voltage / 25

    if mq7_voltage >= 5:
        mq7_voltage = 4.999

    rs = RL_MQ7 * (5-mq7_voltage) / mq7_voltage

    rs_r0_ratio = rs/R0_MQ7

    co = pow(rs_r0_ratio/19.1, 1/-0.645)

    if(co > 10000):
        co = '+10K'
    else:
        if(co >= 1000):
            co = str(round(co/1000, 2)) + 'K'

    return co

# MQ135

def get_co2_ppm():

    # MQ135 CO2 Calculation

    global R0_MQ135
    
    mq135_voltage = 0
    
    for i in range(0, 25):
        mq135_voltage += mq135_pin.read() * 5 / RESOLUTION
        time.sleep(0.1)

    mq135_voltage = mq135_voltage / 25

    if mq135_voltage >= 5:
        mq135_voltage = 4.999

    rs = RL_MQ135 * (5-mq135_voltage) / mq135_voltage

    rs_r0_ratio = rs/R0_MQ135

    co2 = pow(rs_r0_ratio/5.11, 1/-0.343)

    if(co2 > 10000):
        co2 = '+10K'
    else:
        if(co2 >= 1000):
            co2 = str(round(co2/1000, 2)) + 'K'

    return co2


# * Calibration

calibrate_mq4()
#calibrate_mq7()
#calibrate_mq135()

# * Calculations every 3.5 seconds (sensors read in 2.5 seconds due to the 25 times loop to increase accuracy)

while(True):

    print('CH4 PPM: ' + str(get_ch4_ppm()))
    #print('LPG PPM: ' + str(get_lpg_ppm()))
    #print('CO PPM: ' + str(get_co_ppm()))
    #print('CO2 PPM: ' + str(get_co2_ppm()))

    time.sleep(1)