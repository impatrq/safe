import machine, time
from networking import connect_to_wifi, env_update

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
MAX_INPUT_VOLTAGE = 3.3

MQ4_VALUES = {'pin': mq4_pin, 'rl': RL_MQ4, 'r0': 0, 'rca': RCA_MQ4, 'name': 'MQ4'}
MQ7_VALUES = {'pin': mq7_pin, 'rl': RL_MQ7, 'r0': 0, 'rca': RCA_MQ7, 'name': 'MQ7'}
MQ135_VALUES = {'pin': mq135_pin, 'rl': RL_MQ135, 'r0': 0, 'rca': RCA_MQ135, 'name': 'MQ135'}

CH4_VALUES = {'sensor': MQ4_VALUES, 'a': 11.5, 'b': 1/-0.353}
LPG_VALUES = {'sensor': MQ4_VALUES, 'a': 13.6, 'b': 1/-0.317}
CO_VALUES = {'sensor': MQ7_VALUES, 'a': 19.1, 'b': 1/-0.645}
CO2_VALUES = {'sensor': MQ135_VALUES, 'a': 5.11, 'b': 1/-0.343}


def calibrate(mq_values):

    # Calibration

    avg_voltage = 0

    for i in range(0, 50):
        avg_voltage += mq_values['pin'].read() * MAX_INPUT_VOLTAGE / RESOLUTION
        print(mq_values['name'] + ' Calibration: ' + str(i*2) + '%')
        time.sleep(1)

    avg_voltage = avg_voltage / 50

    if avg_voltage >= MAX_INPUT_VOLTAGE:
        avg_voltage = 3.2999

    rs = mq_values['rl'] * (MAX_INPUT_VOLTAGE-avg_voltage) / avg_voltage

    mq_values['r0'] = rs / mq_values['rca']
    
    print(mq_values['name'] + ' Sensor Calibrated Successfully, R0 = ' + str(mq_values['r0']))

def get_ppm(gas_value):

    # PPM Calculation

    voltage = 0
    
    for i in range(0, 25):
        voltage += gas_value['sensor']['pin'].read() * MAX_INPUT_VOLTAGE / RESOLUTION
        time.sleep(0.1)

    voltage = voltage / 25

    if voltage >= MAX_INPUT_VOLTAGE:
        voltage = 3.2999

    rs = gas_value['sensor']['rl'] * (MAX_INPUT_VOLTAGE-voltage) / voltage

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

# * WiFi Connection

connect_to_wifi()

# * Calculations every 5 minutes (sensors read in 2.5 seconds due to the 25 times loop to increase accuracy)

while(True):

    co2_ppm = get_ppm(CO2_VALUES)
    lpg_ppm = get_ppm(LPG_VALUES)
    co_ppm = get_ppm(CO_VALUES)
    ch4_ppm = get_ppm(CH4_VALUES)

    print('CO2 PPM: ' + str(co2_ppm))
    print('LPG PPM: ' + str(lpg_ppm))
    print('CO PPM: ' + str(co_ppm))
    print('CH4 PPM: ' + str(ch4_ppm))

    env_update(co2_ppm, co_ppm, ch4_ppm, lpg_ppm)

    time.sleep(300)