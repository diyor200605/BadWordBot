import asyncio
import time
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties


token='8449419452:AAGLm5kCikDvOAAhs1STkZ16TCygSRRXG-U'

BAD_WORDS = ('дурак','дебил', 'тупой')
WARNING_LIMIT = 3


BLOCKED_USERS = set()
WARNED_USERS = {}
BANNED_USERS = {}

router = Router()



@router.message(CommandStart())
async def cmd_str(message: Message):
    await message.answer('Привет! Ключевые слова которые нужно избегать это "Дурак, Дебил, Тупой" ')


@router.message()
async def check_message(message: Message):
    user_id =message.from_user.id
    text = message.text or ""
    now = time.time()

    if user_id in BANNED_USERS:
        if now < BANNED_USERS[user_id]:
            try:
                await message.delete()
            except Exception:
                pass
            return
        else:
            del BANNED_USERS[user_id]
    if user_id in BLOCKED_USERS:
        try:
            await message.delete()
        except Exception:
            pass
        return
    for bad_word in BAD_WORDS:
        if bad_word in text.lower():
            try:
                await message.delete()
            except Exception:
                pass

            WARNED_USERS[user_id] = WARNED_USERS.get(user_id, 0) + 1
            warns = WARNED_USERS[user_id]

            if warns >= WARNING_LIMIT:
                BANNED_USERS[user_id] = now + 2 * 60 * 60
                await message.answer('Вы заблокированы на 2 часа за повторное нарушение!')
            else:
                user_name = message.from_user.full_name
                await message.bot.send_message(-1002808747520,
                                     f'{user_name} Предупреждение {warns} / {WARNING_LIMIT}: не используй подобное слово!')




async def main():
    bot = Bot(token=token)
    storage=MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

