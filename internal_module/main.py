import machine, time, math

mq4_pin = machine.ADC(machine.Pin(32))
mq7_pin = machine.ADC(machine.Pin(35))
mq135_pin = machine.ADC(machine.Pin(34))

RL_MQ4 = 20000 # 20K
RL_MQ7 = 10000 # 10K
RL_MQ135 = 20000 # 20K

RCA_MQ4 = 4.452
RCA_MQ7 = 26.402
RCA_MQ135 = 3.597

RESOLUTION = 4095

MQ4_VALUES = {'pin': mq4_pin, 'rl': RL_MQ4, 'r0': 0, 'rca': RCA_MQ4, 'name': 'MQ4'}
MQ7_VALUES = {'pin': mq7_pin, 'rl': RL_MQ7, 'r0': 0, 'rca': RCA_MQ7, 'name': 'MQ7'}
MQ135_VALUES = {'pin': mq135_pin, 'rl': RL_MQ135, 'r0': 0, 'rca': RCA_MQ135, 'name': 'MQ135'}

CH4_VALUES = {'sensor': MQ4_VALUES, 'a': 11.5, 'b': 1/-0.353}
LPG_VALUES = {'sensor': MQ4_VALUES, 'a': 13.6, 'b': 1/-0.317}
CO_VALUES = {'sensor': MQ7_VALUES, 'a': 19.1, 'b': 1/-0.645}
CO2_VALUES = {'sensor': MQ135_VALUES, 'a': 5.11, 'b': 1/-0.343}

# Calibration

def calibrate(mq_values):

    avg_voltage = 0

    for i in range(0, 50):
        avg_voltage += mq_values['pin'].read() * 5 / RESOLUTION
        print(mq_values['name'] + ' Calibration: ' + str(i*2) + '%')
        time.sleep(1)

    avg_voltage = avg_voltage / 50

    if avg_voltage >= 5:
        avg_voltage = 4.999

    rs = mq_values['rl'] * (5-avg_voltage) / avg_voltage

    mq_values['r0'] = rs / mq_values['rca']
    
    print(mq_values['name'] + ' Sensor Calibrated Successfully, R0 = ' + str(mq_values['r0']))

def get_ppm(gas_value):

    # PPM Calculation

    voltage = 0
    
    for i in range(0, 25):
        voltage += gas_value['sensor']['pin'].read() * 5 / RESOLUTION
        time.sleep(0.1)

    voltage = voltage / 25

    if voltage >= 5:
        voltage = 4.999

    rs = gas_value['sensor']['rl'] * (5-voltage) / voltage

    rs_r0_ratio = rs/gas_value['sensor']['r0']

    gas = pow(rs_r0_ratio/gas_value['a'], gas_value['b'])

    if(gas > 10000):
        gas = '+10K'
    else:
        if(gas >= 1000):
            gas = str(round(gas/1000, 2)) + 'K'

    return gas

# * Calibration

calibrate(MQ4_VALUES)
calibrate(MQ7_VALUES)
calibrate(MQ135_VALUES)

# * Calculations every 3.5 seconds (sensors read in 2.5 seconds due to the 25 times loop to increase accuracy)

while(True):

    print('CH4 PPM: ' + str(get_ppm(CH4_VALUES)))
    #print('LPG PPM: ' + str(get_ppm(LPG_VALUES)))
    #print('CO PPM: ' + str(get_ppm(CO_VALUES)))
    #print('CO2 PPM: ' + str(get_ppm(CO2_VALUES)))

    time.sleep(1)