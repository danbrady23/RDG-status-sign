# Remotely updatable e-ink status sign

Sign for my office door that is wireless and can be updated remotely.

## Version 1:

Components:

* (Raspberry Pi Zero W with header pins)[https://shop.pimoroni.com/products/raspberry-pi-zero-wh-with-pre-soldered-header]
* (Waveshare 7.5 e-Paper display with Hat)[https://www.waveshare.com/product/7.5inch-e-paper-hat.htm]
* (Ikea MOSSEBO photo frame)[https://www.ikea.com/gb/en/products/decoration/frames-pictures/mossebo-frame-white-stained-oak-effect-art-70303287/]

Requirements:

Telegram bot set up, see guide (here)[https://medium.freecodecamp.org/learn-to-build-your-first-bot-in-telegram-with-python-4c99526765e4]
Set up app for the twitter account messages will be sent to, see guide (here)[https://docs.inboundnow.com/guide/create-twitter-application/]

Python libraries:

Library for e-Paper display - Available (here)[https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT] under demo code
Twython library: `pip install Twython`
Python telegram bot: `pip install python-telegram-bot`
