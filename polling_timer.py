import time

class PollingTimer():
    def __init__(self, interval):
        #t = time.time()
        #f = 1 - (t - int(t))
        #time.sleep(f)
        self.last_time = time.time()
        self.up_state = False
        self.interval = interval
        self.interval_colection = 0
        
    def corected_timer_update(self):
        self.up_state = False
        if self.last_time + self.interval - self.interval_colection <= time.time():
            self.interval_colection = (time.time() - self.last_time) - self.interval
            self.last_time = time.time()
            self.up_state = True
    def corected_timer_update_only(self):
        if self.last_time + self.interval - self.interval_colection <= time.time():
            self.interval_colection = (time.time() - self.last_time) - self.interval
            self.last_time = time.time()
            self.up_state = True
    def timer_update(self):
        self.up_state = False
        if self.last_time + self.interval <= time.time():
            self.last_time = time.time()
            self.up_state = True
    def timer_update_only(self):
        if self.last_time + self.interval <= time.time():
            self.last_time = time.time()
            self.up_state = True

def main():
    INTERVAL = float(0.03125) # Enter the interval time in seconds
    INTERVAL_10s = float(10.0)  # Enter the interval time in seconds

    timer_update = PollingTimer(INTERVAL)
    timer_update_10s = PollingTimer(INTERVAL_10s)
    last = 0
    while True:
        timer_update.timer_update()
        if timer_update.up_state == True:
            print(str(time.time()-last))
            last = time.time()
        timer_update_10s.timer_update()
        if timer_update_10s.up_state ==True:
            print("10sec: " + str(time.time()))
            
if __name__ == "__main__":
  main()