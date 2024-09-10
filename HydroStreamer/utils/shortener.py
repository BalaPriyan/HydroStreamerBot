import random
import string
import pytz
from datetime import datetime
from HydroStreamer.vars import Var
from shortzy import Shortzy
from database import Database  # Import your Database class

# Initialize the database
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

async def get_verify_shorted_link(link):
    shortzy = Shortzy(api_key=Var.SHORT_API, base_site=Var.SHORT_URL)
    link = await shortzy.convert(link)
    return link

async def check_token(bot, userid, token):
    # Check if the token is valid and not used
    is_used = await db.get_token(userid, token)
    if is_used is None:
        return False
    return not is_used

async def get_token(bot, userid, link):
    # Generate a new token and save it to MongoDB
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    await db.set_token(userid, token, used=False)
    link = f"{link}verify-{userid}-{token}"
    shortened_verify_url = await get_verify_shorted_link(link)
    return str(shortened_verify_url)

async def verify_user(bot, userid, token):
    # Mark the token as used and set the verification time
    await db.set_token(userid, token, used=True)
    tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz)
    await db.set_verification_time(userid, today)

async def check_verification(bot, userid):
    # Check if the user's verification is expired
    verification_time = await db.get_verification_time(userid)
    if verification_time is None:
        return False
    return not await db.is_verification_expired(userid)
