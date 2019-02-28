from twython import Twython
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import path
import sys

import netifaces as ni
import textwrap

dir_path = path.dirname(__file__)
sys.path.append(dir_path)

import epd7in5
from auth import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret, telegram_token

# Actions to perform when new message arrives
# what type of message is it?
# Ip: Reply with IP address
# Sign: Put message on sign and twitter


# Updating twitter
def twitter_upload(message):
    twitter = Twython(twitter_consumer_key,
                      twitter_consumer_secret,
                      twitter_access_token,
                      twitter_access_secret)

    twitter.update_status(status=message)


# Generate image
def generate_image(message_text, font_size=50, line_length=30):

    # Set-up
    img_size = (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT)
    font_dir = path.join(dir_path, 'fonts', 'small_pixel-7.ttf')
    # '/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf'
    text_col = 0
    back_col = 255

    # Image set-up
    image = Image.new('1', img_size, color=back_col)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_dir, size=font_size)

    # Generate text
    message_wrapped = textwrap.fill(message_text, line_length)
    time_msg = 'Last updated: ' + datetime.now().strftime('%H:%M')

    # Calculate positions
    msg_dims = draw.textsize(message_wrapped, font)
    msg_pos = ((image.width-msg_dims[0])/2,
               (image.height-msg_dims[1])/2)

    time_dims = draw.textsize(time_msg, font)
    time_pos = (0, image.height-time_dims[1])

    # Draw text to image
    draw.multiline_text(msg_pos, message_wrapped, fill=text_col, font=font, align="center")
    draw.text(time_pos, time_msg, fill=text_col, font=font, align="center")

    return image


# Draw image on sign
def draw_image(image):

    # Convert image to buffer
    img_buf = epd.getbuffer(image)

    # Draw image on display
    epd.display(img_buf)


# Get IP address and return as string
def getIPaddress(ifaceName):

    # This could be updated to show ip for all interfaces...
    iface = ni.ifaddresses(ifaceName).get(ni.AF_INET)[0]
    ip = ifaceName + ': ' + iface['addr'].encode('utf-8')
    return ip    # image.save('tweet.png', 'PNG')


# Initialise e-Paper display
def init_epd():
    epd = epd7in5.EPD()
    epd.init()
    epd.Clear(0xFF)
    return epd


def get_ip(bot, update):
    reply = getIPaddress('wlan0')
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def update_sign(bot, update):

    # This needs error checking

    message = update.message.text

    image = generate_image(message)
    draw_image(image)

    twitter_upload(message)

    bot.send_message(chat_id=update.message.chat_id, text="Updated!")


epd = init_epd()

updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher

ip_handler = CommandHandler('get_ip', get_ip)
dispatcher.add_handler(ip_handler)

sign_handler = MessageHandler(Filters.text, update_sign)
dispatcher.add_handler(sign_handler)

updater.start_polling()
updater.idle()
# body of script

