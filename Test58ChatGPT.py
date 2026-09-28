'''At this point, ChatGPT is thinking the problem is in Q0, since the orignal display problem
continually had segment A being blank'''


from fusion_hat.pin import Pin, Mode 
import time 

SDI = Pin(17, mode=Mode.OUT) 
RCLK = Pin(4, mode=Mode.OUT) 
SRCLK = Pin(27, mode=Mode.OUT) 

def shift(data): 
    for i in range(8): 
        SDI.value(1 if (data & (0x80 >> i)) else 0) 
        SRCLK.high() 
        time.sleep(0.02) 
        SRCLK.low() 
        time.sleep(0.02) 
    RCLK.high() 
    time.sleep(0.02) 
    RCLK.low() 
        
print("Loading 0x00...") 
shift(0x00) 
print("0x00 loaded. Measure pin 15 now.") 
input("Press Enter after measuring...") 

print("Loading 0xFF...") 
shift(0xFF) 
print("0xFF loaded. Measure pin 15 now.") 
input("Press Enter after measuring...") 

print("Done.")