# link command added and code optimized by fyaz05
# Code from SpringsFern

import asyncio
from hydrogram import Client, filters
from hydrogram.errors import FloodWait, UserIsBlocked, ChatWriteForbidden, ChatAdminRequired
from hydrogram.types import Message
from hydrogram.enums.parse_mode import ParseMode

from WebStreamer.utils.Translation import Language
from WebStreamer.bot import StreamBot, multi_clients
from WebStreamer.utils.bot_utils import gen_link, validate_user
from WebStreamer.utils.database import Database
from WebStreamer.utils.file_properties import get_file_info, get_file_ids
from WebStreamer.vars import Var

# Initialize the database
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

async def send_message_with_error_handling(c: Client, chat_id, text, **kwargs):
    try:
        await c.send_message(chat_id=chat_id, text=text, **kwargs)
    except ChatAdminRequired:
        await c.send_message(Var.BIN_CHANNEL, f"Admin rights required to send in this chat ({chat_id}).")
    except ChatWriteForbidden:
        await c.send_message(Var.BIN_CHANNEL, f"Write permission required to send in this chat ({chat_id}).")

@StreamBot.on_message(
    filters.private & (
        filters.document | filters.video | filters.audio |
        filters.animation | filters.voice | filters.video_note |
        filters.photo | filters.sticker
    ),
    group=4,
)
async def private_receive_handler(bot: Client, message: Message):
    lang = Language(message)

    if not await validate_user(message, lang):
        return

    try:
        link_available = await db.link_available(message.from_user.id)
        if not link_available:
            await message.reply_text(lang.LINK_LIMIT_EXCEEDED)
            return

        # Add the file information to the database
        file_info = get_file_info(message)
        inserted_id = await db.add_file(file_info)

        # Generate the file IDs and the link
        await get_file_ids(False, inserted_id, multi_clients)

        reply_markup, stream_text = await gen_link(
            m=message,
            _id=inserted_id,
            name=[StreamBot.username, StreamBot.fname]
        )

        # Send the link back to the user
        await message.reply_text(
            text=stream_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )

    except FloodWait as e:
        await asyncio.sleep(e.value)
        flood_wait_message = (
            f"Got FloodWait of {e.value}s from [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n\n"
            f"**User ID:** `{message.from_user.id}`"
        )
        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=flood_wait_message,
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    except (UserIsBlocked, ChatWriteForbidden):
        pass

@StreamBot.on_message(filters.command(["link"]))
async def link_command_handler(c: Client, m: Message):
    lang = Language(m)
    message = m.reply_to_message

    if not await db.get_user(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined!\n\nName: {m.from_user.first_name}\nStarted Your Bot!"
        )

    try:
        if not message or not message.media:
            await m.reply_text(lang.LINK_CMD_REPLY_MESSAGE, quote=True)
            return

        # Add the file information to the database
        file_info = get_file_info(message)
        inserted_id = await db.add_file(file_info)

        # Generate the file IDs and the link
        await get_file_ids(False, inserted_id, multi_clients)

        reply_markup, stream_text = await gen_link(
            m=message,
            _id=inserted_id,
            name=[StreamBot.username, StreamBot.fname]
        )

        # Send the link back to the user
        await m.reply_text(
            text=stream_text,
            quote=True,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

    except Exception as e:
        await m.reply_text(text=f"An error occurred: {str(e)}", quote=True)

@StreamBot.on_message(filters.group & filters.command(["join"]))
async def join_group(c: Client, m: Message):
    try:
        member_status = await c.get_chat_member(m.chat.id, (await c.get_me()).id)
        if member_status and member_status.status == 'administrator':
            await m.reply_text("Bot is already an admin in this group.")
            return

        await c.join_chat(m.chat.id)
        await m.reply_text("Bot has joined the group.")
    except Exception as e:
        await m.reply_text(f"An error occurred: {str(e)}", quote=True)