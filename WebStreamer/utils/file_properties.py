# Code optimized by fyaz05
# Code from SpringsFern

from __future__ import annotations
import logging
from datetime import datetime
from typing import Any, Optional

from hydrogram import Client
from hydrogram.types import Message
from hydrogram.file_id import FileId

from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.vars import Var

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

async def get_file_ids(client: Client | bool, db_id: str, multi_clients) -> Optional[FileId]:
    logging.debug("Starting get_file_ids")
    file_info = await db.get_file(db_id)

    if "file_ids" not in file_info or not client:
        logging.debug("Storing file_ids for all clients in DB")
        log_msg = await send_file(StreamBot, file_info['file_id'])
        await db.update_file_ids(db_id, await update_file_id(log_msg.id, multi_clients))
        logging.debug("Stored file_ids for all clients in DB")
        if not client:
            return

        file_info = await db.get_file(db_id)

    file_id_info = file_info.get("file_ids", {})

    if str(client.id) not in file_id_info:
        logging.debug("Storing file_id in DB for client %s", client.id)
        log_msg = await send_file(StreamBot, file_info['file_id'])
        msg = await client.get_messages(Var.BIN_CHANNEL, log_msg.id)
        media = get_media_from_message(msg)
        file_id_info[str(client.id)] = getattr(media, "file_id", "")
        await db.update_file_ids(db_id, file_id_info)
        logging.debug("Stored file_id for client %s in DB", client.id)

    logging.debug("Preparing file_id object")
    file_id = FileId.decode(file_id_info[str(client.id)])
    file_id.file_size = file_info['file_size']
    file_id.mime_type = file_info['mime_type']
    file_id.file_name = file_info['file_name']
    file_id.unique_id = file_info['file_unique_id']

    logging.debug("Ending get_file_ids")
    return file_id

def get_media_from_message(message: Message) -> Any:
    media_types = (
        "audio", "document", "photo", "sticker", "animation",
        "video", "voice", "video_note"
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media

def get_media_file_size(m: Message) -> int:
    media = get_media_from_message(m)
    return getattr(media, "file_size", 0)

def get_name(media_msg: Message | FileId) -> str:
    file_name = ''
    if isinstance(media_msg, Message):
        media = get_media_from_message(media_msg)
        file_name = getattr(media, "file_name", "")
    elif isinstance(media_msg, FileId):
        file_name = getattr(media_msg, "file_name", "")
    
    if not file_name:
        if isinstance(media_msg, Message) and media_msg.media:
            media_type = media_msg.media.value
        elif isinstance(media_msg, FileId):
            media_type = media_msg.file_type.name.lower() if media_msg.file_type else "file"
        else:
            media_type = "file"

        formats = {
            "photo": "jpg", "audio": "mp3", "voice": "ogg",
            "video": "mp4", "animation": "mp4", "video_note": "mp4",
            "sticker": "webp"
        }
        
        ext = formats.get(media_type, "")
        ext = f".{ext}" if ext else ""
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{media_type}-{date}{ext}"

    return file_name

def get_file_info(message: Message) -> dict:
    media = get_media_from_message(message)
    return {
        "user_id": message.from_user.id,
        "file_id": getattr(media, "file_id", ""),
        "file_unique_id": getattr(media, "file_unique_id", ""),
        "file_name": get_name(message),
        "file_size": getattr(media, "file_size", 0),
        "mime_type": getattr(media, "mime_type", "None/unknown"),
    }

async def update_file_id(msg_id: int, multi_clients: dict) -> dict:
    file_ids = {}
    for client_id, client in multi_clients.items():
        log_msg = await client.get_messages(Var.BIN_CHANNEL, msg_id)
        media = get_media_from_message(log_msg)
        file_ids[str(client.id)] = getattr(media, "file_id", "")
    return file_ids

async def send_file(client: Client, file_id: str) -> Message:
    return await client.send_cached_media(Var.BIN_CHANNEL, file_id)