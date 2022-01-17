from machine import Pin,PWM
import time
import tm1637
from neopixel import Neopixel


detector = Pin(15, Pin.IN, Pin.PULL_UP)

#########    7-segment section    ####################

mydisplay = tm1637.TM1637(clk=Pin(16), dio=Pin(17)) #7 segment clk pin=gpio16, dio pin=gpio17
mydisplay.brightness(7) #brightness of 7 segment 
mydisplay.number(0000)

count=0

pow_pin=PWM(Pin(14)) #power pin for 7 segment 
pow_pin.freq(1000)

closing_time=60 #if no more baskets within 60 seconds turn off the power

def digit(): #+1
    global count
    pow_pin.duty_u16(65025) #7 segment power pin HIGH
    count=count+1
    mydisplay.number(count)
    


##########    neopixel section ###################
    
numpix = 12 #number of neopixel leds

strip = Neopixel(numpix, 0, 0, "GRB")
#RGB
color = (0, 255, 255) #specify colour
off=(0,0,0)

strip.brightness(25) #brigtness of neopixels led
sleep_time=0.05 #speed of animation

def blink(): #blink after basket
    for i in range(numpix-1,-1,-1):
        strip.set_pixel(i, off)
        
        time.sleep(sleep_time)

    strip.show()

    for i in range(numpix):
        strip.set_pixel(i, color)
        
        time.sleep(sleep_time)
    
    strip.show()
    

def basket(): #basket animation (leds turn on 1 ->12)
    for i in range(numpix):
        strip.set_pixel(i, color)
        strip.show()
        time.sleep(sleep_time)
        
def leds_off(): #leds will be off after animation finishes
    time.sleep(sleep_time*12)
    for i in range(numpix):
        strip.set_pixel(i, off)
    
    strip.show()
    
    
    
#############  main code  ########################
    
timer1=time.time()

while True: #main
    timer2=time.time()
    
    if timer2-timer1>closing_time:  #if no more baskets within 60 seconds turn off the power of 7 segment
        pow_pin.duty_u16(0) #7 segment power pin LOW
        timer1=timer2
        
    if detector.value()==0: #if ball detected 
        digit()
        basket()
        blink()
        blink()
        leds_off()
        timer2=time.time()
        timer1=time.time()         
           
    else:
        time.sleep(0.01)
        

  