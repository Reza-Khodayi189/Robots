from pyrubi import Client
from pyrubi.types import Message
from random import randint, seed, choice
import requests
import asyncio
import json


bot = Client("Self")

my_group = "" # گوید گروهت بزار برای چک کردن عضویت

current_player = 0

def check(guid):
	f = bot.check_join(my_group, guid)
	return f

@bot.on_message()
def save(client: Message):
	try:
		global current_player
		data = json.load(open("data.json", "r"))
		guid = client.author_guid
		target = client.object_guid
		text = client.text

		if text.startswith("بازی"):
			if guid == data["maker"]:
				text = text.split()
				guid_group = target
				num = text[1]
				title = bot.get_chat_info(guid_group)["group"]["group_title"]
				data["group"][guid_group] = {"number_max": int(num)}
				with open("data.json", "w", encoding="utf-8") as f:
					json.dump(data, f, ensure_ascii=False, indent=4)
				data["member"] = {target: []}
				with open("data.json", "w", encoding="utf-8") as f:
					json.dump(data, f, ensure_ascii=False, indent=4)
				client.reply(f'''ربات جرعت حقیقت برای گروه « **{title}** » فعال شد.

تعداد شرکت کننده برای گروه : « **{num}** »

برای بازی کردن کلمه « **منم بازی** » را ارسال کنید.''')
			else:
				client.reply("مالک ربات نیستی /:")
		elif text.startswith("خروج"):
			if guid == data["maker"]:
				if target in data["group"]:
					data["group"].pop(target, None)
					with open("data.json", "w", encoding="utf-8") as f:
						json.dump(data, f, ensure_ascii=False, indent=4)
					client.reply("گروه با موفقیت از لیست بازی حذف شد.")
				else:
					client.reply("گروه توی لیست بازی نیست!!!")
			else:
				client.reply("مالک ربات نیستی تو /:")
		elif text.startswith("منم بازی"):
			if check(guid):
				if target in data["group"]:
					num = data["group"][target]["number_max"]
					if not num == len(data["member"][target]):
						if not guid in data["member"][target]:
							data["member"][target].append(guid)
							with open("data.json", "w", encoding="utf-8") as f:
								json.dump(data, f, ensure_ascii=False, indent=4)
							numb = len(data["member"][target])
							number = num - numb
							if not number == 0:
								client.reply(f'''وارد بازی شدید.

تعداد جای خالی: « {number} »''')
							if number == 0:
								client.reply('''کاربر گرامی تعداد شرکت کننده تکمیل شد.

به سوالت جواب بده 👇''')
								lists = open("list2.txt", "r").read()
								lists = lists.split("\n")
								lists = choice(lists)
								li = data["member"][target]
								guid = li[current_player]
								title = bot.get_chat_info(guid)["user"]["first_name"]
								client.reply(f'''نوبت « {title} » هست به سوالت جواب بده 👇

{lists}

اگه جواب دادی بگو « گفتم »''')
								current_player += 1
						else:
							client.reply("چند بار میخوای بزنی؟! /:")
					else:
						client.reply("❗️ تعداد حداکثر هست برای این گروه.")
				else:
					client.reply("این گروه ثبت نشده ):")
			else:
				a = client.reply('برای بازی در ربات باید عضو گروه زیر باشید.')["message_update"]["message_id"]
				bot.edit_message(target, '''برای بازی در ربات باید عضو گروه زیر باشید.

« https://rubika.ir/joing/IDGDCDJA0PELJDMFKYVJTPBBVOWBSBAJ »''', a)
		elif text.startswith("گفتم"):
			num_max = data["group"][target]["number_max"]
			num = len(data["member"][target])
			if num_max == num:
				lists = open("list2.txt", "r").read()
				lists = lists.split("\n")
				lists = choice(lists)
				if guid in data["member"][target]:
					li = data["member"][target]
					guidd = li[current_player]
					title = bot.get_chat_info(guidd)["user"]["first_name"]
					client.reply(f'''نوبت « {title} » هست به سوالت جواب بده 👇

{lists}

اگه جواب دادی بگو « گفتم »''')
					current_player += 1
					if num == current_player:
						current_player = 0
				else:
					client.reply("تو بازی نیستی تو /:")
			else:
				client.reply("تعداد کامل نیست!")
	except Exception as e:
		print(e)


bot.run()
