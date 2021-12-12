import diff_p_D6F_PH0505 as D6F_PH0505
from polling_timer import PollingTimer
from move_ave import MovingAverage
from collections import deque
from wave_save import WavSave
from buzz_pipi_r import PiPi
from print_with_DP_EH600 import PrintWithDpEh600
import datetime
import multiprocessing as mp
import time

'''
- 2021/12/12 ver.1.00
- Author : emguse
- License: MIT License
'''

D6F_WAITING_MEAS = 0.033 # sec
SAMPLE_FREQ = 16 # Hz
SAMPLE_INTERVAL = 1/SAMPLE_FREQ # 
IVENT_LENGTH = 10 # sec
QUE_SIZE = int(IVENT_LENGTH/2 * SAMPLE_FREQ) # Divide into two parts before and after the trigger.
MOVE_AVE_LENGTH = 2
REFARENCE_PAST_SAMPLE = 2
THRESHOLD = 0.15
MAX_VALUE = 100 # Defines the maximum value of measurements used when creating wav files.
SAVE_DIR = './log/'

ZERO_OFFSET = 0 # Zero point correction
USE_PRINTER = True
EXPORT_CSV = False
EXPORT_WAV = False

def thermal_printing(data) -> None:
    if USE_PRINTER == True:
        p = PrintWithDpEh600()
        for s in data:
            p.set_canvas()
            p.printing(s)
        p.line_feed(1)

def sound_buzzer():
    pipi = PiPi()
    pipi.pipi()

def export_csv(d_a):
    now = datetime.datetime.now()
    now_iso = now.strftime('%Y-%m-%d') + 'T' + now.strftime('%H_%M_%S_%f')
    filename = str(SAVE_DIR + now_iso + '.csv')
    try:
        with open(filename, 'w', newline='') as f:
            #writer = csv.writer(f)
            print("Start exporting data")
            for i in d_a:
                #writer.writerow(i)
                f.write(str(i)+'\n')
            print("Export Complete")
    except:
        print("File export error")

def read_dp() -> float:
    d6f_ph0505 = D6F_PH0505.DifferentialPressureSensorD6F_PH0505()
    #d6f_waiting_meas = PollingTimer(D6F_WAITING_MEAS)
    d6f_ph0505.start_measurement()
    time.sleep(D6F_WAITING_MEAS)
    d6f_ph0505.read()
    dp = d6f_ph0505.diff_p
    return dp

def main():
    read_intarval = PollingTimer(SAMPLE_INTERVAL)
    record_intarval = PollingTimer(IVENT_LENGTH/2 + 2)
    record_intarval.up_state = True
    ma = MovingAverage(MOVE_AVE_LENGTH)
    dq_p = deque(maxlen=QUE_SIZE)  # Store the queue size from the latest measurement value
    dq_ref = deque(maxlen=REFARENCE_PAST_SAMPLE)  # Cue for Triggered Reference Moving Average
    dq_after = deque(maxlen=QUE_SIZE)  # A queue for storing measurements after triggering

    wavesave = WavSave()
    wavesave.set_wav_param(1,2,SAMPLE_FREQ)
    wavesave.set_norm(MAX_VALUE)

    # Fill the queue before trigger monitoring.
    for _ in range(MOVE_AVE_LENGTH):
        while True:
            read_intarval.timer_update()
            if read_intarval.up_state == True:
                ma_p = ma.simple_moving_average(read_dp() - ZERO_OFFSET)
                dq_p.append(ma_p)
                dq_ref.append(ma_p)
                break

    # Main loop
    while True:
        read_intarval.timer_update()
        if read_intarval.up_state == True:
            ma_p = ma.simple_moving_average(read_dp() - ZERO_OFFSET)  # Measurement
            dq_p.append(ma_p)
            dq_ref.append(ma_p)
            if abs(dq_ref[0])+THRESHOLD <= abs(ma_p):  # Trigger monitoring
                record_intarval.timer_update_only()
                if record_intarval.up_state == True:  # Preventing multiple triggers
                    record_intarval.up_state = False

                    # Sound the buzzer
                    buzzer_process = mp.Process(target=sound_buzzer)  
                    buzzer_process.start()
                    # print
                    if USE_PRINTER == True:
                        data = []
                        now = datetime.datetime.now()
                        data.append(now.strftime('%Y-%m-%d') + 'T' + now.strftime('%H:%M:%S.%f'))
                        data.append('DIFF_P:' + str(round(ma_p, 4)) + '  delta P:' + str(round((dq_ref[0] - ma_p),4)))
                        print_process = mp.Process(target=thermal_printing, args=(data,))
                        print_process.start()
                        print(data)

                    # Post-trigger measurement
                    for _ in range(QUE_SIZE):
                        while True:
                            read_intarval.timer_update()
                            if read_intarval.up_state == True:
                                ma_p = ma.simple_moving_average(read_dp() - ZERO_OFFSET)
                                dq_after.append(ma_p)
                                dq_ref.append(ma_p)
                                break
                    # Merge before and after the trigger
                    ar = list(dq_p)
                    ar.extend(dq_after)

                    # File output processing
                    if EXPORT_WAV == True:
                        wavesave.save_w_date(ar)
                    if EXPORT_CSV == True:
                        export_csv(ar)

if __name__ == '__main__':
    main()