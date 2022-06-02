import logging
from aiogram import Bot, types
from aiogram.utils import exceptions
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
import asyncio
import threading
import os
import json
import datetime

from mcstatus import JavaServer
TOKEN = os.getenv("BOT_TOKEN")
USERNAME = os.getenv("BOT_USERNAME")
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

IPADDR = os.getenv("IPADDR")
logging.basicConfig(level=logging.INFO)
server_data = {}
server_data["online"] = False

def get_time(): #последнее обновление
    now = datetime.datetime.now()
    current_time = now.strftime("%a %d %b %Y %H:%M:%S")
    return current_time

async def getServerData(): #вся информация о сервере
    global server_data
    while True:
        server_data["last_update"] = get_time()
        try:
            server = JavaServer.lookup(IPADDR)
            ping_res = server.ping()
            server_data["ping"] = ping_res
            status_res = server.status(tries=1)
            server_data["version"] = status_res.version.name
            server_data["protocol"] = status_res.version.protocol
            server_data["motd"] = status_res.description
            server_data["player_count"] = status_res.players.online
            server_data["player_max"] = status_res.players.max
            server_data["players"] = []
            if status_res.players.sample is not None:
                server_data["players"] = [player.name for player in status_res.players.sample]
            server_data["online"] = True
        except Exception:  
            continue
        json.dumps(server_data, indent=4)
        print(server_data)
        await asyncio.sleep(0.1)

def serverData(): #работа в фоне
    task1 = threading.Thread(target=asyncio.run, daemon=True, args=(getServerData(),))
    task1.start()

def getPlayerList(): #парсинг информации об игроках
    if server_data["player_count"] > 0:
        stat = "\n".join(player for player in server_data["players"])
    elif server_data["player_count"] == 0:
        stat = "На сервере сейчас никого нет."
    return stat

async def serverDataParser(): #парсинг ВСЕЙ информации 
    if not server_data["online"]:
        info = f'🕑 <b>Последнее обновление</b>: {server_data["last_update"]}\nℹ️ <b>Состояние</b>: выключен ❌\n🖥 <b>IP</b>: {IPADDR}'
        return info
    elif server_data["online"]:
        info = f"""
🕑 <b>Последнее обновление</b>: {server_data["last_update"]}
ℹ️ <b>Состояние</b>: включен ✅
🖥 <b>IP</b>: {IPADDR}
📡 <b>PING</b>: {round(server_data["ping"], 1)} ms
📝 <b>Описание</b>: {server_data["motd"]}  
🕹 <b>Версия</b>: {server_data["version"]}
👥 <b>Текущий онлайн</b>: {server_data["player_count"]}/{server_data["player_max"]}
👥<b>Игроки</b>:
{getPlayerList()}"""
        return info

def update_button(): #кнопка "Обновить"
    keys = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text="🔄 Обновить", callback_data=json.dumps({"act": "update"}))
    keys.add(key)
    return keys

@dp.errors_handler(exception=exceptions.MessageNotModified)
async def message_not_modified(update: types.Update, exception: exceptions.CantInitiateConversation):
    return True

@dp.errors_handler(exception=exceptions.RetryAfter)
async def flood_wait_retry_after(update: types.Update, exception: exceptions.RetryAfter):
    print(f"Подозрительная активность! Попробуйте через {exception.timeout} с.")
    await asyncio.sleep(exception.timeout)
    return True

@dp.message_handler(text=[f"{USERNAME}"])
async def sneppi(message: types.Message):  
    await return_message(message, sticker="CAACAgIAAxkBAAEKmttg276yQK1rvsQSBM80_Eyc0gt2DAACCQADci8wB6PyDmoZHBAlIAQ")

@dp.message_handler(commands=['start', 'help'])
async def serverHelp(message):
    help = """
ℹ️ Бот для отслеживания онлайна на сервере @dreammita.
ℹ️ Мои команды:
/start, /help - открыть это меню
/status - проверить онлайн
ℹ️ Код: https://github.com/Sn3ppi/dreammita-status-bot"""
    await return_message(message, help)

@dp.message_handler(commands=['status'])
async def serverStatus(message):
    msg = await serverDataParser()
    await return_message(message, msg, reply_markup=update_button())

@dp.callback_query_handler(text=json.dumps({"act": "update"}))
async def serverStatus(call: types.CallbackQuery):
    msg = await serverDataParser()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, reply_markup=update_button())

async def is_chat(message):
    return True if message.chat.type in ['supergroup', 'group'] else False

async def return_message(message, text=None, reply_markup=None, sticker=None):
    if text != None:
        await message.reply(text, reply_markup=reply_markup) if await is_chat(message) else await message.answer(text, reply_markup=reply_markup) 
    if sticker != None:
        await message.reply_sticker(sticker) if await is_chat(message) else await message.answer_sticker(sticker) 

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()

if __name__ == '__main__':
    serverData()
logging.basicConfig(level=logging.INFO)
start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH,
    skip_updates=True,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
)
