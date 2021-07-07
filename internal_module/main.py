import machine, time

mq4_pin = machine.ADC(machine.Pin(36))
mq7_pin = machine.ADC(machine.Pin(39))
mq135_pin = machine.ADC(machine.Pin(34))

RL_MQ4 = 20000 # 20K
RL_MQ7 = 10000 # 10K
RL_MQ135 = 20000 # 20K

R0_MQ4 = None
R0_MQ7 = None
R0_MQ135 = None

RCA_MQ4 = 4.452
RCA_MQ7 = 26.402
RCA_MQ135 = 3.597

# Calibration

def calibrate_mq4():

    global R0_MQ4

    avg_voltage = None
    
    for i in range(0, 50):
        avg_voltage += mq4_pin.read() * 5 / 1023
        time.sleep(0.5)

    avg_voltage = avg_voltage / 50

    rs = RL_MQ4 * (5-avg_voltage) / avg_voltage

    R0_MQ4 = rs / RCA_MQ4

    print(f'MQ4 Sensor Calibrated Successfully, R0 = {R0_MQ4}')

def calibrate_mq7():
    
    global R0_MQ7

    avg_voltage = None
    
    for i in range(0, 50):
        avg_voltage += mq7_pin.read() * 5 / 1023
        time.sleep(0.5)

    avg_voltage = avg_voltage / 50

    rs = RL_MQ7 * (5-avg_voltage) / avg_voltage

    R0_MQ7 = rs / RCA_MQ7

    print(f'MQ7 Sensor Calibrated Successfully, R0 = {R0_MQ7}')

def calibrate_mq135():
    
    global R0_MQ135

    avg_voltage = None
    
    for i in range(0, 50):
        avg_voltage += mq135_pin.read() * 5 / 1023
        time.sleep(0.5)

    avg_voltage = avg_voltage / 50

    rs = RL_MQ135 * (5-avg_voltage) / avg_voltage

    R0_MQ135 = rs / RCA_MQ135

    print(f'MQ135 Sensor Calibrated Successfully, R0 = {R0_MQ135}')

# MQ4

def get_ch4_ppm():

    # MQ4 CH4 Calculation

    mq4_voltage = mq4_pin.read() * (5.0 / 1023.0)

    rs = RL_MQ4 * (5-mq4_voltage) / mq4_voltage

    rs_r0_ratio = rs/R0_MQ4

    ch4 = pow(rs_r0_ratio/11.5, 1/-0.353)

    return ch4

def get_lpg_ppm():

    # MQ4 LPG Calculation

    mq4_voltage = mq4_pin.read() * (5.0 / 1023.0)

    rs = RL_MQ4 * (5-mq4_voltage) / mq4_voltage
    
    rs_r0_ratio = rs/R0_MQ4

    lpg = pow(rs_r0_ratio/13.6, 1/-0.317)

    return lpg

# MQ7

def get_co_ppm():
    # MQ7 CO Calculation

    mq7_voltaje = mq7_pin.read() * (5.0 / 1023.0)

    rs = RL_MQ7 * (5-mq7_voltaje) / mq7_voltaje
    
    rs_r0_ratio = rs/R0_MQ7

    co = pow(rs_r0_ratio/19.1, 1/-0.645)

    return co

# MQ135

def get_co2_ppm():
    # MQ135 CO2 Calculation

    mq135_voltage = mq135_pin.read() * (5.0 / 1023.0)

    rs = RL_MQ135 * (5-mq135_voltage) / mq135_voltage
    
    rs_r0_ratio = rs/R0_MQ135

    co2 = pow(rs_r0_ratio/5.11, 1/-0.343)

    return co2



# * Calibration

calibrate_mq4()
calibrate_mq7()
calibrate_mq135()

# * Calculations every 10 seconds

while(True):

    print(f'CH4 PPM: {get_ch4_ppm()}')
    print(f'LPG PPM: {get_lpg_ppm()}')
    print(f'CO PPM: {get_co_ppm()}')
    print(f'CO2 PPM: {get_co2_ppm()}')

    time.sleep(10)