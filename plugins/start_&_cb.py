from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from helper.database import db
from config import Config, Txt
import humanize
from time import sleep
import utils


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):


    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if len(message.command)>1:
        data = message.command[1]
        if data.split("-", 1)[0] == "verify": # set if or elif it depend on your code
            userid = data.split("-", 2)[1]
            token = data.split("-", 3)[2]
            if str(message.from_user.id) != str(userid):
                return await message.reply_text(
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )
            is_valid = await utils.check_token(client, userid, token)
            if is_valid == True:
                await utils.verify_user(client, userid, token)
                return await message.reply_text(
                    text=f"<b>Hey {message.from_user.mention}, You are successfully verified !\nNow you have unlimited access for all files till today midnight.</b>",
                    protect_content=True
                )
            else:
                return await message.reply_text(
                    text="<b>Invalid link or Expired link !</b>",
                    protect_content=True
                )

    user = message.from_user
    await db.add_user(client, message)
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            '⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/'),
        InlineKeyboardButton(
            '🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/')
    ], [
        InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('Hᴇʟᴩ', callback_data='help')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)

    if not Config.STRING_SESSION:
        if file.file_size > 2000 * 1024 * 1024:
            return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ")

    data = message.command
    if not await utils.check_verification(client, message.from_user.id) and Config.VERIFY == True:
        btn = [[
            InlineKeyboardButton("Verify", url=await utils.get_token(client, message.from_user.id, f"https://telegram.me/{Config.BOT_USERNAME}?start="))
        ],[
            InlineKeyboardButton("How To Open Link & Verify", url=Config.VERIFY_TUTORIAL)
        ]]
        return await message.reply_text(
            text="<b>You are not verified !\nKindly verify to continue !</b>",
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )

    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename")],
                   [InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename")],
                   [InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    '⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/'),
                InlineKeyboardButton(
                    '🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/')
            ], [
                InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('Hᴇʟᴩ', callback_data='help')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✘ Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("⟪ Bᴀᴄᴋ", callback_data="start")
            ]])
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✘ Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("⟪ Bᴀᴄᴋ", callback_data="start")
            ]])
        )

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
