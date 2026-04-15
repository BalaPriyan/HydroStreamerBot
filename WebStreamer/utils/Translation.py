# Code optimized by fyaz05 & BalaPriyan
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
<b>👋 Welcome, {}</b>\n
I'm your next-generation <b>File Streaming Bot</b> and <b>Link Generator</b>.\n
• Highly optimized performance
• Direct web links for your media\n
⚠️ <i>NSFW content will result in a permanent ban.</i>
"""

        HELP_TEXT: str = """
<b>ℹ️ How to Use Me</b>\n
<code>1.</code> Send or forward any file/media here.
<code>2.</code> Receive a sleek Stream & Download dashboard link instantly.
<code>3.</code> Share with your friends seamlessly.\n
⚠️ <i>NSFW content will result in a permanent ban.</i>\n
👨‍💻 <a href='https://t.me/{}'>Developer Contact</a>
"""

        ABOUT_TEXT: str = """
<b>📕 About Me</b>\n
Next-gen File to Link Generator
Engineered for Speed, Reliability & Minimalist Aesthetics.\n
🔹 Type /help for commands.
"""

        STREAM_MSG_TEXT: str = """
<b>✨ Link Successfully Generated</b>\n
📄 <b>File:</b> <code>{}</code>
💾 <b>Size:</b> <code>{}</code>\n
📥 <b><a href='{}'>Download File</a></b>
📺 <b><a href='{}'>Watch Online</a></b>\n
<b>Provider:</b> <a href='https://t.me/{}'>{}</a>
"""

        BAN_TEXT: str = """
🚫 <b>Access Denied</b>\n
Your account has been banned due to a terms of service violation.\n
👨‍💻 <a href='tg://user?id={}'>Appeal to {}</a>
"""

        LINK_LIMIT_EXCEEDED: str = """
⚠️ <b>Limit Exceeded</b>\n
You have reached your link generation limit.\n
👨‍💻 <a href='tg://user?id={}'>Upgrade with {}</a>
"""

        INFO_TEXT: str = """
<b>👤 Account Dashboard</b>\n
🆔 <b>ID:</b> <code>{}</code>
🚀 <b>Plan:</b> <code>{}</code>
📊 <b>Links Used:</b> <code>{}</code>
📈 <b>Links Left:</b> <code>{}</code>
"""

    class language_code(en):
        pass

class BUTTON(object):
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('📄 About', callback_data='about')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')],
        [InlineKeyboardButton('❌ Close', callback_data='close')]
    ])

    HELP_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('📄 About', callback_data='about')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')],
        [InlineKeyboardButton('❌ Close', callback_data='close')]
    ])

    ABOUT_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('ℹ️ Help', callback_data='help')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')],
        [InlineKeyboardButton('❌ Close', callback_data='close')]
    ])