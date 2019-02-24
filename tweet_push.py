from twython import Twython, TwythonStreamer
from auth import consumer_key, consumer_secret, access_token, access_secret
from PIL import Image, ImageDraw, ImageFont
import textwrap

username = 'TechRdg'


# Pil stuff:
def draw_image(message_text, font_size=45):
    img_size = (600, 384)
    font_dir = '/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf'
    text_col = 0
    back_col = 1

    message_split = textwrap.wrap(message_text, 20)
    message_wrapped = "\n".join(message_split)

    image = Image.new('1', img_size, color=back_col)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_dir, size=font_size)

    text_dims = draw.textsize(message_wrapped, font)

    position = ((image.width-text_dims[0])/2, (image.height-text_dims[1])/2)

    draw.multiline_text(position, message_wrapped, fill=text_col, font=font)

    image.show()


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
            draw_image(tweet)


stream = MyStreamer(
    consumer_key,
    consumer_secret,
    access_token,
    access_secret
)

user_id = get_user_info(username)
stream.statuses.filter(follow=user_id)

