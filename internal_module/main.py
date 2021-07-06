import machine, time

mq4_pin = machine.ADC(machine.Pin(36))
mq7_pin = machine.ADC(machine.Pin(39))
mq135_pin = machine.ADC(machine.Pin(34))

RL_MQ4 = 1000
RL_MQ7 = 1000
RL_MQ135 = 1000

R0_MQ4 = None
R0_MQ7 = None
R0_MQ135 = None

# Calibration

def calibrate_mq4():
    pass

def calibrate_mq7():
    pass

def calibrate_mq135():
    pass

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

    rs = RL_MQ7 * (5-mq7_voltaje) / mq7_voltaje  # TODO Calculamos Rs con un RL de 1k
    
    rs_r0_ratio = rs/R0_MQ7

    co = pow(rs_r0_ratio/19.1, 1/-0.645)

    return co

# MQ135

def get_co2_ppm():
    # MQ135 CO2 Calculation

    mq135_voltage = mq135_pin.read() * (5.0 / 1023.0)

    rs = RL_MQ135 * (5-mq135_voltage) / mq135_voltage  # TODO Calculamos Rs con un RL de 1k
    
    rs_r0_ratio = rs/R0_MQ135

    co2 = pow(rs_r0_ratio/5.11, 1/-0.343)

    return co2

