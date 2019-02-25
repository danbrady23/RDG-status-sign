from twython import Twython, TwythonStreamer
from auth import consumer_key, consumer_secret, access_token, access_secret
from PIL import Image, ImageDraw, ImageFont
import textwrap
import epd7in5
import time


# Need to add:
# - Better fit onto image
#   - Wrapping
#   - Height?
# - Integration with sign
#   - Add decoration to image
#   - Check if image exists and import, if not then create blank


username = 'TechRdg'


# Pil stuff:
def generate_image(message_text, font_size=50, line_length=30):
    img_size = (640, 384)
    font_dir = 'fonts/small_pixel-7.ttf'  # '/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf'
    text_col = 0
    back_col = 1

    message_wrapped = textwrap.fill(message_text, line_length)

    image = Image.new('1', img_size, color=back_col)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_dir, size=font_size)

    text_dims = draw.textsize(message_wrapped, font)

    position = ((image.width-text_dims[0])/2,
                (image.height-text_dims[1])/2)

    draw.multiline_text(position, message_wrapped, fill=text_col, font=font, align="center")

    return image
    # image.show()


def draw_image(image):
    epd.Clear(0xFF)
    epd.display(epd.getbuffer(image))

    time.sleep(2)

    epd.sleep()


# Twitter stuff:
def get_user_info(username):
    twitter = Twython(consumer_key,
                      consumer_secret,
                      access_token,
                      access_secret)

    user_info = twitter.lookup_user(screen_name=username)

    user_id = user_info[0]['id']

    return user_id


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            tweet = data['text']
            image_tweet = generate_image(tweet)
            draw_image(image_tweet)


stream = MyStreamer(
    consumer_key,
    consumer_secret,
    access_token,
    access_secret)

epd = epd7in5.EPD()
epd.init()

user_id = get_user_info(username)
stream.statuses.filter(follow=user_id)

