# stats command added and code optimized by fyaz05
# Code from SpringsFern

import os
import time
import string
import random
import asyncio
import aiofiles
import datetime

from hydrogram import filters, Client
from hydrogram.types import Message
from hydrogram.enums.parse_mode import ParseMode

from WebStreamer.utils.broadcast_helper import send_msg
from WebStreamer.utils.database import Database
from WebStreamer.bot import StreamBot, multi_clients, work_loads
from WebStreamer.utils.file_properties import get_media_from_message
from WebStreamer.vars import Var
from WebStreamer import utils, __version__, StartTime

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)
broadcast_ids = {}

def get_readable_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {seconds}s"

@StreamBot.on_message(filters.command("status") & filters.private & filters.user(Var.OWNER_ID))
async def sts(c: Client, m: Message):
    await m.reply_text(
        text=f"""**Total Users in DB:** `{await db.total_users_count()}`\n**Banned Users in DB:** `{await db.total_banned_users_count()}`\n**Total Links Generated:** `{await db.total_files()}`""",
        parse_mode=ParseMode.MARKDOWN,
        quote=True
    )

@StreamBot.on_message(filters.command("ban") & filters.private & filters.user(Var.OWNER_ID))
async def sts(b, m: Message):
    usr_cmd = m.text.split()
    if len(usr_cmd) < 2:
        return await m.reply_text("Invalid Format\n/ban UserID\n`/ban UserID1 UserID2` .....")
    text = "Banned Users:\n"
    for id in usr_cmd[1:]:
        if not await db.is_user_banned(int(id)):
            try:
                await db.ban_user(int(id))
                text += f"`{id}`: Banned\n"
                await b.send_message(
                    chat_id=id,
                    text="**You are banned from using this bot**",
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
            except Exception as e:
                text += f"`{id}`: Error `{e}`\n"
        else:
            text += f"`{id}`: Already Banned\n"
    await m.reply_text(text)

@StreamBot.on_message(filters.command("unban") & filters.private & filters.user(Var.OWNER_ID))
async def sts(b, m: Message):
    usr_cmd = m.text.split()
    if len(usr_cmd) < 2:
        return await m.reply_text("Invalid Format\n/unban UserID\n`/unban UserID1 UserID2` .....")
    text = "Unbanned Users:\n"
    for id in usr_cmd[1:]:
        if await db.is_user_banned(int(id)):
            try:
                await db.unban_user(int(id))
                text += f"`{id}`: Unbanned\n"
                await b.send_message(
                    chat_id=id,
                    text="**You have been unbanned and can now use this bot**",
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
            except Exception as e:
                text += f"`{id}`: Error `{e}`\n"
        else:
            text += f"`{id}`: Not Banned\n"
    await m.reply_text(text)

@StreamBot.on_message(filters.command("broadcast") & filters.private & filters.user(Var.OWNER_ID) & filters.reply)
async def broadcast_(c, m):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join(random.choice(string.ascii_letters) for _ in range(3))
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text("Broadcast initiated! You will be notified with the log file when all the users are notified.")
    start_time = time.time()
    total_users = await db.total_users_count()
    done, failed, success = 0, 0, 0
    broadcast_ids[broadcast_id] = dict(total=total_users, current=done, failed=failed, success=success)

    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id=int(user['id']), message=broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(dict(current=done, failed=failed, success=success))
                try:
                    await out.edit_text(f"Broadcast Status\n\ncurrent: {done}\nfailed: {failed}\nsuccess: {success}")
                except:
                    pass

    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"Broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"Broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    os.remove('broadcast.txt')

@StreamBot.on_message(filters.command("who") & filters.private & filters.user(Var.OWNER_ID) & filters.reply)
async def sts(c: Client, m: Message):
    media = get_media_from_message(m.reply_to_message)
    if media:
        text = "User List Who sent the file"
        file_info = await db.get_file_by_fileuniqueid(0, media.file_unique_id, True)
        async for x in file_info:
            text += f"\n<a href='tg://user?id={x['user_id']}'>{x['user_id']}</a>"
        await m.reply_text(text)
    else:
        await m.reply_text("Please reply to a file.")

@StreamBot.on_message(filters.command("stats") & filters.private & filters.user(Var.OWNER_ID))
async def stats_handler(bot: StreamBot, message: Message):
    uptime = get_readable_time(time.time() - StartTime)
    loads = {f"bot{c+1}": l for c, (_, l) in enumerate(sorted(work_loads.items(), key=lambda x: x[1], reverse=True))}
    stats_text = (
        f"<b>Server Status:</b> Running\n"
        f"<b>Uptime:</b> {uptime}\n"
        f"<b>Telegram Bot:</b> @{StreamBot.username}\n"
        f"<b>Connected Bots:</b> {len(multi_clients)}\n"
        "<b>Load:</b>\n"
    )
    for bot_name, load in loads.items():
        stats_text += f"  • {bot_name}: {load}\n"
    stats_text += f"<b>Version:</b> {__version__}"
    await message.reply_text(stats_text, parse_mode=ParseMode.HTML)