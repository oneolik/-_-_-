import os
import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

WIN = 5
games = {}  # user_id -> [ты, бот]


def reply(uid, text):
    vk.messages.send(user_id=uid, message=text, random_id=randrange(1, 100000))


for event in longpoll.listen():
    if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
        continue

    text = event.text.lower().strip()
    uid = event.user_id
    s = games.setdefault(uid, [0, 0])

    if text in ("начать", "старт"):
        games[uid] = [0, 0]
        reply(uid, "🏓 До 5 очков. Отправляй 'понг' — один розыгрыш = одно очко.")

    elif text in ("стоп", "конец"):
        reply(uid, f"Итог: ты {s[0]} : {s[1]} бот")
        games[uid] = [0, 0]

    elif text in ("понг", "pong"):
        if s[0] >= WIN or s[1] >= WIN:
            reply(uid, "Партия уже закончена. Напиши 'начать'.")
            continue

        if randrange(2):          # 50/50 — ты взял очко
            s[0] += 1
            line = f"✅ Очко тебе. {s[0]}:{s[1]}"
        else:                     # бот взял очко
            s[1] += 1
            line = f"❌ Очко боту. {s[0]}:{s[1]}"

        if s[0] == WIN:
            line += "\n🏆 Ты победил! Напиши 'начать'."
        elif s[1] == WIN:
            line += "\n💀 Бот победил. Напиши 'начать'."
        reply(uid, line)

    else:
        reply(uid, "Пиши 'начать' или 'понг'.")