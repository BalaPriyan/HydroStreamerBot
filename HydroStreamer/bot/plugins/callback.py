# Code optimized by fyaz05
# Code from SpringsFern

import datetime
import math

from HydroStreamer import __version__
from HydroStreamer.bot import StreamBot
from HydroStreamer.utils.bot_utils import file_format
from HydroStreamer.vars import Var
from HydroStreamer.utils.Translation import Language, BUTTON
from HydroStreamer.utils.database import Database
from HydroStreamer.utils.human_readable import humanbytes
from HydroStreamer.server.exceptions import FIleNotFound

from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

@StreamBot.on_callback_query()
async def cb_data(bot, update: CallbackQuery):
    lang = Language(update)
    usr_cmd = update.data.split("_")

    if usr_cmd[0] == "home":
        await update.message.edit_text(
            text=lang.START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=BUTTON.START_BUTTONS
        )

    elif usr_cmd[0] == "help":
        await update.message.edit_text(
            text=lang.HELP_TEXT.format(Var.UPDATES_CHANNEL),
            disable_web_page_preview=True,
            reply_markup=BUTTON.HELP_BUTTONS
        )

    elif usr_cmd[0] == "about":
        await update.message.edit_text(
            text=lang.ABOUT_TEXT.format(__version__),
            disable_web_page_preview=True,
            reply_markup=BUTTON.ABOUT_BUTTONS
        )

    elif usr_cmd[0] == "N/A":
        await update.answer("N/A", True)

    elif usr_cmd[0] == "close":
        await update.message.delete()

    elif usr_cmd[0] == "msgdelconf2":
        await update.message.edit_caption(
            caption="<b>Do You Want to Delete the file</b>\n" + update.message.caption,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Yes", callback_data=f"msgdelyes_{usr_cmd[1]}_{usr_cmd[2]}"),
                    InlineKeyboardButton("No", callback_data=f"myfile_{usr_cmd[1]}_{usr_cmd[2]}")
                ]
            ])
        )

    elif usr_cmd[0] == "msgdelyes":
        await delete_user_file(usr_cmd[1], update)
        return

    elif usr_cmd[0] == "userfiles":
        file_list, total_files = await gen_file_list_button(int(usr_cmd[1]), update.from_user.id)
        caption_text = "Total files: {}".format(total_files)
        if update.message.caption:
            await update.message.edit_caption(
                caption=caption_text,
                reply_markup=InlineKeyboardMarkup(file_list)
            )
        else:
            await update.message.edit_text(
                text=caption_text,
                reply_markup=InlineKeyboardMarkup(file_list)
            )

    elif usr_cmd[0] == "myfile":
        await gen_file_menu(usr_cmd[1], usr_cmd[2], update)
        return

    elif usr_cmd[0] == "accepttos":
        await db.agreed_tos(int(usr_cmd[1]))
        await update.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I accepted the TOS", callback_data="N/A")]
            ])
        )

    elif usr_cmd[0] == "sendfile":
        myfile = await db.get_file(usr_cmd[1])
        await update.answer(f"Sending File {myfile['file_name']}")
        await update.message.reply_cached_media(myfile['file_id'])

    else:
        await update.message.delete()

async def gen_file_list_button(file_list_no: int, user_id: int):
    file_range = [file_list_no * 10 - 10 + 1, file_list_no * 10]
    user_files, total_files = await db.find_files(user_id, file_range)
    
    file_list = []
    async for file_record in user_files:
        file_list.append([InlineKeyboardButton(file_record["file_name"], callback_data=f"myfile_{file_record['_id']}_{file_list_no}")])

    if total_files > 10:
        file_list.append(
            [
                InlineKeyboardButton("<<", callback_data=f"userfiles_{file_list_no - 1}" if file_list_no > 1 else "N/A"),
                InlineKeyboardButton(f"{file_list_no}/{math.ceil(total_files / 10)}", callback_data="N/A"),
                InlineKeyboardButton(">>", callback_data=f"userfiles_{file_list_no + 1}" if total_files > file_list_no * 10 else "N/A")
            ]
        )

    if not file_list:
        file_list.append([InlineKeyboardButton("Empty", callback_data="N/A")])

    return file_list, total_files

async def gen_file_menu(_id, file_list_no, update: CallbackQuery):
    try:
        myfile_info = await db.get_file(_id)
    except FIleNotFound:
        await update.answer("File Not Found")
        return

    file_type = file_format(myfile_info['file_id'])
    page_link = f"{Var.URL}watch/{myfile_info['_id']}"
    stream_link = f"{Var.URL}dl/{myfile_info['_id']}"
    created_time = myfile_info['time']

    if isinstance(created_time, float):
        date = datetime.datetime.fromtimestamp(created_time)
        created_date = date.date()
        created_time_str = date.time().strftime("%I:%M:%S %p %Z")
    else:
        created_date = created_time
        created_time_str = "N/A"
    
    caption_text = ("Name: {}\nFile Size: {}\nType: {}\nCreated at: {}\nTime: {}"
                    .format(myfile_info['file_name'], 
                            humanbytes(int(myfile_info['file_size'])), 
                            file_type, 
                            created_date, 
                            created_time_str))

    await update.edit_message_caption(
        caption=caption_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data=f"userfiles_{file_list_no}"),
                    InlineKeyboardButton("Delete Link", callback_data=f"msgdelconf2_{myfile_info['_id']}_{file_list_no}")
                ],
                [
                    InlineKeyboardButton("🖥 STREAM", url=page_link), 
                    InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ 📥", url=stream_link)
                ],
                [InlineKeyboardButton("Get File", callback_data=f"sendfile_{myfile_info['_id']}")]
            ]
        )
    )

async def delete_user_file(_id, update: CallbackQuery):
    try:
        myfile_info = await db.get_file(_id)
    except FIleNotFound:
        await update.answer("File Not Found")
        return

    await db.delete_one_file(myfile_info['_id'])
    deleted_caption = update.message.caption.replace("Do You Want to Delete the file", "")

    await update.message.edit_caption(
        caption="<b>Deleted Link Successfully</b>\n" + deleted_caption,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="userfiles_1")]])
    )