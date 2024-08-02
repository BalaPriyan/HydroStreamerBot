# Code optimized by fyaz05
# Code from SpringsFern

from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from WebStreamer.vars import Var

class Language:
    def __new__(cls, message: Message):
        user_language = getattr(message.from_user, 'language_code', 'en')
        if user_language in cls.available:
            return getattr(cls, user_language, cls.en)
        return cls.en

    available = ['en', 'language_code']

    class en:
        START_TEXT: str = """
👋 <i>Hey,</i> {}\n
<i>I'm your friendly Telegram Files Streaming Bot & Direct Links Generator.</i>\n
<i>Click on Help to get more information.</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.
        """

        HELP_TEXT: str = """
📁 <i>Send me any file or media from Telegram.</i>\n
🔗 <i>I will provide an external direct download & streaming link!</i>\n
🚀 <i>Download Link With the Fastest Speed</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.\n
👨‍💻 <i>Contact the developer or report bugs:</i> <b><a href='https://t.me/{}'>[ CLICK HERE ]</a></b>
        """

        ABOUT_TEXT: str = """
📕 <b>My Name:</b> File To Link Generator | File Streamer\n
🔹 <b>Check Commands for more details</b>
        """

        STREAM_MSG_TEXT: str = """
<i><u>Your Link is Generated!</u></i> 🎉\n
📂 <b>File Name:</b> <i>{}</i>\n
💾 <b>File Size:</b> <i>{}</i>\n
⬇️ <b>Download:</b> <i>{}</i>\n
📺 <b>Watch:</b> <i>{}</i>\n
🔗 <b>Link Generated Using:</b> <a href='https://t.me/{}'>{}</a>
        """

        BAN_TEXT: str = """
🚫 <b>Sorry, you are banned from using me.</b>\n
👨‍💻 <i>Contact the developer for help:</i> <b><a href='tg://user?id={}'>{}</a></b>
        """

        LINK_LIMIT_EXCEEDED: str = """
🚫 <b>You have exceeded the number of links you can generate.</b>\n
👨‍💻 <i>Contact the developer for help:</i> <b><a href='tg://user?id={}'>{}</a></b>
        """

        INFO_TEXT: str = """
ℹ️ <b>User ID:</b> <code>{}</code>\n
🚀 <b>Plan:</b> <code>{}</code>\n
🔗 <b>Links Used:</b> <code>{}</code>\n
🔗 <b>Links Left:</b> <code>{}</code>
        """

    class language_code:
        START_TEXT: str = """
👋 <i>Hey,</i> {}\n
<i>I'm your friendly Telegram Files Streaming Bot & Direct Links Generator.</i>\n
<i>Click on Help to get more information.</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.
        """

        HELP_TEXT: str = """
📁 <i>Send me any file or media from Telegram.</i>\n
🔗 <i>I will provide an external direct download link!</i>\n
🚀 <i>Download Link With the Fastest Speed</i>\n
⚠️ <b><u>WARNING:</u></b> 🔞 NSFW content leads to a permanent ban.\n
👨‍💻 <i>Contact the developer or report bugs:</i> <b><a href='https://t.me/{}'>[ CLICK HERE ]</a></b>
        """

        ABOUT_TEXT: str = """
📕 <b>My Name:</b> File To Link Generator | File Streamer\n
🔹 <b>Check Commands for more details</b>
        """

        STREAM_MSG_TEXT: str = """
<i><u>Your Link is Generated!</u></i> 🎉\n
📂 <b>File Name:</b> <i>{}</i>\n
💾 <b>File Size:</b> <i>{}</i>\n
⬇️ <b>Download:</b> <i>{}</i>\n
📺 <b>Watch:</b> <i>{}</i>
        """

        BAN_TEXT: str = """
🚫 <b>Sorry, you are banned from using me.</b>\n
👨‍💻 <i>Contact the developer for help:</i> <b><a href='tg://user?id={}'>{}</a></b>
        """

class BUTTON(object):
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('📄 About', callback_data='about'),
            InlineKeyboardButton('❌ Close', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ])

    HELP_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('📄 About', callback_data='about'),
            InlineKeyboardButton('❌ Close', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ])

    ABOUT_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('❌ Close', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ])