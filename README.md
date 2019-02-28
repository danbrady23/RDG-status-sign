# Remotely updatable e-ink status sign

Sign for my office door that is wireless (eventually) and can be updated remotely.

## Version 1:

### Current operation

The current version uses a Raspberry Pi (RPi) to control everything.  
Messages are sent to a Telegram bot run on the RPi, which creates an image out of it and then renders it on the e-Paper diaplay. As an added bonus it also tweets the message.  

### Components:

* [Raspberry Pi Zero W with header pins](https://shop.pimoroni.com/products/raspberry-pi-zero-wh-with-pre-soldered-header)
* [Waveshare 7.5 e-Paper display with Hat](https://www.waveshare.com/product/7.5inch-e-paper-hat.htm)
* [Ikea MOSSEBO photo frame](https://www.ikea.com/gb/en/products/decoration/frames-pictures/mossebo-frame-white-stained-oak-effect-art-70303287/)

### Requirements:

Telegram bot set up, see guide [here](https://medium.freecodecamp.org/learn-to-build-your-first-bot-in-telegram-with-python-4c99526765e4)  
Set up app for the twitter account messages will be sent to, see guide [here](https://docs.inboundnow.com/guide/create-twitter-application/)  

### Python libraries:

Library for e-Paper display - Available [here](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT) under **demo code**.
Twython library: `pip install Twython`  
Python telegram bot: `pip install python-telegram-bot`  
Net interfaces for getting ip: `pip install netifaces`

### Things to add in this version:

* Error handling
* Logging
* Dealing with long text better (gets cut-off at ~100 characters)


## Next steps:

The current version is not wireless, and the Raspberry Pi zero is too power-hungry to be left on battery power.  
So the next version will split the workload:

1. Deaing with messages and rendering images will be dealt with by a RPi (3 A+) that is connected to the mains.  
2. Displaying the images will be dealt with by a Arduino-like board (candidates below) that is powerd by a LiPo battery.

The two devices will communicate using Bluetooth Low Energy (BLE), Wifi is also power hungry.

The Arduino-like will turn on at a fixed interval (maybe 5 mins) to see if a connection to the RPi can be established. If yes then image data will be transfrerred, otherwise it will go back to sleep.  
The RPi will have Bluetooth off by default, but if it receives a message and successfully renders it as an image then it will turn BLE on. Once the image is transferred to the Arduino-like BLE will be switched off.

### Requirements:

* Changes to Python code to add bluetooth elements - *Possible to do without Arduino-like, send image from Pi to Pi*  
* Purchase Arduino-like - *Front contender is [Feather nRF52840 Express](https://shop.pimoroni.com/products/adafruit-feather-nrf52840-express)*  
* Need code for Arduino-like board  
  + **Language?** - *CircuitPython vs C*  
  + Switch on at set interval (low power rest of the time)  
  + Download data from RPi  
  + Update display
  + Battery indicator (use in-built Neopixel?)  
* LiPo/LiIon batteries - *What capacity?*  


## Further ideas:

Extending battery life even further by not even switching on BLE during specific periods (e.g. 2000-0600, weekends,etc). Will probably require the addition of a Real Time Clock (RTC) module.  
